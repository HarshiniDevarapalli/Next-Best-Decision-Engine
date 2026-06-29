#  Next Best Decision Engine (NBDE) — Agentic Enterprise Crisis Intelligence Platform

**A reusable, multi-agent decision intelligence platform built with FastAPI, LangGraph, and Google Gemini, for explainable, human-reviewed enterprise decision-making**

---

##  Overview

**NBDE** is an agentic AI platform that helps enterprises respond to operational crises — supplier disruptions, inventory shortages, natural disasters, and similar events — by automatically gathering relevant information, reasoning over it using a chain of specialized AI agents, and producing a clear, evidence-backed recommendation for a human decision-maker to review.

Rather than manually pulling data from contracts, inventory systems, vendor records, internal policy, and the news, a user simply describes the situation in plain language. NBDE's planner decides which agents are needed, runs them, and assembles a complete decision report — risk level, recommended actions, cost impact, recovery timeline, and a full account of the reasoning behind it — before pausing for human approval on anything high-impact.

While this repository demonstrates the platform through a **Supply Chain / Enterprise Crisis Intelligence** scenario, the orchestration layer (planner, workflow graph, agent registry) is domain-independent and can be repointed at other enterprise decision problems by defining new agents and a new workflow.

---

##  Problem Statement

When a crisis hits — a supplier's factory is damaged, a critical component runs low, a region becomes unstable — the information needed to respond well is scattered across contracts, inventory systems, vendor databases, internal policy documents, and external news.

Collecting and synthesizing all of that manually is slow, inconsistent, and easy to get wrong under pressure. Decisions made during a crisis often rely on whoever happens to be in the room and whatever they remember, rather than the full picture.

**NBDE addresses this by:**

- Automatically gathering relevant enterprise context the moment an incident is reported
- Using AI agents to reason over that context — detecting risk signals, assessing impact, and generating recommendations
- Simulating alternative response strategies and comparing their likely outcomes
- Keeping a human in the loop for final approval, with every step explained and logged

---

##  Objective

The goal of NBDE is to act as an **always-on crisis intelligence analyst** for enterprise teams — reducing the time between "something just went wrong" and "here is a well-reasoned, evidence-backed plan," while keeping a human firmly in control of what actually gets executed.

---

##  Technology Stack

| Category | Tool / Platform |
|---|---|
| Backend Framework | **FastAPI** (Python) |
| Agent Orchestration | **LangGraph** |
| LLM Reasoning Chains | **LangChain** |
| AI Model | **Google Gemini 2.5 Flash** |
| Knowledge Retrieval (RAG) | **ChromaDB** + **Sentence Transformers** |
| Data Validation | **Pydantic** |
| Frontend | **React** + **Vite** |
| Styling | **Tailwind CSS** |
| Animation | **Framer Motion** |
| Icons | **Lucide React** |

---

##  Workflow Explanation

The platform runs as a single orchestrated pipeline, made up of connected agents, each with one clear responsibility. Below is a step-by-step explanation of each stage and what it does.

### 1️⃣ Dynamic AI Planner

Before anything else runs, a Gemini-powered planner reads the incident description and decides the execution strategy: which datasource agents are relevant, which reasoning agents are needed, in what order, which steps can run in parallel, and whether the situation needs Shadow Mode, What-If simulation, or mandatory human review. This means the platform doesn't run every agent on every incident — it tailors its own response plan per case.

### 2️⃣ Incident Parsing

The raw, free-text incident description is parsed by Gemini into structured fields — category, severity, affected supplier, region, business unit, and critical entities — so every downstream agent works from consistent, structured data instead of raw text.

### 3️⃣ Datasource Agents (run in parallel)

Six independent agents gather enterprise context relevant to the incident:

- **Supplier Contract Agent** — contract terms, exclusivity clauses, penalty conditions
- **Inventory Agent** — current stock levels, warehouse data, shortage risk
- **Vendor Agent** — alternative suppliers, lead times, capacity, cost implications
- **Policy Agent** — internal procurement and business continuity rules that apply
- **News Agent** — relevant external events (disasters, geopolitical disruptions)
- **Incident History Agent** — similar past incidents and how they were resolved

### 4️⃣ Knowledge Layer (RAG)

A ChromaDB vector store, backed by Sentence Transformer embeddings, allows agents to semantically search enterprise documents — policies, vendor records, historical incidents — rather than relying on exact keyword matches.

### 5️⃣ Weak Signal Detection (with Shadow Mode)

This agent looks for early warning indicators in the gathered data. It runs two detectors — a deterministic rule-based detector and an LLM-based detector — and, when the planner determines it's relevant, compares their outputs side by side as **Shadow Mode**, allowing the team to evaluate the LLM detector's behavior against a known baseline before fully trusting it.

### 6️⃣ Risk Assessment

Combines the detected signals into an overall risk profile — operational, financial, reputational, and compliance impact — along with the supporting evidence behind each risk.

### 7️⃣ Recommendation Generation

Produces a structured response plan: immediate actions, short-term actions, long-term strategic actions, business continuity steps, stakeholders to notify, and escalation steps.

### 8️⃣ What-If Simulation

Generates multiple plausible future scenarios (e.g. "rapid recovery," "prolonged disruption," "worst case"), each with an estimated probability, business impact, operational impact, and recommended action — giving decision-makers a sense of the range of outcomes, not just a single prediction.

### 9️⃣ Decision Scoring

Ranks the candidate actions by feasibility, business value, operational risk, and implementation effort, surfacing which action is genuinely the best next step rather than just the most obvious one.

### 🔟 Cost Impact Analysis

Estimates the financial cost, ROI, and operational impact of each simulated scenario, identifying which option is cheapest and which delivers the best return.

### 1️⃣1️⃣ Timeline Prediction

Predicts a realistic recovery timeline, broken into stages with milestones, plus the specific blockers that could delay recovery.

### 1️⃣2️⃣ Scenario Comparison

Weighs every simulated scenario against the others — advantages, disadvantages, and an overall score — and recommends the strongest path forward.

### 1️⃣3️⃣ Explainability

Ties every prior step together into a single, human-readable account: an executive summary, the full chain of reasoning steps taken, the evidence behind each conclusion, the assumptions made, and what remains uncertain.

### 1️⃣4️⃣ Human-in-the-Loop Review

If the planner determined the situation is high-impact enough to require it, the workflow pauses here. A human reviewer sees the full AI-generated report and can **approve**, **reject**, or **revise** the recommendation, with comments — and every decision is permanently logged to an audit trail before the workflow resumes and finalizes.

---

##  How the Planner Makes Decisions

The planner doesn't apply a fixed checklist — it reasons about each incident individually, considering:

- The severity and type of crisis being described
- Whether business continuity is meaningfully at risk
- Whether multiple viable response strategies exist (triggering What-If simulation)
- Whether the decision is impactful enough to require human sign-off

This means two different incidents can take genuinely different paths through the system — a minor, low-ambiguity issue might skip simulation and scoring entirely, while a severe, uncertain one triggers the full reasoning chain.

---

##  Setup Steps (Before Running the Platform)

Follow these steps to get NBDE running locally for the first time.

### 1. Clone the repository

```bash
git clone https://github.com/HarshiniDevarapalli/Next-Best-Decision-Engine.git
cd Next-Best-Decision-Engine
git checkout phase4-experimental
```

### 2. Set up the backend

```bash
cd backend
python -m venv venv
```

Activate the environment:
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API credentials

Create a file named `.env` inside the `backend/` folder:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get a key from [Google AI Studio](https://aistudio.google.com).

### 4. Start the backend

From the **project root** (not from inside `backend/`):

```bash
uvicorn backend.app.main:app --reload --port 8001
```

API docs will be available at `http://127.0.0.1:8001/docs`.

> **First-run note:** the very first request will take noticeably longer, since the RAG embedding model downloads and loads its weights at that point. Subsequent runs are faster.

### 5. Set up and start the frontend

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

---

##  How to Use (Execution Steps)

1. **Open the app** at `http://localhost:5173` and log in.
2. **Describe the incident** in plain language in the text box — for example:
   > *"A major earthquake has disrupted semiconductor manufacturing in Taiwan, affecting our primary supplier. Current inventory shows only 5 days of stock remaining."*
3. **Choose a mode** — Live Analysis, Scenario, or What-If — and click **Run Analysis**.
4. **Wait for processing.** The planner and every relevant agent run in sequence; this can take 30 seconds to a few minutes depending on incident complexity.
5. **If human review is required**, you'll land on a review screen showing the AI's risk assessment, executive summary, and recommended actions. Choose **Approve**, **Reject**, or **Revise**, add comments if needed, and submit.
6. **View the full decision report** — risk assessment, recommendations, simulated scenarios, decision scoring, cost analysis, recovery timeline, scenario comparison, supporting evidence, and the full explainability breakdown.

---

##  Output and Notifications

When an incident analysis completes:

- The full decision report is returned to the frontend and rendered as a structured dashboard
- If human review was required, the case pauses with status `WAITING_FOR_HUMAN_REVIEW` until a reviewer responds
- Every reviewer decision (approve / reject / revise), along with their name, role, comments, and timestamp, is appended to that case's audit log
- The execution trace records exactly which agents ran and which were skipped for that specific incident, since not every incident triggers every agent

---

## Pipeline Summary

| Stage | Function |
|---|---|
| Dynamic Planning | Decides which agents and steps are relevant to this specific incident |
| Incident Parsing | Converts free-text incident description into structured data |
| Data Gathering | Six agents collect supplier, inventory, vendor, policy, news, and history context in parallel |
| Knowledge Retrieval | Semantic search over enterprise documents via ChromaDB |
| Signal Detection | Rule-based and LLM-based weak signal detection, compared in Shadow Mode when relevant |
| Risk Assessment | Combines signals into an overall risk profile |
| Recommendation | Generates a structured, prioritized response plan |
| Simulation | Models multiple plausible future scenarios with probabilities |
| Scoring & Cost | Ranks and costs candidate actions |
| Timeline Prediction | Estimates recovery stages and blockers |
| Scenario Comparison | Weighs all simulated scenarios against each other |
| Explainability | Produces a full, evidence-backed account of the reasoning |
| Human Review | Pauses for approval/rejection/revision on high-impact decisions, with full audit logging |

---

##  Known Limitations

- **Gemini free-tier quota (20 requests/day)** is easily exhausted — a single full incident analysis can involve 10 or more sequential LLM calls. A paid tier or higher-quota key is recommended for repeated testing or live demos.
- **In-memory state storage** — paused workflow state awaiting human review lives in a Python dictionary, not a database. Restarting the backend loses any in-progress reviews.
- **Shadow Mode runs conditionally** — the planner decides per-incident whether comparing rule-based vs. LLM detection is relevant; it is not guaranteed to appear on every run.
- **No live data ingestion yet** — incidents are entered as free text by the user; the platform does not currently ingest real-time meeting transcripts, CRM updates, or emails directly.

---

##  Future Enhancements

- **Persistent storage** (PostgreSQL or Redis) for workflow state and audit logs, replacing the current in-memory store
- **Real-time enterprise data ingestion** — direct integration with CRM systems, email, and meeting transcription tools
- **System metrics dashboard** — surfacing latency, token usage, and per-agent execution traces for observability
- **Authentication and role-based access control** for production deployment
- **Visual workflow designer** allowing new business domains to be defined without code changes
- **Multi-domain expansion** — reusing the same planner/orchestration core for other enterprise decision problems beyond crisis response (e.g. customer success, M&A due diligence)

---

## 🏁 Conclusion

NBDE demonstrates how agentic AI can move beyond a single chatbot or static dashboard into a genuine decision-support system — one that gathers its own context, reasons through multiple specialized agents, simulates alternative futures, and explains every conclusion, while still keeping a human reviewer in control of what actually gets acted on. The Enterprise Crisis Intelligence scenario in this repository is one demonstration of that architecture; the underlying planner and orchestration engine are designed to extend to other enterprise decision domains with minimal structural change.
