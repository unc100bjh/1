import logging
import requests

logger = logging.getLogger(__name__)

TELEGRAM_API_BASE = "https://api.telegram.org/bot{token}"


class TelegramClient:
    """텔레그램 Bot API 클라이언트"""

    def __init__(self, token: str):
        self.token = token
        self.base_url = TELEGRAM_API_BASE.format(token=token)

    def _request(self, method: str, **kwargs) -> dict:
        url = f"{self.base_url}/{method}"
        try:
            response = requests.post(url, json=kwargs, timeout=10)
            response.raise_for_status()
            data = response.json()
            if not data.get("ok"):
                logger.error("Telegram API error: %s", data.get("description"))
            return data
        except requests.RequestException as e:
            logger.error("Telegram request failed: %s", e)
            return {"ok": False, "description": str(e)}

    def send_message(self, chat_id: str, text: str, parse_mode: str = "HTML") -> dict:
        """텍스트 메시지 전송"""
        return self._request(
            "sendMessage",
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
        )

    def set_webhook(self, url: str, secret_token: str = None) -> dict:
        """Webhook URL 등록"""
        params = {"url": url}
        if secret_token:
            params["secret_token"] = secret_token
        return self._request("setWebhook", **params)

    def delete_webhook(self) -> dict:
        """Webhook 해제"""
        return self._request("deleteWebhook")

    def get_webhook_info(self) -> dict:
        """현재 Webhook 정보 조회"""
        url = f"{self.base_url}/getWebhookInfo"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error("Failed to get webhook info: %s", e)
            return {"ok": False, "description": str(e)}

    def get_me(self) -> dict:
        """봇 정보 조회 (토큰 유효성 확인용)"""
        url = f"{self.base_url}/getMe"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error("Failed to get bot info: %s", e)
            return {"ok": False, "description": str(e)}
