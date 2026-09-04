"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, Check, Loader2, ToggleLeft, ToggleRight } from "lucide-react";
import { merchant, products, initializeSteps } from "@/data/fixtures/demo-scenario";
import { routes } from "@/lib/routes";

type Stage = "initial" | "initializing" | "complete" | "error";

export default function OnboardingPage() {
  const router = useRouter();
  const [stage, setStage] = useState<Stage>("initial");
  const [stepIndex, setStepIndex] = useState(0);
  const [aiBuyerEnabled, setAiBuyerEnabled] = useState(true);

  function handleInitialize() {
    setStage("initializing");
    setStepIndex(0);
    let i = 0;
    const interval = setInterval(() => {
      i += 1;
      if (i >= initializeSteps.length) {
        clearInterval(interval);
        setStage("complete");
        setTimeout(() => router.push(routes.overview), 700);
      } else {
        setStepIndex(i);
      }
    }, 550);
  }

  return (
    <div className="min-h-screen bg-surface text-on-surface flex items-center justify-center px-6">
      <div className="max-w-[1024px] w-full mx-auto grid grid-cols-1 md:grid-cols-2 gap-12 items-center min-h-[600px]">
        {/* Left: Brand + value prop */}
        <div className="flex flex-col gap-6 justify-center">
          <div className="flex items-center gap-2">
            <Sparkles className="text-primary" size={28} />
            <span className="font-headline-lg text-headline-lg tracking-tight">RAYGO</span>
          </div>
          <h1 className="font-metric-display text-metric-display text-on-surface mt-4 max-w-sm">
            Turn commerce data into autonomous growth.
          </h1>
          <p className="font-body-base text-body-base text-on-surface-variant max-w-md">
            AI revenue intelligence for modern commerce.
          </p>
        </div>

        {/* Right: Setup card */}
        <div className="bg-surface-container-lowest border border-border-subtle rounded-xl p-8 shadow-sm flex flex-col gap-8 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-1 bg-primary" />

          <div className="flex flex-col gap-2">
            <h2 className="font-headline-md text-headline-md text-on-surface">Store Configuration</h2>
            <p className="font-body-sm text-body-sm text-on-surface-variant">
              Review your connected store details.
            </p>
          </div>

          <div className="flex flex-col gap-4">
            <Row label="Store Name" value={merchant.name} bold />
            <Row label="Category" value={merchant.category} />
            <Row label="Est. Revenue" value="₹2L - ₹5L" mono />
            <Row label="Product Count" value={String(products.length)} mono />
            <div className="flex items-center justify-between py-3 border-b border-border-subtle">
              <span className="font-body-sm text-body-sm text-on-surface-variant">Enable AI Buyer mode</span>
              <button onClick={() => setAiBuyerEnabled((v) => !v)} aria-label="Toggle AI Buyer mode">
                {aiBuyerEnabled ? (
                  <ToggleRight className="text-primary" size={28} />
                ) : (
                  <ToggleLeft className="text-outline-variant" size={28} />
                )}
              </button>
            </div>
          </div>

          <AnimatePresence mode="wait">
            {stage === "initial" && (
              <motion.button
                key="cta"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={handleInitialize}
                className="w-full py-3 rounded-lg bg-primary text-on-primary font-label-bold text-label-bold hover:opacity-90 transition-opacity"
              >
                Initialize RAYGO
              </motion.button>
            )}

            {stage === "initializing" && (
              <motion.div
                key="steps"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex flex-col gap-2"
              >
                {initializeSteps.map((step, i) => (
                  <div key={step} className="flex items-center gap-2 font-body-sm text-body-sm">
                    {i < stepIndex ? (
                      <Check size={15} className="text-growth-green" />
                    ) : i === stepIndex ? (
                      <Loader2 size={15} className="text-reasoning-blue animate-spin" />
                    ) : (
                      <span className="w-[15px] h-[15px] rounded-full border border-outline-variant" />
                    )}
                    <span className={i <= stepIndex ? "text-on-surface" : "text-on-surface-variant"}>
                      {step}
                    </span>
                  </div>
                ))}
              </motion.div>
            )}

            {stage === "complete" && (
              <motion.div
                key="done"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex items-center gap-2 font-label-bold text-label-bold text-growth-green"
              >
                <Check size={16} /> RAYGO is ready. Redirecting...
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}

function Row({ label, value, bold, mono }: { label: string; value: string; bold?: boolean; mono?: boolean }) {
  return (
    <div className="flex items-center justify-between py-3 border-b border-border-subtle">
      <span className="font-body-sm text-body-sm text-on-surface-variant">{label}</span>
      <span
        className={`text-on-surface ${
          mono
            ? "font-data-mono text-data-mono"
            : bold
            ? "font-label-bold text-label-bold"
            : "font-body-sm text-body-sm"
        }`}
      >
        {value}
      </span>
    </div>
  );
}
