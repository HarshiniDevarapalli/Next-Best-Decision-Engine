import json
from pathlib import Path

from models.workflow import Workflow


class WorkflowLoader:
    """
    Loads workflow configurations from JSON files.
    """

    def __init__(self, workflow_directory: str = "data/workflows"):
        self.workflow_directory = Path(workflow_directory)

    def load_workflow(self, workflow_name: str) -> Workflow:
        """
        Load and validate a workflow configuration.

        Args:
            workflow_name (str): Name of the workflow.

        Returns:
            Workflow: Validated workflow object.

        Raises:
            FileNotFoundError: If workflow JSON does not exist.
            ValueError: If JSON is invalid.
        """

        workflow_file = self.workflow_directory / f"{workflow_name}.json"

        if not workflow_file.exists():
            raise FileNotFoundError(
                f"Workflow '{workflow_name}' not found."
            )

        try:
            with open(workflow_file, "r", encoding="utf-8") as file:
                workflow_data = json.load(file)

            return Workflow(**workflow_data)

        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON in workflow '{workflow_name}': {e}"
            )

        except Exception as e:
            raise ValueError(
                f"Failed to load workflow '{workflow_name}': {e}"
            )