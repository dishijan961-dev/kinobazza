import os
import re
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_IDS = {int(x) for x in re.findall(r"\d+", os.getenv("ADMIN_IDS", ""))}
BASE_URL = (os.getenv("BASE_URL") or os.getenv("RENDER_EXTERNAL_URL") or "").strip().rstrip("/")

if not BOT_TOKEN or ":" not in BOT_TOKEN:
    raise SystemExit("XATO: .env faylida BOT_TOKEN to'g'ri yozilmagan.")

DATA_DIR = Path(os.getenv("DATA_DIR") or BASE_DIR / "data")
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR") or BASE_DIR / "uploads")
STATIC_DIR = BASE_DIR / "static"
DB_PATH = DATA_DIR / "kinobot.db"

# Kerakli papkalar o'zi yaratiladi
for p in (DATA_DIR, UPLOAD_DIR / "videos", UPLOAD_DIR / "posters", UPLOAD_DIR / "banners"):
    p.mkdir(parents=True, exist_ok=True)

# Telegram bot orqali yuborish mumkin bo'lgan eng katta fayl (50 MB dan biroz kam)
MAX_BOT_FILE = 49 * 1024 * 1024
