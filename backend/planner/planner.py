from models.execution_context import ExecutionContext
from models.responses import DecisionResponse
from models.workflow import WorkflowDefinition
from planner.workflow_loader import WorkflowLoader
from registry.registry import AgentRegistry


class Planner:
    def __init__(
        self,
        registry: AgentRegistry,
        workflow_loader: WorkflowLoader | None = None,
    ) -> None:
        self.registry = registry
        self.workflow_loader = workflow_loader or WorkflowLoader()

    def execute(self, workflow_name: str, context: ExecutionContext) -> DecisionResponse:
        workflow = self.workflow_loader.load(workflow_name)
        self._run_workflow(workflow, context)
        return self._build_response(workflow_name, context)

    def _run_workflow(self, workflow: WorkflowDefinition, context: ExecutionContext) -> None:
        completed: set[str] = set()

        while len(completed) < len(workflow.steps):
            progress = False
            for step in workflow.steps:
                if step.agent in completed:
                    continue
                if not all(dep in completed for dep in step.depends_on):
                    continue

                agent = self.registry.get(step.agent)
                output = agent.run(context)
                context.set_agent_output(step.agent, output)
                completed.add(step.agent)
                progress = True

            if not progress:
                pending = [s.agent for s in workflow.steps if s.agent not in completed]
                raise RuntimeError(f"Workflow deadlock; unresolved steps: {pending}")

    def _build_response(self, workflow_name: str, context: ExecutionContext) -> DecisionResponse:
        recommendation = context.get_agent_output("recommendation_agent") or {}
        explanation = context.get_agent_output("explainability_agent") or ""

        if isinstance(explanation, dict):
            explanation = explanation.get("summary", str(explanation))

        return DecisionResponse(
            workflow=workflow_name,
            recommendation=recommendation if isinstance(recommendation, dict) else {"value": recommendation},
            explanation=str(explanation),
            agent_outputs=context.agent_outputs,
        )
