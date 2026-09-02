# ============================================================
# GameProjectRenPy
# game_engine.py
# موتور ساده مدیریت بحران
# ============================================================

class GameEngine:

    def __init__(self):
        self.reset()

    def reset(self):
        self.security = 50
        self.public_trust = 50
        self.enemy_influence = 50
        self.stability = 50
        self.casualties = 0
        self.budget = 100
        self.military = 100
        self.time_left = 24

    def clamp(self):
        self.security = max(0, min(100, self.security))
        self.public_trust = max(0, min(100, self.public_trust))
        self.enemy_influence = max(0, min(100, self.enemy_influence))
        self.stability = max(0, min(100, self.stability))
        self.casualties = max(0, self.casualties)
        self.budget = max(0, min(100, self.budget))
        self.military = max(0, min(100, self.military))
        self.time_left = max(0, self.time_left)

    def apply_decision(self, decision):
        if decision == "alert":
            self.security += 10
            self.public_trust -= 5
            self.enemy_influence -= 5
            self.stability += 2
            self.budget -= 5
            self.military -= 2
            self.time_left -= 1

        elif decision == "intelligence":
            self.security += 3
            self.public_trust += 2
            self.enemy_influence -= 8
            self.stability += 1
            self.budget -= 3
            self.time_left -= 1

        elif decision == "ignore":
            self.security -= 8
            self.public_trust += 1
            self.enemy_influence += 10
            self.stability -= 3
            self.time_left -= 1

        elif decision == "cyber":
            self.security += 8
            self.public_trust += 1
            self.enemy_influence -= 12
            self.stability += 4
            self.budget -= 8
            self.military -= 2
            self.time_left -= 2

        elif decision == "border":
            self.security += 6
            self.public_trust -= 2
            self.enemy_influence -= 5
            self.stability += 2
            self.budget -= 6
            self.military -= 5
            self.time_left -= 2

        elif decision == "arrest":
            self.security += 7
            self.public_trust -= 6
            self.enemy_influence -= 4
            self.stability -= 2
            self.budget -= 3
            self.military -= 1
            self.time_left -= 1

        elif decision == "committee":
            self.security += 3
            self.public_trust += 6
            self.enemy_influence -= 4
            self.stability += 7
            self.budget -= 4
            self.military -= 2
            self.time_left -= 2

        elif decision == "military":
            self.security += 10
            self.public_trust -= 7
            self.enemy_influence -= 6
            self.stability -= 1
            self.budget -= 8
            self.military -= 8
            self.time_left -= 1

        elif decision == "preemptive":
            self.security += 8
            self.public_trust -= 4
            self.enemy_influence -= 12
            self.stability -= 4
            self.budget -= 12
            self.military -= 12
            self.casualties += 3
            self.time_left -= 2

        elif decision == "aggressive":
            self.security += 12
            self.public_trust -= 8
            self.enemy_influence -= 18
            self.stability -= 3
            self.budget -= 18
            self.military -= 20
            self.casualties += 8
            self.time_left -= 3

        elif decision == "defensive":
            self.security += 8
            self.public_trust += 5
            self.enemy_influence -= 10
            self.stability += 8
            self.budget -= 10
            self.military -= 10
            self.casualties += 2
            self.time_left -= 2

        elif decision == "deception":
            self.security += 4
            self.public_trust += 3
            self.enemy_influence -= 14
            self.stability += 5
            self.budget -= 6
            self.military -= 4
            self.casualties += 1
            self.time_left -= 2

        self.clamp()

    def calculate_score(self):
        score = 0

        score += self.security * 0.25
        score += self.public_trust * 0.20
        score += self.stability * 0.20
        score += self.military * 0.15
        score += self.budget * 0.10
        score += (100 - self.enemy_influence) * 0.10

        score -= self.casualties * 0.20

        return int(max(0, min(100, score)))

    def get_result(self):
        score = self.calculate_score()

        if score >= 80:
            title = "موفقیت کامل"
            description = "بحران با موفقیت مدیریت شد و تهدید اصلی مهار گردید."

        elif score >= 60:
            title = "موفقیت نسبی"
            description = "بحران کنترل شد، اما تصمیم‌های اتخاذشده هزینه‌هایی به همراه داشت."

        elif score >= 40:
            title = "کنترل ناقص بحران"
            description = "بخش‌هایی از بحران کنترل شد، اما تهدید همچنان قابل توجه است."

        else:
            title = "شکست در مدیریت بحران"
            description = "تصمیم‌های اتخاذشده نتوانستند بحران را به شکل مؤثر کنترل کنند."

        return {
            "score": score,
            "title": title,
            "description": description
        }

    def get_status(self):
        return {
            "security": self.security,
            "public_trust": self.public_trust,
            "enemy_influence": self.enemy_influence,
            "stability": self.stability,
            "casualties": self.casualties,
            "budget": self.budget,
            "military": self.military,
            "time_left": self.time_left
        }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    game = GameEngine()

    print("GameEngine started successfully.")

    game.apply_decision("alert")

    print("Status:")
    print(game.get_status())

    print("Result:")
    print(game.get_result())