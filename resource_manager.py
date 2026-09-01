from engine.variable_manager import variable_manager



class ResourceManager:
    def get_resources(self, state: dict):
        return {
            "budget": state.get("budget", 0),
            "military": state.get("military", 0),
            "intelligence": state.get("intelligence", 0),
            "international_support": state.get("international_support", 0),
            "time": state.get("time", 0),
        }


resource_manager = ResourceManager()
