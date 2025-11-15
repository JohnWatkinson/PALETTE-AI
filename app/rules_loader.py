import yaml
from pathlib import Path
from typing import Dict, Any


class RulesLoader:
    """Loads and provides access to YAML rule files"""

    def __init__(self):
        self.rules_dir = Path(__file__).parent.parent / "rules"
        self._questionnaire = None
        self._seasons = None
        self._mapping_rules = None

    @property
    def questionnaire(self) -> Dict[str, Any]:
        """Load questionnaire rules"""
        if self._questionnaire is None:
            with open(self.rules_dir / "questionnaire.yaml", "r") as f:
                self._questionnaire = yaml.safe_load(f)
        return self._questionnaire

    @property
    def seasons(self) -> Dict[str, Any]:
        """Load season definitions with palettes"""
        if self._seasons is None:
            with open(self.rules_dir / "seasons.yaml", "r") as f:
                self._seasons = yaml.safe_load(f)
        return self._seasons

    @property
    def mapping_rules(self) -> Dict[str, Any]:
        """Load season mapping rules"""
        if self._mapping_rules is None:
            with open(self.rules_dir / "mapping-rules.yaml", "r") as f:
                self._mapping_rules = yaml.safe_load(f)
        return self._mapping_rules

    def get_question_signals(self, question_id: str, answer_id: str) -> Dict[str, Any]:
        """Get signals for a specific answer"""
        questions = self.questionnaire.get("questions", {})

        for q_key, q_data in questions.items():
            if q_data.get("id") == question_id:
                for option in q_data.get("options", []):
                    if option.get("id") == answer_id:
                        return option.get("signals", {})

        return {}

    def get_season_palette(self, season_key: str) -> Dict[str, Any]:
        """Get palette for a specific season"""
        seasons = self.seasons.get("seasons", {})
        return seasons.get(season_key, {})


# Global instance
rules = RulesLoader()
