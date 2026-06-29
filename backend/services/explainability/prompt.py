"""
prompt.py

Prompt templates for the Enterprise Crisis
Explainability Engine.
"""

from textwrap import dedent

from services.weak_signal.schemas import WeakSignalReport
from models.risk_report import RiskReport
from services.recommendation.schemas import RecommendationReport


SYSTEM_PROMPT = dedent("""
You are an Enterprise AI Explainability Engine.

Your job is NOT to make recommendations.

Your job is to explain WHY the AI produced its recommendation.

You must explain:

1. What operational signals were detected
2. Why those signals matter
3. How the operational risk was determined
4. Why the recommendation is appropriate
5. Expected business impact

Return ONLY valid JSON.

Never return markdown.

Never wrap JSON inside ```.

Never explain outside the JSON.
""").strip()


def build_prompt(
    weak_signal_report: WeakSignalReport,
    risk_report: RiskReport,
    recommendation_report: RecommendationReport
) -> str:

    signals = "\n".join(
        f"- {signal.signal.value} "
        f"(confidence={signal.confidence:.2f}, "
        f"severity={signal.severity.value})"
        for signal in weak_signal_report.signals
    )

    recommendations = "\n".join(
        f"- {action}"
        for action in recommendation_report.immediate_actions
    )

    return dedent(f"""
Enterprise Incident Summary

{weak_signal_report.transcript_summary}

------------------------------------------------

Detected Signals

{signals}

------------------------------------------------

Operational Health

{risk_report.operational_health.value}

Risk Score

{risk_report.overall_risk_score:.1f}

Risk Level

{risk_report.overall_risk_level.value}

Business Impact

{risk_report.estimated_business_impact}

------------------------------------------------

Recommended Immediate Actions

{recommendations}

------------------------------------------------

Explain WHY these recommendations were generated.

Return EXACTLY this JSON schema:

{{
    "executive_summary": "...",

    "why_this_decision": "...",

    "confidence": 0.95,

    "decision_trace": [],

    "evidence": [],

    "business_impact": "...",

    "recommended_next_steps": []
}}

Return ONLY JSON.
""").strip()