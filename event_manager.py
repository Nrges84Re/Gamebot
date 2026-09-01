import json
from config import EVENTS_FILE


class EventManager:
    def __init__(self):
        self.events = self._load()

    def _load(self):
        with open(EVENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def apply(self, state: dict, event_id: str):
        if not event_id:
            return state

        event = self.events.get(event_id)
        if not event:
            return state

        # اگر events.json به شکل {"effects": {...}} بود
        effects = event.get("effects", event)

        for key, delta in effects.items():
            if isinstance(delta, (int, float)):
                state[key] = state.get(key, 0) + delta

        return state


event_manager = EventManager()
