import { motion } from "framer-motion";
import { FileText, HelpCircle, ListChecks } from "lucide-react";

function SummaryCard({ explainability }) {
  if (!explainability) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.05 }}
      className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6"
    >
      <div className="flex items-center gap-2 mb-3">
        <FileText size={18} className="text-brand-darkest dark:text-brand-light" />
        <h2 className="text-lg font-bold text-slate-900 dark:text-white tracking-tight">
          Executive Summary
        </h2>
      </div>
      <p className="text-slate-600 dark:text-slate-300 leading-relaxed mb-4">
        {explainability.executive_summary}
      </p>

      {explainability.reasoning_steps?.length > 0 && (
        <div className="mt-4 pt-4 border-t border-slate-100 dark:border-slate-800">
          <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2 flex items-center gap-1.5">
            <ListChecks size={14} />
            Reasoning Steps
          </p>
          <ol className="flex flex-col gap-1.5">
            {explainability.reasoning_steps.map((step, i) => (
              <li key={i} className="text-sm text-slate-500 dark:text-slate-400 flex gap-2">
                <span className="font-semibold text-slate-400 dark:text-slate-500">{i + 1}.</span>
                {step}
              </li>
            ))}
          </ol>
        </div>
      )}

      {explainability.uncertainties?.length > 0 && (
        <div className="mt-4 pt-4 border-t border-slate-100 dark:border-slate-800">
          <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2 flex items-center gap-1.5">
            <HelpCircle size={14} />
            Uncertainties
          </p>
          <ul className="flex flex-col gap-1.5">
            {explainability.uncertainties.map((u, i) => (
              <li key={i} className="text-sm text-slate-500 dark:text-slate-400 flex gap-2">
                <span className="opacity-60">•</span>
                {u}
              </li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  );
}

export default SummaryCard;