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
    - Execute enabled agents in sequence
    - Maintain the shared ExecutionContext
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
        # Execute agents in workflow order
        for agent_config in workflow.agents:

            # Skip disabled agents
            if not agent_config.enabled:
                continue

            # Get the agent (will raise KeyError if not registered)
            agent = self.agent_registry.get(agent_config.name)

            # Execute the agent
            result = agent.execute(context)

            # Store results
            context.agent_results.append(result)
            context.context_data[agent_config.name] = result.data

        context.status = "SUCCESS"

        return context