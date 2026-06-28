import { motion } from "framer-motion";
import { STEPS } from "./LoadingPanel";

function ProgressBar({ currentStep }) {
  const percent = Math.min((currentStep / STEPS.length) * 100, 100);
  const activeLabel = STEPS[Math.min(currentStep, STEPS.length - 1)].label;

  return (
    <div className="flex flex-col items-center justify-center py-20 px-4">
      <div className="w-full max-w-md">
        <div className="flex justify-between mb-2.5">
          <motion.span
            key={activeLabel}
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-sm font-medium text-slate-700 dark:text-slate-300"
          >
            {activeLabel}
          </motion.span>
          <span className="text-sm font-semibold text-brand-darkest dark:text-brand-light">
            {Math.round(percent)}%
          </span>
        </div>
        <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-brand-darkest dark:bg-brand-light rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${percent}%` }}
            transition={{ duration: 0.4, ease: "easeOut" }}
          />
        </div>
      </div>
    </div>
  );
}

export default ProgressBar;