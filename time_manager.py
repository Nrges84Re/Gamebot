from engine.variable_manager import variable_manager



class TimeManager:
    def decrease_time(self, state: dict, amount: int = 1):
        state["time"] = max(0, state.get("time", 0) - amount)
        return state["time"]


time_manager = TimeManager()
