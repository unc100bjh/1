#!/usr/bin/env bash
# iPhone 스파이웨어 흔적 점검 (MVT: Amnesty Mobile Verification Toolkit)
# 실행 환경: macOS / Linux / Windows WSL  ·  iPhone USB 연결 + "이 컴퓨터 신뢰" 승인
#
# 사용법:
#   ./scripts/mvt_scan.sh                # 백업 → 복호화 → IOC 점검 전체
#   ./scripts/mvt_scan.sh --backup-only  # 증거 보존용 암호화 백업만 생성
#
# 필요 패키지: python3, pip, libimobiledevice (idevice_id, idevicebackup2)
#   macOS: brew install libimobiledevice
#   Ubuntu/WSL: sudo apt install libimobiledevice-utils
set -euo pipefail

WORK_DIR="${MVT_WORK_DIR:-$HOME/mvt-work}"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$WORK_DIR/backup"
DECRYPT_DIR="$WORK_DIR/decrypted-$STAMP"
RESULT_DIR="$WORK_DIR/mvt-results/$STAMP"
BACKUP_ONLY=0
[[ "${1:-}" == "--backup-only" ]] && BACKUP_ONLY=1

log() { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*"; }
die() { log "ERROR: $*"; exit 1; }

for cmd in python3 idevice_id idevicebackup2; do
  command -v "$cmd" >/dev/null || die "$cmd 미설치 (스크립트 상단 '필요 패키지' 참조)"
done

if ! command -v mvt-ios >/dev/null; then
  log "MVT 설치"
  python3 -m pip install --user --upgrade mvt
  export PATH="$HOME/.local/bin:$PATH"
fi

UDID="$(idevice_id -l | head -n1)"
[[ -n "$UDID" ]] || die "iPhone 미연결 또는 신뢰 미승인"
log "기기 연결: $UDID"

mkdir -p "$BACKUP_DIR" "$RESULT_DIR"
chmod 700 "$WORK_DIR"

# 암호화 백업이어야 통화기록·Safari·건강 등 핵심 아티팩트가 포함된다
if [[ -z "${MVT_IOS_BACKUP_PASSWORD:-}" ]]; then
  read -rsp "백업 암호 (기존 암호화 백업 암호 또는 신규 설정값): " MVT_IOS_BACKUP_PASSWORD; echo
  export MVT_IOS_BACKUP_PASSWORD
fi
log "백업 암호화 활성화 확인 (이미 켜져 있으면 오류 메시지는 무시)"
idevicebackup2 -u "$UDID" encryption on "$MVT_IOS_BACKUP_PASSWORD" || true

log "전체 백업 시작 (iPhone에서 암호 입력 요구 시 승인)"
idevicebackup2 -u "$UDID" backup --full "$BACKUP_DIR"
log "백업 완료: $BACKUP_DIR/$UDID"

if (( BACKUP_ONLY )); then
  log "증거 보존 백업만 생성하고 종료"
  exit 0
fi

log "최신 IOC(침해지표) 다운로드"
mvt-ios download-iocs

log "백업 복호화"
mvt-ios decrypt-backup -d "$DECRYPT_DIR" "$BACKUP_DIR/$UDID"

log "IOC 점검 실행"
mvt-ios check-backup --output "$RESULT_DIR" "$DECRYPT_DIR"

# 복호화본은 민감 데이터 원문이므로 점검 직후 삭제 (암호화 백업 원본은 보존)
rm -rf "$DECRYPT_DIR"

DETECTED="$(find "$RESULT_DIR" -name '*_detected.json' | wc -l | tr -d ' ')"
echo
echo "================ MVT 점검 결과 ================"
echo " 일시      : $STAMP"
echo " 결과 폴더 : $RESULT_DIR"
if [[ "$DETECTED" == "0" ]]; then
  echo " 판정      : GREEN — 알려진 IOC 탐지 없음"
  echo " 주의      : 미탐지 = 감염 없음 보장 아님 (알려진 지표 기준)"
else
  echo " 판정      : RED — IOC 탐지 파일 ${DETECTED}건"
  find "$RESULT_DIR" -name '*_detected.json' -printf '   - %f\n' 2>/dev/null \
    || find "$RESULT_DIR" -name '*_detected.json'
  echo " 조치      : docs/incident-response.md 3단계 즉시 실행, 백업·결과 원본 보존"
fi
echo "==============================================="
