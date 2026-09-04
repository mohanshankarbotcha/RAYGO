# 03 — Razorpay Test Mode Integration

## Goal

Replace the simulated payment flow in `apps/web/src/app/checkout/[orderIntentId]/page.tsx`
with a real Razorpay Test Mode integration end to end, per PRD sections 10.9
and 16.

## Requirements

1. Backend (`apps/api`):
   - `POST /api/v1/payments/razorpay/order` — creates a Razorpay order
     server-side (amount in smallest currency unit, i.e. paise) using
     `RAZORPAY_KEY_ID` / `RAZORPAY_KEY_SECRET`, persists a `RazorpayOrder`
     document linked to the `OrderIntent`, returns `{ orderId, amount,
     currency, keyId }` (never the secret).
   - `POST /api/v1/payments/razorpay/verify` — verifies
     `razorpay_payment_id`, `razorpay_order_id`, `razorpay_signature`
     server-side per Razorpay's signature verification scheme. Only on
     success does it mark the order `captured` and write the audit events
     listed in PRD section 17 (Razorpay order created, payment verified).
     On signature mismatch, treat as failure — do not fulfill the order.
   - `POST /api/v1/payments/razorpay/failure` — records a failed
     `PaymentAttempt`, and per PRD section 15's hard rule, Policy Guard must
     block any automatic retry. Write an audit event for both the failure
     and the blocked retry.
   - `POST /api/v1/webhooks/razorpay` — verifies `X-Razorpay-Signature`
     against the raw request body using `RAZORPAY_WEBHOOK_SECRET`, handles
     `order.paid`, `payment.captured`, `payment.failed`, `payment.authorized`
     idempotently (store `WebhookEvent.id`, skip if already processed),
     reconciles order/payment state, writes an audit event.

2. Frontend (`apps/web`):
   - Load the Razorpay Checkout script and open it with the `orderId` /
     `keyId` returned from step 1, instead of the current `setTimeout`
     simulation.
   - On Checkout success, POST to `/payments/razorpay/verify` with the
     returned `razorpay_payment_id/order_id/signature`; route to
     `/payment/success` only after the backend confirms verification.
   - On Checkout failure/dismiss, POST to `/payments/razorpay/failure`; route
     to `/payment/failure`. Never auto-retry from the client.
   - Keep the existing "simulate payment failure (demo)" button, but wire it
     to actually trigger a Razorpay Test Mode failure path (Razorpay test
     cards support this) rather than only a client-side redirect.
   - Update `/payment/success` and `/payment/failure` to read the real order
     ID, amount, and status from the backend response instead of the static
     `paymentResult` fixture.

3. Security (non-negotiable, per PRD section 16):
   - `RAZORPAY_KEY_SECRET` and `RAZORPAY_WEBHOOK_SECRET` never reach the
     frontend bundle — audit `apps/web` for any accidental non-`NEXT_PUBLIC_`
     env usage.
   - Orders are never fulfilled from a client-reported success alone —
     verification must happen server-side before `/payment/success` reflects
     a captured state.

## Acceptance criteria

- A real Razorpay Test Mode payment (using Razorpay's published test card
  numbers) completes end to end: order created server-side → Checkout →
  verify → `/payment/success` shows the real order ID and amount.
- A Razorpay test failure card routes to `/payment/failure`, and the backend
  audit trail (`GET /api/v1/audit`) shows both the failure and the blocked
  retry.
- Webhook delivery (test via Razorpay's webhook test tool or the CLI) is
  verified and idempotent — replaying the same webhook payload does not
  double-write state.
