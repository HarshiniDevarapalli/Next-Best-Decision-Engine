# Next Best Decision Engine

An agentic decision engine that orchestrates datasource and reasoning agents to produce next-best-action recommendations with explainability.

## Project Structure

```
backend/          FastAPI service, planner, agent registry, and workflow execution
frontend/         Web UI (placeholder)
docs/             Documentation
```

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs at `/docs`.

### Example Request

```bash
curl -X POST http://localhost:8000/api/v1/decide \
  -H "Content-Type: application/json" \
  -d '{"workflow": "customer_success", "context": {"customer_id": "cust_001"}}'
```

## Architecture

1. **Workflow Loader** — loads workflow definitions from JSON
2. **Planner** — resolves workflow steps and agent execution order
3. **Registry** — maps agent names to agent implementations
4. **Agents** — datasource agents fetch context; reasoning agents analyze and recommend
5. **API** — exposes decision endpoints

## Workflows

Workflow definitions live in `backend/data/workflows/`. See `customer_success.json` for an example.
