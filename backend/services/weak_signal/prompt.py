"""
prompt.py

Prompt templates for Weak Signal Intelligence.

This module contains the system prompt and helper functions
used by the LLMWeakSignalDetector.
"""

from textwrap import dedent


SYSTEM_PROMPT = dedent("""
You are an Enterprise Customer Success Intelligence Engine.

Your task is to analyze meeting transcripts and identify hidden
business signals that influence customer retention, expansion,
and business risk.

You are NOT summarizing the meeting.

You are detecting latent business signals.

Analyze the transcript carefully and identify the following signals:

1. budget_concern
2. competitor_mention
3. negative_sentiment
4. positive_sentiment
5. renewal_urgency
6. low_adoption
7. expansion_opportunity
8. executive_escalation

For EACH detected signal provide:

- confidence (0.0 - 1.0)
- severity (low, medium, high, critical)
- explanation
- supporting evidence quoted directly from the transcript

If a signal is not present,
do NOT invent evidence.

Return ONLY valid JSON.

Never return markdown.

Never return explanations outside JSON.
""").strip()


def build_prompt(transcript: str) -> str:
    """
    Builds the complete prompt sent to the LLM.

    Parameters
    ----------
    transcript : str
        Meeting transcript.

    Returns
    -------
    str
        Complete prompt.
    """

    return dedent(f"""
    Analyze the following customer meeting transcript.

    Meeting Transcript
    ------------------

    {transcript}

    ------------------

    Return JSON in the following format:

    {{
      "summary": "...",

      "signals": [

        {{
          "signal": "budget_concern",

          "confidence": 0.92,

          "severity": "high",

          "explanation": "...",

          "evidence": [
            {{
              "text": "...",
              "confidence": 0.95
            }}
          ]
        }}

      ]
    }}

    Return ONLY JSON.
    """).strip()