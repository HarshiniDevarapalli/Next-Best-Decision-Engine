import { motion } from "framer-motion";
import { FlaskConical } from "lucide-react";
import RiskCard from "./RiskCard";
import SummaryCard from "./SummaryCard";
import WeakSignalsCard from "./WeakSignalsCard";
import RecommendationsCard from "./RecommendationsCard";
import StakeholdersCard from "./StakeholdersCard";
import EvidenceCard from "./EvidenceCard";

function ResultsDashboard({ result, onReset, onOpenWhatIf }) {
  if (!result) return null;

  const contextData = result.context_data || {};

  return (
    <div className="max-w-5xl mx-auto px-6 py-10 flex flex-col gap-5">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex items-center justify-between flex-wrap gap-3 mb-1"
      >
        <h1 className="text-xl font-bold text-slate-900 dark:text-white tracking-tight">
          Case: {result.case_id}
        </h1>
        <div className="flex items-center gap-3">
          <button
            onClick={onOpenWhatIf}
            className="flex items-center gap-2 border border-brand-darkest dark:border-brand-light text-brand-darkest dark:text-brand-light px-4 py-2.5 rounded-full font-semibold text-sm hover:bg-brand-lightest dark:hover:bg-slate-800 transition"
          >
            <FlaskConical size={15} />
            What-If Simulator
          </button>
          <button
            onClick={onReset}
            className="bg-brand-darkest dark:bg-brand-light text-white dark:text-slate-900 px-5 py-2.5 rounded-full font-semibold text-sm hover:opacity-90 transition"
          >
            Run Another Case
          </button>
        </div>
      </motion.div>

      <RiskCard riskReport={contextData.risk_report} />
      <SummaryCard explainabilityReport={contextData.explainability_report} />
      <WeakSignalsCard weakSignalReport={contextData.weak_signal_report} />
      <RecommendationsCard
        recommendationReport={contextData.recommendation_report}
        executionId={result.execution_id}
      />
      <StakeholdersCard recommendationReport={contextData.recommendation_report} />
      <EvidenceCard contextData={contextData} />
    </div>
  );
}

export default ResultsDashboard;