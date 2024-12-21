import numpy as np
import pandas as pd
import logging


class DataTransformation:
    """
    Transforms text data into numerical representations or structured formats.
    """

    def __init__(self):
        """
        Initialize logging for DataTransformation.
        """
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def text_to_vector(self, text, vocabulary):
        """
        Convert text to a vector representation using a vocabulary.
        Returns: Numpy array representing the vector.
        """
        self.logger.info("Converting text to vector...")
        vector = np.zeros(len(vocabulary))
        words = text.split()
        for word in words:
            if word in vocabulary:
                vector[vocabulary.index(word)] += 1
        return vector

    def create_dataframe(self, texts, labels):
        """
        Create a Pandas DataFrame from texts and labels.
        """
        self.logger.info("Creating DataFrame from text and labels...")
        data = {"text": texts, "label": labels}
        return pd.DataFrame(data)

    def split_data(self, dataframe, test_size=0.2):
        """
        Split DataFrame into training and testing sets.
        """
        self.logger.info("Splitting data into training and test sets...")
        train = dataframe.sample(frac=1 - test_size, random_state=42)
        test = dataframe.drop(train.index)
        return train, test

    def generate_n_grams(self, text, n=2):
        """
        Generate n-grams from text.
        Returns: List of n-grams.
        """
        self.logger.info(f"Generating {n}-grams...")
        words = text.split()
        n_grams = [" ".join(words[i : i + n]) for i in range(len(words) - n + 1)]
        return n_grams

    def normalize_data(self, array):
        """
        Normalize numerical data to a range of 0 to 1.
        """
        self.logger.info("Normalizing data...")
        normalized = (array - np.min(array)) / (np.max(array) - np.min(array))
        return normalized
