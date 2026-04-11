import logging
from app.config import Config
from app.telegram_client import TelegramClient

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """외부 이벤트를 텔레그램으로 알림 전송하는 모듈"""

    def __init__(self, token: str = None, chat_id: str = None):
        config = Config()
        self.token = token or config.TELEGRAM_BOT_TOKEN
        self.chat_id = chat_id or config.TELEGRAM_CHAT_ID
        self.client = TelegramClient(self.token)

    def send_text(self, text: str, chat_id: str = None) -> dict:
        """일반 텍스트 알림 전송"""
        target = chat_id or self.chat_id
        return self.client.send_message(chat_id=target, text=text)

    def send_alert(self, title: str, message: str, level: str = "INFO", chat_id: str = None) -> dict:
        """포맷된 알림 전송"""
        level_icons = {
            "INFO": "ℹ️",
            "WARNING": "⚠️",
            "ERROR": "🚨",
            "SUCCESS": "✅",
        }
        icon = level_icons.get(level.upper(), "📌")
        text = f"{icon} <b>{title}</b>\n\n{message}"
        target = chat_id or self.chat_id
        return self.client.send_message(chat_id=target, text=text)

    def send_deploy_notification(self, service: str, version: str, status: str, chat_id: str = None) -> dict:
        """배포 알림 전송"""
        status_icon = "✅" if status == "success" else "❌"
        text = (
            f"{status_icon} <b>배포 알림</b>\n\n"
            f"서비스: <code>{service}</code>\n"
            f"버전: <code>{version}</code>\n"
            f"상태: {status}"
        )
        target = chat_id or self.chat_id
        return self.client.send_message(chat_id=target, text=text)

    def send_error_notification(self, error_type: str, error_message: str, source: str = "", chat_id: str = None) -> dict:
        """에러 알림 전송"""
        text = (
            f"🚨 <b>에러 발생</b>\n\n"
            f"유형: <code>{error_type}</code>\n"
            f"메시지: {error_message}"
        )
        if source:
            text += f"\n출처: <code>{source}</code>"
        target = chat_id or self.chat_id
        return self.client.send_message(chat_id=target, text=text)
