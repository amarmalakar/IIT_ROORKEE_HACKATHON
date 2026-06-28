interface ComplexityDashboardProps {
  report?: Record<string, unknown>;
}

export function ComplexityDashboard({ report }: ComplexityDashboardProps) {
  if (!report || Object.keys(report).length === 0) {
    return (
      <div className="text-sm text-gray-500 italic">Complexity analysis will appear after optimization.</div>
    );
  }

  return (
    <div className="grid grid-cols-2 gap-3">
      <MetricCard label="Time Complexity" value={String(report.time_complexity || "—")} />
      <MetricCard label="Space Complexity" value={String(report.space_complexity || "—")} />
      <MetricCard label="Approach" value={String(report.selected_approach || "—")} />
      <MetricCard
        label="Improvement"
        value={String(report.improvement_over_initial || "—")}
        span
      />
    </div>
  );
}

function MetricCard({ label, value, span }: { label: string; value: string; span?: boolean }) {
  return (
    <div className={`bg-gray-800 rounded-lg p-3 ${span ? "col-span-2" : ""}`}>
      <div className="text-xs text-gray-400 mb-1">{label}</div>
      <div className="text-sm font-mono text-forge-300">{value}</div>
    </div>
  );
}
