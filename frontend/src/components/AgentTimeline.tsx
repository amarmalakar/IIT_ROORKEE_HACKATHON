import { CheckCircle, Circle, Loader2, RefreshCw, XCircle } from "lucide-react";
import { TimelineEvent } from "../lib/api";

const AGENT_LABELS: Record<string, string> = {
  router: "Router",
  requirement_extraction: "Requirements",
  persona: "Persona",
  context_retrieval: "Context",
  language_specialist: "Code Gen",
  optimization: "Optimization",
  code_review: "Review",
  security_review: "Security",
  unit_test_generator: "Tests",
  execution: "Execution",
  evaluator: "Evaluator",
  explanation: "Explanation",
  documentation: "Docs",
};

const PIPELINE_ORDER = [
  "router",
  "requirement_extraction",
  "persona",
  "context_retrieval",
  "language_specialist",
  "optimization",
  "code_review",
  "security_review",
  "unit_test_generator",
  "execution",
  "evaluator",
  "explanation",
  "documentation",
];

interface AgentTimelineProps {
  events: TimelineEvent[];
  activeAgent: string;
  streaming: boolean;
}

function StatusIcon({ status, isLoop }: { status: string; isLoop?: boolean }) {
  if (isLoop) return <RefreshCw size={14} className="text-amber-400 shrink-0" />;
  if (status === "completed") return <CheckCircle size={14} className="text-green-400 shrink-0" />;
  if (status === "error") return <XCircle size={14} className="text-red-400 shrink-0" />;
  if (status === "running") return <Loader2 size={14} className="text-forge-400 animate-spin shrink-0" />;
  return <Circle size={14} className="text-gray-600 shrink-0" />;
}

export function AgentTimeline({ events, activeAgent, streaming }: AgentTimelineProps) {
  const runCounts: Record<string, number> = {};
  events.forEach((e) => {
    runCounts[e.agent] = (runCounts[e.agent] || 0) + 1;
  });

  const latestByAgent: Record<string, TimelineEvent> = {};
  events.forEach((e) => {
    latestByAgent[e.agent] = e;
  });

  const hasLoop = Object.values(runCounts).some((c) => c > 1);

  return (
    <div className="flex flex-col min-h-0">
      <div className="flex items-center justify-between mb-2 shrink-0">
        <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wide">Agent Timeline</h3>
        {hasLoop && (
          <span className="text-[10px] text-amber-400 flex items-center gap-1">
            <RefreshCw size={10} /> Loop active
          </span>
        )}
      </div>

      {/* Pipeline steps — scrollable, no overlap */}
      <div className="flex-1 min-h-0 max-h-[340px] overflow-y-auto overflow-x-hidden pr-1 space-y-1.5">
        {PIPELINE_ORDER.map((agent) => {
          const event = latestByAgent[agent];
          const runs = runCounts[agent] || 0;
          const isActive = streaming && activeAgent === agent;
          const status = isActive ? "running" : event?.status || "pending";
          const isLoop = runs > 1;

          return (
            <div
              key={agent}
              className={`flex items-start gap-2.5 px-2.5 py-2 rounded-lg text-sm shrink-0 ${
                isActive
                  ? "bg-forge-900/50 border border-forge-600"
                  : isLoop
                  ? "bg-amber-900/25 border border-amber-700/50"
                  : event
                  ? "bg-gray-800/40 border border-transparent"
                  : "opacity-50"
              }`}
            >
              <div className="pt-0.5">
                <StatusIcon status={status} isLoop={isLoop && !isActive} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-1.5 flex-wrap">
                  <span className="font-medium text-gray-200 text-xs">{AGENT_LABELS[agent]}</span>
                  {runs > 1 && (
                    <span className="text-[10px] text-amber-400 bg-amber-900/40 px-1 rounded">×{runs}</span>
                  )}
                  {isActive && (
                    <span className="text-[10px] text-forge-300">running…</span>
                  )}
                </div>
                {event?.summary && (
                  <p className="text-[11px] text-gray-500 mt-0.5 leading-snug break-words line-clamp-2">
                    {event.summary}
                    {event.duration_ms != null && event.duration_ms > 0 && (
                      <span className="text-gray-600"> · {event.duration_ms}ms</span>
                    )}
                  </p>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Event log — separate scroll area */}
      {events.length > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-800 shrink-0">
          <p className="text-[10px] text-gray-500 mb-1.5 uppercase tracking-wide">
            Event log ({events.length})
          </p>
          <div className="max-h-[100px] overflow-y-auto space-y-1 pr-1">
            {events.map((e, i) => (
              <p key={i} className="text-[10px] text-gray-500 leading-snug break-words">
                <span className="text-gray-400">{AGENT_LABELS[e.agent] || e.agent}:</span>{" "}
                {e.summary || e.status}
              </p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
