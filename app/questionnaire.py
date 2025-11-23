from typing import Dict, Any, Tuple
from collections import defaultdict
from .rules_loader import rules
from .schemas import QuestionnaireSubmission, PaletteResult, ColorInfo


class SeasonAnalyzer:
    """Determines color season from questionnaire responses using rule-based algorithm"""

    def __init__(self):
        self.rules = rules

    def analyze(self, submission: QuestionnaireSubmission) -> PaletteResult:
        """
        Main analysis pipeline:
        1. Accumulate signals from responses
        2. Determine characteristics (undertone, value, chroma)
        3. Map to specific season
        4. Calculate confidence
        5. Return palette
        """

        # Step 1: Accumulate signals
        signals = self._accumulate_signals(submission)

        # Step 2: Determine characteristics
        undertone = self._determine_undertone(signals)
        value = self._determine_value(signals)
        chroma = self._determine_chroma(signals)

        # Step 3: Map to season
        season_key = self._map_to_season(undertone, value, chroma, signals)

        # Step 4: Calculate confidence
        confidence = self._calculate_confidence(season_key, undertone, value, chroma, signals, submission)

        # Step 5: Get palette
        season_data = self.rules.get_season_palette(season_key)

        # Step 6: Build result
        return PaletteResult(
            season=season_key,
            season_display_name=season_data.get("name", season_key.replace("_", " ").title()),
            confidence=confidence,
            undertone=undertone,
            value=value,
            chroma=chroma,
            core_neutrals=[ColorInfo(**color) for color in season_data.get("core_neutrals", [])],
            accent_colors=[ColorInfo(**color) for color in season_data.get("accent_colors", [])],
            avoid_colors=season_data.get("avoid_colors", []),
            explanation=None  # TODO: Add AI explanation in Phase 5
        )

    def _accumulate_signals(self, submission: QuestionnaireSubmission) -> Dict[str, int]:
        """Sum up all signals from questionnaire responses"""
        signals = defaultdict(int)

        # Map submission fields to question IDs
        question_map = {
            "q1": submission.hair_color,
            "q2": submission.skin_tone,
            "q3": submission.eye_color,
            "q4": submission.vein_color,
            "q5": submission.jewelry_preference,
            "q6": submission.colors_worn,  # Multi-select
            "q7": submission.colors_avoided,  # Multi-select
            "q8": submission.color_feedback,
        }

        for question_id, answer in question_map.items():
            if isinstance(answer, list):
                # Multi-select questions - normalize by number of selections to prevent inflation
                if len(answer) > 0:
                    normalization_factor = 1.0 / len(answer)
                    for answer_id in answer:
                        self._add_signals(signals, question_id, answer_id, normalization_factor)
            else:
                # Single-select questions - no normalization needed
                self._add_signals(signals, question_id, answer, 1.0)

        return signals

    def _add_signals(self, signals: Dict[str, int], question_id: str, answer_id: str, normalization_factor: float = 1.0):
        """Add signals from a specific answer to the accumulator, applying normalization factor"""
        answer_signals = self.rules.get_question_signals(question_id, answer_id)

        for signal_type, values in answer_signals.items():
            if isinstance(values, dict):
                for key, weight in values.items():
                    signal_key = f"{signal_type}_{key}"
                    # Apply normalization (for multi-select questions)
                    signals[signal_key] += weight * normalization_factor

    def _determine_undertone(self, signals: Dict[str, int]) -> str:
        """Determine dominant undertone: warm, cool, or neutral"""
        warm = signals.get("undertone_warm", 0)
        cool = signals.get("undertone_cool", 0)
        neutral = signals.get("undertone_neutral", 0)

        mapping = self.rules.mapping_rules.get("mapping_logic", {}).get("undertone_rules", {})
        warm_threshold = mapping.get("warm_threshold", 8)
        cool_threshold = mapping.get("cool_threshold", 8)

        # Strong signals
        if warm >= warm_threshold and warm > cool:
            return "warm"
        if cool >= cool_threshold and cool > warm:
            return "cool"

        # Neutral or close
        if abs(warm - cool) <= 2 or neutral >= 3:
            return "neutral"

        # Default to whichever is higher
        return "warm" if warm > cool else "cool"

    def _determine_value(self, signals: Dict[str, int]) -> str:
        """Determine dominant value: light, medium, or deep"""
        light = signals.get("value_light", 0)
        medium = signals.get("value_medium", 0)
        deep = signals.get("value_deep", 0)

        mapping = self.rules.mapping_rules.get("mapping_logic", {}).get("value_rules", {})
        light_threshold = mapping.get("light_threshold", 6)
        deep_threshold = mapping.get("deep_threshold", 6)

        if light >= light_threshold and light > deep:
            return "light"
        if deep >= deep_threshold and deep > light:
            return "deep"

        return "medium"

    def _determine_chroma(self, signals: Dict[str, int]) -> str:
        """Determine dominant chroma: bright, muted, soft, rich"""
        bright = signals.get("chroma_bright", 0)
        muted = signals.get("chroma_muted", 0)
        soft = signals.get("chroma_soft", 0)
        rich = signals.get("chroma_rich", 0)

        mapping = self.rules.mapping_rules.get("mapping_logic", {}).get("chroma_rules", {})
        bright_threshold = mapping.get("bright_threshold", 5)
        muted_threshold = mapping.get("muted_threshold", 5)

        # Priority: bright > rich > muted > soft
        if bright >= bright_threshold:
            return "bright"
        if rich >= 4:
            return "rich"
        if muted >= muted_threshold:
            return "muted"
        if soft >= 4:
            return "soft"

        # Default: clear (moderate brightness)
        return "clear"

    def _map_to_season(self, undertone: str, value: str, chroma: str, signals: Dict[str, int]) -> str:
        """Map characteristics to specific season using decision tree"""

        season_mappings = self.rules.mapping_rules.get("season_mappings", {})

        # Find matching season
        for season_key, season_rules in season_mappings.items():
            conditions = season_rules.get("conditions", {})

            # Check undertone match
            undertone_match = self._check_condition(undertone, conditions.get("undertone"))
            if not undertone_match:
                continue

            # Check value match
            value_match = self._check_condition(value, conditions.get("value"))
            if not value_match:
                continue

            # Check chroma match
            chroma_match = self._check_condition(chroma, conditions.get("chroma"))
            if not chroma_match:
                continue

            # All conditions match!
            return season_key

        # Fallback to simple mapping
        return self._simple_season_map(undertone, value, chroma)

    def _check_condition(self, actual_value: str, expected_value: Any) -> bool:
        """Check if actual value matches expected (can be string or list)"""
        if expected_value is None:
            return True  # No condition specified

        if isinstance(expected_value, list):
            return actual_value in expected_value

        return actual_value == expected_value

    def _simple_season_map(self, undertone: str, value: str, chroma: str) -> str:
        """Simple fallback mapping if complex rules don't match"""

        # Spring family (warm + bright/light)
        if undertone == "warm" and chroma == "bright":
            return "bright_spring"
        if undertone == "warm" and value == "light":
            return "light_spring"
        if undertone == "warm" and chroma == "clear":
            return "true_spring"

        # Summer family (cool + soft/light)
        if undertone == "cool" and value == "light":
            return "light_summer"
        if undertone == "cool" and chroma == "muted":
            return "true_summer"
        if undertone in ["cool", "neutral"] and chroma in ["muted", "soft"]:
            return "soft_summer"

        # Autumn family (warm + muted/deep)
        if undertone == "warm" and chroma == "muted":
            return "soft_autumn"
        if undertone == "warm" and chroma == "rich":
            return "true_autumn"
        if undertone == "warm" and value == "deep":
            return "dark_autumn"

        # Winter family (cool + bright/deep)
        if undertone == "cool" and value == "deep":
            return "dark_winter"
        if undertone == "cool" and chroma == "bright":
            return "true_winter"
        if undertone == "cool" and chroma == "very_bright":
            return "bright_winter"

        # Ultimate fallback
        return "true_spring" if undertone == "warm" else "true_summer"

    def _calculate_confidence(
        self,
        season: str,
        undertone: str,
        value: str,
        chroma: str,
        signals: Dict[str, int],
        submission: QuestionnaireSubmission
    ) -> int:
        """Calculate confidence score 0-100"""

        base_score = 60

        # Get season-specific confidence modifiers
        season_mappings = self.rules.mapping_rules.get("season_mappings", {})
        season_rules = season_mappings.get(season, {})
        modifiers = season_rules.get("confidence_modifiers", [])

        # Apply modifiers
        boost = 0
        for modifier in modifiers:
            if "if_avoids" in modifier:
                avoided = submission.colors_avoided
                if any(color in avoided for color in modifier["if_avoids"]):
                    boost += modifier.get("boost", 0)

            if "if_wears" in modifier:
                worn = submission.colors_worn
                if any(color in worn for color in modifier["if_wears"]):
                    boost += modifier.get("boost", 0)

            if "if_prefers" in modifier:
                jewelry = submission.jewelry_preference
                if jewelry in modifier["if_prefers"]:
                    boost += modifier.get("boost", 0)

            if "if_has" in modifier:
                # Check physical characteristics
                has_trait = (
                    submission.hair_color in modifier["if_has"] or
                    submission.skin_tone in modifier["if_has"]
                )
                if has_trait:
                    boost += modifier.get("boost", 0)

        # Calculate final score (boost is already in percentage points, e.g., 0.15 = 15%)
        confidence = int(base_score * (1.0 + boost))

        # Clamp to 0-100
        return max(0, min(100, confidence))


# Global instance
analyzer = SeasonAnalyzer()
