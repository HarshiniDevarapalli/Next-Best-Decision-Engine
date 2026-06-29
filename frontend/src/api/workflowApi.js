const BASE_URL = "http://127.0.0.1:8001";

export async function analyzeIncident(incident, mode = "live", overrides = {}) {
  const response = await fetch(`${BASE_URL}/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      workflow: "crisis_response",
      mode,
      incident,
      overrides,
    }),
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  const data = await response.json();
  return data;
}

export async function submitReview(caseId, reviewer, reviewerRole, decision, comments, updatedRecommendation) {
  const response = await fetch(`${BASE_URL}/review/submit`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      case_id: caseId,
      reviewer,
      reviewer_role: reviewerRole,
      decision,
      comments: comments || "",
      updated_recommendation: updatedRecommendation || null,
    }),
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  const data = await response.json();
  return data;
}