"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter, notFound } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  TrendingUp,
  Loader2,
  X,
  AlertCircle,
  Activity,
} from "lucide-react";
import { AppShell } from "@/components/app-shell/shell";
import { PageHeader, GlassPanel, SolidPanel, StatusBadge } from "@/components/shared/primitives";
import { experiments as fixtureExperiments } from "@/data/fixtures/demo-scenario";
import { formatPct } from "@/lib/formatters";
import { routes } from "@/lib/routes";
import {
  getExperiment,
  scaleExperiment,
  rejectExperiment,
  getExperimentTimeline,
} from "@/lib/api-client";

interface TimelineNode {
  id?: string;
  timestamp?: string;
  stage?: string;
  agent?: string;
  message?: string;
  auditEventId?: string;
}

export default function ExperimentDetailPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const expId = params.id;

  const [exp, setExp] = useState(fixtureExperiments.find((e) => e.id === expId) || fixtureExperiments[0]);
  const [timeline, setTimeline] = useState<TimelineNode[]>([]);
  const [loadingTimeline, setLoadingTimeline] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [actionType, setActionType] = useState<"scale" | "keep_running">("scale");
  const [confirming, setConfirming] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      if (!expId) return;
      try {
        const data = await getExperiment(expId);
        if (data) setExp((prev) => ({ ...prev, ...data }));
      } catch {
        // fallback
      }
      try {
        setLoadingTimeline(true);
        const tData = await getExperimentTimeline(expId);
        if (tData?.timeline) {
          setTimeline(tData.timeline);
        }
      } catch {
        // fallback
      } finally {
        setLoadingTimeline(false);
      }
    }
    loadData();
  }, [expId]);

  if (!exp) return notFound();

  async function handleScale() {
    setActionType("scale");
    setModalOpen(true);
    setConfirming(true);
    setErrorMessage(null);
    try {
      await scaleExperiment(exp.id, "merchant_demo_user", "Scale Experiment");
      setTimeout(() => {
        router.push(routes.aiCommerce);
      }, 1400);
    } catch (err: unknown) {
      const error = err as Error;
      setErrorMessage(error.message || "Policy Guard prevented scaling.");
      setConfirming(false);
    }
  }

  async function handleKeepRunning() {
    setActionType("keep_running");
    setModalOpen(true);
    setConfirming(true);
    setErrorMessage(null);
    try {
      await rejectExperiment(exp.id, "merchant_demo_user", "Merchant selected Keep Running to collect more sample data.");
      setTimeout(() => {
        setModalOpen(false);
        setConfirming(false);
      }, 1200);
    } catch (err: unknown) {
      const error = err as Error;
      setErrorMessage(error.message || "Action failed.");
      setConfirming(false);
    }
  }

  return (
    <AppShell>
      <PageHeader
        title={exp.name}
        description="Growth Experiment & Autonomous Strategy Lifecycle"
        action={
          <div className="flex items-center gap-3">
            <StatusBadge status={exp.status} />
            <button
              onClick={handleKeepRunning}
              className="px-4 py-2 rounded-lg border border-border-subtle font-label-bold text-sm text-on-surface hover:bg-surface-container transition-colors"
            >
              Keep Running
            </button>
            <button
              onClick={handleScale}
              className="px-5 py-2.5 rounded-lg bg-primary text-on-primary font-semibold text-sm hover:opacity-90 shadow-md transition-all"
            >
              Scale Experiment
            </button>
          </div>
        }
      />

      {/* Hypothesis Card */}
      <SolidPanel className="mb-6">
        <h2 className="font-headline-md text-base font-bold mb-2 text-on-surface">Hypothesis & Growth Thesis</h2>
        <p className="font-body-base text-sm text-on-surface-variant leading-relaxed">
          {exp.hypothesis ||
            "Bundling a Laptop Stand with Wireless Keyboard purchases will increase basket conversion without reducing merchant margin below policy."}
        </p>
      </SolidPanel>

      {/* Control vs Variant Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <SolidPanel>
          <div className="flex items-center justify-between mb-2">
            <p className="font-label-bold text-xs uppercase tracking-wider text-on-surface-variant font-semibold">Control (A)</p>
            <span className="text-xs font-mono text-on-surface-variant">50% Traffic</span>
          </div>
          <p className="font-body-base text-sm text-on-surface mb-1 font-medium">Keyboard standalone</p>
          <p className="font-metric-display-sm text-2xl font-bold font-mono text-on-surface">{exp.controlConversion}% <span className="text-xs font-normal text-on-surface-variant">conversion</span></p>
        </SolidPanel>

        <SolidPanel>
          <div className="flex items-center justify-between mb-2">
            <p className="font-label-bold text-xs uppercase tracking-wider text-growth-green font-semibold">Variant (B)</p>
            <span className="text-xs font-mono text-growth-green font-semibold">50% Traffic</span>
          </div>
          <p className="font-body-base text-sm text-on-surface mb-1 font-medium">Keyboard + Stand (10% Bundle Discount)</p>
          <p className="font-metric-display-sm text-2xl font-bold font-mono text-growth-green">{exp.variantConversion}% <span className="text-xs font-normal text-growth-green/80">conversion</span></p>
        </SolidPanel>
      </div>

      {/* Key Uplift Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <GlassPanel className="!p-4 border border-border-subtle shadow-sm">
          <p className="text-xs text-on-surface-variant font-medium mb-1">Conversion Uplift</p>
          <p className="text-2xl font-bold font-mono text-growth-green">{formatPct(exp.conversionUplift, { signed: true })}</p>
        </GlassPanel>
        <GlassPanel className="!p-4 border border-border-subtle shadow-sm">
          <p className="text-xs text-on-surface-variant font-medium mb-1">Revenue Uplift</p>
          <p className="text-2xl font-bold font-mono text-growth-green">{formatPct(exp.revenueUplift, { signed: true })}</p>
        </GlassPanel>
        <GlassPanel className="!p-4 border border-border-subtle shadow-sm">
          <p className="text-xs text-on-surface-variant font-medium mb-1">AOV Impact</p>
          <p className="text-2xl font-bold font-mono text-growth-green">{formatPct(exp.aovUplift, { signed: true })}</p>
        </GlassPanel>
        <GlassPanel className="!p-4 border border-border-subtle shadow-sm">
          <p className="text-xs text-on-surface-variant font-medium mb-1">Statistical Confidence</p>
          <p className="text-2xl font-bold font-mono text-primary">{exp.confidence}%</p>
        </GlassPanel>
      </div>

      {/* Recommendation Banner */}
      <GlassPanel strong className="flex items-start gap-3 mb-6 border border-growth-green/30 bg-growth-green/5">
        <TrendingUp className="text-growth-green shrink-0 mt-1" size={20} />
        <div>
          <p className="font-label-bold text-xs uppercase tracking-wider text-growth-green mb-1 font-bold">
            RECOMMENDATION: {exp.recommendation || "SCALE VARIANT"}
          </p>
          <p className="font-body-base text-sm text-on-surface-variant">
            {exp.decisionReason ||
              "Variant performance exceeds control while remaining within the merchant's margin policy and sample-size thresholds."}
          </p>
        </div>
      </GlassPanel>

      {/* Experiment Lifecycle Timeline Visualizer */}
      <SolidPanel>
        <div className="flex items-center gap-2 mb-4">
          <Activity className="w-5 h-5 text-primary" />
          <h2 className="font-headline-md text-base font-bold text-on-surface">Lifecycle & Decision Timeline</h2>
        </div>

        {loadingTimeline ? (
          <div className="flex items-center gap-2 py-6 justify-center text-sm text-on-surface-variant">
            <Loader2 className="w-4 h-4 animate-spin text-primary" />
            <span>Loading agent activity and audit events...</span>
          </div>
        ) : (
          <div className="relative pl-6 border-l-2 border-primary/20 space-y-6 my-2">
            {timeline.map((node, i) => (
              <div key={node.id || i} className="relative group">
                {/* Node circle */}
                <div className="absolute -left-[31px] top-1 w-4 h-4 rounded-full bg-surface border-2 border-primary group-hover:scale-125 transition-transform" />
                <div className="flex items-center gap-2 text-xs text-on-surface-variant mb-1">
                  <span className="font-mono font-semibold">{node.timestamp || "Today"}</span>
                  <span>•</span>
                  <span className="px-2 py-0.5 rounded bg-surface-container font-medium text-on-surface">{node.agent || "System Agent"}</span>
                </div>
                <p className="text-sm font-medium text-on-surface">{node.message}</p>
                {node.auditEventId && (
                  <p className="text-xs font-mono text-primary mt-0.5">Audit: {node.auditEventId}</p>
                )}
              </div>
            ))}
          </div>
        )}
      </SolidPanel>

      {/* Action Modal */}
      <AnimatePresence>
        {modalOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-on-surface/40 flex items-center justify-center px-4"
          >
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              className="glass-surface-strong rounded-xl p-6 max-w-sm w-full relative border border-border-subtle shadow-xl"
            >
              {!confirming && (
                <button
                  onClick={() => setModalOpen(false)}
                  className="absolute top-4 right-4 text-on-surface-variant hover:text-on-surface"
                  aria-label="Close"
                >
                  <X size={16} />
                </button>
              )}

              <h3 className="font-headline-md text-base font-bold text-on-surface mb-3">
                {actionType === "scale" ? "Scaling Variant Strategy" : "Updating Experiment"}
              </h3>

              {errorMessage ? (
                <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-red-700 text-xs flex items-center gap-2 mb-4">
                  <AlertCircle className="w-4 h-4 shrink-0" />
                  <span>{errorMessage}</span>
                </div>
              ) : confirming ? (
                <div className="flex items-center gap-3 py-2">
                  <Loader2 size={18} className="text-primary animate-spin shrink-0" />
                  <span className="text-xs text-on-surface">
                    {actionType === "scale"
                      ? "Evaluating sample size guardrails and recording approval..."
                      : "Recording decision in audit trail..."}
                  </span>
                </div>
              ) : (
                <p className="text-xs text-on-surface-variant mb-4">Action completed.</p>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </AppShell>
  );
}
