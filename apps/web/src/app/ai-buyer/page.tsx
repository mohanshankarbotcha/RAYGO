"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, Search, Check, Loader2 } from "lucide-react";
import { aiBuyerRecommendation, orderIntent } from "@/data/fixtures/demo-scenario";
import { formatINR } from "@/lib/formatters";
import { routes } from "@/lib/routes";

type Stage = "idle" | "searching" | "results";

export default function AiBuyerPage() {
  const router = useRouter();
  const [query, setQuery] = useState(
    "I need a laptop setup for AI development and college under ₹70,000."
  );
  const [stage, setStage] = useState<Stage>("idle");
  const [basketAdded, setBasketAdded] = useState(false);

  function search() {
    setStage("searching");
    setTimeout(() => setStage("results"), 1300);
  }

  function addToBasket() {
    setBasketAdded(true);
  }

  return (
    <div className="min-h-screen bg-surface">
      <header className="glass-surface flex items-center justify-between px-6 h-16 sticky top-0 z-10">
        <div className="flex items-center gap-2">
          <Sparkles className="text-primary" size={22} />
          <span className="font-headline-md text-headline-md">RAYGO AI Commerce</span>
        </div>
        <span className="font-body-sm text-body-sm text-on-surface-variant">NovaTech Store</span>
      </header>

      <div className="max-w-2xl mx-auto px-6 py-12">
        <h1 className="font-metric-display-sm text-metric-display-sm text-center mb-6">
          Tell me what you&apos;re looking for.
        </h1>

        <div className="flex items-center gap-2 bg-surface-container-lowest border border-border-subtle rounded-xl p-2 mb-6">
          <Search size={16} className="text-on-surface-variant ml-2" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") search();
            }}
            placeholder="Type your hardware or budget request (Press Enter)..."
            className="flex-1 bg-transparent outline-none font-body-base text-body-base px-2 text-on-surface"
          />
          <button
            onClick={search}
            className="px-5 py-2.5 rounded-lg bg-primary text-on-primary font-label-bold text-label-bold hover:opacity-90 active:scale-95 transition-all shadow-sm"
          >
            Search
          </button>
        </div>

        <AnimatePresence mode="wait">
          {stage === "searching" && (
            <motion.div
              key="loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex items-center justify-center gap-2 py-12 text-on-surface-variant font-body-sm text-body-sm"
            >
              <Loader2 size={16} className="animate-spin" />
              Matching buyer intent to AI-readable catalog...
            </motion.div>
          )}

          {stage === "results" && (
            <motion.div key="results" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
              <div className="glass-surface-strong rounded-xl p-6 mb-4 relative">
                <span className="absolute top-4 right-4 px-2.5 py-1 rounded-full bg-growth-green/10 text-growth-green font-label-bold text-label-bold">
                  Top Match · {aiBuyerRecommendation.fitPct}% Fit
                </span>
                <h2 className="font-headline-md text-headline-md text-on-surface mb-1">{aiBuyerRecommendation.name}</h2>
                <p className="font-headline-lg text-headline-lg text-on-surface mb-2">{formatINR(aiBuyerRecommendation.price)}</p>
                <p className="font-body-sm text-body-sm text-on-surface-variant mb-4">{aiBuyerRecommendation.specs}</p>

                <p className="font-label-bold text-label-bold text-on-surface-variant mb-2">Why RAYGO selected this</p>
                <div className="flex flex-col gap-2 mb-5">
                  {aiBuyerRecommendation.reasons.map((r) => (
                    <div key={r.label} className="flex items-start gap-2 font-body-sm text-body-sm">
                      <Check size={14} className="text-growth-green shrink-0 mt-0.5" />
                      <span>
                        <span className="font-label-bold text-label-bold">{r.label}:</span> {r.detail}
                      </span>
                    </div>
                  ))}
                </div>

                {!basketAdded ? (
                  <button
                    onClick={addToBasket}
                    className="w-full py-3 rounded-lg bg-primary text-on-primary font-label-bold text-label-bold hover:opacity-90"
                  >
                    Add to Basket
                  </button>
                ) : (
                  <button
                    onClick={() => router.push(routes.checkout(orderIntent.orderIntentId))}
                    className="w-full py-3 rounded-lg bg-growth-green text-white font-label-bold text-label-bold hover:opacity-90"
                  >
                    Review Purchase
                  </button>
                )}
              </div>

              <p className="font-label-bold text-label-bold text-on-surface-variant mb-2 mt-6">Other valid options</p>
              <div className="grid grid-cols-2 gap-3">
                {aiBuyerRecommendation.otherOptions.map((opt) => (
                  <div key={opt.name} className="bg-surface-container-lowest border border-border-subtle rounded-lg p-4">
                    <p className="font-body-sm text-body-sm text-on-surface">{opt.name}</p>
                    <p className="font-label-bold text-label-bold">{formatINR(opt.price)}</p>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
