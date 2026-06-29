import { motion } from "framer-motion";
import { Trophy, Award } from "lucide-react";

function DecisionScoringCard({ decisionScoring }) {
  if (!decisionScoring?.ranked_decisions?.length) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.18 }}
      className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6"
    >
      <div className="flex items-center gap-2 mb-4">
        <Trophy size={18} className="text-brand-darkest dark:text-brand-light" />
        <h2 className="text-lg font-bold text-slate-900 dark:text-white tracking-tight">
          Decision Scoring
        </h2>
      </div>

      <div className="flex flex-col gap-3">
        {decisionScoring.ranked_decisions.map((d, i) => {
          const isBest = d.action === decisionScoring.best_decision;
          return (
            <div
              key={i}
              className={`rounded-xl p-4 ${
                isBest
                  ? "bg-brand-lightest dark:bg-slate-800 border border-brand-darkest dark:border-brand-light"
                  : "bg-slate-50 dark:bg-slate-800/60"
              }`}
            >
              <div className="flex items-start justify-between gap-3 mb-2">
                <p className="text-sm font-semibold text-slate-800 dark:text-slate-100 flex-1">
                  {isBest && <Award size={14} className="inline mr-1.5 text-brand-darkest dark:text-brand-light" />}
                  {d.action}
                </p>
                <span className="text-sm font-bold text-brand-darkest dark:text-brand-light shrink-0">
                  {d.overall_score}
                </span>
              </div>
              <div className="flex gap-3 text-xs text-slate-500 dark:text-slate-400 mb-2">
                <span>Feasibility: {d.feasibility}</span>
                <span>Value: {d.business_value}</span>
                <span>Risk: {d.operational_risk}</span>
                <span>Effort: {d.implementation_effort}</span>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400">{d.reasoning}</p>
            </div>
          );
        })}
      </div>
    </motion.div>
  );
}

export default DecisionScoringCard;