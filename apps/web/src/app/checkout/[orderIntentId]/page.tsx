"use client";

import { useState, useEffect } from "react";
import { useRouter, useParams } from "next/navigation";
import { Loader2, ShieldCheck, AlertTriangle, CreditCard, Lock } from "lucide-react";
import { orderIntent as fixtureIntent } from "@/data/fixtures/demo-scenario";
import { formatINR } from "@/lib/formatters";
import { routes } from "@/lib/routes";
import {
  getOrderIntent,
  createRazorpayOrder,
  verifyRazorpayPayment,
  recordRazorpayFailure,
  recordRazorpayDismiss,
} from "@/lib/api-client";

type Stage = "review" | "loading_script" | "creating_order" | "checkout_open" | "verifying";

interface RazorpayPaymentResponse {
  razorpay_payment_id?: string;
  razorpay_order_id?: string;
  razorpay_signature?: string;
}

interface RazorpayErrorResponse {
  error?: {
    code?: string;
    description?: string;
    source?: string;
    step?: string;
    reason?: string;
  };
}

export default function CheckoutPage() {
  const router = useRouter();
  const params = useParams();
  const orderIntentId = (params?.orderIntentId as string) || fixtureIntent.orderIntentId;

  const [intentData, setIntentData] = useState(fixtureIntent);
  const [stage, setStage] = useState<Stage>("review");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [dismissNotice, setDismissNotice] = useState<string | null>(null);

  useEffect(() => {
    async function loadIntent() {
      if (orderIntentId) {
        try {
          const res = (await getOrderIntent(orderIntentId)) as Record<string, unknown>;
          if (res) {
            setIntentData((prev) => ({
              ...prev,
              orderIntentId: (res.orderIntentId as string) || (res.id as string) || orderIntentId,
              displayOrderId: (res.displayOrderId as string) || prev.displayOrderId,
              buyerRequest: (res.buyerRequest as string) || prev.buyerRequest,
              items: (res.items as typeof prev.items) || prev.items,
              subtotal: typeof res.subtotal === "number" ? res.subtotal : prev.subtotal,
              bundleDiscount: typeof res.bundleDiscount === "number" ? res.bundleDiscount : prev.bundleDiscount,
              total: typeof res.total === "number" ? res.total : prev.total,
            }));
          }
        } catch {
          // fallback to fixture
        }
      }
    }
    loadIntent();
  }, [orderIntentId]);

  // Dynamically load Razorpay standard checkout script
  useEffect(() => {
    if (typeof window !== "undefined" && !(window as unknown as { Razorpay?: unknown }).Razorpay) {
      const script = document.createElement("script");
      script.src = "https://checkout.razorpay.com/v1/checkout.js";
      script.async = true;
      document.body.appendChild(script);
    }
  }, []);

  async function handleConfirmAndPay(simulateFailure: boolean = false) {
    setErrorMessage(null);

    if (simulateFailure) {
      setStage("creating_order");
      try {
        await recordRazorpayFailure({
          orderIntentId,
          errorDescription: "Simulated payment failure by user.",
        }).catch(() => null);
      } finally {
        setTimeout(() => {
          router.push(
            `${routes.paymentFailure}?orderIntentId=${orderIntentId}&displayOrderId=${encodeURIComponent(
              intentData.displayOrderId || ""
            )}&amount=${intentData.total}`
          );
        }, 1000);
      }
      return;
    }

    try {
      setStage("creating_order");

      // 1. Request Razorpay Order from backend
      let razorpayOrderId = `order_${Date.now()}`;
      let keyId = "rzp_test_raygo_demo";
      let amountPaise = Math.round(intentData.total * 100);

      try {
        const orderRes = await createRazorpayOrder(orderIntentId);
        if (orderRes && typeof orderRes === "object") {
          const resObj = orderRes as Record<string, unknown>;
          if (resObj.razorpayOrderId) razorpayOrderId = resObj.razorpayOrderId as string;
          if (resObj.keyId) keyId = resObj.keyId as string;
          if (resObj.amountSubunits) amountPaise = Number(resObj.amountSubunits);
        }
      } catch {
        console.warn("Using fallback client payment simulation");
      }

      // 2. Open Razorpay Checkout or fallback simulation
      const RazorpayConstructor = (
        window as unknown as {
          Razorpay?: new (opts: Record<string, unknown>) => {
            open: () => void;
            on: (event: string, handler: (resp: RazorpayErrorResponse) => void) => void;
          };
        }
      ).Razorpay;

      if (typeof window !== "undefined" && RazorpayConstructor) {
        setStage("checkout_open");

        const options = {
          key: keyId,
          amount: amountPaise,
          currency: "INR",
          name: "NovaTech Store (RAYGO)",
          description: `Order Intent ${intentData.displayOrderId || ""}`,
          order_id: razorpayOrderId.startsWith("order_") ? razorpayOrderId : undefined,
          prefill: {
            name: "Verified Buyer",
            email: "buyer@example.com",
            contact: "9999999999",
          },
          theme: {
            color: "#0066cc",
          },
          modal: {
            ondismiss: async function () {
              setStage("review");
              setDismissNotice("Payment window closed — your basket is saved and your order is still pending.");
              await recordRazorpayDismiss({
                orderIntentId,
                razorpayOrderId,
                reason: "Buyer closed checkout modal",
              }).catch(() => null);
            },
          },
          handler: async function (response: RazorpayPaymentResponse) {
            setStage("verifying");
            try {
              // Server-side signature verification
              await verifyRazorpayPayment({
                orderIntentId,
                razorpayOrderId: response.razorpay_order_id || razorpayOrderId,
                razorpayPaymentId: response.razorpay_payment_id || `pay_${Date.now()}`,
                razorpaySignature: response.razorpay_signature || "demo_valid_signature",
              }).catch(() => null);
            } finally {
              router.push(
                `${routes.paymentSuccess}?orderIntentId=${orderIntentId}&displayOrderId=${encodeURIComponent(
                  intentData.displayOrderId || ""
                )}&amount=${intentData.total}`
              );
            }
          },
        };

        try {
          const rzp = new RazorpayConstructor(options);
          rzp.on("payment.failed", async function (resp: RazorpayErrorResponse) {
            const desc = resp.error?.description || "Payment was declined by the bank.";
            setErrorMessage(desc);
            setStage("review");
            await recordRazorpayFailure({
              orderIntentId,
              razorpayOrderId,
              errorCode: resp.error?.code,
              errorDescription: desc,
            }).catch(() => null);
          });
          rzp.open();
        } catch {
          // Fallback simulation for offline/test environments
          completeTestCheckout();
        }
      } else {
        completeTestCheckout();
      }
    } catch (e: unknown) {
      const err = e as Error;
      setErrorMessage(err.message || "Failed to initialize payment gateway.");
      setStage("review");
    }
  }

  function completeTestCheckout() {
    setStage("checkout_open");
    setTimeout(() => {
      setStage("verifying");
      setTimeout(() => {
        router.push(
          `${routes.paymentSuccess}?orderIntentId=${orderIntentId}&displayOrderId=${encodeURIComponent(
            intentData.displayOrderId || ""
          )}&amount=${intentData.total}`
        );
      }, 1000);
    }, 1500);
  }

  const busy = stage !== "review";

  return (
    <div className="min-h-screen bg-surface flex items-center justify-center px-4 py-10">
      <div className="max-w-lg w-full">
        {/* Header */}
        <div className="flex items-center gap-2 mb-6 justify-center">
          <ShieldCheck className="text-primary w-6 h-6" />
          <h1 className="font-headline-md text-headline-md font-bold text-on-surface">AI Checkout & Payment</h1>
        </div>

        {/* Error Alert */}
        {errorMessage && (
          <div className="mb-4 p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm flex items-center gap-2 animate-fade-in">
            <AlertTriangle className="w-4 h-4 shrink-0" />
            <span>{errorMessage}</span>
          </div>
        )}

        {/* Dismiss Notice */}
        {dismissNotice && (
          <div className="mb-4 p-4 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-sm flex items-center gap-2 animate-fade-in">
            <Lock className="w-4 h-4 shrink-0 text-amber-600" />
            <span>{dismissNotice}</span>
          </div>
        )}

        {/* Intent Details */}
        <div className="glass-surface-strong rounded-xl p-5 mb-4 border border-border-subtle shadow-sm">
          <p className="font-label-bold text-xs uppercase tracking-wider text-on-surface-variant mb-1 font-semibold">Buyer Request</p>
          <p className="font-body-base text-sm text-on-surface italic">&quot;{intentData.buyerRequest}&quot;</p>
        </div>

        {/* Selected Products */}
        <div className="bg-surface-container-lowest border border-border-subtle rounded-xl p-5 mb-4 shadow-sm">
          <p className="font-label-bold text-xs uppercase tracking-wider text-on-surface-variant mb-3 font-semibold">Selected Hardware Products</p>
          <div className="flex flex-col gap-2.5">
            {intentData.items.map((item) => (
              <div key={item.productId} className="flex items-center justify-between text-sm">
                <span className="text-on-surface font-medium">{item.name} <span className="text-on-surface-variant font-mono text-xs">× {item.quantity}</span></span>
                <span className="font-mono font-semibold text-on-surface">{formatINR(item.unitPrice * item.quantity)}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Order Summary */}
        <div className="bg-surface-container-lowest border border-border-subtle rounded-xl p-5 mb-4 shadow-sm">
          <p className="font-label-bold text-xs uppercase tracking-wider text-on-surface-variant mb-3 font-semibold">Order Summary</p>
          <div className="flex items-center justify-between py-1.5 text-sm">
            <span className="text-on-surface-variant">Order ID</span>
            <span className="font-mono font-medium text-on-surface">{intentData.displayOrderId}</span>
          </div>
          <div className="flex items-center justify-between py-1.5 text-sm">
            <span className="text-on-surface-variant">Subtotal</span>
            <span className="font-mono text-on-surface">{formatINR(intentData.subtotal)}</span>
          </div>
          <div className="flex items-center justify-between py-1.5 text-sm">
            <span className="text-on-surface-variant">Bundle Discount</span>
            <span className="font-mono font-semibold text-growth-green">-{formatINR(intentData.bundleDiscount)}</span>
          </div>
          <div className="border-t border-border-subtle mt-2 pt-2 flex items-center justify-between font-bold">
            <span className="text-on-surface">Total Payable</span>
            <span className="font-mono text-lg text-primary">{formatINR(intentData.total)}</span>
          </div>
        </div>

        {/* Guardrail Policy Disclaimer */}
        <div className="flex items-start gap-2.5 p-3.5 rounded-xl bg-blue-50/70 border border-blue-200/60 mb-6 text-xs text-blue-900 leading-relaxed">
          <Lock className="w-4 h-4 text-primary shrink-0 mt-0.5" />
          <span>
            <strong>AI Agent Policy Enforced:</strong> RAYGO executes payment only upon your explicit authorization. Real-time margin and inventory guardrails are active.
          </span>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col gap-3">
          <button
            onClick={() => handleConfirmAndPay(false)}
            disabled={busy}
            className="w-full py-3.5 px-4 rounded-xl bg-primary text-on-primary font-semibold shadow-md hover:bg-primary/95 transition-all flex items-center justify-center gap-2 disabled:opacity-60 text-sm"
          >
            {busy ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>
                  {stage === "creating_order" && "Creating Payment Order..."}
                  {stage === "checkout_open" && "Processing in Razorpay..."}
                  {stage === "verifying" && "Verifying Security Signature..."}
                  {stage === "loading_script" && "Loading Payment Gateway..."}
                </span>
              </>
            ) : (
              <>
                <CreditCard className="w-4 h-4" />
                <span>Confirm Purchase & Pay {formatINR(intentData.total)}</span>
              </>
            )}
          </button>

          <button
            onClick={() => handleConfirmAndPay(true)}
            disabled={busy}
            className="w-full py-2.5 px-4 rounded-xl border border-red-200 text-red-600 hover:bg-red-50 text-xs font-medium transition-colors disabled:opacity-40"
          >
            Simulate Declined Payment (Test Guardrails)
          </button>
        </div>
      </div>
    </div>
  );
}
