import { motion } from "framer-motion";
import RiskCard from "./RiskCard";
import SummaryCard from "./SummaryCard";
import WeakSignalsCard from "./WeakSignalsCard";
import RecommendationsCard from "./RecommendationsCard";
import StakeholdersCard from "./StakeholdersCard";
import WhatIfSimulator from "./WhatIfSimulator";
import DecisionScoringCard from "./DecisionScoringCard";
import CostAnalysisCard from "./CostAnalysisCard";
import TimelineCard from "./TimelineCard";
import ScenarioComparisonCard from "./ScenarioComparisonCard";
import EvidenceCard from "./EvidenceCard";

function ResultsDashboard({ result, onReset }) {
  if (!result) return null;

  // result may be the raw /analyze completed response, OR the
  // wrapped { case_id, status, result } shape from a normal
  // (non-paused) completion - normalize both to the same inner shape.
  const data = result.result || result;

  return (
    <div className="max-w-5xl mx-auto px-6 py-10 flex flex-col gap-5">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex items-center justify-between flex-wrap gap-3 mb-1"
      >
        <h1 className="text-xl font-bold text-slate-900 dark:text-white tracking-tight">
          Case: {result.case_id || "—"}
        </h1>
        <button
          onClick={onReset}
          className="bg-brand-darkest dark:bg-brand-light text-white dark:text-slate-900 px-5 py-2.5 rounded-full font-semibold text-sm hover:opacity-90 transition"
        >
          Run Another Case
        </button>
      </motion.div>

      <RiskCard risk={data.risk} />
      <SummaryCard explainability={data.explainability} />
      <WeakSignalsCard weakSignal={data.weak_signal} />
      <RecommendationsCard recommendation={data.recommendation} />
      <WhatIfSimulator simulation={data.simulation} />
      <DecisionScoringCard decisionScoring={data.decision_scoring} />
      <CostAnalysisCard costAnalysis={data.cost_analysis} />
      <TimelineCard timelinePrediction={data.timeline_prediction} />
      <ScenarioComparisonCard scenarioComparison={data.scenario_comparison} />
      <StakeholdersCard recommendation={data.recommendation} />
      <EvidenceCard contextData={data.enterprise_context} />
    </div>
  );
}

export default ResultsDashboard;