from game_engine_final import GameEngine


class RenPyBridge:

    def __init__(self):
        self.engine = GameEngine()

    def get_status(self):
        return self.engine.get_status()

    def get_state(self):
        return self.engine.get_status().copy()

    def load_state(self, state):

        required_keys = [
            "security",
            "public_trust",
            "enemy_influence",
            "stability",
            "casualties",
            "budget",
            "military",
            "time_left",
        ]

        for key in required_keys:
            if key not in state:
                raise ValueError(f"Missing state value: {key}")

        self.engine.security = state["security"]
        self.engine.public_trust = state["public_trust"]
        self.engine.enemy_influence = state["enemy_influence"]
        self.engine.stability = state["stability"]
        self.engine.casualties = state["casualties"]
        self.engine.budget = state["budget"]
        self.engine.military = state["military"]
        self.engine.time_left = state["time_left"]

        self.engine.clamp()

        return self.get_status()

    def apply_decision(self, decision):

        decision_map = {
            "choice_1": "alert",
            "choice_2": "intelligence",
            "choice_3": "ignore",

            "choice_4": "cyber",
            "choice_5": "border",
            "choice_6": "arrest",

            "choice_7": "committee",
            "choice_8": "military",
            "choice_9": "preemptive",

            "choice_10": "aggressive",
            "choice_11": "defensive",
            "choice_12": "deception",
        }

        real_decision = decision_map.get(decision)

        if real_decision is None:
            raise ValueError(
                f"Unknown decision: {decision}"
            )

        self.engine.apply_decision(real_decision)

        return self.get_status()

    def get_result(self):
        return self.engine.get_result()

    def reset(self):
        self.engine.reset()
        return self.get_status()


if __name__ == "__main__":

    bridge = RenPyBridge()

    print("RenPyBridge started successfully.")

    print("Initial Status:")
    print(bridge.get_status())

    print()
    print("Applying test decision: choice_1")

    result = bridge.apply_decision("choice_1")

    print()
    print("Updated Status:")
    print(result)

    print()
    print("Final Result:")
    print(bridge.get_result())