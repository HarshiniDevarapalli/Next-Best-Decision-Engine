import { motion } from "framer-motion";
import { Users } from "lucide-react";

function StakeholdersCard({ recommendation }) {
  if (!recommendation?.stakeholders?.length) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.26 }}
      className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6"
    >
      <div className="flex items-center gap-2 mb-4">
        <Users size={18} className="text-brand-darkest dark:text-brand-light" />
        <h2 className="text-lg font-bold text-slate-900 dark:text-white tracking-tight">
          Stakeholders to Notify
        </h2>
      </div>
      <div className="flex gap-2 flex-wrap">
        {recommendation.stakeholders.map((person) => (
          <span
            key={person}
            className="px-3.5 py-1.5 rounded-full bg-brand-lightest dark:bg-slate-800 text-brand-darkest dark:text-brand-light text-sm font-medium"
          >
            {person}
          </span>
        ))}
      </div>
    </motion.div>
  );
}

export default StakeholdersCard;