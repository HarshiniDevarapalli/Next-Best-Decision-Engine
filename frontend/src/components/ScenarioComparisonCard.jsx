import { motion } from "framer-motion";
import { GitCompare, ThumbsUp, ThumbsDown } from "lucide-react";

function ScenarioComparisonCard({ scenarioComparison }) {
  if (!scenarioComparison?.comparisons?.length) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.24 }}
      className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6"
    >
      <div className="flex items-center gap-2 mb-4">
        <GitCompare size={18} className="text-brand-darkest dark:text-brand-light" />
        <h2 className="text-lg font-bold text-slate-900 dark:text-white tracking-tight">
          Scenario Comparison
        </h2>
      </div>

      <div className="flex flex-col gap-4">
        {scenarioComparison.comparisons.map((c, i) => {
          const isRecommended = c.scenario === scenarioComparison.recommended_scenario;
          return (
            <div
              key={i}
              className={`rounded-xl p-4 ${
                isRecommended
                  ? "bg-brand-lightest dark:bg-slate-800 border border-brand-darkest dark:border-brand-light"
                  : "bg-slate-50 dark:bg-slate-800/60"
              }`}
            >
              <div className="flex items-center justify-between gap-2 mb-3">
                <p className="text-sm font-bold text-slate-900 dark:text-white">
                  {c.scenario}
                </p>
                <span className="text-sm font-bold text-brand-darkest dark:text-brand-light">
                  Score: {c.score}/10
                </span>
              </div>

              <div className="grid md:grid-cols-2 gap-3">
                {c.advantages?.length > 0 && (
                  <div>
                    <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1.5 flex items-center gap-1">
                      <ThumbsUp size={12} />
                      Advantages
                    </p>
                    <ul className="flex flex-col gap-1">
                      {c.advantages.slice(0, 3).map((a, j) => (
                        <li key={j} className="text-xs text-slate-500 dark:text-slate-400 flex gap-1.5">
                          <span className="opacity-60">•</span>
                          {a}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {c.disadvantages?.length > 0 && (
                  <div>
                    <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1.5 flex items-center gap-1">
                      <ThumbsDown size={12} />
                      Disadvantages
                    </p>
                    <ul className="flex flex-col gap-1">
                      {c.disadvantages.slice(0, 3).map((d, j) => (
                        <li key={j} className="text-xs text-slate-500 dark:text-slate-400 flex gap-1.5">
                          <span className="opacity-60">•</span>
                          {d}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {scenarioComparison.reasoning && (
        <p className="text-sm text-slate-500 dark:text-slate-400 mt-4 pt-4 border-t border-slate-100 dark:border-slate-800 italic">
          {scenarioComparison.reasoning}
        </p>
      )}
    </motion.div>
  );
}

export default ScenarioComparisonCard;