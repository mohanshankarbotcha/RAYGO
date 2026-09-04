"use client";

import { Suspense } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { XCircle, ShieldAlert, Check } from "lucide-react";
import { paymentResult } from "@/data/fixtures/demo-scenario";
import { formatINR } from "@/lib/formatters";
import { routes } from "@/lib/routes";

const safetyResponses = [
  "No duplicate payment attempted",
  "Order remains unpaid",
  "Inventory unchanged",
  "Failure recorded in audit trail",
  "Recovery option generated",
];

function PaymentFailureContent() {
  const searchParams = useSearchParams();
  const orderIntentId = searchParams.get("orderIntentId") || "intent_ai_setup_001";
  const rawAmount = searchParams.get("amount");
  const amount = rawAmount ? parseFloat(rawAmount) : paymentResult.amount;
  const errorMsg = searchParams.get("error") || "Payment attempt was unsuccessful. No funds have been captured from your account.";
  const failureType = searchParams.get("failureType") || "card_declined";
  const recommendedAction = searchParams.get("recommendedAction") || "Try a different card or payment method.";

  return (
    <div className="min-h-screen bg-surface flex items-center justify-center px-6 py-12">
      <div className="max-w-lg w-full text-center">
        <XCircle className="text-red-500 mx-auto mb-4" size={56} />
        <h1 className="font-headline-lg text-headline-lg mb-1 font-bold text-on-surface">Payment Unsuccessful</h1>
        <p className="font-metric-display text-metric-display text-on-surface mb-2 font-mono text-2xl font-bold">
          {formatINR(amount)}
        </p>
        <p className="font-body-sm text-sm text-on-surface-variant mb-4">
          {errorMsg}
        </p>

        {/* Diagnosis & Recommended Recovery Action */}
        <div className="border border-amber-200 bg-amber-50/70 rounded-xl p-4 mb-4 text-left shadow-sm">
          <div className="flex items-center justify-between mb-1.5">
            <p className="font-bold text-xs uppercase tracking-wider text-amber-800">DIAGNOSIS: {failureType.replace(/_/g, " ").toUpperCase()}</p>
            <span className="px-2 py-0.5 rounded text-[11px] font-mono bg-amber-200/60 text-amber-900">Safe Recovery</span>
          </div>
          <p className="text-xs font-medium text-amber-900">{recommendedAction}</p>
        </div>

        <div className="border border-red-200 bg-red-50/60 rounded-xl p-4 mb-4 flex items-center gap-3 text-left shadow-sm">
          <ShieldAlert className="text-red-600 shrink-0" size={22} />
          <div>
            <p className="font-bold text-xs uppercase tracking-wider text-red-700">AUTOMATIC RETRY: BLOCKED</p>
            <p className="text-xs text-on-surface-variant mt-0.5">Reason: Duplicate-charge protection enforced by Policy Guard</p>
          </div>
        </div>

        <div className="bg-surface-container-lowest border border-border-subtle rounded-xl p-5 mb-6 text-left shadow-sm">
          <p className="font-label-bold text-xs uppercase tracking-wider text-on-surface-variant mb-3 font-semibold">RAYGO Safety Response</p>
          <div className="flex flex-col gap-2">
            {safetyResponses.map((s) => (
              <div key={s} className="flex items-center gap-2 font-body-sm text-sm text-on-surface">
                <Check size={14} className="text-growth-green shrink-0" />
                {s}
              </div>
            ))}
          </div>
        </div>

        <div className="flex flex-col gap-3">
          <Link
            href={`/checkout/${orderIntentId}`}
            className="w-full py-3 rounded-xl bg-primary text-on-primary font-semibold hover:opacity-90 shadow-md text-sm transition-all text-center"
          >
            Try Another Payment Method
          </Link>
          <Link
            href={routes.aiBuyer}
            className="w-full py-2.5 rounded-xl border border-border-subtle font-medium text-sm text-on-surface hover:bg-surface-container transition-colors text-center"
          >
            Return to AI Buyer Basket
          </Link>
          <Link
            href={routes.overview}
            className="text-xs text-on-surface-variant hover:text-on-surface py-1 text-center"
          >
            Back to Merchant Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function PaymentFailurePage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-surface flex items-center justify-center">Loading failure state...</div>}>
      <PaymentFailureContent />
    </Suspense>
  );
}
