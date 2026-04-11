import logging
from flask import Flask
from app.config import Config
from app.webhook import webhook_bp
from app.telegram_client import TelegramClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Flask 앱 생성 및 설정"""
    app = Flask(__name__)
    app.register_blueprint(webhook_bp)
    return app


def setup_webhook():
    """텔레그램 Webhook 등록"""
    config = Config()
    if not config.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN이 설정되지 않았습니다.")
        return False

    client = TelegramClient(config.TELEGRAM_BOT_TOKEN)

    # 봇 정보 확인
    bot_info = client.get_me()
    if bot_info.get("ok"):
        bot_name = bot_info["result"]["username"]
        logger.info("Bot 연결 성공: @%s", bot_name)
    else:
        logger.error("Bot 토큰이 유효하지 않습니다.")
        return False

    # Webhook 등록
    if config.WEBHOOK_HOST:
        result = client.set_webhook(
            url=config.webhook_url,
            secret_token=config.WEBHOOK_SECRET or None,
        )
        if result.get("ok"):
            logger.info("Webhook 등록 완료: %s", config.webhook_url)
        else:
            logger.error("Webhook 등록 실패: %s", result.get("description"))
            return False

    return True
