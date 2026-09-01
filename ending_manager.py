import json
from config import ENDINGS_FILE


class EndingManager:
    def __init__(self):
        self.endings = self._load()

    def _load(self):
        with open(ENDINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_ending(self, ending_id: str):
        return self.endings.get(ending_id)

    def all(self):
        return self.endings


ending_manager = EndingManager()
