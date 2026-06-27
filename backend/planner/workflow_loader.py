import json
from pathlib import Path

from app.config import settings
from models.workflow import WorkflowDefinition


class WorkflowLoader:
    def __init__(self, workflows_dir: Path | None = None) -> None:
        self.workflows_dir = workflows_dir or settings.workflows_dir

    def load(self, workflow_name: str) -> WorkflowDefinition:
        path = self.workflows_dir / f"{workflow_name}.json"
        if not path.exists():
            raise FileNotFoundError(f"Workflow not found: {workflow_name}")

        with path.open() as f:
            data = json.load(f)

        return WorkflowDefinition(**data)

    def list_workflows(self) -> list[str]:
        return [p.stem for p in self.workflows_dir.glob("*.json")]
