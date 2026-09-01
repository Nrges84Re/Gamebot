from database.database import init_db
from engine.game_engine import game_engine


def main():
    init_db()

    user_id = 1
    response = game_engine.start(user_id)

    while True:
        print("\n" + "=" * 40)
        print(response["text"])

        if response["type"] in ("ending", "game_over", "error"):
            break

        for i, btn in enumerate(response["buttons"], start=1):
            print(f"{i}. {btn}")

        user_input = input("\nشماره انتخاب (یا restart / exit): ").strip().lower()

        if user_input == "exit":
            break
        if user_input == "restart":
            response = game_engine.restart(user_id)
            continue
        if not user_input.isdigit():
            print("ورودی نامعتبر.")
            continue

        response = game_engine.choose(user_id, int(user_input))


if __name__ == "__main__":
    main()
