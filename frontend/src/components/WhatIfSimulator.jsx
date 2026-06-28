import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  FlaskConical,
  ArrowLeft,
  ArrowRight,
  Loader2,
  TrendingDown,
  TrendingUp,
  Minus,
} from "lucide-react";
import { runSimulation } from "../api/workflowApi";
import RiskCard from "./RiskCard";
import SummaryCard from "./SummaryCard";
import WeakSignalsCard from "./WeakSignalsCard";
import RecommendationsCard from "./RecommendationsCard";
import StakeholdersCard from "./StakeholdersCard";

function ComparisonRow({ label, baselineValue, simulatedValue, isNumeric }) {
  let trendIcon = <Minus size={14} className="text-slate-400" />;
  let trendColor = "text-slate-400";

  if (isNumeric && baselineValue !== simulatedValue) {
    if (simulatedValue < baselineValue) {
      trendIcon = <TrendingDown size={14} />;
      trendColor = "text-brand-darkest dark:text-brand-light";
    } else {
      trendIcon = <TrendingUp size={14} />;
      trendColor = "text-red-500";
    }
  }

  const changed = baselineValue !== simulatedValue;

  return (
    <div className="grid grid-cols-3 gap-4 py-3 border-b border-slate-100 dark:border-slate-800 last:border-0 items-center">
      <span className="text-sm text-slate-500 dark:text-slate-400">{label}</span>
      <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
        {String(baselineValue)}
      </span>
      <span
        className={`text-sm font-semibold flex items-center gap-1.5 ${
          changed ? trendColor : "text-slate-700 dark:text-slate-300"
        }`}
      >
        {changed && trendIcon}
        {String(simulatedValue)}
      </span>
    </div>
  );
}

function FullScenarioSection({ title, data, accentClass }) {
  return (
    <div>
      <div className={`flex items-center gap-2 mb-4 ${accentClass}`}>
        <h3 className="text-sm font-bold uppercase tracking-wide">{title}</h3>
      </div>
      <div className="flex flex-col gap-5">
        <RiskCard riskReport={data.risk_report} />
        <SummaryCard explainabilityReport={data.explainability_report} />
        <WeakSignalsCard weakSignalReport={data.weak_signal_report} />
        <RecommendationsCard recommendationReport={data.recommendation_report} />
        <StakeholdersCard recommendationReport={data.recommendation_report} />
      </div>
    </div>
  );
}

function WhatIfSimulator({ caseId, onBack }) {
  const [stockDays, setStockDays] = useState(5);
  const [serviceLevel, setServiceLevel] = useState("High Priority");
  const [penaltyClause, setPenaltyClause] = useState(true);
  const [newsImpact, setNewsImpact] = useState("Critical");
  const [backupVendorAvailable, setBackupVendorAvailable] = useState(true);
  const [status, setStatus] = useState("form"); // form | loading | result | error
  const [result, setResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState("");
  const [showFullDetails, setShowFullDetails] = useState(false);

  async function handleRunSimulation() {
    setStatus("loading");
    setErrorMsg("");

    const overrides = {
      inventory: { stock_days_remaining: Number(stockDays) },
      supplier_contract: {
        service_level: serviceLevel,
        penalty_clause: penaltyClause,
      },
      news: { impact: newsImpact },
    };

    if (!backupVendorAvailable) {
      overrides.vendor = { _set_all: { approved_vendor: false } };
    }

    try {
      const data = await runSimulation(caseId, overrides);
      setResult(data);
      setStatus("result");
    } catch (err) {
      setErrorMsg(err.message);
      setStatus("error");
    }
  }

  function handleReset() {
    setStatus("form");
    setResult(null);
    setShowFullDetails(false);
  }

  const baseline = result?.context_data?.baseline;
  const simulated = result?.context_data?.simulated;

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <button
        onClick={onBack}
        className="flex items-center gap-1.5 text-sm text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 transition mb-6"
      >
        <ArrowLeft size={15} />
        Back to results
      </button>

      <div className="flex items-center gap-2 mb-2">
        <FlaskConical size={20} className="text-brand-darkest dark:text-brand-light" />
        <h1 className="text-xl font-bold text-slate-900 dark:text-white tracking-tight">
          What-If Simulator
        </h1>
      </div>
      <p className="text-slate-500 dark:text-slate-400 mb-8">
        Adjust the case details below to see how the risk assessment and recommendations would change.
      </p>

      <AnimatePresence mode="wait">
        {status === "form" || status === "error" ? (
          <motion.div
            key="form"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 flex flex-col gap-5 max-w-xl mx-auto"
          >
            <div>
              <label className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Stock Days Remaining
              </label>
              <input
                type="number"
                min="0"
                value={stockDays}
                onChange={(e) => setStockDays(e.target.value)}
                className="mt-1.5 w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-brand-dark transition"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Supplier Service Level
              </label>
              <select
                value={serviceLevel}
                onChange={(e) => setServiceLevel(e.target.value)}
                className="mt-1.5 w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-brand-dark transition"
              >
                <option value="High Priority">High Priority</option>
                <option value="Standard">Standard</option>
              </select>
            </div>

            <div>
              <label className="text-sm font-medium text-slate-700 dark:text-slate-300">
                News Impact
              </label>
              <select
                value={newsImpact}
                onChange={(e) => setNewsImpact(e.target.value)}
                className="mt-1.5 w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-brand-dark transition"
              >
                <option value="Critical">Critical</option>
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
              </select>
            </div>

            <label className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300 cursor-pointer select-none">
              <input
                type="checkbox"
                checked={penaltyClause}
                onChange={(e) => setPenaltyClause(e.target.checked)}
                className="w-4 h-4 rounded border-slate-300 dark:border-slate-600 text-brand-darkest focus:ring-brand-dark"
              />
              Contract includes penalty clause
            </label>

            <label className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300 cursor-pointer select-none">
              <input
                type="checkbox"
                checked={backupVendorAvailable}
                onChange={(e) => setBackupVendorAvailable(e.target.checked)}
                className="w-4 h-4 rounded border-slate-300 dark:border-slate-600 text-brand-darkest focus:ring-brand-dark"
              />
              Approved backup vendor available
            </label>

            {status === "error" && (
              <p className="text-sm text-red-500">Simulation failed: {errorMsg}</p>
            )}

            <button
              onClick={handleRunSimulation}
              className="flex items-center justify-center gap-2 bg-brand-darkest dark:bg-brand-light text-white dark:text-slate-900 py-3 rounded-xl font-semibold hover:opacity-90 transition mt-1"
            >
              Run Simulation
              <ArrowRight size={16} />
            </button>
          </motion.div>
        ) : status === "loading" ? (
          <motion.div
            key="loading"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex flex-col items-center justify-center py-20 gap-3"
          >
            <Loader2 size={28} className="animate-spin text-brand-darkest dark:text-brand-light" />
            <p className="text-sm text-slate-500 dark:text-slate-400">Running simulation...</p>
          </motion.div>
        ) : (
          <motion.div
            key="result"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col gap-5"
          >
            <div className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6">
              <h2 className="text-sm font-bold text-slate-900 dark:text-white mb-4">
                Quick Comparison
              </h2>

              <div className="grid grid-cols-3 gap-4 pb-3 border-b border-slate-200 dark:border-slate-700 mb-1">
                <span className="text-xs font-semibold uppercase text-slate-400">Metric</span>
                <span className="text-xs font-semibold uppercase text-slate-400">Baseline</span>
                <span className="text-xs font-semibold uppercase text-slate-400">Simulated</span>
              </div>

              <ComparisonRow
                label="Risk Score"
                baselineValue={baseline.risk.risk_score}
                simulatedValue={simulated.risk.risk_score}
                isNumeric
              />
              <ComparisonRow
                label="Risk Level"
                baselineValue={baseline.risk.risk_level}
                simulatedValue={simulated.risk.risk_level}
              />
              <ComparisonRow
                label="Operational Health"
                baselineValue={baseline.risk.operational_health}
                simulatedValue={simulated.risk.operational_health}
              />
              <ComparisonRow
                label="Signals Detected"
                baselineValue={baseline.weak_signal.signals_detected}
                simulatedValue={simulated.weak_signal.signals_detected}
                isNumeric
              />
              <ComparisonRow
                label="Recommendation"
                baselineValue={baseline.recommendation.title}
                simulatedValue={simulated.recommendation.title}
              />
            </div>

            <button
              onClick={() => setShowFullDetails(!showFullDetails)}
              className="self-center text-sm font-semibold text-brand-darkest dark:text-brand-light hover:opacity-80 transition px-4 py-2"
            >
              {showFullDetails ? "Hide full details ▲" : "Show full details for both scenarios ▼"}
            </button>

            <AnimatePresence>
              {showFullDetails && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="overflow-hidden"
                >
                  <div className="grid md:grid-cols-2 gap-6 pt-2">
                    <FullScenarioSection
                      title="Baseline (Real Data)"
                      data={baseline}
                      accentClass="text-slate-500 dark:text-slate-400"
                    />
                    <FullScenarioSection
                      title="Simulated (With Overrides)"
                      data={simulated}
                      accentClass="text-brand-darkest dark:text-brand-light"
                    />
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            <button
              onClick={handleReset}
              className="self-start text-sm font-medium text-brand-darkest dark:text-brand-light hover:opacity-80 transition"
            >
              ← Adjust values and run again
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default WhatIfSimulator;