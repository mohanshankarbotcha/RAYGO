"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { AppShell } from "@/components/app-shell/shell";
import { PageHeader, GlassPanel, SolidPanel, StatusBadge } from "@/components/shared/primitives";
import { opportunities, metrics } from "@/data/fixtures/demo-scenario";
import { formatINR } from "@/lib/formatters";
import { routes } from "@/lib/routes";

type SortKey = "impact" | "confidence" | "newest";

export default function OpportunityCenterPage() {
  const router = useRouter();
  const [typeFilter, setTypeFilter] = useState<string>("all");
  const [sortKey, setSortKey] = useState<SortKey>("impact");

  const types = useMemo(() => Array.from(new Set(opportunities.map((o) => o.type))), []);

  const rows = useMemo(() => {
    let list = [...opportunities];
    if (typeFilter !== "all") list = list.filter((o) => o.type === typeFilter);
    if (sortKey === "impact") list.sort((a, b) => b.expectedMonthlyImpact - a.expectedMonthlyImpact);
    if (sortKey === "confidence") list.sort((a, b) => b.confidence - a.confidence);
    return list;
  }, [typeFilter, sortKey]);

  const readyCount = opportunities.filter((o) => o.status === "ready_for_review").length;
  const runningCount = opportunities.filter((o) => o.status === "running_experiment").length;

  return (
    <AppShell>
      <PageHeader title="Opportunity Center" description="Ranked workspace for detected growth opportunities." />

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <GlassPanel className="!p-4">
          <p className="font-body-sm text-body-sm text-on-surface-variant">Projected Impact</p>
          <p className="font-metric-display-sm text-metric-display-sm">{formatINR(metrics.projectedOpportunityImpact)}</p>
        </GlassPanel>
        <GlassPanel className="!p-4">
          <p className="font-body-sm text-body-sm text-on-surface-variant">Active</p>
          <p className="font-metric-display-sm text-metric-display-sm">{opportunities.length + 4}</p>
        </GlassPanel>
        <GlassPanel className="!p-4">
          <p className="font-body-sm text-body-sm text-on-surface-variant">Ready for Review</p>
          <p className="font-metric-display-sm text-metric-display-sm">{readyCount + 2}</p>
        </GlassPanel>
        <GlassPanel className="!p-4">
          <p className="font-body-sm text-body-sm text-on-surface-variant">Running</p>
          <p className="font-metric-display-sm text-metric-display-sm">{runningCount + 1}</p>
        </GlassPanel>
      </div>

      <div className="flex items-center gap-3 mb-4">
        <select
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
          className="px-3 py-2 rounded-lg border border-border-subtle bg-surface-container-lowest font-body-sm text-body-sm"
        >
          <option value="all">All types</option>
          {types.map((t) => (
            <option key={t} value={t}>
              {t.replace(/_/g, " ")}
            </option>
          ))}
        </select>
        <select
          value={sortKey}
          onChange={(e) => setSortKey(e.target.value as SortKey)}
          className="px-3 py-2 rounded-lg border border-border-subtle bg-surface-container-lowest font-body-sm text-body-sm"
        >
          <option value="impact">Sort: Impact</option>
          <option value="confidence">Sort: Confidence</option>
          <option value="newest">Sort: Newest</option>
        </select>
      </div>

      <SolidPanel className="!p-0 overflow-x-auto">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-border-subtle">
              {["Opportunity", "Type", "Projected Impact", "AI Confidence", "Risk", "Status", "Action"].map((h) => (
                <th key={h} className="px-5 py-3 font-label-bold text-label-bold text-on-surface-variant whitespace-nowrap">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((opp) => (
              <tr
                key={opp.id}
                onClick={() => router.push(routes.opportunity(opp.id))}
                className="border-b border-border-subtle last:border-0 hover:bg-surface-container-low cursor-pointer"
              >
                <td className="px-5 py-4 font-label-bold text-label-bold text-on-surface whitespace-nowrap">{opp.shortTitle}</td>
                <td className="px-5 py-4 font-body-sm text-body-sm text-on-surface-variant capitalize whitespace-nowrap">{opp.type.replace(/_/g, " ")}</td>
                <td className="px-5 py-4 font-data-mono text-data-mono text-growth-green whitespace-nowrap">{formatINR(opp.expectedMonthlyImpact)}</td>
                <td className="px-5 py-4 font-data-mono text-data-mono whitespace-nowrap">{opp.confidence}%</td>
                <td className="px-5 py-4 whitespace-nowrap"><StatusBadge status={opp.risk} /></td>
                <td className="px-5 py-4 whitespace-nowrap"><StatusBadge status={opp.status} /></td>
                <td className="px-5 py-4 font-label-bold text-label-bold text-primary whitespace-nowrap">Review →</td>
              </tr>
            ))}
          </tbody>
        </table>
      </SolidPanel>
    </AppShell>
  );
}
