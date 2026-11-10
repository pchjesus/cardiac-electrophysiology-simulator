# Cardiac Experience v2 — 사용자 승인 전 전면 재설계 계약

> **상태: 개발 후보 / 사용자 시각 검수 대기 / 운영 반영 금지**
> 기준 저장소 `pchjesus/cardiac-electrophysiology-simulator`; 원본 `main` @ `71cded83e4a445ca681dfaf821efce5b2a3062ac` (2026-11-10). 개발 브랜치 `feat/v2-cardiac-experience-reimagined`.
> **절대 금지:** 사용자 최종 승인 이전 `main` 병합·Pages 운영 배포.

## 문제 정의와 학습 목적

현재 v1.13은 ECG·심장 운동·위거스·상태·자료를 여러 차례 중첩된 패치로 표현해 학습 목적보다 정보량과 카드 구조가 먼저 보인다. 대학 간호학 입문 학습자가 **전기 신호를 관찰 → 심장 수축과 판막 사건 비교 → 간호학적 해석 확인 → 통합 도표 탐구 → 기존 심화/문항 풀이** 흐름을 스스로 발견하도록 새 구성으로 재설계한다. 기존 UI의 격자·색상·카드 위계와 위치는 보존 대상이 아니다.

## 본 설계에서 선택한 화면 (후보, 사용자 승인 전)

- **통합 브랜딩:** Light study canvas + deep navy physiological observation field + teal state feedback. RAAS v7.1의 인과적 정보 위계와 원본 노드 재사용만 참고하고 페이지 레이아웃·그래픽은 독자적으로 설계.
- **시뮬레이터:** 교육 목적/행동을 알려주는 소형 머리말 → **심전도 파형(원본 ECG Canvas) → 단일 원본 Play/Pause/Reset + Timeline + HR 조작 레일 → 좌측 선택 시각화(전기 전도/수축·판막/Wiggers)와 우측 동기화 생리·간호 해설 → 원본 6개 ECG 측정값과 모델 한계·출처**.
- **학습:** 독립 6단원 읽기 작업대(기존 Course의 교육/간호/한계 원문을 사용), 선택 주제에 한해서 원본 Guided 5단계·10문항 표시. 수업 모드·완료 표시·복귀 맥락은 원본 state만 사용.
- **임상:** 개발 QA 플래그 `?v113Preview=1`와 기존 `publicReady` 게이트를 유지한 채 기존 가상 사례 UI를 간호 상황/근거/판단의 넓은 읽기형 작업대로 표현. 신규 임상 데이터/정답 생성 금지.
- **모바일:** 좁은 화면에서 ECG, 조작, 시각화, 해설, 측정값 순서로 한 열 구성. 상위 3탭은 넓은 44px 정도의 원본 내비 버튼을 하단에 배치. Wiggers 원본 1000px SVG는 자체 가로 스크롤로 접근.
- **모션:** 현재 활성 보기/학습 카드/탭의 180–240ms 시각 전환, 원본 버튼의 명확한 선택 피드백과 Wiggers 보기. `prefers-reduced-motion`은 비필수 효과 제거. ECG·Mechanical·Wiggers의 과학적 애니메이션 자체는 CSS 모션과 구분.
- **조작:** 원본 버튼·슬라이더·Canvas·SVG·가이드·답안을 **이동(appendChild)** 하여 이벤트·식별자·세션을 유지. UI 렌더 전용 모듈에는 별도의 시계·requestAnimationFrame·setInterval·심박수/압력 계산을 절대 추가하지 않음.

## 분리 전략 및 안전 장치

- 이번 후보의 **진입점은 `experience.html`**. 원본 `index.html`과 역사적 백업, JS 생리/임상/학습 엔진을 그대로 유지한다. `experience.html`은 원본 HTML을 참조 버전으로 복제해 기존 스크립트를 동일한 순서로 실행한 뒤 `cardiac-experience-v2.js`와 `cardiac-experience-v2.css`만 추가하는 별도 사용자 시각 검수용 페이지.
- 새 JS는 최종 DOM 표현 어댑터. 기존 원본 `dashboard-v111.js`, `main-tabs-v113.js`, `course-v113.js`, `clinical-v113.js`의 권위 있는 상태/이벤트를 그대로 사용하고, 원본 임상 공개 제한을 우회하지 않는다.
- RAAS v7.1 참고: 위계·인접성·모바일 및 state read-only projection. **의학적 경로/약물 UI 복사하지 않음.** UI 도구 Atlas는 현재 설치/연결 목록에서 발견되지 않아 사용한 것으로 주장하지 않는다.

## 위험 / 대응

| 위험 | 대응 |
|---|---|
| 원본 DOM 이동으로 컨트롤러/Canvas 이벤트가 사라짐 | 실제 원본 노드의 정확한 ID 1개 보존, 엔진·임상·Guide 인스턴스 추가 생성 금지. Play/Pause/Reset, HR, Timeline, P/PR/QRS/ST/T 버튼 실브라우저 회귀 |
| 탭 이동으로 A/B 시계, Guided 답안, Course 완료, Clinical 답안이 초기화 | 기존 `CardiacMainTabs.switchTo`/원본 핸들러를 유일한 동작. 전후 스냅샷·복귀 QA |
| Wiggers details 열림/닫힘과 새 화면 애니메이션 충돌 | 원본 `CardiacDashboard.setView`와 `#wiggersDetails` 유지. 원본 판막/ECG 그래프에 장식 이동·가짜 파형 오버레이 금지 |
| 새 모바일 스와이프가 그래프의 수평 스크롤을 가로챔 | 심장 SVG 영역에서만 선택형 전환, 원본 위거스 스크롤엔 제스처 미부착; 버튼·키보드 동등 대안 보존 |
| 원본 CSS의 높이/그리드 규칙이 새 UI에 누적 | `.cx-enabled` 범위의 별도 토큰/영역 구성과 명시적 반응형 오버라이드, 레거시 index는 손대지 않음 |
| 교육 용어·상태를 옮기는 중 임상 가상 사례가 공개됨 | `clinical-v113.js` gate 미변경, 일반 화면 disabled, QA만 검증, 합성 지표 표시/의료 한계 공지 유지 |
| 운영/로컬 검수가 혼동됨 | 브랜치에서만 테스트 스크린샷/오프라인 ZIP 제공, PR 미병합, 실제 iOS/Android·Safari·전문가 검토는 별도로 NOT VERIFIED |

## 테스트 수락 기준

1. 320/360/390/768/1024/1440 픽셀에서 문서 전체 가로 넘침 없이 원본 그래프만 자체 가로 스크롤.
2. 정확히 하나의 `#ecgCanvas`, `#heartSVG`, `#mechanicalSVG`, `#wiggersChart`, `#playBtn`, `#timeSlider`, `#heartRateSlider`, `#guidedV112Panel` 유지.
3. 과학적 시간 A/B·HR·파형·상대압력/용적·미완료 임상 게이트 불변; 명시적 재생/일시정지/시간 이동/초기화 작동.
4. 전기/기계/Wiggers UI 전환으로 생리 시계 불변; 화면 탭 이동은 기존 정지 정책만 따름.
5. P/PR/QRS/ST/T 설명, 7개 개념 팝업, Guided 5단계·10문항, 6단원 교육, 임상 QA 원본 데이터 및 진행/복습 유지.
6. 키보드 포커스, Escape, 200% 확대에 대한 자동 가능한 수준, `prefers-reduced-motion`, 수평 Wiggers 탐색 확인.
7. 별도 브라우저 테스트·주요 화면 PNG 캡처·실행 가능한 오프라인 zip을 GitHub PR Actions 아티팩트로 제공. CI 성공과 실제 사용자·전문가 승인 엄격 구분.

## 필수 사용자 검수

브랜치 빌드만으로는 최종 승인하지 않는다. 주요 화면(PC 시뮬레이터 기본/위거스, 학습, Clinical QA, 모바일 시뮬레이터/학습), 스와이프·터치·탭 복귀, 판독성과 시각화 비율에 대한 실제 사용자 확인 후에만 차기 정식 운영 이전을 논의한다. **사용자가 명시적으로 승인하기 전까지 PR은 미병합.**
