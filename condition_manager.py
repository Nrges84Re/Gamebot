import json
from config import CONDITIONS_FILE


class ConditionManager:
    def __init__(self):
        with open(CONDITIONS_FILE, "r", encoding="utf-8") as file:
            self.conditions = json.load(file)

    def check(self, state):
        # پشتیبانی از هر دو حالت dict و list
        if isinstance(self.conditions, dict):
            conditions_iter = self.conditions.values()
        elif isinstance(self.conditions, list):
            conditions_iter = self.conditions
        else:
            return None

        for condition in conditions_iter:
            # سازگاری با typoهای JSON فعلی
            variable = condition.get("variable", condition.get("vriable"))
            operator = condition.get("operator")
            value = condition.get("value")
            ending = condition.get("ending", condition.get("endind "))

            if variable is None or operator is None or value is None or ending is None:
                continue

            current = state.get(variable)
            if current is None:
                continue

            if operator == "<=" and current <= value:
                return ending
            if operator == ">=" and current >= value:
                return ending
            if operator == "==" and current == value:
                return ending
            if operator == "<" and current < value:
                return ending
            if operator == ">" and current > value:
                return ending

        return None


condition_manager = ConditionManager()
