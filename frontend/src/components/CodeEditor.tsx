import Editor from "@monaco-editor/react";
import { Copy, Download } from "lucide-react";

interface CodeEditorProps {
  code: string;
  language: string;
  onChange?: (value: string) => void;
  readOnly?: boolean;
}

const LANG_MAP: Record<string, string> = {
  python: "python",
  sql: "sql",
  java: "java",
  javascript: "javascript",
  typescript: "typescript",
  cpp: "cpp",
  go: "go",
  bash: "shell",
  pyspark: "python",
};

export function CodeEditor({ code, language, onChange, readOnly = true }: CodeEditorProps) {
  const monacoLang = LANG_MAP[language] || "python";

  const handleCopy = () => navigator.clipboard.writeText(code);
  const handleDownload = () => {
    const blob = new Blob([code], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `solution.${language === "python" ? "py" : language}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex flex-col h-full rounded-lg border border-gray-700 overflow-hidden">
      <div className="flex items-center justify-between px-3 py-2 bg-gray-800 border-b border-gray-700">
        <span className="text-xs text-gray-400 font-mono">{monacoLang}</span>
        <div className="flex gap-2">
          <button onClick={handleCopy} className="p-1 hover:bg-gray-700 rounded" title="Copy">
            <Copy size={14} />
          </button>
          <button onClick={handleDownload} className="p-1 hover:bg-gray-700 rounded" title="Download">
            <Download size={14} />
          </button>
        </div>
      </div>
      <Editor
        height="100%"
        language={monacoLang}
        value={code}
        onChange={(v) => onChange?.(v || "")}
        theme="vs-dark"
        options={{
          readOnly,
          minimap: { enabled: false },
          fontSize: 13,
          scrollBeyondLastLine: false,
          padding: { top: 8 },
        }}
      />
    </div>
  );
}
