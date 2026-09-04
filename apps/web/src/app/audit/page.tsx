"use client";

import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { X } from "lucide-react";
import { AppShell } from "@/components/app-shell/shell";
import { PageHeader, SolidPanel, StatusBadge } from "@/components/shared/primitives";
import { auditEvents } from "@/data/fixtures/demo-scenario";
import { formatCompactDate } from "@/lib/formatters";

export default function AuditTrailPage() {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const selected = auditEvents.find((e) => e.id === selectedId);

  return (
    <AppShell>
      <PageHeader title="Audit Trail" description="Every consequential AI and payment action, explainable and reconstructable." />

      <SolidPanel className="!p-0 overflow-x-auto">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-border-subtle">
              {["Timestamp", "Agent", "Action", "Reason", "Policy", "Approval", "Outcome"].map((h) => (
                <th key={h} className="px-5 py-3 font-label-bold text-label-bold text-on-surface-variant whitespace-nowrap">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {auditEvents.map((event) => (
              <tr
                key={event.id}
                onClick={() => setSelectedId(event.id)}
                className="border-b border-border-subtle last:border-0 hover:bg-surface-container-low cursor-pointer"
              >
                <td className="px-5 py-4 font-data-mono text-data-mono whitespace-nowrap">{formatCompactDate(event.timestamp)}</td>
                <td className="px-5 py-4 font-body-sm text-body-sm whitespace-nowrap capitalize">{event.actor.replace(/_/g, " ")}</td>
                <td className="px-5 py-4 font-label-bold text-label-bold whitespace-nowrap">{event.action}</td>
                <td className="px-5 py-4 font-body-sm text-body-sm text-on-surface-variant max-w-xs truncate">{event.detail}</td>
                <td className="px-5 py-4 whitespace-nowrap">
                  <StatusBadge status={event.outcome === "blocked" ? "blocked" : "active"} label={event.outcome === "blocked" ? "Blocked" : "Passed"} />
                </td>
                <td className="px-5 py-4 font-body-sm text-body-sm text-on-surface-variant whitespace-nowrap">
                  {event.outcome === "blocked" ? "N/A" : "Confirmed"}
                </td>
                <td className="px-5 py-4 whitespace-nowrap">
                  <StatusBadge status={event.outcome} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </SolidPanel>

      <AnimatePresence>
        {selected && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedId(null)}
              className="fixed inset-0 bg-on-surface/30 z-40"
            />
            <motion.div
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "tween", duration: 0.25 }}
              className="fixed right-0 top-0 h-screen w-full max-w-md bg-surface-container-lowest border-l border-border-subtle z-50 overflow-y-auto p-6"
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="font-headline-md text-headline-md">Audit Event</h2>
                <button onClick={() => setSelectedId(null)} aria-label="Close">
                  <X size={18} />
                </button>
              </div>

              <DetailSection title="Decision Summary" body={selected.detail} />
              <DetailSection title="Action" body={selected.action} />
              <DetailSection title="Policy Checks" body={selected.outcome === "blocked" ? "Blocked by Payment Retry policy" : "Passed all applicable policy checks"} />
              <DetailSection title="Approval" body={selected.outcome === "blocked" ? "N/A" : "Merchant approval confirmed"} />
              <DetailSection title="Execution Result" body={selected.outcome === "blocked" ? "Prevented — no action executed" : "Success"} />
              <DetailSection title="Related Order" body={selected.target} />

              <details className="mt-4">
                <summary className="font-label-bold text-label-bold text-on-surface-variant cursor-pointer">
                  Raw metadata
                </summary>
                <pre className="mt-2 bg-surface-container rounded-lg p-3 font-data-mono text-data-mono text-on-surface-variant overflow-x-auto">
{JSON.stringify(selected, null, 2)}
                </pre>
              </details>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </AppShell>
  );
}

function DetailSection({ title, body }: { title: string; body: string }) {
  return (
    <div className="mb-4">
      <p className="font-label-bold text-label-bold text-on-surface-variant mb-1">{title}</p>
      <p className="font-body-sm text-body-sm text-on-surface">{body}</p>
    </div>
  );
}
