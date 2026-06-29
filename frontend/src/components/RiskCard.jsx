import { motion } from "framer-motion";
import { AlertTriangle, Activity } from "lucide-react";

const LEVEL_STYLES = {
  Critical: "bg-red-50 dark:bg-red-950/30 border-red-200 dark:border-red-900 text-red-600 dark:text-red-400",
  High: "bg-orange-50 dark:bg-orange-950/30 border-orange-200 dark:border-orange-900 text-orange-600 dark:text-orange-400",
  Medium: "bg-amber-50 dark:bg-amber-950/30 border-amber-200 dark:border-amber-900 text-amber-600 dark:text-amber-400",
  Low: "bg-brand-lightest dark:bg-slate-800 border-brand-light dark:border-slate-700 text-brand-darkest dark:text-brand-light",
};

function RiskCard({ risk }) {
  if (!risk) return null;

  const style = LEVEL_STYLES[risk.overall_risk] || LEVEL_STYLES.Medium;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className={`rounded-2xl border-2 p-6 ${style}`}
    >
      <div className="flex items-center gap-2 mb-4">
        <AlertTriangle size={18} />
        <h2 className="text-lg font-bold tracking-tight">Risk Assessment</h2>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <Stat label="Overall Risk" value={risk.overall_risk} />
        <Stat label="Operational Impact" value={risk.operational_impact} />
        <Stat label="Financial Impact" value={risk.financial_impact} />
        <Stat label="Reputational Impact" value={risk.reputational_impact} />
        <Stat label="Supplier Risk" value={risk.supplier_risk} />
        <Stat label="Vendor Risk" value={risk.vendor_risk} />
        <Stat label="Inventory Risk" value={risk.inventory_risk} />
        <Stat label="Compliance Impact" value={risk.compliance_impact} />
      </div>

      {risk.key_risks?.length > 0 && (
        <div className="mt-4 pt-4 border-t border-current/15">
          <p className="text-sm font-medium opacity-80 mb-2 flex items-center gap-1.5">
            <Activity size={14} />
            Key Risks
          </p>
          <ul className="flex flex-col gap-1.5">
            {risk.key_risks.map((r, i) => (
              <li key={i} className="text-sm flex gap-2">
                <span className="opacity-60">•</span>
                {r}
              </li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  );
}

function Stat({ label, value }) {
  if (!value) return null;
  return (
    <div>
      <p className="text-xs opacity-70 mb-0.5">{label}</p>
      <p className="text-sm font-bold">{value}</p>
    </div>
  );
}

export default RiskCard;