from datetime import datetime
from .nlp_engine import NLPEngine
from .memory_simulation import MemorySimulation


class ThoughtGenerator:
    def __init__(self):
        """
        Initialize Thought Generator with NLP Engine and Memory Simulation.
        """
        self.nlp_engine = NLPEngine()
        self.memory_simulator = MemorySimulation()

    def generate_thought(self, seed_text):
        """
        Generate a memory-degraded thought based on seed text.
        Returns: Generated thought as a string.
        """
        keywords = self.nlp_engine.extract_keywords(seed_text)
        memory_degraded_thought = self.memory_simulator.degrade_memory(" ".join(keywords))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] {memory_degraded_thought}"

    def random_thought(self):
        """
        Generate a random, abstract thought.
        Returns: Thought as a string.
        """
        random_prompts = [
            "I wonder what it feels like to remember everything.",
            "What happens to the moments we forget?",
            "Sometimes, even silence feels loud.",
        ]
        seed = random.choice(random_prompts)
        return self.generate_thought(seed)

    def simulate_repeated_thoughts(self, seed_text):
        """
        Generate a thought with simulated repetition.
        Returns: Repeated thought as a string.
        """
        degraded = self.memory_simulator.amplify_repetition(seed_text)
        return degraded

    def generate_confused_thought(self, seed_text):
        """
        Generate a thought with simulated confusion.
        Returns: Confused thought as a string.
        """
        reordered = self.memory_simulator.reorder_memory(seed_text)
        return reordered