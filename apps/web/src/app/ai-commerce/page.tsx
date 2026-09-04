"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { AlertTriangle, Sparkles } from "lucide-react";
import { AppShell } from "@/components/app-shell/shell";
import { PageHeader, GlassPanel, SolidPanel } from "@/components/shared/primitives";
import { aiCommerceReadinessScore } from "@/data/fixtures/demo-scenario";
import { formatINR } from "@/lib/formatters";
import { routes } from "@/lib/routes";

export default function AiCommercePage() {
  const router = useRouter();
  const [toast, setToast] = useState(false);
  const { overall, summary, breakdown, blockers, sampleProfile } = aiCommerceReadinessScore;

  function optimize() {
    setToast(true);
    setTimeout(() => setToast(false), 2600);
  }

  return (
    <AppShell>
      <PageHeader
        title="AI Commerce Readiness"
        description="How ready your catalog is for autonomous AI buyers."
        action={
          <div className="flex items-center gap-3">
            <button
              onClick={() => router.push(routes.products)}
              className="px-4 py-2.5 rounded-lg border border-border-subtle font-label-bold text-label-bold hover:bg-surface-container"
            >
              Manage Catalog & Issues
            </button>
            <button
              onClick={optimize}
              className="px-4 py-2.5 rounded-lg border border-border-subtle font-label-bold text-label-bold hover:bg-surface-container"
            >
              Optimize with AI
            </button>
            <button
              onClick={() => router.push(routes.aiBuyer)}
              className="px-4 py-2.5 rounded-lg bg-primary text-on-primary font-label-bold text-label-bold hover:opacity-90 shadow-sm"
            >
              Preview as AI Buyer
            </button>
          </div>
        }
      />

      <GlassPanel strong className="mb-6 flex items-center gap-6 flex-wrap">
        <div className="flex items-center justify-center w-24 h-24 rounded-full border-4 border-growth-green shrink-0">
          <span className="font-headline-lg text-headline-lg">{overall}</span>
        </div>
        <div>
          <p className="font-headline-md text-headline-md text-on-surface">{overall} / 100</p>
          <p className="font-body-base text-body-base text-on-surface-variant">{summary}</p>
        </div>
      </GlassPanel>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <SolidPanel className="xl:col-span-2">
          <h2 className="font-headline-md text-headline-md mb-4">Score Breakdown</h2>
          <div className="flex flex-col gap-4">
            {breakdown.map((item) => (
              <div key={item.label}>
                <div className="flex items-center justify-between mb-1">
                  <span className="font-body-sm text-body-sm text-on-surface">{item.label}</span>
                  <span className="font-data-mono text-data-mono text-on-surface-variant">{item.score}</span>
                </div>
                <div className="h-2 rounded-full bg-surface-container overflow-hidden">
                  <div
                    className={`h-full rounded-full ${item.score >= 80 ? "bg-growth-green" : item.score >= 65 ? "bg-warning-amber" : "bg-error"}`}
                    style={{ width: `${item.score}%` }}
                  />
                </div>
              </div>
            ))}
          </div>

          <h2 className="font-headline-md text-headline-md mt-6 mb-3">AI Buyer Blockers</h2>
          <div className="flex flex-col gap-2">
            {blockers.map((b) => (
              <div key={b} className="flex items-start gap-2 font-body-sm text-body-sm text-on-surface-variant">
                <AlertTriangle size={14} className="text-warning-amber shrink-0 mt-0.5" />
                {b}
              </div>
            ))}
          </div>
        </SolidPanel>

        <GlassPanel>
          <div className="flex items-center gap-2 mb-4">
            <Sparkles size={16} className="text-reasoning-blue" />
            <h2 className="font-headline-md text-headline-md">AI-Readable Product Profile</h2>
          </div>
          <p className="font-label-bold text-label-bold text-on-surface mb-3">{sampleProfile.name}</p>
          <div className="flex flex-col gap-2 mb-4">
            <Row label="Price" value={formatINR(sampleProfile.price)} />
            <Row label="Availability" value={sampleProfile.availability} />
            <Row label="Category" value={sampleProfile.category} />
            <Row label="Best for" value={sampleProfile.bestFor} />
            <Row label="Specs" value={sampleProfile.specs} />
          </div>
          <p className="font-body-sm text-body-sm text-on-surface-variant italic">
            &quot;{sampleProfile.aiDescription}&quot;
          </p>
        </GlassPanel>
      </div>

      {toast && (
        <div className="fixed bottom-6 right-6 glass-surface-strong rounded-lg px-5 py-3 font-body-sm text-body-sm text-on-surface z-50">
          Catalog optimization queued — 6 product profiles updated.
        </div>
      )}
    </AppShell>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-start justify-between gap-3 py-1.5 border-b border-border-subtle last:border-0">
      <span className="font-body-sm text-body-sm text-on-surface-variant shrink-0">{label}</span>
      <span className="font-body-sm text-body-sm text-on-surface text-right">{value}</span>
    </div>
  );
}
