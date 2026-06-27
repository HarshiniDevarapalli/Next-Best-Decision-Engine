# planner/planner.py

from models.execution_context import ExecutionContext
from planner.workflow_loader import WorkflowLoader
from registry.registry import AgentRegistry


class Planner:
    """
    The Planner orchestrates workflow execution.

    Responsibilities:
    - Load workflow configuration
    - Retrieve required agents from the registry
    - Execute agents in sequence
    - Return the updated ExecutionContext

    The Planner contains NO business logic.
    """

    def __init__(
        self,
        workflow_loader: WorkflowLoader,
        agent_registry: AgentRegistry
    ):
        self.workflow_loader = workflow_loader
        self.agent_registry = agent_registry

    def execute_workflow(
        self,
        workflow_name: str,
        customer_id: str
    ) -> ExecutionContext:

        # Load workflow configuration
        workflow = self.workflow_loader.load_workflow(workflow_name)

        # Create execution context
        context = ExecutionContext(
            workflow_name=workflow.workflow_name,
            customer_id=customer_id
        )

        # Execute agents in workflow order
        for agent_name in workflow.agents:

            agent = self.agent_registry.get(agent_name)

            result = agent.execute(context)

            context.agent_results.append(result)

            # Store output in shared context
            context.context_data[agent_name] = result.data

        context.status = "SUCCESS"

        return context