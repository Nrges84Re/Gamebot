import json
from config import VARIABLES_FILE


class VariableManager:
    def __init__(self):
        self.default_variables = self._load_defaults()

    def _load_defaults(self):
        with open(VARIABLES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # اگر فایل به صورت {"security": 50, ...} بود
        if isinstance(data, dict):
            return data

        # اگر فایل ساختار دیگری داشت
        raise ValueError("variables.json must be a JSON object")

    def new_state(self):
        return dict(self.default_variables)

    def get(self, state: dict, name: str, default=0):
        return state.get(name, default)

    def set(self, state: dict, name: str, value):
        state[name] = value

    def increase(self, state: dict, name: str, amount: int):
        state[name] = state.get(name, 0) + amount

    def decrease(self, state: dict, name: str, amount: int):
        state[name] = state.get(name, 0) - amount

    def all(self, state: dict):
        return dict(state)


variable_manager = VariableManager()
