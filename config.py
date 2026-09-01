import os
from dotenv import load_dotenv

# بارگذاری فایل .env
load_dotenv()

# مسیر اصلی پروژه
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# مسیر پوشه‌ها
DATABASE_DIR = os.path.join(BASE_DIR, "database")
GAME_DATA_DIR = os.path.join(BASE_DIR, "game_data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# مسیر دیتابیس
DATABASE_FILE = os.path.join(
    DATABASE_DIR,
    "crisis_room.db"
)

# مسیر فایل‌های بازی
SCENES_FILE = os.path.join(
    GAME_DATA_DIR,
    "scenes.json"
)

CHOICES_FILE = os.path.join(
    GAME_DATA_DIR,
    "choices.json"
)

EVENTS_FILE = os.path.join(
    GAME_DATA_DIR,
    "events.json"
)

CONDITIONS_FILE = os.path.join(
    GAME_DATA_DIR,
    "conditions.json"
)

ENDINGS_FILE = os.path.join(
    GAME_DATA_DIR,
    "endings.json"
)

VARIABLES_FILE = os.path.join(
    GAME_DATA_DIR,
    "variables.json"
)

# فایل ذخیره قدیمی - در صورت نیاز
SAVE_FILE = os.path.join(
    BASE_DIR,
    "savegame.json"
)

# صحنه شروع بازی
INITIAL_SCENE_ID = "scene_001"

# =========================
# توکن ربات‌ها
# =========================

TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN",
    ""
)

BALE_BOT_TOKEN = os.getenv(
    "BALE_BOT_TOKEN",
    ""
)
