import { motion } from "framer-motion";
import { Radar } from "lucide-react";

function WeakSignalsCard({ weakSignalReport }) {
  if (!weakSignalReport?.signals) return null;

  const severityStyles = {
    critical: "bg-red-500",
    high: "bg-orange-500",
    medium: "bg-amber-500",
    low: "bg-brand-dark",
  };

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
          Weak Signals Detected ({weakSignalReport.signals.length})
        </h2>
      </div>

      <div className="flex flex-col gap-3">
        {weakSignalReport.signals.map((signal, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.05 }}
            className="flex gap-3 p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60"
          >
            <div
              className={`w-1.5 rounded-full shrink-0 ${
                severityStyles[signal.severity] || "bg-slate-400"
              }`}
            />
            <div className="flex-1">
              <div className="flex items-center justify-between flex-wrap gap-2">
                <p className="font-semibold text-slate-900 dark:text-white capitalize text-sm">
                  {signal.signal.replace(/_/g, " ")}
                </p>
                <span className="text-xs uppercase font-bold text-slate-400 dark:text-slate-500">
                  {signal.severity} · {Math.round(signal.confidence * 100)}%
                </span>
              </div>
              <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                {signal.explanation}
              </p>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}

export default WeakSignalsCard;