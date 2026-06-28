interface ExecutionLogsProps {
  result?: Record<string, unknown>;
}

export function ExecutionLogs({ result }: ExecutionLogsProps) {
  if (!result || Object.keys(result).length === 0) {
    return <div className="text-sm text-gray-500 italic">Execution logs will appear after running tests.</div>;
  }

  const status = String(result.execution_status || "unknown");
  const summary = result.tests_summary as Record<string, number> | undefined;

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2">
        <span className="text-xs text-gray-400">Status:</span>
        <span
          className={`text-xs font-semibold px-2 py-0.5 rounded ${
            status === "success"
              ? "bg-green-900 text-green-300"
              : status === "skipped"
              ? "bg-yellow-900 text-yellow-300"
              : "bg-red-900 text-red-300"
          }`}
        >
          {status}
        </span>
        {result.runtime_ms != null && (
          <span className="text-xs text-gray-500">{String(result.runtime_ms)}ms</span>
        )}
      </div>
      {summary && (
        <div className="grid grid-cols-4 gap-2 text-center">
          {["total", "passed", "failed", "errors"].map((k) => (
            <div key={k} className="bg-gray-800 rounded p-2">
              <div className="text-lg font-bold text-white">{summary[k] ?? 0}</div>
              <div className="text-xs text-gray-400 capitalize">{k}</div>
            </div>
          ))}
        </div>
      )}
      {Boolean(result.stdout) && (
        <pre className="text-xs bg-gray-900 rounded p-2 overflow-auto max-h-32 text-green-300 font-mono">
          {String(result.stdout).slice(0, 500)}
        </pre>
      )}
      {Boolean(result.stderr) && status !== "success" && (
        <pre className="text-xs bg-red-950/40 border border-red-900 rounded p-2 overflow-auto max-h-32 text-red-300 font-mono">
          {String(result.stderr).slice(0, 800)}
        </pre>
      )}
      {Boolean(result.traceback) && result.traceback !== result.stderr && (
        <pre className="text-xs bg-gray-900 rounded p-2 overflow-auto max-h-24 text-orange-300 font-mono">
          {String(result.traceback).slice(0, 400)}
        </pre>
      )}
      {Boolean(result.sandbox_notes) && status === "success" && (
        <p className="text-xs text-gray-500">{String(result.sandbox_notes)}</p>
      )}
    </div>
  );
}
