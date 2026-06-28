import { Moon, Sun } from "lucide-react";

interface HeaderProps {
  dark: boolean;
  onToggleTheme: () => void;
}

export function Header({ dark, onToggleTheme }: HeaderProps) {
  return (
    <header className="flex items-center justify-between px-6 py-4 border-b border-gray-800 bg-gray-900/80 backdrop-blur">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-forge-600 flex items-center justify-center font-bold text-sm">
          CF
        </div>
        <div>
          <h1 className="text-lg font-semibold text-white">CodeForge AI</h1>
          <p className="text-xs text-gray-400">Persona-Driven Multi-Agent Engineering</p>
        </div>
      </div>
      <button
        onClick={onToggleTheme}
        className="p-2 rounded-lg bg-gray-800 hover:bg-gray-700 transition-colors"
        aria-label="Toggle theme"
      >
        {dark ? <Sun size={18} /> : <Moon size={18} />}
      </button>
    </header>
  );
}
