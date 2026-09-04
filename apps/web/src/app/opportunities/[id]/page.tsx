"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Eye, Search, Lightbulb, TrendingUp, Check, Loader2, X } from "lucide-react";
import { AppShell } from "@/components/app-shell/shell";
import { PageHeader, GlassPanel, SolidPanel, StatusBadge } from "@/components/shared/primitives";
import { opportunities, experiments } from "@/data/fixtures/demo-scenario";
import { formatINR } from "@/lib/formatters";
import { routes } from "@/lib/routes";
import { notFound, useParams } from "next/navigation";

import { approveOpportunity } from "@/lib/api-client";

const timelineIcons = [Eye, Search, Lightbulb, TrendingUp];
const timelineLabels = ["Observed", "Detected", "Hypothesized", "Predicted Outcome"];

type ApprovalStage = "idle" | "policy" | "approval" | "creating" | "done";

export default function OpportunityDetailPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const opp = opportunities.find((o) => o.id === params.id);
  const [modalOpen, setModalOpen] = useState(false);
  const [stage, setStage] = useState<ApprovalStage>("idle");

  if (!opp) return notFound();

  const timelineValues = [opp.observed, opp.detected, opp.hypothesized, opp.predicted];
  const experiment = experiments.find((e) => e.opportunityId === opp.id);

  async function runApproval() {
    setModalOpen(true);
    setStage("policy");
    if (opp) {
      try {
        approveOpportunity(opp.id).catch(() => null);
      } catch {
        // fallback to simulated animation
      }
    }
    setTimeout(() => setStage("approval"), 700);
    setTimeout(() => setStage("creating"), 1400);
    setTimeout(() => setStage("done"), 2100);
    setTimeout(() => {
      router.push(routes.experiment(experiment?.id ?? "exp_keyboard_stand"));
    }, 2700);
  }

  return (
    <AppShell>
      <PageHeader
        title={opp.title}
        description={`Expected impact ${formatINR(opp.expectedMonthlyImpact)} / month · Confidence ${opp.confidence}% · Target segment ${opp.targetSegment}`}
        action={
          <button
            onClick={runApproval}
            className="px-5 py-2.5 rounded-lg bg-primary text-on-primary font-label-bold text-label-bold hover:opacity-90"
          >
            Approve & Create Experiment
          </button>
        }
      />

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <div className="xl:col-span-2 flex flex-col gap-6">
          <GlassPanel>
            <h2 className="font-headline-md text-headline-md mb-5">AI Reasoning Timeline</h2>
            <div className="flex flex-col gap-5">
              {timelineLabels.map((label, i) => {
                const Icon = timelineIcons[i];
                return (
                  <div key={label} className="flex gap-3">
                    <div className="flex flex-col items-center">
                      <div className="w-8 h-8 rounded-full bg-reasoning-blue/10 flex items-center justify-center shrink-0">
                        <Icon size={15} className="text-reasoning-blue" />
                      </div>
                      {i < timelineLabels.length - 1 && <div className="w-px flex-1 bg-border-subtle mt-1" />}
                    </div>
                    <div className="pb-4">
                      <p className="font-label-bold text-label-bold text-on-surface-variant mb-1">{label}</p>
                      <p className="font-body-base text-body-base text-on-surface">{timelineValues[i]}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </GlassPanel>

          <SolidPanel>
            <h2 className="font-headline-md text-headline-md mb-4">Proposed Action</h2>
            <p className="font-body-base text-body-base text-on-surface mb-4">
              Create a 10% Keyboard + Laptop Stand bundle experiment.
            </p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Field label="Discount" value="10%" />
              <Field label="Expected uplift" value={`${formatINR(opp.expectedMonthlyImpact)}/mo`} />
              <Field label="Estimated margin" value=">25%" />
              <Field label="Budget" value="Within policy" />
            </div>
          </SolidPanel>
        </div>

        <div className="flex flex-col gap-6">
          <SolidPanel>
            <h2 className="font-headline-md text-headline-md mb-4">Evidence</h2>
            <div className="grid grid-cols-2 gap-3">
              <MiniStat label="Purchase correlation" value="2.3x" />
              <MiniStat label="Current attach rate" value={`${opp.currentAttachRate}%`} />
              <MiniStat label="Projected attach rate" value={`${opp.projectedAttachRate}%`} />
              <MiniStat label="Eligible journeys" value={opp.eligibleJourneys.toLocaleString("en-IN")} />
            </div>
          </SolidPanel>

          <SolidPanel>
            <h2 className="font-headline-md text-headline-md mb-4">Policy Guard</h2>
            <div className="flex flex-col gap-3">
              <PolicyRow label="Discount below 20%" status="pass" />
              <PolicyRow label="Margin above 25%" status="pass" />
              <PolicyRow label="Campaign budget available" status="pass" />
              <PolicyRow label="Merchant approval required" status="required" />
            </div>
          </SolidPanel>
        </div>
      </div>

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
              exit={{ opacity: 0, y: 12 }}
              className="glass-surface-strong rounded-xl p-8 max-w-md w-full"
            >
              {stage !== "done" && (
                <button
                  onClick={() => { setModalOpen(false); setStage("idle"); }}
                  className="absolute top-4 right-4 text-on-surface-variant"
                  aria-label="Close"
                >
                  <X size={16} />
                </button>
              )}
              <h3 className="font-headline-md text-headline-md mb-5">Approving Experiment</h3>
              <ApprovalStep label="Policy check" active={stage === "policy"} done={["approval", "creating", "done"].includes(stage)} />
              <ApprovalStep label="Merchant approval" active={stage === "approval"} done={["creating", "done"].includes(stage)} />
              <ApprovalStep label="Experiment created" active={stage === "creating"} done={stage === "done"} />
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </AppShell>
  );
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="font-body-sm text-body-sm text-on-surface-variant">{label}</p>
      <p className="font-label-bold text-label-bold text-on-surface">{value}</p>
    </div>
  );
}

function MiniStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-surface-container-lowest border border-border-subtle rounded-lg p-3">
      <p className="font-body-sm text-body-sm text-on-surface-variant">{label}</p>
      <p className="font-data-mono text-data-mono text-on-surface mt-1">{value}</p>
    </div>
  );
}

function PolicyRow({ label, status }: { label: string; status: "pass" | "required" }) {
  return (
    <div className="flex items-center justify-between">
      <span className="font-body-sm text-body-sm text-on-surface">{label}</span>
      <StatusBadge status={status === "pass" ? "active" : "ready_for_review"} label={status} />
    </div>
  );
}

function ApprovalStep({ label, active, done }: { label: string; active: boolean; done: boolean }) {
  return (
    <div className="flex items-center gap-3 py-2">
      {done ? (
        <Check size={16} className="text-growth-green" />
      ) : active ? (
        <Loader2 size={16} className="text-reasoning-blue animate-spin" />
      ) : (
        <span className="w-4 h-4 rounded-full border border-outline-variant" />
      )}
      <span className={`font-body-sm text-body-sm ${done || active ? "text-on-surface" : "text-on-surface-variant"}`}>
        {label}
      </span>
    </div>
  );
}
