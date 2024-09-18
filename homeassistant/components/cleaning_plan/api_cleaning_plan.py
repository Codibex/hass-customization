"""The CleaningPlanAPI class is for loading and parsing JSON files."""

import json
from typing import Any


class CleaningPlanAPI:
    """Load and parse the JSON file."""

    def __init__(self, json_file_path: str) -> None:
        """Initialize the API."""

        self.json_file_path = json_file_path
        self.data = self.load_data()

    def load_data(self) -> dict:
        """Load and parse the JSON file."""
        with open(self.json_file_path, encoding="utf-8") as file:
            return json.load(file)

    def get_cleaning_plan(self) -> dict[str, Any]:
        """Get the cleaning plan data."""
        return self.data
