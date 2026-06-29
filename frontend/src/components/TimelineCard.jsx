import { motion } from "framer-motion";
import { Clock, AlertCircle } from "lucide-react";

function TimelineCard({ timelinePrediction }) {
  if (!timelinePrediction) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.22 }}
      className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6"
    >
      <div className="flex items-center gap-2 mb-2">
        <Clock size={18} className="text-brand-darkest dark:text-brand-light" />
        <h2 className="text-lg font-bold text-slate-900 dark:text-white tracking-tight">
          Timeline Prediction
        </h2>
      </div>

      {timelinePrediction.estimated_recovery_time && (
        <p className="text-sm font-semibold text-brand-darkest dark:text-brand-light mb-4">
          Estimated recovery: {timelinePrediction.estimated_recovery_time}
        </p>
      )}

      {timelinePrediction.stages?.length > 0 && (
        <div className="flex flex-col gap-3 mb-4">
          {timelinePrediction.stages.map((stage, i) => (
            <div key={i} className="flex gap-3">
              <div className="flex flex-col items-center pt-1">
                <div className="w-2.5 h-2.5 rounded-full bg-brand-darkest dark:bg-brand-light shrink-0" />
                {i < timelinePrediction.stages.length - 1 && (
                  <div className="w-0.5 flex-1 bg-slate-200 dark:bg-slate-700 mt-1" />
                )}
              </div>
              <div className="pb-3">
                <p className="text-sm font-semibold text-slate-800 dark:text-slate-100">
                  {stage.stage}
                  <span className="ml-2 text-xs font-normal text-slate-400">{stage.estimated_duration}</span>
                </p>
                <p className="text-sm text-slate-500 dark:text-slate-400">{stage.milestone}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {timelinePrediction.blockers?.length > 0 && (
        <div className="pt-4 border-t border-slate-100 dark:border-slate-800">
          <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2 flex items-center gap-1.5">
            <AlertCircle size={14} />
            Blockers
          </p>
          <ul className="flex flex-col gap-1.5">
            {timelinePrediction.blockers.map((b, i) => (
              <li key={i} className="text-sm text-slate-500 dark:text-slate-400 flex gap-2">
                <span className="opacity-60">•</span>
                {b}
              </li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  );
}

export default TimelineCard;