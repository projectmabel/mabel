import random


class MemorySimulation:
    def __init__(self, recall_rate=0.7):
        """
        Initialize Memory Simulation with a given recall rate.
        Default recall rate: 70%.
        """
        self.recall_rate = recall_rate

    def degrade_memory(self, text):
        """
        Simulate memory degradation by omitting words based on the recall rate.
        Returns: Memory-degraded text.
        """
        words = text.split()
        return " ".join([word if random.random() < self.recall_rate else "..." for word in words])

    def partial_recall(self, thoughts):
        """
        Simulate partial recall by returning a subset of thoughts.
        Returns: List of remembered thoughts.
        """
        return random.sample(thoughts, k=max(1, int(len(thoughts) * self.recall_rate)))

    def reorder_memory(self, text):
        """
        Simulate confusion by shuffling the order of words in a sentence.
        Returns: Text with shuffled word order.
        """
        words = text.split()
        random.shuffle(words)
        return " ".join(words)

    def amplify_repetition(self, text):
        """
        Simulate repetition by duplicating random words.
        Returns: Text with repeated words.
        """
        words = text.split()
        repeated_words = [
            word if random.random() > 0.2 else word + " " + word for word in words
        ]
        return " ".join(repeated_words)

    def forget_sentences(self, text):
        """
        Remove random sentences from a multi-sentence text.
        Returns: Text with missing sentences.
        """
        sentences = text.split(". ")
        filtered = [
            sentence for sentence in sentences if random.random() < self.recall_rate
        ]
        return ". ".join(filtered) + ("." if filtered else "")
