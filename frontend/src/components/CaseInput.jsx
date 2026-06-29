import { useState } from "react";
import { motion } from "framer-motion";
import { Search, AlertTriangle } from "lucide-react";

function CaseInput({ onRun, disabled }) {
  const [incident, setIncident] = useState("");
  const [mode, setMode] = useState("live");
  const [error, setError] = useState("");

  function handleSubmit(e) {
    e.preventDefault();

    if (!incident.trim()) {
      setError("Please describe the incident before running analysis.");
      return;
    }

    setError("");
    onRun(incident.trim(), mode);
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="flex flex-col items-center justify-center py-16 px-4"
    >
      <h1 className="text-2xl font-bold text-slate-900 dark:text-white mb-2 tracking-tight">
        Enterprise Crisis Intelligence
      </h1>
      <p className="text-slate-500 dark:text-slate-400 mb-8 text-center max-w-lg">
        Describe the incident in plain language. The AI planner will decide how to investigate it.
      </p>

      <form
        onSubmit={handleSubmit}
        className="w-full max-w-2xl flex flex-col gap-4"
      >
        <div>
          <label className="text-sm font-medium text-slate-700 dark:text-slate-300">
            Incident Description
          </label>
          <textarea
            value={incident}
            onChange={(e) => setIncident(e.target.value)}
            disabled={disabled}
            rows={5}
            className="mt-1.5 w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-brand-dark transition disabled:opacity-50 resize-none"
            placeholder="e.g. A major earthquake has disrupted semiconductor manufacturing in Taiwan, affecting our primary supplier. Current inventory shows only 5 days of stock remaining."
          />
        </div>

        <div>
          <label className="text-sm font-medium text-slate-700 dark:text-slate-300">
            Mode
          </label>
          <select
            value={mode}
            onChange={(e) => setMode(e.target.value)}
            disabled={disabled}
            className="mt-1.5 w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-brand-dark transition disabled:opacity-50"
          >
            <option value="live">Live Analysis</option>
            <option value="scenario">Scenario</option>
            <option value="what_if">What-If</option>
          </select>
        </div>

        {error && (
          <p className="flex items-center gap-1.5 text-sm text-red-500">
            <AlertTriangle size={15} />
            {error}
          </p>
        )}

        <motion.button
          type="submit"
          disabled={disabled}
          whileHover={{ scale: disabled ? 1 : 1.02 }}
          whileTap={{ scale: disabled ? 1 : 0.98 }}
          className="flex items-center justify-center gap-2 bg-brand-darkest dark:bg-brand-light text-white dark:text-slate-900 py-3 rounded-xl font-semibold hover:opacity-90 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Search size={17} />
          {disabled ? "Running Analysis..." : "Run Analysis"}
        </motion.button>
      </form>
    </motion.div>
  );
}

export default CaseInput;