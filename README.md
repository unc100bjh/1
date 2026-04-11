# Telegram Webhook Integration

Python(Flask) 기반 텔레그램 Webhook 연동 서버입니다.

## 기능

- 텔레그램 Webhook 수신 및 메시지 처리
- 텔레그램 알림 전송 (텍스트, 알림, 배포, 에러)
- Secret Token 기반 Webhook 보안 검증
- 헬스 체크 엔드포인트

## Bot Token 발급 방법

1. 텔레그램에서 **@BotFather** 를 검색하여 대화를 시작합니다
2. `/newbot` 명령어를 입력합니다
3. 봇 이름(표시 이름)을 입력합니다 (예: `My Notification Bot`)
4. 봇 username을 입력합니다 (예: `my_noti_bot` - 반드시 `bot`으로 끝나야 함)
5. 발급된 토큰을 복사합니다 (형식: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## 설치 및 실행

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 TELEGRAM_BOT_TOKEN 등을 설정합니다

# 3. 서버 실행
python run.py
```

## Chat ID 확인 방법

1. 서버를 실행하고 Webhook을 설정합니다
2. 텔레그램에서 봇에게 `/start` 또는 `/chatid` 명령을 보냅니다
3. 봇이 응답하는 Chat ID를 `.env` 파일의 `TELEGRAM_CHAT_ID`에 설정합니다

## 알림 전송 사용 예시

```python
from app.notifier import TelegramNotifier

notifier = TelegramNotifier()

# 일반 텍스트 전송
notifier.send_text("서버가 시작되었습니다.")

# 포맷된 알림 전송
notifier.send_alert("서버 상태", "CPU 사용률 90% 초과", level="WARNING")

# 배포 알림
notifier.send_deploy_notification("api-server", "v1.2.3", "success")

# 에러 알림
notifier.send_error_notification("DatabaseError", "Connection refused", source="user-service")
```

## 환경 변수

| 변수 | 설명 | 필수 |
|------|------|------|
| `TELEGRAM_BOT_TOKEN` | BotFather에서 발급받은 봇 토큰 | O |
| `WEBHOOK_HOST` | Webhook 수신 서버 도메인 (https) | O |
| `WEBHOOK_PATH` | Webhook 경로 (기본: `/webhook/telegram`) | X |
| `WEBHOOK_SECRET` | Webhook 보안 Secret Token | X |
| `TELEGRAM_CHAT_ID` | 알림 수신 Chat ID | O |
| `FLASK_HOST` | 서버 호스트 (기본: `0.0.0.0`) | X |
| `FLASK_PORT` | 서버 포트 (기본: `5000`) | X |

## 프로덕션 배포

```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```
