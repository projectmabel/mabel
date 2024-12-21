import random


class EmotionModel:
    def __init__(self):
        """
        Initialize Emotion Model with predefined emotions.
        """
        self.emotions = ["happy", "sad", "confused", "nostalgic", "anxious", "calm"]
        self.contextual_weights = {
            "happy": ["joy", "love", "success"],
            "sad": ["loss", "forget", "lonely"],
            "nostalgic": ["memory", "past", "childhood"],
            "anxious": ["worry", "stress", "uncertain"],
        }

    def predict_emotion(self, text):
        """
        Predict an emotional response based on keywords in the text.
        Returns: Predicted emotion.
        """
        for emotion, triggers in self.contextual_weights.items():
            if any(trigger in text for trigger in triggers):
                return emotion
        return random.choice(self.emotions)

    def adjust_emotion(self, emotion, intensity=1.0):
        """
        Adjust the intensity of an emotion (e.g., 'slightly happy').
        Returns: Adjusted emotion as a string.
        """
        intensity_modifiers = {0.5: "slightly", 1.0: "", 1.5: "very"}
        modifier = intensity_modifiers.get(intensity, "")
        return f"{modifier} {emotion}".strip()

    def simulate_emotion_shift(self, text):
        """
        Simulate shifting emotions in response to text.
        Returns: List of emotional states.
        """
        base_emotion = self.predict_emotion(text)
        shifts = random.sample(self.emotions, k=2)
        return [base_emotion] + shifts