"""The LastCleanedAPI class is for loading and parsing JSON files."""

import json
from typing import Any


class LastCleanedAPI:
    """Load and parse the JSON file."""

    def __init__(self, json_file_path: str) -> None:
        """Initialize the API."""

        self.json_file_path = json_file_path
        self.data = self.load_data()

    def load_data(self) -> dict:
        """Load and parse the JSON file."""
        with open(self.json_file_path, encoding="utf-8") as file:
            return json.load(file)

    def get_last_cleaned(self) -> dict[str, Any]:
        """Get the last cleaned data."""
        return self.data
