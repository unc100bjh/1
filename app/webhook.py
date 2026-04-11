import logging
from flask import Blueprint, request, jsonify
from app.config import Config

logger = logging.getLogger(__name__)

webhook_bp = Blueprint("webhook", __name__)
config = Config()


@webhook_bp.route("/webhook/telegram", methods=["POST"])
def telegram_webhook():
    """텔레그램 Webhook 수신 엔드포인트"""
    # Secret Token 검증
    if config.WEBHOOK_SECRET:
        header_secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if header_secret != config.WEBHOOK_SECRET:
            logger.warning("Invalid webhook secret token received")
            return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data"}), 400

    logger.info("Received webhook update: %s", data.get("update_id"))

    # 메시지 처리
    if "message" in data:
        _handle_message(data["message"])
    elif "callback_query" in data:
        _handle_callback_query(data["callback_query"])

    return jsonify({"ok": True})


@webhook_bp.route("/health", methods=["GET"])
def health_check():
    """헬스 체크 엔드포인트"""
    return jsonify({"status": "ok"})


def _handle_message(message: dict):
    """수신된 메시지 처리"""
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")
    user = message.get("from", {})
    username = user.get("username", user.get("first_name", "Unknown"))

    logger.info("Message from %s (chat_id: %s): %s", username, chat_id, text)

    # /start 명령어 처리
    if text == "/start":
        from app.telegram_client import TelegramClient

        client = TelegramClient(config.TELEGRAM_BOT_TOKEN)
        client.send_message(
            chat_id=str(chat_id),
            text=(
                f"안녕하세요, {username}님!\n\n"
                f"이 봇이 연결되었습니다.\n"
                f"당신의 Chat ID: <code>{chat_id}</code>\n\n"
                "이 Chat ID를 .env 파일의 TELEGRAM_CHAT_ID에 설정해주세요."
            ),
        )

    # /chatid 명령어 처리
    elif text == "/chatid":
        from app.telegram_client import TelegramClient

        client = TelegramClient(config.TELEGRAM_BOT_TOKEN)
        client.send_message(
            chat_id=str(chat_id),
            text=f"Chat ID: <code>{chat_id}</code>",
        )


def _handle_callback_query(callback_query: dict):
    """콜백 쿼리 처리"""
    callback_data = callback_query.get("data", "")
    logger.info("Callback query: %s", callback_data)
