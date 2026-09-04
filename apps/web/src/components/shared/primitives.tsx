import { ReactNode } from "react";
import { ArrowUpRight } from "lucide-react";

export function GlassPanel({
  children,
  className = "",
  strong = false,
  onClick,
}: {
  children: ReactNode;
  className?: string;
  strong?: boolean;
  onClick?: () => void;
}) {
  return (
    <div
      onClick={onClick}
      className={`${strong ? "glass-surface-strong" : "glass-surface"} rounded-xl p-6 ${className}`}
    >
      {children}
    </div>
  );
}

export function SolidPanel({
  children,
  className = "",
  onClick,
}: {
  children: ReactNode;
  className?: string;
  onClick?: () => void;
}) {
  return (
    <div
      onClick={onClick}
      className={`bg-surface-container-lowest border border-border-subtle rounded-xl p-6 ${className}`}
    >
      {children}
    </div>
  );
}

export function KpiCard({
  label,
  value,
  delta,
  deltaTone = "positive",
  hint,
}: {
  label: string;
  value: string;
  delta?: string;
  deltaTone?: "positive" | "neutral" | "warning";
  hint?: string;
}) {
  const toneClass =
    deltaTone === "positive"
      ? "text-growth-green"
      : deltaTone === "warning"
      ? "text-warning-amber"
      : "text-on-surface-variant";
  return (
    <GlassPanel className="flex flex-col gap-2">
      <span className="font-body-sm text-body-sm text-on-surface-variant">{label}</span>
      <span className="font-metric-display text-metric-display text-on-surface">{value}</span>
      {delta && (
        <span className={`flex items-center gap-1 font-label-bold text-label-bold ${toneClass}`}>
          {deltaTone === "positive" && <ArrowUpRight size={13} />}
          {delta}
        </span>
      )}
      {hint && <span className="font-body-sm text-body-sm text-on-surface-variant">{hint}</span>}
    </GlassPanel>
  );
}

const statusStyles: Record<string, string> = {
  ready_for_review: "bg-reasoning-blue/10 text-reasoning-blue",
  running_experiment: "bg-warning-amber/10 text-warning-amber",
  approved: "bg-growth-green/10 text-growth-green",
  declined: "bg-error/10 text-error",
  running: "bg-warning-amber/10 text-warning-amber",
  completed: "bg-growth-green/10 text-growth-green",
  paused: "bg-outline-variant/40 text-on-surface-variant",
  active: "bg-growth-green/10 text-growth-green",
  ready: "bg-reasoning-blue/10 text-reasoning-blue",
  error: "bg-error/10 text-error",
  success: "bg-growth-green/10 text-growth-green",
  blocked: "bg-error/10 text-error",
  failed: "bg-error/10 text-error",
  dismissed: "bg-amber-100/80 text-amber-800 border border-amber-200",
  uncertain: "bg-indigo-100/80 text-indigo-800 border border-indigo-200",
  payment_uncertain: "bg-indigo-100/80 text-indigo-800 border border-indigo-200",
  low: "bg-growth-green/10 text-growth-green",
  medium: "bg-warning-amber/10 text-warning-amber",
  high: "bg-error/10 text-error",
};

export function StatusBadge({ status, label }: { status: string; label?: string }) {
  const style = statusStyles[status] ?? "bg-outline-variant/40 text-on-surface-variant";
  const text = label ?? status.replace(/_/g, " ");
  return (
    <span className={`inline-flex items-center px-2.5 py-1 rounded-full font-label-bold text-label-bold capitalize ${style}`}>
      {text}
    </span>
  );
}

export function PageHeader({
  title,
  description,
  action,
}: {
  title: string;
  description?: string;
  action?: ReactNode;
}) {
  return (
    <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
      <div>
        <h1 className="font-headline-lg text-headline-lg text-on-surface">{title}</h1>
        {description && (
          <p className="font-body-base text-body-base text-on-surface-variant mt-1">{description}</p>
        )}
      </div>
      {action}
    </div>
  );
}
