"use client";

import { useRouter } from "next/navigation";
import { AppShell } from "@/components/app-shell/shell";
import { PageHeader, GlassPanel, SolidPanel, StatusBadge } from "@/components/shared/primitives";
import { experiments } from "@/data/fixtures/demo-scenario";
import { formatPct } from "@/lib/formatters";
import { routes } from "@/lib/routes";

export default function ExperimentsPage() {
  const router = useRouter();

  return (
    <AppShell>
      <PageHeader title="Experiments" description="RAYGO measures before it scales." />

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <GlassPanel className="!p-4">
          <p className="font-body-sm text-body-sm text-on-surface-variant">Active Experiments</p>
          <p className="font-metric-display-sm text-metric-display-sm">3</p>
        </GlassPanel>
        <GlassPanel className="!p-4">
          <p className="font-body-sm text-body-sm text-on-surface-variant">Completed</p>
          <p className="font-metric-display-sm text-metric-display-sm">12</p>
        </GlassPanel>
        <GlassPanel className="!p-4">
          <p className="font-body-sm text-body-sm text-on-surface-variant">Revenue Uplift</p>
          <p className="font-metric-display-sm text-metric-display-sm text-growth-green">+₹31,800</p>
        </GlassPanel>
        <GlassPanel className="!p-4">
          <p className="font-body-sm text-body-sm text-on-surface-variant">Average Confidence</p>
          <p className="font-metric-display-sm text-metric-display-sm">91%</p>
        </GlassPanel>
      </div>

      <SolidPanel className="!p-0 overflow-x-auto">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-border-subtle">
              {["Experiment", "Type", "Status", "Control", "Variant", "Revenue Uplift", "Confidence"].map((h) => (
                <th key={h} className="px-5 py-3 font-label-bold text-label-bold text-on-surface-variant whitespace-nowrap">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {experiments.map((exp) => (
              <tr
                key={exp.id}
                onClick={() => router.push(routes.experiment(exp.id))}
                className="border-b border-border-subtle last:border-0 hover:bg-surface-container-low cursor-pointer"
              >
                <td className="px-5 py-4 font-label-bold text-label-bold whitespace-nowrap">{exp.name} Bundle</td>
                <td className="px-5 py-4 font-body-sm text-body-sm text-on-surface-variant whitespace-nowrap">Cross-sell</td>
                <td className="px-5 py-4 whitespace-nowrap"><StatusBadge status={exp.status} /></td>
                <td className="px-5 py-4 font-data-mono text-data-mono whitespace-nowrap">{exp.controlConversion}%</td>
                <td className="px-5 py-4 font-data-mono text-data-mono whitespace-nowrap">{exp.variantConversion}%</td>
                <td className="px-5 py-4 font-data-mono text-data-mono text-growth-green whitespace-nowrap">{formatPct(exp.revenueUplift, { signed: true })}</td>
                <td className="px-5 py-4 font-data-mono text-data-mono whitespace-nowrap">{exp.confidence}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </SolidPanel>
    </AppShell>
  );
}
