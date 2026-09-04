"use client";

import { Suspense } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { CheckCircle2, Check } from "lucide-react";
import { paymentResult } from "@/data/fixtures/demo-scenario";
import { formatINR } from "@/lib/formatters";
import { routes } from "@/lib/routes";

function PaymentSuccessContent() {
  const searchParams = useSearchParams();
  const orderId = searchParams.get("displayOrderId") || paymentResult.orderId;
  const rawAmount = searchParams.get("amount");
  const amount = rawAmount ? parseFloat(rawAmount) : paymentResult.amount;

  return (
    <div className="min-h-screen bg-surface flex items-center justify-center px-6 py-12">
      <div className="max-w-lg w-full text-center">
        <CheckCircle2 className="text-growth-green mx-auto mb-4" size={56} />
        <h1 className="font-headline-lg text-headline-lg mb-1 font-bold text-on-surface">Payment Successful</h1>
        <p className="font-metric-display text-metric-display text-on-surface mb-6 font-mono text-2xl font-bold">
          {formatINR(amount)}
        </p>

        <div className="glass-surface-strong rounded-xl p-6 mb-4 text-left border border-border-subtle shadow-sm">
          <Row label="Order ID" value={orderId} />
          <Row label="Status" value="Captured & Verified" />
          <Row label="Environment" value="Razorpay Test Mode" />
        </div>

        <div className="bg-surface-container-lowest border border-border-subtle rounded-xl p-6 mb-4 text-left shadow-sm">
          <p className="font-label-bold text-xs uppercase tracking-wider text-on-surface-variant mb-3 font-semibold">Transaction timeline</p>
          <div className="flex flex-col gap-2">
            {paymentResult.timeline.map((step) => (
              <div key={step} className="flex items-center gap-2 font-body-sm text-sm text-on-surface">
                <Check size={14} className="text-growth-green shrink-0" />
                {step}
              </div>
            ))}
          </div>
        </div>

        <div className="bg-surface-container-lowest border border-border-subtle rounded-xl p-6 mb-6 text-left shadow-sm">
          <p className="font-label-bold text-xs uppercase tracking-wider text-on-surface-variant mb-3 font-semibold">AI Commerce Summary</p>
          <Row label="Decision time" value={`${paymentResult.decisionTimeSec} sec`} />
          <Row label="Recommendation confidence" value={`${paymentResult.recommendationConfidence}%`} />
          <Row label="Inventory Finalization" value="Synchronously Decremented" />
          <Row label="Action" value="Checkout Completed" />
        </div>

        <Link
          href={routes.overview}
          className="inline-block px-6 py-3 rounded-xl bg-primary text-on-primary font-semibold hover:opacity-90 shadow-md text-sm transition-all"
        >
          Return to Merchant Dashboard
        </Link>
      </div>
    </div>
  );
}

export default function PaymentSuccessPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-surface flex items-center justify-center">Loading payment receipt...</div>}>
      <PaymentSuccessContent />
    </Suspense>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between py-1.5">
      <span className="font-body-sm text-sm text-on-surface-variant">{label}</span>
      <span className="font-mono text-sm font-semibold text-on-surface">{value}</span>
    </div>
  );
}
