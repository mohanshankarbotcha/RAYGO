"use client";

import { useState } from "react";
import { ShieldCheck, ShieldOff } from "lucide-react";
import { AppShell } from "@/components/app-shell/shell";
import { PageHeader, GlassPanel, SolidPanel, StatusBadge } from "@/components/shared/primitives";
import { policies as initialPolicies, actionMatrix } from "@/data/fixtures/demo-scenario";

export default function PoliciesPage() {
  const [policies, setPolicies] = useState(initialPolicies);

  function toggle(id: string) {
    setPolicies((prev) =>
      prev.map((p) => {
        if (p.id !== id) return p;
        if (p.id === "pol_payment_retry") return p; // must remain blocked
        return { ...p, status: p.status === "active" ? "paused" : "active" };
      })
    );
  }

  return (
    <AppShell>
      <PageHeader
        title="Policies · Revenue Action Firewall"
        description="RAYGO cannot freely manipulate money. Every consequential action is gated here."
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4 mb-8">
        {policies.map((p) => (
          <GlassPanel key={p.id} className="flex flex-col gap-3">
            <div className="flex items-center justify-between">
              <span className="font-label-bold text-label-bold text-on-surface">{p.name}</span>
              {p.status === "active" ? (
                <ShieldCheck size={16} className="text-growth-green" />
              ) : (
                <ShieldOff size={16} className="text-on-surface-variant" />
              )}
            </div>
            <p className="font-headline-md text-headline-md text-on-surface">{p.limitLabel}</p>
            <p className="font-body-sm text-body-sm text-on-surface-variant">{p.description}</p>
            <button
              onClick={() => toggle(p.id)}
              disabled={p.id === "pol_payment_retry"}
              className="mt-1 self-start font-label-bold text-label-bold text-primary hover:underline disabled:text-on-surface-variant disabled:no-underline disabled:cursor-not-allowed"
            >
              {p.id === "pol_payment_retry" ? "Locked for MVP" : p.status === "active" ? "Pause" : "Activate"}
            </button>
          </GlassPanel>
        ))}
      </div>

      <SolidPanel className="!p-0 overflow-x-auto">
        <h2 className="font-headline-md text-headline-md p-5 pb-3">Action Matrix</h2>
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-border-subtle">
              {["Action Type", "Can Propose", "Can Execute", "Approval Requirement"].map((h) => (
                <th key={h} className="px-5 py-3 font-label-bold text-label-bold text-on-surface-variant whitespace-nowrap">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {actionMatrix.map((row) => (
              <tr key={row.action} className="border-b border-border-subtle last:border-0">
                <td className="px-5 py-4 font-label-bold text-label-bold whitespace-nowrap">{row.action}</td>
                <td className="px-5 py-4 whitespace-nowrap">
                  <StatusBadge status={row.canPropose ? "active" : "declined"} label={row.canPropose ? "Yes" : "No"} />
                </td>
                <td className="px-5 py-4 whitespace-nowrap">
                  <StatusBadge status={row.canExecute ? "active" : "declined"} label={row.canExecute ? "Yes" : "No"} />
                </td>
                <td className="px-5 py-4 font-body-sm text-body-sm text-on-surface-variant whitespace-nowrap">{row.approval}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </SolidPanel>
    </AppShell>
  );
}
