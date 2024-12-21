import os
import json
import pandas as pd
import logging


class DataStorage:
    """
    Handles data storage in JSON and CSV formats.
    """

    def __init__(self, storage_dir="storage"):
        """
        Initialize DataStorage with a default directory.
        """
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def save_to_json(self, data, filename):
        """
        Save data to a JSON file.
        """
        self.logger.info(f"Saving data to JSON file: {filename}")
        filepath = os.path.join(self.storage_dir, filename)
        with open(filepath, "w") as json_file:
            json.dump(data, json_file, indent=4)

    def load_from_json(self, filename):
        """
        Load data from a JSON file.
        """
        self.logger.info(f"Loading data from JSON file: {filename}")
        filepath = os.path.join(self.storage_dir, filename)
        with open(filepath, "r") as json_file:
            return json.load(json_file)

    def save_to_csv(self, dataframe, filename):
        """
        Save a DataFrame to a CSV file.
        """
        self.logger.info(f"Saving DataFrame to CSV file: {filename}")
        filepath = os.path.join(self.storage_dir, filename)
        dataframe.to_csv(filepath, index=False)

    def load_from_csv(self, filename):
        """
        Load a DataFrame from a CSV file.
        """
        self.logger.info(f"Loading DataFrame from CSV file: {filename}")
        filepath = os.path.join(self.storage_dir, filename)
        return pd.read_csv(filepath)

    def list_files(self):
        """
        List all files in the storage directory.
        """
        self.logger.info("Listing all files in storage directory...")
        return os.listdir(self.storage_dir)
