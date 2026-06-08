import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL: str = "gemini-2.5-flash-lite"
MAX_HISTORY_MESSAGES: int = 10

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не задан в .env файле!")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY не задан в .env файле!")
