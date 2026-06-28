interface SelectorProps {
  label: string;
  value: string;
  options: Array<{ id: string; name: string; description?: string }>;
  onChange: (value: string) => void;
}

export function Selector({ label, value, options, onChange }: SelectorProps) {
  return (
    <div className="flex flex-col gap-1">
      <label className="text-xs font-medium text-gray-400 uppercase tracking-wide">{label}</label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-100 focus:outline-none focus:ring-2 focus:ring-forge-500"
      >
        <option value="">Auto-detect</option>
        {options.map((opt) => (
          <option key={opt.id} value={opt.id}>
            {opt.name}
          </option>
        ))}
      </select>
    </div>
  );
}
