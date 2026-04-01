# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import string
from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        Improvements implemented:
          - Removes punctuation
          - Maps emojis to sentiment words
          - Strips leading/trailing whitespace
          - Converts to lowercase
        """
        # Map common emojis to sentiment words before processing
        emoji_map = {
            "😂": "amazing",
            "🥲": "sad",
            ":)": "happy",
            ":(": "sad",
            ":-)": "happy",
            ":-(": "sad",
            "💀": "sad",
            "🔥": "awesome",
            "✨": "awesome",
        }
        
        cleaned = text.strip()
        # Replace emojis with words
        for emoji, word in emoji_map.items():
            cleaned = cleaned.replace(emoji, " " + word + " ")
        
        # Remove punctuation
        cleaned = cleaned.translate(str.maketrans('', '', string.punctuation))
        cleaned = cleaned.lower()
        
        tokens = cleaned.split()
        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def _detect_sarcasm(self, text: str) -> bool:
        """Check if the text contains common sarcasm patterns."""
        lowered = text.lower()

        # Known sarcastic phrases
        sarcastic_phrases = [
            "oh great",
            "yeah right",
            "sure thing",
            "thanks for nothing",
            "how wonderful",
            "oh wonderful",
            "just wonderful",
            "oh fantastic",
            "just fantastic",
            "oh perfect",
            "just perfect",
            "what a surprise",
            "totally love",
            "absolutely love",
            "so fun",
        ]

        for phrase in sarcastic_phrases:
            if phrase in lowered:
                return True

        # Sarcasm markers: positive word near a clearly negative context
        sarcasm_markers = ["yeah", "sure", "totally", "absolutely", "obviously"]
        tokens = lowered.split()
        for marker in sarcasm_markers:
            if marker in tokens:
                # Check if a negative topic follows nearby
                marker_index = tokens.index(marker)
                nearby_words = tokens[marker_index:marker_index + 4]
                negative_topics = {"traffic", "monday", "mondays", "homework",
                                   "chores", "waiting", "meetings", "bills"}
                if any(w in negative_topics for w in nearby_words):
                    return True

        return False

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Improvements:
          - Counts word frequency (not just presence)
          - Handles negation ("not happy" -> negative)
          - Detects common sarcasm patterns and flips the score
        """
        tokens = self.preprocess(text)
        score = 0
        negation_words = {"not", "never", "no", "neither", "nor"}
        
        for i, token in enumerate(tokens):
            # Check if the word before this one is a negation word
            has_word_before = i > 0
            is_negated = has_word_before and tokens[i - 1] in negation_words

            is_positive = token in self.positive_words
            is_negative = token in self.negative_words

            if is_positive:
                if is_negated:
                    score -= 1  # "not happy" counts as negative
                else:
                    score += 1  # "happy" counts as positive

            elif is_negative:
                if is_negated:
                    score += 1  # "not sad" counts as positive
                else:
                    score -= 1  # "sad" counts as negative

        # If sarcasm detected, flip the score
        if self._detect_sarcasm(text) and score != 0:
            score = -score

        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        Mapping:
          - score > 0  -> "positive"
          - score < 0  -> "negative"
          - score == 0 and equal positive/negative counts -> "mixed"
          - score == 0 and no balance                     -> "neutral"
        """
        score = self.score_text(text)

        if score > 0:
            return "positive"
        elif score < 0:
            return "negative"
        else:
            # Score is 0 — figure out if it's mixed or neutral
            tokens = self.preprocess(text)
            positive_count = sum(1 for t in tokens if t in self.positive_words)
            negative_count = sum(1 for t in tokens if t in self.negative_words)

            both_sides_present = positive_count > 0 and negative_count > 0
            if both_sides_present and positive_count == negative_count:
                return "mixed"
            else:
                return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0

        for token in tokens:
            if token in self.positive_words:
                positive_hits.append(token)
                score += 1
            if token in self.negative_words:
                negative_hits.append(token)
                score -= 1

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
