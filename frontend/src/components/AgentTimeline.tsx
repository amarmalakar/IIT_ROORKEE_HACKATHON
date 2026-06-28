import { CheckCircle, Circle, Loader2, XCircle } from "lucide-react";
import { TimelineEvent } from "../lib/api";

const AGENT_LABELS: Record<string, string> = {
  router: "Router",
  requirement_extraction: "Requirements",
  persona: "Persona",
  language_specialist: "Code Gen",
  code_review: "Review",
  execution: "Execution",
  explanation: "Explanation",
};

const ALL_AGENTS = Object.keys(AGENT_LABELS);

interface AgentTimelineProps {
  events: TimelineEvent[];
  activeAgent: string;
  streaming: boolean;
}

function StatusIcon({ status }: { status: string }) {
  if (status === "completed") return <CheckCircle size={16} className="text-green-400" />;
  if (status === "error") return <XCircle size={16} className="text-red-400" />;
  if (status === "running") return <Loader2 size={16} className="text-forge-400 animate-spin" />;
  return <Circle size={16} className="text-gray-600" />;
}

export function AgentTimeline({ events, activeAgent, streaming }: AgentTimelineProps) {
  const eventMap = Object.fromEntries(events.map((e) => [e.agent, e]));

  return (
    <div className="flex flex-col gap-1">
      <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Agent Timeline</h3>
      <div className="space-y-1 max-h-80 overflow-y-auto">
        {ALL_AGENTS.map((agent) => {
          const event = eventMap[agent];
          const isActive = streaming && activeAgent === agent;
          const status = isActive ? "running" : event?.status || "pending";
          return (
            <div
              key={agent}
              className={`flex items-start gap-2 px-2 py-1.5 rounded-lg text-sm ${
                isActive ? "bg-forge-900/40 border border-forge-700" : "hover:bg-gray-800/50"
              }`}
            >
              <StatusIcon status={status} />
              <div className="flex-1 min-w-0">
                <div className="font-medium text-gray-200">{AGENT_LABELS[agent]}</div>
                {event?.summary && (
                  <div className="text-xs text-gray-500 truncate">
                    {event.summary}
                    {event.duration_ms != null && event.duration_ms > 0 && (
                      <span className="text-gray-600"> · {event.duration_ms}ms</span>
                    )}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
