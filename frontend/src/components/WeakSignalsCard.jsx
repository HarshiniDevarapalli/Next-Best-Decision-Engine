import { motion } from "framer-motion";
import { Radar, GitCompareArrows } from "lucide-react";

function WeakSignalsCard({ weakSignal }) {
  if (!weakSignal) return null;

  const hasShadow = weakSignal.shadow_comparison;
  const ruleBased = weakSignal.rule_based;
  const llm = weakSignal.llm;

  if (!ruleBased && !llm) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.1 }}
      className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6"
    >
      <div className="flex items-center gap-2 mb-4">
        <Radar size={18} className="text-brand-darkest dark:text-brand-light" />
        <h2 className="text-lg font-bold text-slate-900 dark:text-white tracking-tight">
          Weak Signal Detection
        </h2>
      </div>

      {hasShadow ? (
        <div>
          <div className="flex items-center gap-2 mb-4 px-3 py-2 rounded-lg bg-brand-lightest dark:bg-slate-800">
            <GitCompareArrows size={14} className="text-brand-darkest dark:text-brand-light" />
            <span className="text-xs font-semibold text-brand-darkest dark:text-brand-light">
              Shadow Mode Active — comparing rule-based vs. LLM detection
            </span>
          </div>
          <div className="grid md:grid-cols-2 gap-4">
            <SignalBlock title="Rule-Based" data={ruleBased} />
            <SignalBlock title="LLM-Based" data={llm} />
          </div>
        </div>
      ) : (
        <SignalBlock title={llm ? "LLM-Based" : "Rule-Based"} data={llm || ruleBased} />
      )}
    </motion.div>
  );
}

function SignalBlock({ title, data }) {
  if (!data) return null;

  return (
    <div className="bg-slate-50 dark:bg-slate-800/60 rounded-xl p-4">
      <p className="text-sm font-semibold text-slate-700 dark:text-slate-200 mb-2">{title}</p>
      {Array.isArray(data) ? (
        <ul className="flex flex-col gap-1.5">
          {data.map((s, i) => (
            <li key={i} className="text-sm text-slate-600 dark:text-slate-300 flex gap-2">
              <span className="opacity-60">•</span>
              {typeof s === "string" ? s : JSON.stringify(s)}
            </li>
          ))}
        </ul>
      ) : (
        <pre className="text-xs text-slate-600 dark:text-slate-300 whitespace-pre-wrap">
          {JSON.stringify(data, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default WeakSignalsCard;