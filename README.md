# Next Best Decision Engine (NBDE)

> **A Reusable Agentic Decision Intelligence Platform for Enterprise Workflows**

NBDE is a modular multi-agent workflow orchestration platform that helps organizations make high-quality decisions under uncertainty by combining information from multiple enterprise data sources, reasoning over that information, and generating explainable recommendations.

The platform is **domain-independent**. While this repository demonstrates its capabilities using an **Enterprise Crisis Intelligence** workflow, the same architecture can be reused for any enterprise decision-making problem by simply defining a new workflow and plugging in different agents.

---

# Why NBDE?

Modern enterprises face decisions that require information from multiple disconnected systems.

Examples include:

- Supply chain disruptions
- Mergers & Acquisitions
- Customer Success
- Regulatory Compliance
- Fraud Investigation
- IT Incident Response
- Procurement
- Healthcare Operations

Instead of manually collecting information from multiple sources, NBDE orchestrates specialized agents that gather relevant information, analyze it, assess risks, recommend actions, and explain every recommendation.

---

# Demo Use Case

This project demonstrates the platform using an **Enterprise Crisis Intelligence** workflow.

### Scenario

A critical supplier unexpectedly shuts down operations.

The platform gathers information from multiple enterprise sources:

- Supplier Contracts
- Inventory Status
- Alternative Vendors
- Enterprise Policies
- External News
- Historical Incident Reports

It then reasons over this information to answer questions such as:

- Should production continue?
- Should procurement activate a backup supplier?
- Should legal teams be notified?
- Should customers be informed?
- What is the operational risk?
- Why is this recommendation being made?

This workflow is only an example implementation of the platform.

---

# Platform Reusability

One of the core goals of NBDE is to separate **business logic** from **workflow orchestration**.

The workflow engine never contains domain-specific logic.

Instead, every business domain is represented through configurable workflows and modular agents.

For example:

### Enterprise Crisis Response

```
Supplier Contracts
↓
Inventory
↓
Vendors
↓
Policies
↓
News
↓
Incident History
↓
Risk Assessment
↓
Recommendation
```

### Customer Success

```
CRM
↓
Meetings
↓
Product Usage
↓
Knowledge Base
↓
Customer Health
↓
Recommendation
```

### M&A Due Diligence

```
Financial Reports
↓
Legal Documents
↓
Compliance
↓
Cybersecurity
↓
Vendor Contracts
↓
Risk Assessment
```

The **Planner**, **Workflow Loader**, **Registry**, and **Execution Context** remain exactly the same.

Only the workflow configuration changes.

---

# Architecture

```
                        User
                          │
                          ▼
                  React Dashboard
                          │
                          ▼
                  FastAPI Backend
                          │
                          ▼
            Workflow Orchestration Engine
        ┌──────────────────────────────┐
        │ Planner                      │
        │ Workflow Loader              │
        │ Agent Registry               │
        │ Execution Context            │
        └──────────────────────────────┘
                          │
                          ▼
                 Configurable Workflow
                          │
                          ▼
              Domain-Specific Agents
                          │
                          ▼
               Shared Execution Context
                          │
                          ▼
                Decision Recommendations
```

---

# Key Features

- Configurable workflow execution
- Plugin-based agent architecture
- Dynamic workflow loading from JSON
- Shared execution context
- Explainable recommendations
- Reusable orchestration engine
- Domain-independent design
- Extensible AI pipeline

---

# Current Demo Workflow

```
Workflow
        ↓
Supplier Contract Agent
        ↓
Inventory Agent
        ↓
Vendor Agent
        ↓
Policy Agent
        ↓
News Agent
        ↓
Incident History Agent
        ↓
Weak Signal Intelligence
        ↓
Risk Assessment
        ↓
Recommendation Engine
        ↓
Explainability Engine
        ↓
Decision Response
```

---

# Core Components

## Planner

Coordinates workflow execution.

Responsibilities:

- Load workflow
- Execute agents
- Maintain execution order
- Store outputs in shared context

---

## Workflow Loader

Loads workflow definitions from JSON.

No source code modifications are required when introducing a new workflow.

---

## Agent Registry

Maps workflow agent names to implementations.

Allows new agents to be plugged into the platform without modifying the planner.

---

## Execution Context

Acts as shared memory for every workflow.

Each agent can:

- Read outputs produced by previous agents
- Add its own results
- Pass enriched information to subsequent agents

---

## AgentResult

Every agent returns a standardized response:

```python
AgentResult
{
    agent_name,
    status,
    data,
    execution_time_ms,
    message
}
```

This allows the planner to execute all agents uniformly.

---

# Why the Platform is Reusable

The orchestration layer is completely independent of business logic.

To support a new domain, developers only need to:

1. Create new data source agents
2. Create new reasoning agents (optional)
3. Define a workflow JSON
4. Register the new agents

The Planner, Workflow Loader, Registry, Execution Context, and API remain unchanged.

This enables the same platform to support multiple enterprise workflows without architectural changes.

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

- Hugging Face Transformers (planned)
- DistilBERT (planned)
- Scikit-learn

## Data

- JSON (Demo)
- PostgreSQL (Future)

---

# Future Enhancements

- Replace rule-based reasoning with fine-tuned ML models
- PostgreSQL integration
- Enterprise API integrations (ERP, Procurement, CRM)
- Authentication & RBAC
- Visual workflow designer
- Real-time event streaming
- Workflow versioning
- Agent monitoring & observability

---

# Vision

NBDE is not tied to a single business domain.

It is designed as a **reusable Agentic Decision Intelligence Platform** capable of orchestrating specialized AI agents across multiple enterprise workflows.

The Enterprise Crisis Intelligence scenario included in this repository serves as a demonstration of how the platform can be adapted to solve real-world decision-making problems in any enterprise environment.
