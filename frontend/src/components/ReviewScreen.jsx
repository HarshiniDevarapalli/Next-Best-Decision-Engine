import { useState } from "react";
import { motion } from "framer-motion";
import {
  ShieldAlert,
  CheckCircle2,
  XCircle,
  Edit3,
  ArrowLeft,
  Loader2,
} from "lucide-react";
import { submitReview } from "../api/workflowApi";
import { useAuth } from "../context/AuthContext";

function ReviewScreen({ result, onReviewSubmitted, onBack }) {
  const { currentUser } = useAuth();
  const [decision, setDecision] = useState(null); // "approve" | "reject" | "revise"
  const [comments, setComments] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  if (!result) return null;

  const risk = result.risk;
  const recommendation = result.recommendation;
  const explainability = result.explainability;

  async function handleSubmit() {
    if (!decision) {
      setError("Please choose Approve, Reject, or Revise before submitting.");
      return;
    }

    setSubmitting(true);
    setError("");

    try {
      const reviewerName = currentUser.charAt(0).toUpperCase() + currentUser.slice(1);

      await submitReview(
        result.case_id,
        reviewerName,
        "Crisis Manager",
        decision,
        comments
      );

      onReviewSubmitted({
        ...result,
        status: "COMPLETED",
        review_status: decision,
      });
    } catch (err) {
      setError(err.message);
      setSubmitting(false);
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <button
        onClick={onBack}
        className="flex items-center gap-1.5 text-sm text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 transition mb-6"
      >
        <ArrowLeft size={15} />
        Run another case
      </button>

      <div className="flex items-center gap-2 mb-2">
        <ShieldAlert size={20} className="text-amber-500" />
        <h1 className="text-xl font-bold text-slate-900 dark:text-white tracking-tight">
          Awaiting Your Review
        </h1>
      </div>
      <p className="text-slate-500 dark:text-slate-400 mb-8">
        This incident requires human approval before the recommendation is finalized.
      </p>

      <div className="flex flex-col gap-5">
        {risk && (
          <div className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6">
            <h2 className="text-sm font-bold text-slate-900 dark:text-white mb-3">
              Risk Assessment
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3">
              <Stat label="Overall Risk" value={risk.overall_risk} />
              <Stat label="Operational Impact" value={risk.operational_impact} />
              <Stat label="Financial Impact" value={risk.financial_impact} />
              <Stat label="Reputational Impact" value={risk.reputational_impact} />
            </div>
            {risk.key_risks?.length > 0 && (
              <ul className="flex flex-col gap-1.5 mt-2">
                {risk.key_risks.slice(0, 3).map((r, i) => (
                  <li key={i} className="text-sm text-slate-600 dark:text-slate-300 flex gap-2">
                    <span className="text-amber-500 mt-0.5">•</span>
                    {r}
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}

        {explainability?.executive_summary && (
          <div className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6">
            <h2 className="text-sm font-bold text-slate-900 dark:text-white mb-2">
              Executive Summary
            </h2>
            <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              {explainability.executive_summary}
            </p>
          </div>
        )}

        {recommendation && (
          <div className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6">
            <h2 className="text-sm font-bold text-slate-900 dark:text-white mb-3">
              Recommended Immediate Actions
            </h2>
            <ul className="flex flex-col gap-2">
              {recommendation.immediate_actions?.map((action, i) => (
                <li key={i} className="text-sm text-slate-600 dark:text-slate-300 flex gap-2">
                  <span className="w-1 h-1 rounded-full bg-brand-darkest dark:bg-brand-light mt-1.5 shrink-0" />
                  {action}
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6">
          <h2 className="text-sm font-bold text-slate-900 dark:text-white mb-4">
            Your Decision
          </h2>

          <div className="grid grid-cols-3 gap-3 mb-4">
            <button
              onClick={() => setDecision("approve")}
              className={`flex flex-col items-center gap-1.5 py-3 rounded-xl border-2 transition ${
                decision === "approve"
                  ? "border-green-500 bg-green-50 dark:bg-green-950/30"
                  : "border-slate-200 dark:border-slate-700"
              }`}
            >
              <CheckCircle2
                size={20}
                className={decision === "approve" ? "text-green-600" : "text-slate-400"}
              />
              <span className="text-sm font-medium text-slate-700 dark:text-slate-200">
                Approve
              </span>
            </button>

            <button
              onClick={() => setDecision("revise")}
              className={`flex flex-col items-center gap-1.5 py-3 rounded-xl border-2 transition ${
                decision === "revise"
                  ? "border-amber-500 bg-amber-50 dark:bg-amber-950/30"
                  : "border-slate-200 dark:border-slate-700"
              }`}
            >
              <Edit3
                size={20}
                className={decision === "revise" ? "text-amber-600" : "text-slate-400"}
              />
              <span className="text-sm font-medium text-slate-700 dark:text-slate-200">
                Revise
              </span>
            </button>

            <button
              onClick={() => setDecision("reject")}
              className={`flex flex-col items-center gap-1.5 py-3 rounded-xl border-2 transition ${
                decision === "reject"
                  ? "border-red-500 bg-red-50 dark:bg-red-950/30"
                  : "border-slate-200 dark:border-slate-700"
              }`}
            >
              <XCircle
                size={20}
                className={decision === "reject" ? "text-red-600" : "text-slate-400"}
              />
              <span className="text-sm font-medium text-slate-700 dark:text-slate-200">
                Reject
              </span>
            </button>
          </div>

          <textarea
            value={comments}
            onChange={(e) => setComments(e.target.value)}
            rows={3}
            placeholder="Add review comments (optional)"
            className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-brand-dark transition resize-none mb-4"
          />

          {error && <p className="text-sm text-red-500 mb-3">{error}</p>}

          <button
            onClick={handleSubmit}
            disabled={submitting}
            className="w-full flex items-center justify-center gap-2 bg-brand-darkest dark:bg-brand-light text-white dark:text-slate-900 py-3 rounded-xl font-semibold hover:opacity-90 transition disabled:opacity-50"
          >
            {submitting ? (
              <>
                <Loader2 size={16} className="animate-spin" />
                Submitting...
              </>
            ) : (
              "Submit Review"
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div>
      <p className="text-xs text-slate-400 dark:text-slate-500 mb-0.5">{label}</p>
      <p className="text-sm font-semibold text-slate-800 dark:text-slate-200">{value}</p>
    </div>
  );
}

export default ReviewScreen;