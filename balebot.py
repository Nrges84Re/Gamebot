import os
import sys
import time
import requests

# =========================================
# دسترسی به پوشه اصلی پروژه
# =========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

print("BASE_DIR:", BASE_DIR)
print("PYTHON PATH:", sys.path)

# =========================================
# تنظیمات
# =========================================

from dotenv import load_dotenv
from engine.game_engine import game_engine

load_dotenv(
    os.path.join(BASE_DIR, ".env"),
    override=True
)

TOKEN = os.getenv("BALE_BOT_TOKEN")

if not TOKEN:
    raise ValueError(
        "BALE_BOT_TOKEN در فایل .env پیدا نشد."
    )

BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}"


# =========================================
# ارسال پیام
# =========================================

def send_message(chat_id, text, reply_markup=None):

    url = f"{BASE_URL}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:

        response = requests.post(
            url,
            json=payload,
            timeout=15
        )

        print("SEND:", response.status_code)

        result = response.json()

        print("SEND RESULT:", result)

        return result

    except Exception as e:

        print("Error sending message:", e)

        return None


# =========================================
# ساخت کیبورد
# =========================================

def build_keyboard(response):

    if not response:
        return None

    # -------------------------------------
    # پایان بازی
    # -------------------------------------

    if response.get("type") == "game_over":

        return {
            "inline_keyboard": [
                [
                    {
                        "text": "🔄 شروع بازی جدید",
                        "callback_data": "restart_game"
                    }
                ]
            ]
        }

    # -------------------------------------
    # پایان با type=ending
    # -------------------------------------

    if response.get("type") == "ending":

        return {
            "inline_keyboard": [
                [
                    {
                        "text": "🔄 شروع بازی جدید",
                        "callback_data": "restart_game"
                    }
                ]
            ]
        }

    # -------------------------------------
    # انتخاب‌های معمول بازی
    # -------------------------------------

    choices = response.get("buttons", [])

    keyboard = []

    for i, choice in enumerate(choices, start=1):

        keyboard.append(
            [
                {
                    "text": choice,
                    "callback_data": str(i)
                }
            ]
        )

    if not keyboard:
        return None

    return {
        "inline_keyboard": keyboard
    }


# =========================================
# نمایش صحنه
# =========================================

def send_scene(chat_id, response):

    if not response:

        send_message(
            chat_id,
            "❌ خطایی رخ داد.\n\nلطفاً /restart را بزنید."
        )

        return

    text = response.get("text", "")

    keyboard = build_keyboard(response)

    reply_markup = keyboard if keyboard else None

    print()
    print("===== SEND SCENE =====")
    print("RESPONSE:", response)
    print("TEXT:", text)
    print("KEYBOARD:", reply_markup)

    # مهم:
    # فقط یک بار ارسال پیام

    result = send_message(
        chat_id,
        text,
        reply_markup
    )

    print("SEND RESULT:", result)

    print("======================")
    print()


# =========================================
# پردازش آپدیت
# =========================================

def process_update(update):

    print("UPDATE:", update)

    # =====================================
    # پیام معمولی
    # =====================================

    message = update.get("message")

    if message:

        chat = message.get("chat", {})
        chat_id = chat.get("id")

        text = message.get("text", "").strip().lower()

        if not chat_id:
            return

        # ---------------------------------
        # شروع بازی
        # ---------------------------------

        if text == "/start":

            print(f"Starting game for user {chat_id}")

            # /start = شروع بازی از ابتدا
            response = game_engine.restart(chat_id)

            send_scene(
                chat_id,
                response
            )

            return

        # ---------------------------------
        # شروع مجدد
        # ---------------------------------

        if text == "/restart":

            print(f"Restarting game for user {chat_id}")

            response = game_engine.restart(chat_id)

            send_scene(
                chat_id,
                response
            )

            return

        # ---------------------------------
        # خروج
        # ---------------------------------

        if text == "/exit":

            print(f"User {chat_id} exited the game")

            send_message(
                chat_id,
                "👋 از بازی خارج شدید.\n\n"
                "برای شروع دوباره /start را بزنید."
            )

            return

        # ---------------------------------
        # راهنما
        # ---------------------------------

        if text == "/help":

            send_message(
                chat_id,
                "🎮 راهنمای بازی اتاق بحران\n\n"
                "/start - شروع بازی\n"
                "/restart - شروع مجدد بازی\n"
                "/exit - خروج از بازی\n"
                "/help - راهنما"
            )

            return

        # ---------------------------------
        # دستور نامعتبر
        # ---------------------------------

        send_message(
            chat_id,
            "❌ دستور نامعتبر است.\n\n"
            "دستورات موجود:\n"
            "/start - شروع بازی\n"
            "/restart - شروع مجدد بازی\n"
            "/exit - خروج از بازی\n"
            "/help - راهنما"
        )

        return

    # =====================================
    # callback دکمه‌ها
    # =====================================

    callback = update.get("callback_query")

    if callback:

        callback_data = callback.get("data")

        user = callback.get("from", {})

        chat_id = user.get("id")

        if not callback_data or not chat_id:
            return

        print(
            f"Callback received from user {chat_id}: "
            f"{callback_data}"
        )

        # =================================
        # شروع بازی جدید از دکمه پایان
        # =================================

        if callback_data == "restart_game":

            print(
                f"Restarting game from button "
                f"for user {chat_id}"
            )

            response = game_engine.restart(chat_id)

            print("RESTART RESULT:", response)

            send_scene(
                chat_id,
                response
            )

            return

        # =================================
        # انتخاب معمول بازی
        # =================================

        try:

            choice_number = int(callback_data)

        except (ValueError, TypeError):

            print(
                "Invalid callback data:",
                callback_data
            )

            return

        print(
            f"User {chat_id} selected "
            f"{choice_number}"
        )

        response = game_engine.choose(
            chat_id,
            choice_number
        )

        print(
            "CHOOSE RESULT:",
            response
        )

        # ---------------------------------
        # نمایش نتیجه / صحنه بعد
        # ---------------------------------

        send_scene(
            chat_id,
            response
        )

        return


# =========================================
# دریافت آپدیت‌ها
# =========================================

def get_updates(offset=None):

    url = f"{BASE_URL}/getUpdates"

    params = {
        "timeout": 30
    }

    if offset is not None:
        params["offset"] = offset

    try:

        response = requests.get(
            url,
            params=params,
            timeout=40
        )

        print(
            "GET UPDATES:",
            response.status_code
        )

        return response.json()

    except Exception as e:

        print(
            "Error getting updates:",
            e
        )

        return None


# =========================================
# اجرای ربات
# =========================================

def main():

    print("================================")
    print("🤖 Bale Bot")
    print("ربات بله در حال اجراست...")
    print("================================")

    offset = None

    while True:

        try:

            data = get_updates(offset)

            if not data:
                continue

            if not data.get("ok"):
                print("GET UPDATES ERROR:", data)
                continue

            updates = data.get("result", [])

            for update in updates:

                update_id = update.get("update_id")

                # ---------------------------------
                # پردازش آپدیت
                # ---------------------------------

                process_update(update)

                # ---------------------------------
                # جلوگیری از دریافت دوباره
                # ---------------------------------

                if update_id is not None:

                    offset = update_id + 1

        except KeyboardInterrupt:

            print()
            print("Bot stopped.")

            break

        except Exception as e:

            print(
                "MAIN LOOP ERROR:",
                e
            )


# =========================================
# شروع برنامه
# =========================================

if __name__ == "__main__":
    main()
