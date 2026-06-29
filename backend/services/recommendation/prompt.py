"""
prompt.py

Prompt templates for the Enterprise Crisis
Recommendation Engine.
"""

from textwrap import dedent

from models.risk_report import RiskReport
from services.weak_signal.schemas import WeakSignalReport


SYSTEM_PROMPT = dedent("""
You are an Enterprise Crisis Response Planner.

You help executives decide the best course of action
during operational crises.

Your recommendations must prioritize:

1. Human Safety
2. Business Continuity
3. Regulatory Compliance
4. Financial Impact
5. Reputation

You receive:

- Weak operational signals
- Operational risk assessment

Generate an executive crisis response plan.

Return ONLY valid JSON.

Never return markdown.

Never wrap JSON inside ```.

Never explain outside the JSON.
""").strip()


def build_prompt(
    weak_signal_report: WeakSignalReport,
    risk_report: RiskReport
) -> str:

    signals = "\n".join(
        f"- {signal.signal.value} "
        f"(confidence={signal.confidence:.2f}, "
        f"severity={signal.severity.value})"
        for signal in weak_signal_report.signals
    )

    return dedent(f"""
Enterprise Incident Summary

{weak_signal_report.transcript_summary}

------------------------------------------------

Detected Operational Signals

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

Recovery Estimate

{risk_report.estimated_recovery_time}

------------------------------------------------

Generate an executive crisis response plan.

Return EXACTLY this schema:

{{
    "title": "...",

    "priority": "LOW | MEDIUM | HIGH | CRITICAL",

    "confidence": 0.95,

    "executive_summary": "...",

    "immediate_actions": [],

    "short_term_actions": [],

    "long_term_actions": [],

    "stakeholders": [],

    "business_continuity_actions": [],

    "expected_business_outcome": "...",

    "reasoning": []
}}

Return ONLY valid JSON.
""").strip()