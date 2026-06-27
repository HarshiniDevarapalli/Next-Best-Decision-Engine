# Next Best Decision Engine (NBDE)

An AI-powered multi-agent decision intelligence platform that assists Customer Success teams by analyzing customer data, identifying risks, generating recommendations, and explaining every decision through an extensible workflow engine.

---

## Overview

The **Next Best Decision Engine (NBDE)** is designed to automate customer success decision-making using a modular multi-agent architecture.

Instead of hardcoding business logic, NBDE executes configurable workflows where each agent performs a specific task. Data collection agents gather customer information, reasoning agents analyze the collected data, and the system produces transparent, explainable recommendations.

The platform is designed to be scalable, extensible, and model-agnostic, allowing traditional rule-based logic to be replaced by machine learning models in the future.

---

# Project Goals

- Build a configurable workflow execution platform
- Support modular AI agents
- Enable explainable decision making
- Allow easy integration of ML models
- Provide an interactive dashboard for Customer Success teams

---

# Business Use Case

Customer Success Managers often need to analyze information scattered across multiple systems:

- CRM records
- Meeting notes
- Product adoption metrics
- Customer health scores
- Company news
- Internal knowledge base

NBDE automatically combines all these sources to recommend the **next best action** for every customer.

Example recommendations:

- Schedule an Executive Business Review
- Offer pricing flexibility
- Escalate churn risk
- Engage executive stakeholders
- Recommend product training

---

# System Architecture

```
                React Dashboard
                        │
                        ▼
                FastAPI Backend
                        │
                        ▼
            Workflow Orchestration Engine
        ┌─────────────────────────────────┐
        │ Planner                         │
        │ Workflow Loader                 │
        │ Agent Registry                  │
        │ Execution Context               │
        └─────────────────────────────────┘
                        │
                        ▼
                Plugin Agent Layer
      CRM → Meeting → News → Knowledge
          → Weak Signal → Risk
      → Recommendation → Explainability
                        │
                        ▼
               Shared Execution Context
                        │
                        ▼
                 JSON API Response
```

---

# Project Structure

Next-Best-Decision-Agent/
│
├── README.md
├── LICENSE
├── .gitignore
│
├── backend/
│   │
│   ├── app/
│   │   └── main.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── agents/
│   │   ├── base_agent.py
│   │   │
│   │   ├── datasource/
│   │   │   ├── crm_agent.py
│   │   │   ├── meeting_agent.py
│   │   │   ├── news_agent.py
│   │   │   └── knowledge_agent.py
│   │   │
│   │   └── reasoning/
│   │       ├── weak_signal_agent.py
│   │       ├── risk_agent.py
│   │       ├── recommendation_agent.py
│   │       └── explainability_agent.py
│   │
│   ├── planner/
│   │   ├── planner.py
│   │   └── workflow_loader.py
│   │
│   ├── registry/
│   │   └── registry.py
│   │
│   ├── models/
│   │   ├── workflow.py
│   │   ├── execution_context.py
│   │   ├── agent_result.py
│   │   └── request.py
│   │
│   ├── workflows/
│   │   └── customer_success.json
│   │
│   ├── data/
│   │   ├── crm.json
│   │   ├── meetings.json
│   │   ├── news.json
│   │   └── knowledge.json
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   └── helpers.py
│   │
│   ├── tests/
│   │   ├── test_planner.py
│   │   ├── test_registry.py
│   │   ├── test_workflow_loader.py
│   │   └── test_agents.py
│   │
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── public/
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard/
│   │   │   ├── WhatIfSimulator/
│   │   │   ├── ShadowMode/
│   │   │   ├── DecisionTimeline/
│   │   │   └── Explainability/
│   │   │
│   │   ├── pages/
│   │   │   └── Home.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── hooks/
│   │   │
│   │   ├── assets/
│   │   │
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── ml/
│   │
│   ├── datasets/
│   │   ├── synthetic_meetings.json
│   │   └── labeled_signals.json
│   │
│   ├── training/
│   │   ├── train_weak_signal.py
│   │   ├── train_risk.py
│   │   └── evaluate.py
│   │
│   ├── inference/
│   │   ├── weak_signal_model.py
│   │   ├── risk_model.py
│   │   └── recommendation_model.py
│   │
│   └── models/
│       ├── weak_signal/
│       ├── risk/
│       └── recommendation/
│
├── docs/
│   ├── architecture.png
│   ├── architecture.md
│   ├── api_documentation.md
│   └── workflow_examples.md
│
└── presentation/
    ├── diagrams/
    ├── screenshots/
    └── demo.mp4

---

# Workflow Execution

A workflow is defined as JSON.

Example:
'''
Workflow Definition
        ↓
Workflow Orchestrator (Planner)
        ↓
Data Collection Agents
    ├── CRM Agent
    ├── Meeting Agent
    ├── News Agent
    └── Knowledge Agent
        ↓
Shared Execution Context
        ↓
Decision Intelligence Agents
    ├── Weak Signal Intelligence
    ├── Risk Assessment
    ├── Recommendation Engine
    └── Explainability Engine
        ↓
Decision Response
'''
The Planner dynamically loads this workflow and executes every enabled agent in sequence.

---

# Core Components

## Planner

Responsible for orchestrating workflow execution.

Responsibilities:

- Load workflow
- Execute agents
- Maintain execution order
- Update ExecutionContext

The planner contains **no business logic**.

---

## Workflow Loader

Loads workflow definitions from JSON.

Allows workflows to be modified without changing source code.

---

## Agent Registry

Maintains all available agents.

Maps

```
crm
```

to

```
CRMAgent
```

allowing dynamic execution.

---

## Execution Context

Acts as shared memory across all agents.

Stores

- customer information
- agent outputs
- intermediate results
- metadata

Every agent reads from and writes to the Execution Context.

---

## AgentResult

Every agent returns a standardized response.

```python
AgentResult
{
    agent_name
    status
    data
    execution_time_ms
    message
}
```

---

# Current Agents

## Data Collection

- CRM Agent
- Meeting Agent
- News Agent
- Knowledge Agent

These agents collect customer-specific information.

---

## Reasoning Agents

- Weak Signal Intelligence
- Risk Assessment
- Recommendation Engine
- Explainability Engine

These agents consume outputs from previous agents and generate actionable insights.

---

# API

## Run Workflow

```
POST /workflow/run
```

Example request

```json
{
    "workflow": "customer_success",
    "customer_id": "cust_001"
}
```

Example response

```json
{
    "workflow_name": "customer_success",
    "status": "SUCCESS",
    "context_data": {
        ...
    },
    "agent_results": [
        ...
    ]
}
```

---

# Technology Stack

## Backend

- Python
- FastAPI
- Pydantic

## Frontend

- React
- Tailwind CSS

## AI / ML

- HuggingFace Transformers
- DistilBERT (planned)
- Scikit-learn

## Data

- JSON (current)
---

# Future Enhancements

- Fine-tune the Weak Signal Intelligence model using DistilBERT
- Replace rule-based Risk Assessment with an ML-based risk prediction model
- Replace rule-based Recommendation Engine with a learning-to-rank recommendation model
- PostgreSQL integration
- CRM API integration (Salesforce, HubSpot, etc.)
- Real-time News API integration
- Authentication & Role-Based Access Control
- Workflow Designer UI
- Real-time event processing
- Model monitoring and performance analytics

---

# Team Responsibilities

### Platform & Workflow Engine

- FastAPI backend
- Planner
- Workflow Loader
- Agent Registry
- Execution Context
- Data Source Agents

### AI Reasoning

- Weak Signal Intelligence
- Risk Assessment
- Recommendation Engine
- Explainability

### Frontend

- React Dashboard
- What-If Simulator
- Shadow Mode
- Decision Visualization

---

# Design Principles

- Modular Plugin Architecture
- Dynamic Workflow Execution
- Explainable AI
- Separation of Concerns
- Extensible ML Pipeline
- Configurable Workflows
- Reusable Agent Interfaces

---

# Setup and Running the Project

Clone the repository

```bash
git clone <repository-url>
```

Navigate to the backend

```bash
cd backend
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

**Windows**

```bash
venv\Scripts\activate
```

**macOS/Linux**

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the backend

```bash
uvicorn app.main:app --reload
```

Open Swagger

```
http://127.0.0.1:8000/docs
```

---

# Vision

NBDE aims to evolve into a configurable enterprise decision intelligence platform where organizations can create workflows composed of specialized AI agents that analyze business data, generate explainable recommendations, and support high-quality decision making across multiple domains.
