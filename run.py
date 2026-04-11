#!/usr/bin/env python3
"""텔레그램 Webhook 서버 실행"""
from app.config import Config
from app.server import create_app, setup_webhook

config = Config()
app = create_app()

if __name__ == "__main__":
    setup_webhook()
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG,
    )
