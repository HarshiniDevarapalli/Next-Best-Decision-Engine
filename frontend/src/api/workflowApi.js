const BASE_URL = "http://127.0.0.1:8000";

export async function runWorkflow(caseId) {
  const response = await fetch(`${BASE_URL}/workflow/run`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      workflow: "crisis_response",
      case_id: caseId,
    }),
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  const data = await response.json();
  return data;
}

export async function runSimulation(caseId, overrides) {
  const response = await fetch(`${BASE_URL}/workflow/simulate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      workflow: "crisis_response",
      case_id: caseId,
      overrides,
    }),
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  const data = await response.json();
  return data;
}