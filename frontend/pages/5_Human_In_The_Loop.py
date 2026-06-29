import streamlit as st
import requests

st.set_page_config(
    page_title="Human-in-the-Loop",
    page_icon="👤",
    layout="wide",
)

REVIEW_API = "http://localhost:8000/review/submit"

st.title("👤 Human-in-the-Loop Review")
st.caption("Review AI recommendations before they are finalized.")

# -------------------------------------------------
# Session State
# -------------------------------------------------

if "workflow_result" not in st.session_state:
    st.session_state.workflow_result = None

# -------------------------------------------------
# Demo / Placeholder Data
# Replace with your backend result later
# -------------------------------------------------

result = st.session_state.workflow_result or {
    "case_id": "CASE-001",
    "recommendation": {
        "immediate_actions": [
            "Activate Backup Supplier B",
            "Notify Procurement Team",
            "Increase Safety Stock",
        ]
    },
    "planner": {
        "confidence": 0.94,
        "requires_human_review": True,
    },
    "explainability": {
        "executive_summary":
            "The AI selected the backup supplier to minimize downtime while balancing operational cost and recovery speed."
    },
}

# -------------------------------------------------
# Summary
# -------------------------------------------------

c1, c2, c3 = st.columns(3)

c1.metric("Case ID", result["case_id"])
c2.metric(
    "AI Confidence",
    f"{result['planner']['confidence']:.2f}",
)
c3.metric(
    "Review Required",
    "Yes" if result["planner"]["requires_human_review"] else "No",
)

st.divider()

# -------------------------------------------------
# AI Recommendation
# -------------------------------------------------

st.subheader("🤖 AI Recommendation")

recommendation_text = "\n".join(
    result["recommendation"]["immediate_actions"]
)

edited = st.text_area(
    "Edit Recommendation",
    value=recommendation_text,
    height=220,
)

st.divider()

# -------------------------------------------------
# Explainability
# -------------------------------------------------

st.subheader("🧠 AI Reasoning")

st.info(
    result["explainability"]["executive_summary"]
)

st.divider()

# -------------------------------------------------
# Reviewer Details
# -------------------------------------------------

reviewer = st.text_input("Reviewer Name")

role = st.selectbox(
    "Role",
    [
        "Operations Manager",
        "Supply Chain Manager",
        "Risk Officer",
        "Executive",
    ],
)

comments = st.text_area(
    "Reviewer Comments"
)

st.divider()

# -------------------------------------------------
# Actions
# -------------------------------------------------

c1, c2, c3 = st.columns(3)

approve = c1.button(
    "✅ Approve",
    use_container_width=True,
)

reject = c2.button(
    "❌ Reject",
    use_container_width=True,
)

revise = c3.button(
    "✏ Request Changes",
    use_container_width=True,
)

decision = None

if approve:
    decision = "approve"

elif reject:
    decision = "reject"

elif revise:
    decision = "revise"

if decision:

    payload = {
        "case_id": result["case_id"],
        "reviewer": reviewer,
        "reviewer_role": role,
        "decision": decision,
        "comments": comments,
        "updated_recommendation": {
            "edited_text": edited
        },
    }

    try:

        response = requests.post(
            REVIEW_API,
            json=payload,
            timeout=60,
        )

        if response.ok:

            st.success("Review submitted successfully.")

            st.json(response.json())

        else:

            st.error(response.text)

    except Exception as e:

        st.error(f"Backend unavailable: {e}")