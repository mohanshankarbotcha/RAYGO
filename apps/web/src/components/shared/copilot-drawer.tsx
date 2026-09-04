"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { 
  Sparkles, 
  X, 
  Send, 
  Loader2, 
  ShieldCheck, 
  ArrowRight, 
  CheckCircle2, 
  TrendingUp,
  Layers,
  CreditCard,
  Sliders
} from "lucide-react";
import { askCopilot } from "@/lib/api-client";

interface CopilotResponseData {
  answer: string;
  intent: string;
  evidence: string[];
  relatedEntities: Array<{ type: string; id: string; route: string }>;
  recommendedAction?: string | null;
  actionStatus: string;
  policyStatus?: string | null;
  approvalRequired: boolean;
  correlationId: string;
}

const suggestedQuestions = [
  { label: "What is driving revenue right now?", icon: TrendingUp },
  { label: "Which products need attention?", icon: Layers },
  { label: "Should I scale this experiment?", icon: Sliders },
  { label: "Why was payment retry blocked?", icon: CreditCard },
  { label: "What needs my approval?", icon: CheckCircle2 },
];

export function CopilotDrawer({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const router = useRouter();
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<CopilotResponseData | null>(null);

  if (!isOpen) return null;

  async function handleAsk(qToAsk?: string) {
    const q = (qToAsk || question).trim();
    if (!q) return;

    setLoading(true);
    setResponse(null);

    try {
      const res = (await askCopilot({ question: q })) as CopilotResponseData;
      setResponse(res);
    } catch {
      setResponse({
        answer: "Unable to contact RAYGO Copilot backend. Running in offline mode.",
        intent: "fallback",
        evidence: ["FastAPI endpoint reachable locally on port 8000."],
        relatedEntities: [],
        actionStatus: "none",
        approvalRequired: false,
        correlationId: `copilot_local_${Date.now()}`,
      });
    } finally {
      setLoading(false);
    }
  }

  function handleNavigate(route: string) {
    onClose();
    router.push(route);
  }

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/30 backdrop-blur-xs transition-opacity animate-fade-in">
      <div 
        className="w-full max-w-lg bg-surface-container-lowest h-full shadow-2xl border-l border-border-subtle flex flex-col justify-between overflow-hidden animate-slide-left"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-border-subtle bg-surface-container/40">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-primary/10 text-primary flex items-center justify-center font-bold">
              <Sparkles size={18} />
            </div>
            <div>
              <h2 className="font-label-bold text-sm text-on-surface font-semibold">RAYGO Copilot</h2>
              <p className="text-[11px] text-on-surface-variant font-mono">Conversational Revenue Operations</p>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-surface-container text-on-surface-variant transition-colors"
          >
            <X size={18} />
          </button>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* Quick Suggestions */}
          {!response && !loading && (
            <div className="space-y-3">
              <p className="font-label-bold text-xs uppercase tracking-wider text-on-surface-variant">
                Suggested Operational Questions
              </p>
              <div className="grid gap-2">
                {suggestedQuestions.map(({ label, icon: Icon }) => (
                  <button
                    key={label}
                    onClick={() => {
                      setQuestion(label);
                      handleAsk(label);
                    }}
                    className="flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl border border-border-subtle bg-surface hover:bg-surface-container/50 text-left text-xs font-medium text-on-surface transition-all group"
                  >
                    <Icon size={14} className="text-primary shrink-0 group-hover:scale-110 transition-transform" />
                    <span className="flex-1">{label}</span>
                    <ArrowRight size={12} className="text-on-surface-variant opacity-0 group-hover:opacity-100 transition-opacity" />
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="flex flex-col items-center justify-center py-16 space-y-3 text-on-surface-variant">
              <Loader2 size={28} className="animate-spin text-primary" />
              <p className="text-xs font-medium font-mono">Grounded Intelligence Scanning...</p>
            </div>
          )}

          {/* Answer Card */}
          {response && !loading && (
            <div className="space-y-4 animate-fade-in">
              {/* Answer Headline */}
              <div className="glass-surface-strong rounded-xl p-4 border border-border-subtle shadow-sm space-y-2">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-mono text-primary uppercase text-[10px] font-bold px-2 py-0.5 rounded bg-primary/10">
                    {response.intent.replace(/_/g, " ")}
                  </span>
                  <span className="text-[10px] text-on-surface-variant font-mono">{response.correlationId}</span>
                </div>
                <p className="text-sm font-medium text-on-surface leading-relaxed">{response.answer}</p>
              </div>

              {/* Grounded Evidence List */}
              {response.evidence && response.evidence.length > 0 && (
                <div className="bg-surface-container/30 rounded-xl p-4 border border-border-subtle space-y-2">
                  <p className="font-label-bold text-xs uppercase tracking-wider text-on-surface-variant">
                    Grounded Application Evidence
                  </p>
                  <ul className="space-y-1.5 text-xs text-on-surface">
                    {response.evidence.map((ev, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5 shrink-0" />
                        <span>{ev}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Policy & Safety Boundary Status */}
              {response.policyStatus && (
                <div className="flex items-center gap-2 p-3 rounded-lg border border-border-subtle bg-surface-container-lowest text-xs text-on-surface">
                  <ShieldCheck size={15} className="text-primary shrink-0" />
                  <span className="font-mono font-medium">{response.policyStatus}</span>
                </div>
              )}

              {/* Recommended Action Deep-Link */}
              {response.recommendedAction && response.relatedEntities?.[0] && (
                <div className="pt-2">
                  <button
                    onClick={() => handleNavigate(response.relatedEntities[0].route)}
                    className="w-full flex items-center justify-between px-4 py-3 rounded-xl bg-primary text-on-primary font-semibold text-xs shadow-md hover:opacity-95 transition-all"
                  >
                    <span>{response.recommendedAction}</span>
                    <ArrowRight size={14} />
                  </button>
                  <p className="text-[10px] text-center text-on-surface-variant mt-1.5">
                    Opens authenticated workspace. Never executes inline.
                  </p>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div className="p-4 border-t border-border-subtle bg-surface-container-lowest">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleAsk();
            }}
            className="flex items-center gap-2"
          >
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask RAYGO anything about revenue, catalog, experiments..."
              className="flex-1 bg-surface-container/60 border border-border-subtle rounded-xl px-3.5 py-2.5 text-xs text-on-surface outline-none focus:border-primary transition-all placeholder:text-on-surface-variant"
            />
            <button
              type="submit"
              disabled={loading || !question.trim()}
              className="p-2.5 rounded-xl bg-primary text-on-primary disabled:opacity-40 hover:opacity-90 transition-all shrink-0"
            >
              <Send size={15} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
