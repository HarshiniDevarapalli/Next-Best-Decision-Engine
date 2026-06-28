import { motion } from "framer-motion";
import { Gauge, Activity, Clock, AlertTriangle } from "lucide-react";

function RiskCard({ riskReport }) {
  if (!riskReport) return null;

  const levelStyles = {
    CRITICAL: "bg-red-50 dark:bg-red-950/30 border-red-200 dark:border-red-900 text-red-600 dark:text-red-400",
    HIGH: "bg-orange-50 dark:bg-orange-950/30 border-orange-200 dark:border-orange-900 text-orange-600 dark:text-orange-400",
    MEDIUM: "bg-amber-50 dark:bg-amber-950/30 border-amber-200 dark:border-amber-900 text-amber-600 dark:text-amber-400",
    LOW: "bg-brand-lightest dark:bg-slate-800 border-brand-light dark:border-slate-700 text-brand-darkest dark:text-brand-light",
  };

  const style = levelStyles[riskReport.overall_risk_level] || levelStyles.MEDIUM;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className={`rounded-2xl border-2 p-6 ${style}`}
    >
      <div className="flex items-center justify-between flex-wrap gap-6">
        <Stat icon={AlertTriangle} label="Overall Risk Level" value={riskReport.overall_risk_level} />
        <Stat icon={Gauge} label="Risk Score" value={`${riskReport.overall_risk_score}/100`} />
        <Stat icon={Activity} label="Operational Health" value={riskReport.operational_health} />
        <Stat icon={Clock} label="Recovery Estimate" value={riskReport.estimated_recovery_time} small />
      </div>

      {riskReport.affected_functions?.length > 0 && (
        <div className="mt-5 pt-4 border-t border-current/15">
          <p className="text-sm font-medium opacity-70 mb-2">Affected Functions</p>
          <div className="flex gap-2 flex-wrap">
            {riskReport.affected_functions.map((fn) => (
              <span
                key={fn}
                className="px-3 py-1 rounded-full bg-white/60 dark:bg-black/20 text-sm font-medium"
              >
                {fn}
              </span>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
}

function Stat({ icon: Icon, label, value, small }) {
  return (
    <div>
      <p className="text-xs font-medium opacity-70 flex items-center gap-1.5 mb-1">
        <Icon size={13} />
        {label}
      </p>
      <p className={small ? "text-xl font-bold" : "text-3xl font-bold tracking-tight"}>
        {value}
      </p>
    </div>
  );
}

export default RiskCard;