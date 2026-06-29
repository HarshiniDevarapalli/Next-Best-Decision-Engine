import json
from pathlib import Path
from typing import List

from langchain_core.documents import Document


class EnterpriseDocumentLoader:
    """
    Loads enterprise knowledge from JSON files.

    Supported:
    - vendors.json
    - inventory.json
    - supplier_contracts.json
    - policies.json
    - incident_history.json
    - news.json

    Every JSON object becomes one LangChain Document.
    """

    def __init__(self, data_dir: str):

        self.data_dir = Path(data_dir)

    def load(self) -> List[Document]:

        documents = []

        json_files = self.data_dir.rglob("*.json")

        for json_file in json_files:

            try:

                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # JSON Array
                if isinstance(data, list):

                    for record in data:

                        documents.append(
                            Document(
                                page_content=json.dumps(
                                    record,
                                    indent=2,
                                ),
                                metadata={
                                    "source": json_file.name,
                                    "file_path": str(json_file),
                                },
                            )
                        )

                # JSON Object
                elif isinstance(data, dict):

                    documents.append(
                        Document(
                            page_content=json.dumps(
                                data,
                                indent=2,
                            ),
                            metadata={
                                "source": json_file.name,
                                "file_path": str(json_file),
                            },
                        )
                    )

            except Exception as e:

                print(f"Error loading {json_file}: {e}")

        return documents