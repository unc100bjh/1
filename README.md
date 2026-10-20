# iPhone 해킹차단 보안관리 체계 (iSEC-OPS)

> 대상: 경영진·소송 당사자 등 **고가치 표적(High-Value Target)** iPhone 사용자
> 기준: iOS 26 / 2026-10 · 실행 단위: 1회 하드닝(30분) + 자동화 루틴(일·주·월)

---

## 1. 구조 (Vision → Strategy → Tactics → Execution → KPI)

| 단계 | 정의 |
|---|---|
| **Vision** | 기기·계정·통신 3계층 모두에서 "침투 불가 + 침투 시 즉시 탐지·복구" 상태 상시 유지 |
| **Strategy** | ① 공격면 축소 ② 계정 탈취 차단 ③ 통신(SIM) 탈취 차단 ④ 정기 탐지 ⑤ 사고 대응 표준화 |
| **Tactics** | L1 필수(전원) / L2 강화(경영진) / L3 최고(소송·분쟁 당사자: Lockdown Mode) |
| **Execution** | 체크리스트 1회 적용 → 단축어 자동화 상시 → 월 1회 MVT 포렌식 점검 |
| **KPI** | 하드닝 점수 ≥ 90% · 패치 지연 ≤ 72h · 미확인 프로파일 0 · 월 점검 이행률 100% |

## 2. 위협 모델 → 통제 매핑

| 위협 | 경로 | 핵심 통제 | 문서 |
|---|---|---|---|
| 제로클릭 스파이웨어 (Pegasus·Predator 계열) | iMessage·FaceTime·웹 | 즉시 업데이트, Lockdown Mode, 일일 재부팅 | [체크리스트](docs/hardening-checklist.md) |
| Apple 계정 탈취 | 피싱, 비밀번호 재사용 | 보안키, 복구키, 도난 기기 보호 | 〃 |
| SIM 스와핑 / 유심 복제 | 통신사 사회공학 | SIM PIN, 유심보호서비스, 명의도용방지 | 〃 |
| 악성 프로파일 / MDM | 링크 유도 설치 | VPN 및 기기 관리 점검 (프로파일 0) | 〃 |
| 물리 접근 (분실·압수·탈취) | 잠금 화면, USB | 6자리 이상 암호, USB 액세서리 차단, 10회 실패 시 초기화 | 〃 |
| 스토커웨어 / 공유 남용 | 위치·계정 공유 | 안전 확인(Safety Check) | 〃 |

## 3. 산출물

| 경로 | 용도 |
|---|---|
| [`docs/hardening-checklist.md`](docs/hardening-checklist.md) | L1~L3 하드닝 체크리스트 (설정 경로 포함) |
| [`docs/shortcuts-automation.md`](docs/shortcuts-automation.md) | iOS 단축어 자동화 레시피 (일·주·월 루틴) |
| [`docs/incident-response.md`](docs/incident-response.md) | 해킹 의심 시 대응 런북 (0~24h) |
| [`scripts/mvt_scan.sh`](scripts/mvt_scan.sh) | MVT(Amnesty) 기반 스파이웨어 흔적 포렌식 자동 점검 |
| [`dashboard/index.html`](dashboard/index.html) | 하드닝 점수 자가진단 대시보드 (모바일 대응) |

## 4. 실행 순서

- [ ] **D0 (30분)** — 대시보드 열고 L1 → L2 → (해당 시) L3 순서로 적용, 점수 90% 이상 확보
- [ ] **D0 (10분)** — 통신사 유심보호서비스 + 명의도용방지(msafer.or.kr) 가입
- [ ] **D1 (15분)** — 단축어 자동화 3종 설치 (일일 재부팅 알림·주간 점검·공용 Wi-Fi VPN)
- [ ] **D7** — PC에서 `scripts/mvt_scan.sh` 최초 실행, 기준선(baseline) 확보
- [ ] **매월 1일** — MVT 재점검 + 대시보드 점수 재측정

## 5. 한계 (명시)

- iOS 샌드박스 구조상 **제3자 앱·클라우드가 iPhone 설정을 원격 강제 변경하는 것은 불가**. 본 체계는 "1회 수동 하드닝 + 단축어로 가능한 범위 자동화 + 외부 포렌식"의 조합이다.
- 완전 자동 강제 적용이 필요하면 Apple Business Manager + MDM(감독 모드) 도입이 유일한 경로다 (조직 단위, 별도 과제).
- MVT는 **알려진 IOC 기반** 탐지다. "흔적 없음"이 "감염 없음"을 보장하지 않는다. 고위험 의심 시 전문기관 의뢰.
