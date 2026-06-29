import { motion } from "framer-motion";
import { DollarSign } from "lucide-react";

function CostAnalysisCard({ costAnalysis }) {
  if (!costAnalysis?.impacts?.length) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.2 }}
      className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6"
    >
      <div className="flex items-center gap-2 mb-4">
        <DollarSign size={18} className="text-brand-darkest dark:text-brand-light" />
        <h2 className="text-lg font-bold text-slate-900 dark:text-white tracking-tight">
          Cost Impact Analysis
        </h2>
      </div>

      <div className="flex flex-col gap-3">
        {costAnalysis.impacts.map((impact, i) => {
          const isLowest = impact.action === costAnalysis.lowest_cost_option;
          const isHighestROI = impact.action === costAnalysis.highest_roi_option;
          return (
            <div key={i} className="bg-slate-50 dark:bg-slate-800/60 rounded-xl p-4">
              <div className="flex items-center gap-2 flex-wrap mb-2">
                <p className="text-sm font-semibold text-slate-800 dark:text-slate-100">{impact.action}</p>
                {isLowest && (
                  <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-brand-lightest dark:bg-slate-700 text-brand-darkest dark:text-brand-light">
                    Lowest Cost
                  </span>
                )}
                {isHighestROI && (
                  <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-brand-darkest dark:bg-brand-light text-white dark:text-slate-900">
                    Highest ROI
                  </span>
                )}
              </div>
              <p className="text-sm text-slate-600 dark:text-slate-300 mb-1">
                <span className="font-semibold">Cost: </span>{impact.estimated_cost}
              </p>
              <p className="text-sm text-slate-600 dark:text-slate-300 mb-1">
                <span className="font-semibold">ROI: </span>{impact.roi}
              </p>
              <p className="text-sm text-slate-500 dark:text-slate-400">{impact.financial_impact}</p>
            </div>
          );
        })}
      </div>
    </motion.div>
  );
}

export default CostAnalysisCard;