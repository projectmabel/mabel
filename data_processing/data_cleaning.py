import re
import logging


class DataCleaning:
    """
    Cleans and pre-processes raw text data.
    """

    def __init__(self):
        """
        Initialize logging for DataCleaning.
        """
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def remove_special_characters(self, text):
        """
        Remove special characters from text.
        """
        self.logger.info("Removing special characters...")
        cleaned_text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        return cleaned_text

    def to_lowercase(self, text):
        """
        Convert text to lowercase.
        """
        self.logger.info("Converting text to lowercase...")
        return text.lower()

    def remove_stopwords(self, text, stopwords=None):
        """
        Remove stopwords from text.
        """
        if stopwords is None:
            stopwords = {"the", "and", "is", "in", "to", "of", "a", "that"}
        self.logger.info("Removing stopwords...")
        words = text.split()
        filtered_text = " ".join([word for word in words if word not in stopwords])
        return filtered_text

    def remove_urls(self, text):
        """
        Remove URLs from text.
        """
        self.logger.info("Removing URLs...")
        cleaned_text = re.sub(r"http\S+|www\S+", "", text)
        return cleaned_text

    def normalize_whitespace(self, text):
        """
        Normalize whitespace in text.
        """
        self.logger.info("Normalizing whitespace...")
        cleaned_text = re.sub(r"\s+", " ", text).strip()
        return cleaned_text

    def clean_text(self, text):
        """
        Perform all cleaning steps on text.
        """
        self.logger.info("Starting full cleaning process...")
        text = self.remove_special_characters(text)
        text = self.to_lowercase(text)
        text = self.remove_urls(text)
        text = self.remove_stopwords(text)
        text = self.normalize_whitespace(text)
        self.logger.info("Cleaning process completed.")
        return text
