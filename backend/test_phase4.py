# backend/test_phase4.py

from pprint import pprint

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

print("\nReturned object type:")
print(type(result))

print("\nReturned keys:")
print(list(result.keys()))

print("\nFull Result:")
pprint(result)