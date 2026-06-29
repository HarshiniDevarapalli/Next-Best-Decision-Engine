import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Database, ChevronDown } from "lucide-react";

function formatLabel(key) {
  return key
    .replace(/Agent$/, "")
    .replace(/([A-Z])/g, " $1")
    .trim();
}

function ValueRenderer({ value }) {
  if (value === null || value === undefined || value === "") return null;

  if (Array.isArray(value)) {
    return (
      <ul className="flex flex-col gap-1.5">
        {value.map((item, i) => (
          <li key={i} className="text-sm text-slate-600 dark:text-slate-300 flex gap-2">
            <span className="opacity-60 mt-0.5">•</span>
            <span>
              {typeof item === "object" ? <ValueRenderer value={item} /> : String(item)}
            </span>
          </li>
        ))}
      </ul>
    );
  }

  if (typeof value === "object") {
    return (
      <div className="flex flex-col gap-1">
        {Object.entries(value).map(([k, v]) => (
          <div key={k} className="flex justify-between gap-4 py-1 text-sm border-b border-slate-100 dark:border-slate-800 last:border-0">
            <span className="text-slate-400 dark:text-slate-500">{formatLabel(k)}</span>
            <span className="text-slate-700 dark:text-slate-200 font-medium text-right">
              {typeof v === "object" ? JSON.stringify(v) : String(v)}
            </span>
          </div>
        ))}
      </div>
    );
  }

  return <p className="text-sm text-slate-600 dark:text-slate-300">{String(value)}</p>;
}

function EvidenceCard({ contextData }) {
  const [open, setOpen] = useState(false);

  if (!contextData || Object.keys(contextData).length === 0) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.28 }}
      className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6"
    >
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between text-left"
      >
        <div className="flex items-center gap-2">
          <Database size={18} className="text-brand-darkest dark:text-brand-light" />
          <h2 className="text-lg font-bold text-slate-900 dark:text-white tracking-tight">
            Supporting Evidence
          </h2>
        </div>
        <motion.div animate={{ rotate: open ? 180 : 0 }} transition={{ duration: 0.2 }}>
          <ChevronDown size={18} className="text-slate-400" />
        </motion.div>
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25 }}
            className="overflow-hidden"
          >
            <div className="mt-5 flex flex-col gap-5">
              {Object.entries(contextData).map(([key, value]) => {
                if (!value) return null;
                return (
                  <div
                    key={key}
                    className="pt-4 border-t border-slate-100 dark:border-slate-800 first:border-0 first:pt-0"
                  >
                    <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
                      {formatLabel(key)}
                    </p>
                    <ValueRenderer value={value} />
                  </div>
                );
              })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

export default EvidenceCard;