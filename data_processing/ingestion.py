import requests
import logging
import json


class DataIngestion:
    """
    Handles data ingestion from APIs, files, and other sources.
    """

    def __init__(self):
        """
        Initialize logging for DataIngestion.
        """
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def fetch_from_api(self, url, headers=None):
        """
        Fetch data from an API endpoint.
        """
        self.logger.info(f"Fetching data from API: {url}")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            self.logger.error(f"Failed to fetch data: {response.status_code}")
            response.raise_for_status()

    def read_from_file(self, filepath):
        """
        Read data from a file (supports JSON and text).
        """
        self.logger.info(f"Reading data from file: {filepath}")
        with open(filepath, "r") as file:
            if filepath.endswith(".json"):
                return json.load(file)
            else:
                return file.read()

    def fetch_sample_data(self):
        """
        Fetch sample data for testing purposes.
        """
        self.logger.info("Fetching sample data...")
        return [
            {"id": 1, "text": "This is a sample text.", "label": "positive"},
            {"id": 2, "text": "Another example here.", "label": "neutral"},
        ]