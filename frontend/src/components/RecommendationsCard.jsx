import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ListChecks, Zap, Calendar, TrendingUp, Check, X, RotateCcw } from "lucide-react";

function buildActionState(recommendationReport) {
  const categories = [
    { key: "immediate_actions", icon: Zap, title: "Immediate Actions" },
    { key: "short_term_actions", icon: Calendar, title: "Short-Term Actions" },
    { key: "long_term_actions", icon: TrendingUp, title: "Long-Term Actions" },
  ];

  return categories.map((cat) => ({
    ...cat,
    actions: (recommendationReport[cat.key] || []).map((text, index) => ({
      id: `${cat.key}_${index}`,
      text,
      status: "pending", // pending | approved | rejected
    })),
  }));
}

function ActionRow({ action, onDecide }) {
  const isPending = action.status === "pending";
  const isApproved = action.status === "approved";
  const isRejected = action.status === "rejected";

  return (
    <motion.li
      layout
      className={`flex items-start gap-2.5 text-sm rounded-lg px-2 py-1.5 -mx-2 transition-colors ${
        isApproved
          ? "bg-brand-lightest/60 dark:bg-brand-darkest/15"
          : isRejected
          ? "bg-slate-50 dark:bg-slate-800/40"
          : ""
      }`}
    >
      <span
        className={`mt-1.5 w-1 h-1 rounded-full shrink-0 ${
          isRejected
            ? "bg-slate-300 dark:bg-slate-600"
            : "bg-brand-darkest dark:bg-brand-light"
        }`}
      />

      <span
        className={`flex-1 ${
          isRejected
            ? "text-slate-400 dark:text-slate-500 line-through"
            : "text-slate-600 dark:text-slate-300"
        }`}
      >
        {action.text}
      </span>

      <div className="flex items-center gap-1 shrink-0">
        <AnimatePresence mode="wait">
          {isPending && (
            <motion.div
              key="pending-controls"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex items-center gap-1"
            >
              <button
                onClick={() => onDecide(action.id, "approved")}
                title="Approve"
                className="w-6 h-6 rounded-md flex items-center justify-center text-slate-400 hover:bg-brand-lightest hover:text-brand-darkest dark:hover:bg-slate-700 dark:hover:text-brand-light transition"
              >
                <Check size={14} />
              </button>
              <button
                onClick={() => onDecide(action.id, "rejected")}
                title="Reject"
                className="w-6 h-6 rounded-md flex items-center justify-center text-slate-400 hover:bg-red-50 hover:text-red-500 dark:hover:bg-red-950/40 dark:hover:text-red-400 transition"
              >
                <X size={14} />
              </button>
            </motion.div>
          )}

          {isApproved && (
            <motion.span
              key="approved-badge"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0 }}
              className="flex items-center gap-1 text-xs font-semibold text-brand-darkest dark:text-brand-light"
            >
              <Check size={13} />
              Approved
              <button
                onClick={() => onDecide(action.id, "pending")}
                title="Undo"
                className="ml-1 text-slate-300 hover:text-slate-500 dark:hover:text-slate-300"
              >
                <RotateCcw size={11} />
              </button>
            </motion.span>
          )}

          {isRejected && (
            <motion.span
              key="rejected-badge"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0 }}
              className="flex items-center gap-1 text-xs font-semibold text-slate-400 dark:text-slate-500"
            >
              <X size={13} />
              Rejected
              <button
                onClick={() => onDecide(action.id, "pending")}
                title="Undo"
                className="ml-1 text-slate-300 hover:text-slate-500 dark:hover:text-slate-300"
              >
                <RotateCcw size={11} />
              </button>
            </motion.span>
          )}
        </AnimatePresence>
      </div>
    </motion.li>
  );
}

function ActionCategory({ icon: Icon, title, actions, onDecide }) {
  if (!actions?.length) return null;

  const approvedCount = actions.filter((a) => a.status === "approved").length;
  const decidedCount = actions.filter((a) => a.status !== "pending").length;

  return (
    <div>
      <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2.5 flex items-center justify-between">
        <span className="flex items-center gap-1.5">
          <Icon size={14} className="text-brand-darkest dark:text-brand-light" />
          {title}
        </span>
        {decidedCount > 0 && (
          <span className="text-xs font-normal text-slate-400">
            {approvedCount}/{actions.length} approved
          </span>
        )}
      </p>
      <ul className="flex flex-col gap-0.5">
        {actions.map((action) => (
          <ActionRow key={action.id} action={action} onDecide={onDecide} />
        ))}
      </ul>
    </div>
  );
}

function RecommendationsCard({ recommendationReport, executionId }) {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    if (recommendationReport) {
      setCategories(buildActionState(recommendationReport));
    }
  }, [recommendationReport]);

  if (!recommendationReport) return null;

  function handleDecide(actionId, status) {
    // STEP 1: update local state immediately for a responsive UI.
    setCategories((prev) =>
      prev.map((cat) => ({
        ...cat,
        actions: cat.actions.map((a) =>
          a.id === actionId ? { ...a, status } : a
        ),
      }))
    );

    // STEP 2 (future): persist the decision once a backend endpoint exists.
    // Example shape once available:
    // saveActionDecision(executionId, actionId, status);
  }

  const allActions = categories.flatMap((c) => c.actions);
  const totalDecided = allActions.filter((a) => a.status !== "pending").length;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.15 }}
      className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6"
    >
      <div className="flex items-center justify-between flex-wrap gap-2 mb-2">
        <div className="flex items-center gap-2">
          <ListChecks size={18} className="text-brand-darkest dark:text-brand-light" />
          <h2 className="text-lg font-bold text-slate-900 dark:text-white tracking-tight">
            {recommendationReport.title}
          </h2>
        </div>
        <span className="text-xs font-bold uppercase px-2.5 py-1 rounded-full bg-brand-lightest dark:bg-slate-800 text-brand-darkest dark:text-brand-light">
          {Math.round(recommendationReport.confidence * 100)}% confidence
        </span>
      </div>

      <p className="text-slate-500 dark:text-slate-400 mb-2 ml-7">
        {recommendationReport.summary}
      </p>

      {allActions.length > 0 && (
        <p className="text-xs text-slate-400 dark:text-slate-500 mb-5 ml-7">
          {totalDecided === 0
            ? "Review each action below — approve or reject before proceeding."
            : `${totalDecided} of ${allActions.length} actions reviewed`}
        </p>
      )}

      <div className="grid md:grid-cols-3 gap-6">
        {categories.map((cat) => (
          <ActionCategory
            key={cat.key}
            icon={cat.icon}
            title={cat.title}
            actions={cat.actions}
            onDecide={handleDecide}
          />
        ))}
      </div>

      {recommendationReport.expected_business_outcome && (
        <div className="mt-6 pt-4 border-t border-slate-100 dark:border-slate-800">
          <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-1">
            Expected Outcome
          </p>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            {recommendationReport.expected_business_outcome}
          </p>
        </div>
      )}
    </motion.div>
  );
}

export default RecommendationsCard;