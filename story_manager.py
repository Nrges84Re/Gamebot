import json
from config import SCENES_FILE


class StoryManager:
    def __init__(self):
        self.scenes = self._load()

    def _load(self):
        with open(SCENES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_scene(self, scene_id: str):
        return self.scenes.get(scene_id)

    def all(self):
        return self.scenes


story_manager = StoryManager()
