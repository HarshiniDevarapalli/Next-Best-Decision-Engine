import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FlaskConical, ChevronDown, TrendingUp, TrendingDown, Minus } from "lucide-react";

const PROBABILITY_COLOR = {
  high: "text-brand-darkest dark:text-brand-light",
  medium: "text-amber-600 dark:text-amber-400",
  low: "text-red-500",
};

function getProbabilityTier(p) {
  if (p >= 0.4) return "high";
  if (p >= 0.2) return "medium";
  return "low";
}

function ScenarioCard({ scenario, isBest, isWorst }) {
  const [open, setOpen] = useState(false);
  const tier = getProbabilityTier(scenario.probability);

  return (
    <div
      className={`rounded-xl border p-4 ${
        isBest
          ? "border-brand-darkest dark:border-brand-light bg-brand-lightest dark:bg-slate-800"
          : isWorst
          ? "border-red-300 dark:border-red-800 bg-red-50 dark:bg-red-950/20"
          : "border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60"
      }`}
    >
      <button onClick={() => setOpen(!open)} className="w-full flex items-center justify-between text-left">
        <div className="flex-1 pr-3">
          <div className="flex items-center gap-2 mb-1">
            <p className="text-sm font-bold text-slate-900 dark:text-white">{scenario.title}</p>
            {isBest && (
              <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-brand-darkest dark:bg-brand-light text-white dark:text-slate-900">
                Best
              </span>
            )}
            {isWorst && (
              <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-red-500 text-white">
                Worst
              </span>
            )}
          </div>
          <p className={`text-xs font-semibold ${PROBABILITY_COLOR[tier]}`}>
            {Math.round(scenario.probability * 100)}% probability
          </p>
        </div>
        <motion.div animate={{ rotate: open ? 180 : 0 }}>
          <ChevronDown size={16} className="text-slate-400" />
        </motion.div>
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className="mt-3 pt-3 border-t border-current/10 flex flex-col gap-2 text-sm text-slate-600 dark:text-slate-300">
              <p>{scenario.description}</p>
              <p><span className="font-semibold">Business impact: </span>{scenario.business_impact}</p>
              <p><span className="font-semibold">Operational impact: </span>{scenario.operational_impact}</p>
              <p><span className="font-semibold">Recommended action: </span>{scenario.recommended_action}</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function WhatIfSimulator({ simulation }) {
  if (!simulation) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.15 }}
      className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6"
    >
      <div className="flex items-center gap-2 mb-4">
        <FlaskConical size={18} className="text-brand-darkest dark:text-brand-light" />
        <h2 className="text-lg font-bold text-slate-900 dark:text-white tracking-tight">
          What-If Simulation
        </h2>
      </div>

      {simulation.baseline && (
        <p className="text-sm text-slate-500 dark:text-slate-400 mb-4 italic">
          {simulation.baseline}
        </p>
      )}

      <div className="flex flex-col gap-3">
        {simulation.scenarios?.map((s, i) => (
          <ScenarioCard
            key={i}
            scenario={s}
            isBest={s.title === simulation.best_scenario}
            isWorst={s.title === simulation.worst_scenario}
          />
        ))}
      </div>

      {simulation.assumptions?.length > 0 && (
        <div className="mt-5 pt-4 border-t border-slate-100 dark:border-slate-800">
          <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Assumptions</p>
          <ul className="flex flex-col gap-1.5">
            {simulation.assumptions.map((a, i) => (
              <li key={i} className="text-sm text-slate-500 dark:text-slate-400 flex gap-2">
                <span className="opacity-60">•</span>
                {a}
              </li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  );
}

export default WhatIfSimulator;