import { motion } from "framer-motion";
import {
  FileText,
  Boxes,
  Truck,
  ScrollText,
  Newspaper,
  History,
  Radar,
  ShieldAlert,
  ListChecks,
  Sparkles,
  Check,
} from "lucide-react";

const STEPS = [
  { label: "Gathering supplier contract details", icon: FileText },
  { label: "Checking inventory levels", icon: Boxes },
  { label: "Reviewing vendor availability", icon: Truck },
  { label: "Checking company policies", icon: ScrollText },
  { label: "Scanning external news", icon: Newspaper },
  { label: "Reviewing past incident history", icon: History },
  { label: "Detecting weak signals", icon: Radar },
  { label: "Assessing overall risk", icon: ShieldAlert },
  { label: "Generating recommendations", icon: ListChecks },
  { label: "Preparing explainability report", icon: Sparkles },
];

function LoadingPanel({ currentStep }) {
  return (
    <motion.div
      initial={{ x: 320, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.35, ease: "easeOut" }}
      className="fixed top-0 right-0 h-full w-80 bg-white dark:bg-slate-900 border-l border-slate-100 dark:border-slate-800 shadow-xl p-6 flex flex-col gap-1 overflow-y-auto z-40"
    >
      <h2 className="text-sm font-bold text-slate-900 dark:text-white mb-1 tracking-tight">
        Running Analysis
      </h2>
      <p className="text-xs text-slate-400 dark:text-slate-500 mb-5">
        Step {Math.min(currentStep + 1, STEPS.length)} of {STEPS.length}
      </p>

      {STEPS.map((step, index) => {
        const isDone = index < currentStep;
        const isActive = index === currentStep;
        const Icon = step.icon;

        return (
          <motion.div
            key={step.label}
            initial={{ opacity: 0, x: 10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.03 }}
            className="flex items-center gap-3 py-2 text-sm"
          >
            <div
              className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 transition-colors ${
                isDone
                  ? "bg-brand-darkest dark:bg-brand-light text-white dark:text-slate-900"
                  : isActive
                  ? "bg-brand-lightest dark:bg-slate-800 text-brand-darkest dark:text-brand-light"
                  : "bg-slate-50 dark:bg-slate-800 text-slate-300 dark:text-slate-600"
              }`}
            >
              {isDone ? (
                <Check size={14} />
              ) : (
                <Icon size={14} className={isActive ? "animate-pulse" : ""} />
              )}
            </div>
            <span
              className={
                isDone
                  ? "text-slate-400 dark:text-slate-500 line-through"
                  : isActive
                  ? "text-slate-900 dark:text-white font-medium"
                  : "text-slate-400 dark:text-slate-500"
              }
            >
              {step.label}
            </span>
          </motion.div>
        );
      })}
    </motion.div>
  );
}

export default LoadingPanel;
export { STEPS };