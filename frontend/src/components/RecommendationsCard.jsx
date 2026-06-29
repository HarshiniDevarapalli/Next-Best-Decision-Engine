import { motion } from "framer-motion";
import { ListChecks, Zap, Calendar, TrendingUp, Users, AlertOctagon } from "lucide-react";

function ActionList({ icon: Icon, title, items }) {
  if (!items?.length) return null;

  return (
    <div>
      <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2.5 flex items-center gap-1.5">
        <Icon size={14} className="text-brand-darkest dark:text-brand-light" />
        {title}
      </p>
      <ul className="flex flex-col gap-2">
        {items.map((item, index) => (
          <li key={index} className="flex gap-2 text-sm text-slate-600 dark:text-slate-300">
            <span className="mt-1.5 w-1 h-1 rounded-full bg-brand-darkest dark:bg-brand-light shrink-0" />
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

function RecommendationsCard({ recommendation }) {
  if (!recommendation) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.1 }}
      className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6"
    >
      <div className="flex items-center justify-between flex-wrap gap-2 mb-5">
        <div className="flex items-center gap-2">
          <ListChecks size={18} className="text-brand-darkest dark:text-brand-light" />
          <h2 className="text-lg font-bold text-slate-900 dark:text-white tracking-tight">
            Recommendations
          </h2>
        </div>
        <span className="text-xs font-bold uppercase px-2.5 py-1 rounded-full bg-brand-lightest dark:bg-slate-800 text-brand-darkest dark:text-brand-light">
          {recommendation.priority} priority
        </span>
      </div>

      <div className="grid md:grid-cols-3 gap-6 mb-5">
        <ActionList icon={Zap} title="Immediate Actions" items={recommendation.immediate_actions} />
        <ActionList icon={Calendar} title="Short-Term Actions" items={recommendation.short_term_actions} />
        <ActionList icon={TrendingUp} title="Long-Term Actions" items={recommendation.long_term_actions} />
      </div>

      <ActionList icon={AlertOctagon} title="Business Continuity Actions" items={recommendation.business_continuity_actions} />

      {recommendation.stakeholders?.length > 0 && (
        <div className="mt-5 pt-4 border-t border-slate-100 dark:border-slate-800">
          <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2 flex items-center gap-1.5">
            <Users size={14} />
            Stakeholders
          </p>
          <div className="flex gap-2 flex-wrap">
            {recommendation.stakeholders.map((s) => (
              <span key={s} className="px-3 py-1 rounded-full bg-brand-lightest dark:bg-slate-800 text-brand-darkest dark:text-brand-light text-xs font-medium">
                {s}
              </span>
            ))}
          </div>
        </div>
      )}

      {recommendation.escalation_steps?.length > 0 && (
        <div className="mt-5 pt-4 border-t border-slate-100 dark:border-slate-800">
          <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Escalation Steps</p>
          <ul className="flex flex-col gap-1.5">
            {recommendation.escalation_steps.map((e, i) => (
              <li key={i} className="text-sm text-slate-500 dark:text-slate-400 flex gap-2">
                <span className="opacity-60">•</span>
                {e}
              </li>
            ))}
          </ul>
        </div>
      )}

      {recommendation.expected_outcomes?.length > 0 && (
        <div className="mt-5 pt-4 border-t border-slate-100 dark:border-slate-800">
          <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-1">Expected Outcomes</p>
          <ul className="flex flex-col gap-1.5">
            {recommendation.expected_outcomes.map((o, i) => (
              <li key={i} className="text-sm text-slate-500 dark:text-slate-400 flex gap-2">
                <span className="opacity-60">•</span>
                {o}
              </li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  );
}

export default RecommendationsCard;