import json
from config import CHOICES_FILE


class ChoiceManager:
    def __init__(self):
        self.choices = self._load()

    def _load(self):
        with open(CHOICES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_choice(self, choice_id: str):
        return self.choices.get(choice_id)

    def all(self):
        return self.choices


choice_manager = ChoiceManager()
