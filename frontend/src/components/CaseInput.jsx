import { useState } from "react";
import { motion } from "framer-motion";
import { Search } from "lucide-react";

function CaseInput({ onRun, disabled }) {
  const [caseId, setCaseId] = useState("incident_001");

  function handleSubmit(e) {
    e.preventDefault();
    if (caseId.trim()) {
      onRun(caseId.trim());
    }
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
      <p className="text-slate-500 dark:text-slate-400 mb-8 text-center max-w-md">
        Enter a case ID to run the full crisis analysis workflow.
      </p>

      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md flex flex-col gap-4"
      >
        <div>
          <label className="text-sm font-medium text-slate-700 dark:text-slate-300">
            Case ID
          </label>
          <input
            type="text"
            value={caseId}
            onChange={(e) => setCaseId(e.target.value)}
            disabled={disabled}
            className="mt-1.5 w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-brand-dark transition disabled:opacity-50"
            placeholder="e.g. incident_001"
          />
        </div>

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