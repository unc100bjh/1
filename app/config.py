import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "")
    WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook/telegram")
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")
    FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

    @property
    def webhook_url(self):
        return f"{self.WEBHOOK_HOST}{self.WEBHOOK_PATH}"
