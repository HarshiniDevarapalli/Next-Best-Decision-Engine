import { motion } from "framer-motion";
import { FileText } from "lucide-react";

function SummaryCard({ explainabilityReport }) {
  if (!explainabilityReport) return null;

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
      <p className="text-slate-600 dark:text-slate-300 leading-relaxed">
        {explainabilityReport.executive_summary}
      </p>

      {explainabilityReport.reasoning && (
        <p className="text-sm text-slate-400 dark:text-slate-500 mt-3 italic">
          {explainabilityReport.reasoning}
        </p>
      )}
    </motion.div>
  );
}

export default SummaryCard;