import spacy
from transformers import pipeline


class NLPEngine:
    def __init__(self):
        """
        Initialize NLP Engine with SpaCy and Hugging Face pipelines.
        """
        self.nlp = spacy.load("en_core_web_sm")
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.summarizer = pipeline("summarization")

    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of the given text.
        Returns: List of dictionaries containing label and score.
        """
        return self.sentiment_analyzer(text)

    def extract_keywords(self, text):
        """
        Extract keywords from text using SpaCy.
        Returns: List of keywords.
        """
        doc = self.nlp(text)
        return [token.text for token in doc if token.is_alpha and not token.is_stop]

    def summarize_text(self, text, max_length=50, min_length=20):
        """
        Summarize the given text.
        """
        return self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)

    def parse_named_entities(self, text):
        """
        Extract named entities (e.g., names, places) from text.
        Returns: List of entities with their labels.
        """
        doc = self.nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]

    def detect_language(self, text):
        """
        Detect the language of the input text using SpaCy.
        Returns: Language code (e.g., 'en' for English).
        """
        doc = self.nlp(text)
        return doc.lang_

    def tokenize_text(self, text):
        """
        Tokenize the input text into words and punctuation.
        Returns: List of tokens.
        """
        doc = self.nlp(text)
        return [token.text for token in doc]