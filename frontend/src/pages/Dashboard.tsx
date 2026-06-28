import { useEffect, useMemo, useState } from "react";
import { Loader2, Zap } from "lucide-react";
import { Header } from "../components/Header";
import { Selector } from "../components/Selector";
import { CodeEditor } from "../components/CodeEditor";
import { AgentTimeline } from "../components/AgentTimeline";
import { WorkflowGraph } from "../components/WorkflowGraph";
import { ComplexityDashboard } from "../components/ComplexityDashboard";
import { ExecutionLogs } from "../components/ExecutionLogs";
import {
  extractApiError,
  fetchLanguages,
  fetchModels,
  fetchPersonas,
  generateCode,
  Language,
  ModelInfo,
  Persona,
  WorkflowState,
} from "../lib/api";

type Tab = "code" | "tests" | "explanation";

export default function Dashboard() {
  const [dark, setDark] = useState(true);
  const [request, setRequest] = useState(
    "Write a Python function to check if a string is a palindrome."
  );
  const [persona, setPersona] = useState("");
  const [language, setLanguage] = useState("");
  const [model, setModel] = useState("");
  const [personas, setPersonas] = useState<Persona[]>([]);
  const [languages, setLanguages] = useState<Language[]>([]);
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [state, setState] = useState<WorkflowState>({});
  const [tab, setTab] = useState<Tab>("code");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const timeline = useMemo(() => state.agent_timeline ?? [], [state.agent_timeline]);

  const activeAgent = useMemo(() => {
    if (loading || timeline.length === 0) return "";
    const last = timeline[timeline.length - 1];
    return last.status === "completed" ? last.agent : "";
  }, [loading, timeline]);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
  }, [dark]);

  useEffect(() => {
    Promise.all([fetchPersonas(), fetchLanguages(), fetchModels()]).then(
      ([p, l, m]) => {
        setPersonas(p);
        setLanguages(l);
        setModels(m.map((x) => ({ ...x, id: (x as ModelInfo & { id?: string }).id || String((x as unknown as { id: string }).id) })));
      }
    ).catch(() => {});
  }, []);

  const handleGenerate = async () => {
    setError("");
    setLoading(true);
    setState({});
    try {
      const result = await generateCode({ request, persona, language, model });
      setState(result);
    } catch (e) {
      setError(extractApiError(e));
    } finally {
      setLoading(false);
    }
  };

  const displayCode = state.optimized_code || state.generated_code || "";
  const displayLang = language || "python";

  return (
    <div className="min-h-screen flex flex-col bg-gray-950">
      <Header dark={dark} onToggleTheme={() => setDark(!dark)} />

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <aside className="w-80 border-r border-gray-800 p-4 flex flex-col gap-3 overflow-hidden min-h-0">
          <Selector label="Persona" value={persona} options={personas} onChange={setPersona} />
          <Selector label="Language" value={language} options={languages} onChange={setLanguage} />
          <Selector
            label="Model"
            value={model}
            options={models.map((m) => ({
              id: (m as ModelInfo & { id: string }).id,
              name: (m as ModelInfo & { id: string }).id,
            }))}
            onChange={setModel}
          />

          <div className="flex flex-col gap-1 shrink-0">
            <label className="text-xs font-medium text-gray-400 uppercase tracking-wide">Request</label>
            <textarea
              value={request}
              onChange={(e) => setRequest(e.target.value)}
              rows={4}
              className="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-100 resize-none focus:outline-none focus:ring-2 focus:ring-forge-500"
            />
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading || !request.trim()}
            className="flex items-center justify-center gap-2 bg-forge-600 hover:bg-forge-500 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg py-2.5 text-sm font-medium transition-colors shrink-0"
          >
            {loading ? (
              <><Loader2 size={16} className="animate-spin" /> Running...</>
            ) : (
              <><Zap size={16} /> Generate</>
            )}
          </button>

          {error && <p className="text-xs text-red-400 shrink-0 break-words">{error}</p>}

          <div className="flex-1 min-h-0 overflow-hidden">
            <AgentTimeline events={timeline} activeAgent={activeAgent} streaming={loading} />
          </div>
        </aside>

        {/* Main content */}
        <main className="flex-1 flex flex-col overflow-hidden p-4 gap-4">
          <WorkflowGraph activeAgent={activeAgent} />

          <div className="flex gap-2">
            {(["code", "tests", "explanation"] as Tab[]).map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`px-4 py-1.5 rounded-lg text-sm capitalize transition-colors ${
                  tab === t ? "bg-forge-600 text-white" : "bg-gray-800 text-gray-400 hover:text-white"
                }`}
              >
                {t}
              </button>
            ))}
            {state.evaluation && (
              <span className="ml-auto flex items-center gap-2 text-sm">
                <span className="text-gray-400">Verdict:</span>
                <span
                  className={`font-semibold ${
                    (state.evaluation as { verdict?: string }).verdict === "PASS"
                      ? "text-green-400"
                      : "text-red-400"
                  }`}
                >
                  {String((state.evaluation as { verdict?: string }).verdict || "—")}
                </span>
                <span className="text-gray-500">
                  ({String((state.evaluation as { confidence_score?: number }).confidence_score ?? "—")})
                </span>
                {state.loop_count != null && state.loop_count > 0 && (
                  <span className="text-gray-500">· {state.loop_count} loop(s)</span>
                )}
              </span>
            )}
          </div>

          <div className="flex-1 min-h-0">
            {tab === "code" && (
              <CodeEditor code={displayCode || "# Generated code will appear here..."} language={displayLang} />
            )}
            {tab === "tests" && (
              <CodeEditor
                code={state.tests || "# Generated tests will appear here..."}
                language={displayLang}
              />
            )}
            {tab === "explanation" && (
              <div className="h-full overflow-auto bg-gray-900 rounded-lg border border-gray-700 p-4 text-sm text-gray-300 prose prose-invert max-w-none">
                <pre className="whitespace-pre-wrap font-sans">
                  {state.explanation || "Explanation will appear after the pipeline completes."}
                </pre>
              </div>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-900 rounded-lg border border-gray-700 p-4">
              <h3 className="text-xs font-semibold text-gray-400 uppercase mb-3">Complexity</h3>
              <ComplexityDashboard report={state.optimization_report} />
            </div>
            <div className="bg-gray-900 rounded-lg border border-gray-700 p-4">
              <h3 className="text-xs font-semibold text-gray-400 uppercase mb-3">Execution</h3>
              <ExecutionLogs result={state.execution_result} />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
