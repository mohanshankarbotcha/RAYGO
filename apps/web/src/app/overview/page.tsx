"use client";

import Link from "next/link";
import { AreaChart, Area, ResponsiveContainer, XAxis, Tooltip } from "recharts";
import { Sparkles, ArrowRight } from "lucide-react";
import { AppShell } from "@/components/app-shell/shell";
import { PageHeader, KpiCard, GlassPanel, StatusBadge } from "@/components/shared/primitives";
import { metrics, opportunities, revenueTrend } from "@/data/fixtures/demo-scenario";
import { formatINR, formatPct } from "@/lib/formatters";
import { routes } from "@/lib/routes";

export default function OverviewPage() {
  const topOpportunities = opportunities.slice(0, 3);

  return (
    <AppShell>
      <PageHeader
        title="Executive Overview"
        description="RAYGO's live read on NovaTech Store's revenue performance."
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-8">
        <KpiCard label="Total Revenue" value={formatINR(metrics.totalRevenue)} delta={formatPct(metrics.revenueGrowthPct, { signed: true }) + " vs last period"} />
        <KpiCard label="RAYGO Influenced" value={formatINR(metrics.raygoInfluencedRevenue)} delta={formatPct(metrics.raygoLiftPct, { signed: true }) + " AI lift"} />
        <KpiCard label="Active Opportunities" value={String(metrics.activeOpportunities)} delta="Action required" deltaTone="warning" />
        <KpiCard label="AI Commerce Readiness" value={`${metrics.aiCommerceReadiness} / 100`} hint="3 areas need attention" />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 mb-8">
        <GlassPanel className="xl:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-headline-md text-headline-md">Revenue Trend, 30 days</h2>
          </div>
          <ResponsiveContainer width="100%" height={220}>
            <AreaChart data={revenueTrend}>
              <defs>
                <linearGradient id="rev" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#0F172A" stopOpacity={0.25} />
                  <stop offset="95%" stopColor="#0F172A" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis dataKey="day" tick={{ fontSize: 11, fill: "#45464d" }} axisLine={false} tickLine={false} />
              <Tooltip formatter={(v) => formatINR(Number(v))} />
              <Area type="monotone" dataKey="revenue" stroke="#0F172A" strokeWidth={2} fill="url(#rev)" />
            </AreaChart>
          </ResponsiveContainer>
        </GlassPanel>

        <GlassPanel>
          <div className="flex items-center gap-2 mb-3">
            <Sparkles size={16} className="text-reasoning-blue" />
            <h2 className="font-headline-md text-headline-md">RAYGO&apos;s Latest Reasoning</h2>
          </div>
          <p className="font-body-base text-body-base text-on-surface-variant leading-relaxed">
            RAYGO analyzed 1,842 relevant purchase journeys and found a strong correlation between
            Wireless Keyboard purchases and Laptop Stand views. Current attach rate is 4.1%. Similar
            interventions suggest a potential increase to 7.8%.
          </p>
          <Link
            href={routes.opportunity("opp_keyboard_stand")}
            className="mt-4 inline-flex items-center gap-1 font-label-bold text-label-bold text-primary hover:underline"
          >
            Review Opportunity <ArrowRight size={14} />
          </Link>
        </GlassPanel>
      </div>

      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-headline-md text-headline-md">RAYGO found {opportunities.length} revenue opportunities</h2>
          <Link href={routes.opportunities} className="font-label-bold text-label-bold text-primary hover:underline">
            View all
          </Link>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {topOpportunities.map((opp) => (
            <Link key={opp.id} href={routes.opportunity(opp.id)}>
              <GlassPanel className="h-full hover:shadow-md transition-shadow cursor-pointer">
                <div className="flex items-center justify-between mb-3">
                  <StatusBadge status={opp.status} label={opp.status.replace(/_/g, " ")} />
                  <StatusBadge status={opp.risk} label={`${opp.risk} risk`} />
                </div>
                <h3 className="font-headline-md text-headline-md text-on-surface mb-1">{opp.shortTitle}</h3>
                <p className="font-body-sm text-body-sm text-on-surface-variant mb-4">{opp.targetSegment}</p>
                <div className="flex items-end justify-between">
                  <div>
                    <p className="font-body-sm text-body-sm text-on-surface-variant">Expected impact</p>
                    <p className="font-label-bold text-label-bold text-growth-green">
                      {formatINR(opp.expectedMonthlyImpact)}/mo
                    </p>
                  </div>
                  <p className="font-data-mono text-data-mono text-on-surface-variant">{opp.confidence}% conf.</p>
                </div>
              </GlassPanel>
            </Link>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
