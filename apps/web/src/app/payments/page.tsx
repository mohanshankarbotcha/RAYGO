"use client";

import { AppShell } from "@/components/app-shell/shell";
import { PageHeader, GlassPanel, SolidPanel, StatusBadge } from "@/components/shared/primitives";
import { paymentResult } from "@/data/fixtures/demo-scenario";
import { formatCompactDate, formatINR } from "@/lib/formatters";

const payments = [
  { id: "pay_H8k2Lm", order: paymentResult.orderId, amount: paymentResult.amount, method: "UPI", status: "success", failureType: "none", timestamp: "2026-08-31T11:30:04Z" },
  { id: "pay_attempt_failed_01", order: "#RGO-10465", amount: 62999, method: "Card", status: "failed", failureType: "card_declined", timestamp: "2026-08-31T11:32:12Z" },
  { id: "pay_attempt_dsm_02", order: "#RGO-10478", amount: 14999, method: "Razorpay Test Mode", status: "dismissed", failureType: "buyer_cancelled", timestamp: "2026-08-31T11:45:00Z" },
  { id: "pay_A3nQ9x", order: "#RGO-10471", amount: 4999, method: "UPI", status: "success", failureType: "none", timestamp: "2026-08-30T09:14:22Z" },
];

export default function PaymentsPage() {
  const successful = payments.filter((p) => p.status === "success").length;
  const failed = payments.filter((p) => p.status === "failed").length;
  const dismissed = payments.filter((p) => p.status === "dismissed").length;

  return (
    <AppShell>
      <PageHeader
        title="Payments"
        description="Payment resilience and status workspace — Razorpay Test Mode."
      />

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <GlassPanel className="!p-4">
          <p className="font-body-sm text-body-sm text-on-surface-variant">Successful</p>
          <p className="font-metric-display-sm text-metric-display-sm text-growth-green">{successful}</p>
        </GlassPanel>
        <GlassPanel className="!p-4">
          <p className="font-body-sm text-body-sm text-on-surface-variant">Failed</p>
          <p className="font-metric-display-sm text-metric-display-sm text-error">{failed}</p>
        </GlassPanel>
        <GlassPanel className="!p-4">
          <p className="font-body-sm text-body-sm text-on-surface-variant">Dismissed (Pending)</p>
          <p className="font-metric-display-sm text-metric-display-sm text-amber-600">{dismissed}</p>
        </GlassPanel>
        <GlassPanel className="!p-4">
          <p className="font-body-sm text-body-sm text-on-surface-variant">Refunds</p>
          <p className="font-metric-display-sm text-metric-display-sm">0</p>
        </GlassPanel>
      </div>

      <SolidPanel className="!p-0 overflow-x-auto">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-border-subtle">
              {["Payment ID", "Order", "Amount", "Method", "Diagnosis", "Status", "Timestamp"].map((h) => (
                <th key={h} className="px-5 py-3 font-label-bold text-label-bold text-on-surface-variant whitespace-nowrap">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {payments.map((p) => (
              <tr key={p.id} className="border-b border-border-subtle last:border-0 hover:bg-surface-container/30 transition-colors">
                <td className="px-5 py-4 font-data-mono text-data-mono whitespace-nowrap font-medium text-primary">{p.id}</td>
                <td className="px-5 py-4 font-data-mono text-data-mono whitespace-nowrap">{p.order}</td>
                <td className="px-5 py-4 font-data-mono text-data-mono whitespace-nowrap font-semibold">{formatINR(p.amount)}</td>
                <td className="px-5 py-4 font-body-sm text-body-sm text-on-surface-variant whitespace-nowrap">{p.method}</td>
                <td className="px-5 py-4 whitespace-nowrap">
                  {p.failureType !== "none" ? (
                    <span className="px-2 py-0.5 rounded-full text-[11px] font-mono bg-amber-100/80 text-amber-800 border border-amber-200">
                      {p.failureType}
                    </span>
                  ) : (
                    <span className="text-xs text-on-surface-variant font-mono">—</span>
                  )}
                </td>
                <td className="px-5 py-4 whitespace-nowrap"><StatusBadge status={p.status} /></td>
                <td className="px-5 py-4 font-data-mono text-data-mono text-on-surface-variant whitespace-nowrap">{formatCompactDate(p.timestamp)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </SolidPanel>
    </AppShell>
  );
}
