"use client";

import { useEffect, useState } from "react";
import { Bot, RefreshCw, Activity, Terminal, Shield, Clock, X, ChevronRight, AlertTriangle } from "lucide-react";
import { AppShell } from "@/components/app-shell/shell";
import { PageHeader, GlassPanel, SolidPanel, StatusBadge } from "@/components/shared/primitives";
import { agents as fixtureAgents, agentTimeline as fixtureTimeline } from "@/data/fixtures/demo-scenario";
import { getAgentStatus, getAgentActivity, getAgentRuns } from "@/lib/api-client";

interface AgentRun {
  runId: string;
  agent: string;
  action: string;
  status: string;
  startedAt: string;
  completedAt?: string;
  durationMs?: number;
  inputPayload?: Record<string, unknown>;
  outputPayload?: Record<string, unknown>;
  error?: string;
  policyEvaluationId?: string;
  correlationIds?: Record<string, unknown>;
}

interface TimelineItem {
  time?: string;
  timestamp?: string;
  agent?: string;
  name?: string;
  event?: string;
  action?: string;
  reason?: string;
  agentRunId?: string;
}

export default function AgentActivityPage() {
  const [agentsList, setAgentsList] = useState(fixtureAgents);
  const [timeline, setTimeline] = useState<TimelineItem[]>(fixtureTimeline as TimelineItem[]);
  const [runs, setRuns] = useState<AgentRun[]>([]);
  const [selectedRun, setSelectedRun] = useState<AgentRun | null>(null);
  const [activeTab, setActiveTab] = useState<"timeline" | "runs">("timeline");
  const [filterAgent, setFilterAgent] = useState<string>("all");
  const [loading, setLoading] = useState<boolean>(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const [statusRes, actRes, runsRes] = await Promise.allSettled([
        getAgentStatus(),
        getAgentActivity(),
        getAgentRuns({ limit: 30 }),
      ]);

      if (statusRes.status === "fulfilled" && statusRes.value?.items) {
        setAgentsList(statusRes.value.items);
      }
      if (actRes.status === "fulfilled" && actRes.value?.items) {
        setTimeline(actRes.value.items);
      }
      if (runsRes.status === "fulfilled" && runsRes.value?.items) {
        setRuns(runsRes.value.items);
      }
    } catch {
      // Fallback already provided in client
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const timer = setInterval(loadData, 15000);
    return () => clearInterval(timer);
  }, []);

  const filteredTimeline = filterAgent === "all"
    ? timeline
    : timeline.filter((t) => t.agent?.toLowerCase().includes(filterAgent.toLowerCase()) || t.name?.toLowerCase().includes(filterAgent.toLowerCase()));

  const filteredRuns = filterAgent === "all"
    ? runs
    : runs.filter((r) => r.agent?.toLowerCase().includes(filterAgent.toLowerCase()));

  return (
    <AppShell>
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <PageHeader
          title="Agent Orchestration & Control Plane"
          description="Autonomous agent lifecycle, policy boundaries, and live execution traces."
        />
        <div className="flex items-center gap-2">
          <button
            onClick={loadData}
            disabled={loading}
            className="px-3 py-1.5 rounded-lg border border-border-subtle bg-surface-container-lowest text-xs font-medium text-on-surface hover:bg-surface-elevated transition-colors flex items-center gap-2"
          >
            <RefreshCw size={14} className={loading ? "animate-spin" : ""} />
            {loading ? "Syncing..." : "Sync Runs"}
          </button>
        </div>
      </div>

      {/* Agents Card Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-8">
        {agentsList.map((agent) => (
          <GlassPanel
            key={agent.id}
            className={`flex flex-col gap-2 transition-all cursor-pointer ${
              filterAgent === agent.id ? "ring-2 ring-primary bg-primary/5" : "hover:border-border-focus"
            }`}
            onClick={() => setFilterAgent(filterAgent === agent.id ? "all" : agent.id)}
          >
            <div className="flex items-center justify-between">
              <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                <Bot size={15} className="text-primary" />
              </div>
              <StatusBadge status={agent.status || "active"} />
            </div>
            <p className="font-label-bold text-label-bold text-on-surface">{agent.name}</p>
            <p className="font-body-sm text-body-sm text-on-surface-variant line-clamp-2">{agent.description}</p>
            <div className="mt-2 flex items-center justify-between text-xs text-on-surface-variant pt-2 border-t border-border-subtle">
              <span className="flex items-center gap-1">
                <Shield size={12} className="text-secondary" /> Policy Guarded
              </span>
              <span className="font-data-mono">{agent.id}</span>
            </div>
          </GlassPanel>
        ))}
      </div>

      {/* Main Tabbed Panel */}
      <SolidPanel>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6 pb-4 border-b border-border-subtle">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveTab("timeline")}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                activeTab === "timeline"
                  ? "bg-primary/10 text-primary border border-primary/20"
                  : "text-on-surface-variant hover:text-on-surface"
              }`}
            >
              Live Activity Timeline ({filteredTimeline.length})
            </button>
            <button
              onClick={() => setActiveTab("runs")}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                activeTab === "runs"
                  ? "bg-primary/10 text-primary border border-primary/20"
                  : "text-on-surface-variant hover:text-on-surface"
              }`}
            >
              Execution Run Traces ({filteredRuns.length})
            </button>
          </div>

          {filterAgent !== "all" && (
            <div className="flex items-center gap-2">
              <span className="text-xs text-on-surface-variant">Filtered by:</span>
              <span className="text-xs px-2 py-1 rounded bg-primary/10 text-primary font-medium flex items-center gap-1">
                {filterAgent}
                <button onClick={() => setFilterAgent("all")}>
                  <X size={12} />
                </button>
              </span>
            </div>
          )}
        </div>

        {/* Timeline View */}
        {activeTab === "timeline" && (
          <div className="flex flex-col">
            {filteredTimeline.length === 0 ? (
              <div className="py-12 text-center text-on-surface-variant text-sm">
                No activity records found for the selected filter.
              </div>
            ) : (
              filteredTimeline.map((event, i) => (
                <div
                  key={`${event.time || event.timestamp}-${i}`}
                  className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 py-3.5 border-b border-border-subtle last:border-0 hover:bg-surface-elevated/40 px-2 rounded-lg transition-colors cursor-pointer"
                  onClick={() => {
                    const matchedRun = runs.find((r) => r.agent === event.agent || r.runId === event.agentRunId);
                    if (matchedRun) setSelectedRun(matchedRun);
                  }}
                >
                  <span className="font-data-mono text-data-mono text-on-surface-variant w-24 shrink-0 flex items-center gap-1.5">
                    <Clock size={12} className="text-on-surface-variant/60" />
                    {event.time || (event.timestamp ? new Date(event.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" }) : "Recent")}
                  </span>
                  <span className="font-label-bold text-label-bold text-on-surface w-48 shrink-0 flex items-center gap-2">
                    <Bot size={14} className="text-primary" />
                    {event.agent || event.name || "System"}
                  </span>
                  <span className="font-body-sm text-body-sm text-on-surface flex-1">
                    {event.event || event.action || event.reason || "Autonomous evaluation completed"}
                  </span>
                  {event.agentRunId && (
                    <span className="text-xs font-data-mono px-2 py-0.5 rounded bg-surface border border-border-subtle text-on-surface-variant shrink-0 flex items-center gap-1">
                      <Terminal size={11} /> {event.agentRunId.slice(0, 10)}
                    </span>
                  )}
                  <ChevronRight size={14} className="text-on-surface-variant/40 shrink-0 hidden sm:block" />
                </div>
              ))
            )}
          </div>
        )}

        {/* Run Traces View */}
        {activeTab === "runs" && (
          <div className="flex flex-col">
            {filteredRuns.length === 0 ? (
              <div className="py-12 text-center text-on-surface-variant text-sm">
                No active execution runs recorded yet. Runs are tracked automatically when agents coordinate actions.
              </div>
            ) : (
              filteredRuns.map((run) => (
                <div
                  key={run.runId}
                  onClick={() => setSelectedRun(run)}
                  className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 py-3.5 border-b border-border-subtle last:border-0 hover:bg-surface-elevated/40 px-3 rounded-lg transition-colors cursor-pointer"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-surface border border-border-subtle flex items-center justify-center text-primary">
                      <Activity size={16} />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-label-bold text-label-bold text-on-surface">{run.agent}</span>
                        <span className="text-xs text-on-surface-variant">({run.action})</span>
                      </div>
                      <span className="font-data-mono text-xs text-on-surface-variant">{run.runId}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    {run.durationMs !== undefined && (
                      <span className="font-data-mono text-xs text-on-surface-variant">
                        {run.durationMs.toFixed(1)} ms
                      </span>
                    )}
                    <span
                      className={`text-xs px-2.5 py-1 rounded-full font-medium ${
                        run.status === "completed"
                          ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                          : run.status === "failed"
                          ? "bg-rose-500/10 text-rose-400 border border-rose-500/20"
                          : "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                      }`}
                    >
                      {run.status}
                    </span>
                    <ChevronRight size={14} className="text-on-surface-variant/40" />
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </SolidPanel>

      {/* Trace Inspector Drawer / Modal */}
      {selectedRun && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex justify-end">
          <div className="w-full max-w-xl h-full bg-surface border-l border-border-subtle p-6 overflow-y-auto flex flex-col gap-6 shadow-2xl animate-in slide-in-from-right duration-200">
            <div className="flex items-center justify-between pb-4 border-b border-border-subtle">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
                  <Terminal size={18} />
                </div>
                <div>
                  <h3 className="font-headline-md text-headline-md text-on-surface">Agent Run Trace</h3>
                  <p className="font-data-mono text-xs text-on-surface-variant">{selectedRun.runId}</p>
                </div>
              </div>
              <button
                onClick={() => setSelectedRun(null)}
                className="p-1.5 rounded-lg hover:bg-surface-elevated text-on-surface-variant"
              >
                <X size={18} />
              </button>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="p-3 rounded-lg bg-surface-elevated border border-border-subtle">
                <p className="text-xs text-on-surface-variant">Agent Identity</p>
                <p className="font-label-bold text-sm text-on-surface mt-0.5">{selectedRun.agent}</p>
              </div>
              <div className="p-3 rounded-lg bg-surface-elevated border border-border-subtle">
                <p className="text-xs text-on-surface-variant">Target Action</p>
                <p className="font-label-bold text-sm text-on-surface mt-0.5">{selectedRun.action}</p>
              </div>
              <div className="p-3 rounded-lg bg-surface-elevated border border-border-subtle">
                <p className="text-xs text-on-surface-variant">Execution Status</p>
                <p className="font-label-bold text-sm text-emerald-400 mt-0.5 capitalize">{selectedRun.status}</p>
              </div>
              <div className="p-3 rounded-lg bg-surface-elevated border border-border-subtle">
                <p className="text-xs text-on-surface-variant">Elapsed Latency</p>
                <p className="font-data-mono text-sm text-on-surface mt-0.5">
                  {selectedRun.durationMs ? `${selectedRun.durationMs.toFixed(1)} ms` : "Instant Fast-Path"}
                </p>
              </div>
            </div>

            {selectedRun.policyEvaluationId && (
              <div className="p-3.5 rounded-lg bg-primary/5 border border-primary/20 flex items-start gap-3">
                <Shield size={16} className="text-primary shrink-0 mt-0.5" />
                <div>
                  <p className="text-xs font-medium text-primary">Policy Guard Gated</p>
                  <p className="text-xs text-on-surface-variant mt-0.5 font-data-mono">
                    Evaluation ID: {selectedRun.policyEvaluationId}
                  </p>
                </div>
              </div>
            )}

            {selectedRun.error && (
              <div className="p-3.5 rounded-lg bg-rose-500/10 border border-rose-500/20 flex items-start gap-3">
                <AlertTriangle size={16} className="text-rose-400 shrink-0 mt-0.5" />
                <div>
                  <p className="text-xs font-medium text-rose-400">Execution Error</p>
                  <p className="text-xs text-rose-300 mt-0.5">{selectedRun.error}</p>
                </div>
              </div>
            )}

            {selectedRun.inputPayload && (
              <div>
                <p className="text-xs font-semibold text-on-surface mb-2">Input Context</p>
                <pre className="p-3 rounded-lg bg-surface-elevated border border-border-subtle text-xs font-data-mono text-on-surface-variant overflow-x-auto">
                  {JSON.stringify(selectedRun.inputPayload, null, 2)}
                </pre>
              </div>
            )}

            {selectedRun.outputPayload && (
              <div>
                <p className="text-xs font-semibold text-on-surface mb-2">Execution Output</p>
                <pre className="p-3 rounded-lg bg-surface-elevated border border-border-subtle text-xs font-data-mono text-on-surface-variant overflow-x-auto">
                  {JSON.stringify(selectedRun.outputPayload, null, 2)}
                </pre>
              </div>
            )}

            <div className="mt-auto pt-4 border-t border-border-subtle flex justify-end">
              <button
                onClick={() => setSelectedRun(null)}
                className="px-4 py-2 rounded-lg border border-border-subtle bg-surface-elevated text-xs font-medium text-on-surface hover:bg-surface-container-lowest transition-colors"
              >
                Close Trace
              </button>
            </div>
          </div>
        </div>
      )}
    </AppShell>
  );
}
