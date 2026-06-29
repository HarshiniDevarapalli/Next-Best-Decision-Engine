# backend/test_phase4.py
from dotenv import load_dotenv

load_dotenv()
from backend.planner.planner import Planner


planner = Planner()

incident = """
ABC Components Ltd. has reported a two-week delay in supplying
Semiconductor Chip X due to flooding at its manufacturing facility.
Current inventory is below safety stock and production of Product Z
is expected to stop within 5 days.
"""

result = planner.execute(
    workflow="incident_response",
    mode="analysis",
    incident=incident,
)

print("=" * 80)
print("PHASE 4 TEST")
print("=" * 80)

print("\nPlanner")
print(result["planner"])

print("\nRisk")
print(result["risk"])

print("\nRecommendation")
print(result["recommendation"])

print("\nSimulation")
print(result["simulation"])

print("\nDecision Scoring")
print(result["decision_scoring"])

print("\nCost Analysis")
print(result["cost_analysis"])

print("\nTimeline Prediction")
print(result["timeline_prediction"])

print("\nScenario Comparison")
print(result["scenario_comparison"])

print("\nExplainability")
print(result["explainability"])