# Next Best Decision Engine (NBDE)

## Team Details

**Team Name:** PHI

| Name | Email |
|------|-------|
| Harshini Devarapalli | devarapalliharshini10@gmail.com |
| Praneeth Dutt Nadimpally | praneethdutt@gmail.com |
| Ishitha Alluru | alluruishitha@gmail.com |

---

# Project Overview

The **Next Best Decision Engine (NBDE)** is an AI-powered **Enterprise Decision Intelligence Platform** designed to help organizations make intelligent, explainable, and timely decisions during critical business incidents.

Modern enterprises often struggle to make rapid decisions because relevant information is distributed across contracts, inventory systems, policies, historical incidents, vendor databases, and external news sources. Existing systems typically provide isolated alerts or a single recommendation, leaving decision-makers to manually analyze multiple systems before taking action.

NBDE addresses this challenge through a **multi-agent AI architecture orchestrated using LangGraph**. Instead of relying on a single AI model, the platform dynamically coordinates specialized agents that retrieve enterprise knowledge, assess risks, generate recommendations, simulate multiple response strategies, estimate business impact, and explain every recommendation before requiring human approval for critical decisions.

The workflow consists of:

- Incident parsing
- Enterprise knowledge retrieval
- Weak signal detection
- Risk assessment
- Recommendation generation
- What-If scenario simulation
- Decision scoring
- Cost impact analysis
- Timeline prediction
- Scenario comparison
- Explainable AI reasoning
- Human-in-the-Loop approval

### Key Features

- Multi-Agent AI Architecture
- LangGraph Workflow Orchestration
- Enterprise Knowledge Retrieval
- Weak Signal Detection
- Risk Assessment
- AI-driven Recommendations
- What-If Scenario Simulation
- Decision Scoring
- Cost Impact Estimation
- Recovery Timeline Prediction
- Scenario Comparison
- Explainable AI (XAI)
- Human-in-the-Loop (HITL) Review
- Audit Logging

---

# GitHub Repository Link

> **Repository:**  
> https://github.com/HarshiniDevarapalli/Next-Best-Decision-Engine

---

# Setup Instructions

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm
- Git
- Google Gemini API Key

---

## 1. Clone the Repository

```bash
git clone <repository-url>
cd Next-Best-Decision-Agent
```

---

## 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

### macOS/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the backend folder:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Run the backend server:

```bash
cd ..
uvicorn backend.app.main:app --reload
```

Backend URL:

```
http://localhost:8000
```

API Documentation:

```
http://localhost:8000/docs
```

---

## 3. Frontend Setup

Navigate to the frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run the React application:

```bash
npm run dev
```

Frontend URL:

```
http://localhost:5173
```

---

## 4. Testing

To execute the complete backend workflow:

```bash
python -m backend.test_phase4
```

---

# Project Structure

```text
Next-Best-Decision-Agent/
│
├── backend/
│   │
│   ├── agents/
│   │   ├── datasource/
│   │   │   ├── supplier_contract_agent.py
│   │   │   ├── vendor_agent.py
│   │   │   ├── inventory_agent.py
│   │   │   ├── policy_agent.py
│   │   │   ├── news_agent.py
│   │   │   └── incident_history_agent.py
│   │   │
│   │   └── reasoning/
│   │       ├── weak_signal_agent.py
│   │       ├── risk_agent.py
│   │       ├── recommendation_agent.py
│   │       ├── what_if_agent.py
│   │       ├── decision_scoring_agent.py
│   │       ├── cost_impact_agent.py
│   │       ├── timeline_prediction_agent.py
│   │       ├── scenario_comparison_agent.py
│   │       ├── explainability_agent.py
│   │       └── human_review_agent.py
│   │
│   ├── api/
│   │   ├── routes.py
│   │   └── review.py
│   │
│   ├── app/
│   │   └── main.py
│   │
│   ├── graph/
│   │   ├── workflow_graph.py
│   │   ├── nodes.py
│   │   └── state.py
│   │
│   ├── planner/
│   │   └── planner.py
│   │
│   ├── registry/
│   │   └── registry.py
│   │
│   ├── services/
│   │   ├── ai/
│   │   ├── human_review_service.py
│   │   └── ...
│   │
│   ├── models/
│   ├── data/
│   ├── rag/
│   ├── utils/
│   ├── vector_db/
│   ├── vector_db_backup/
│   ├── test_phase4.py
│   ├── requirements.txt
│   └── venv/
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── public/
│   ├── components/
│   ├── pages/
│   ├── assets/
│   ├── utils/
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   └── index.html
│
├── README.md
├── .gitignore
└── LICENSE
```

---

# Additional Notes

- The platform uses **LangGraph** to orchestrate a multi-agent workflow.
- AI reasoning is powered by **Google Gemini** models.
- Vector search is implemented using **ChromaDB** and **Sentence Transformers**.
- Critical recommendations require **Human-in-the-Loop (HITL)** approval before workflow completion.
- Every recommendation includes explainability, confidence scores, supporting evidence, assumptions, and reasoning steps.
- The frontend communicates with the backend through REST APIs developed using FastAPI.
- The architecture is modular, allowing additional datasource agents and reasoning agents to be integrated easily.

---

## Future Enhancements

- Persistent workflow storage using PostgreSQL or Redis
- Role-Based Access Control (RBAC)
- Real-time notifications (Email, Slack, Microsoft Teams)
- Interactive analytics dashboard
- Docker and Kubernetes deployment
- CI/CD pipeline integration
- Multi-model AI support
- Enterprise RAG over organizational documents

---

## License

This project was developed by **Team PHI** as part of an academic software engineering project.
