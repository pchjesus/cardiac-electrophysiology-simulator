# Cardiac Electrophysiology Simulator v1.13 — 3탭 개발 계약

- **문서 상태:** 설계 확정 초안 · 구현 전 개발 계약
- **확정 UX 결정:** A안 — 최상위 탭 이동 시 자동 Pause, A/B 시간과 표시 위치 유지, 복귀 후 수동 Play
- **Cardiac 기준:** `pchjesus/cardiac-electrophysiology-simulator` `main` / v1.12 Patch 14 / `b77b6d6176093e7807b35eab5e96da751dc94578` (NOT FINAL, PC·모바일 검수 대기)
- **참조:** `pchjesus/raas-simulator` v5.5.1의 3탭·임상 세션 분리 계약 및 해당 동작을 유지한 v5.5.2
- **범위:** UI·상태 관리·기존 학습 보호·임상 교육 기반·위험 및 검증. 이 문서는 코드 구현이나 배포 완료를 뜻하지 않는다.

## 1. 목표 및 3탭 역할

심장 생리의 **관찰 → 개념 학습 → 임상 적용**을 별도 화면으로 구성하되, 하나의 기존 Simulation Engine을 사용한다.

| 최상위 탭 | 교육 목적 | 구성 | 기존 요소 보호 |
|---|---|---|---|
| ① 시뮬레이터 | 자유 관찰·조작 | ECG, HR, Timeline, Play/Pause/Reset, Electrical/Mechanical/Wiggers, Measurements, 실시간 설명·자료 | v1.12 Patch 14 기능 전부 |
| ② 학습 | 기전·간호 이해 | 안내형 코스 + 자유 탐색, 기존 심장주기 5단계·학습 수준·10개 개념 문항, 원문·근거 | Guided Learning 데이터·문항·관찰 동작 |
| ③ 임상 적용 | 환자 자료 종합·간호 판단 | 검토된 가상 사례, 활력징후·ECG·Lab, 임상 판단→간호 행동→재평가→복습 | 신규 데이터/상태만 사용 |

- Electrical/Mechanical/Wiggers는 **최상위 탭이 아닌 시뮬레이터 내부 시각화**로 유지한다.
- 기존 10문항은 **학습 탭**에 두고, **임상 적용에는 새로운 사례형 문항만** 추가한다(A안).
- 초기 임상 사례의 데이터는 사전 검토된 가상 정보로 제공한다. 기존 동율동 중심 엔진에 병적 파형·검사값을 자동 연동하거나 실제 환자 예측값처럼 표시하지 않는다.

## 2. 최상위 탭 이동 — 최우선 불변 계약

**MUST:** 현재 재생 중이라면 기존 `script.js`의 정식 `pause()` 동작으로 재생을 중지한 뒤 화면을 전환한다.

**MUST PRESERVE:** 다음 상태는 탭 이동 자체로 변경하지 않는다.

- `heartState.physiologicalTime` — A 시간
- `heartState.visualizationTime` — B 시간
- `heartState.cycleStartTime`, `heartState.cycleLength`, `heartState.ecgTime`(A 미러)
- `heartState.sweepPosition`, Timeline 값, 현재 생리학적 위상, ECG·전도·판막의 관찰 위치
- HR, 애니메이션 속도, 기존 Electrical/Mechanical/Wiggers 선택, 선택형 상세 설명의 열림 상태
- 기존 Guided Learning 단계·수준·10문항 답안, 신규 임상 사례 선택·답안·해설·진도

**MAY CHANGE:** `heartState.playing=false`, 애니메이션 무효화용 `playbackGeneration` 증가 및 `lastTimestamp=null`, 최상위 탭의 선택 상태와 표시/포커스 상태, 필요 시 화면 재그리기. 이들은 정식 Pause의 기존 동작이다.

**MUST NOT:** 탭 전환 코드에서 `reset()`, Timeline `input` 이벤트, 임의 A/B 시간 대입, Guided `observeSelected()`, 학습 시작 버튼의 가상 클릭, 임상 세션 종료·다시 풀기를 호출하지 않는다. 새로운 RAF/타이머/시계 또는 별도 환자 생리학 상태를 만들지 않는다.

**이벤트별 동작:**

| 사용자 행동 | 재생 상태 | A/B 시간 | 학습·임상 상태 |
|---|---|---|---|
| Play 중 시뮬레이터→학습/임상 | 기존 Pause로 정지 | 유지 | 유지 |
| 이미 Pause 중 상위 탭 변경 | 계속 정지 | 유지 | 유지 |
| 학습↔임상 | 정지 유지 | 유지 | 유지 |
| 시뮬레이터로 복귀 | **자동 Play 금지**, 명시적 Play 필요 | 보존 위치 | 유지 |
| 동일 상위 탭 재선택 | 실질적 no-op | 유지 | 유지 |
| Electrical↔Mechanical↔Wiggers | 기존 내부 뷰 정책 사용 | 유지 | 유지 |
| 명시적 기존 Timeline 이동 | 정식 Pause + A/B Seek | **사용자 지시대로 변경** | 답안 유지 |
| 명시적 Reset | 기존 시뮬레이션 초기화 | **초기화** | 임상·학습 답안은 유지(새 상위 계약) |

**해석상 예외:** 위 ‘A/B 유지’는 **상위 탭 클릭 자체**에만 적용된다. 사용자가 그 이후에 별도의 Play, Timeline 이동 또는 기존 학습 단계 이동을 지시하면 해당 기능의 기존 시간 규칙을 따른다.

## 3. 기존 Guided Learning 보호 계약

현행 `guided-learning.js`의 동작을 유지한다.

1. 단순히 **학습 탭에 들어가는 것**은 Guided Learning의 `setOpen(true)` 또는 `observeSelected()`를 실행하지 않는다. Ready 화면의 A/B=0을 유지한다.
2. **사용자가 5단계 학습 시작을 명시적으로 선택한 경우**, 기존 규칙대로 최초 Ready 진입 1회에 한해 첫 단계 관찰점으로 기존 Timeline Seek를 수행할 수 있다. 이 행동은 ‘탭 이동’이 아닌 ‘학습 시작’이다.
3. 기존 **이전/다음/단계 선택**은 선택된 단계의 관찰점으로 *기존 Timeline*을 통해 한 번 Pause/Seek한다. 단계와 현재 재생 단계의 차이도 계속 구분 표시한다.
4. **학습 수준(기초 이해·간호 연결·추가학습) 변경**, 문항 선택/제출·해설, 단순 닫기/복귀는 A/B를 변경하지 않는다.
5. **학습 탭을 떠났다가 복귀**해도 `selectedIndex`, `detailLevel`, `answers`, 시작 여부와 펼침 상태를 보존하며, 다시 들어왔다는 이유로 최초 학습 시작 또는 자동 Seek를 반복하지 않는다.
6. 기존 5단계 모델의 충만 구간·Wiggers 상대 압력/용적·ECG와 기계적 사건의 비동시성·심음 마커·10문항의 원문과 피드백을 임의 변경하지 않는다.
7. `guided-learning.js`는 현재 Dashboard Inspector의 제목/요약/패널에 직접 연결되어 있다. **같은 DOM·퀴즈 인스턴스를 복제하지 않는다.** 학습 탭 이전은 UI 결합부를 작은 패치로 분리하는 방식으로 수행한다.

## 4. RAAS 기반 임상 세션 보존 계약

RAAS v5.5.1의 `switchStudyMode()`처럼 **상위 탭 상태와 임상 풀이 세션을 분리**한다. 현재 RAAS v5.5.2에서도 이 규칙은 유지된다.

- `activeMainTab = simulator | learning | clinical`은 **화면 선택만** 담당한다.
- 시뮬레이션의 재생·A/B 시간은 **기존 `heartState`**, 학습 답안·단계는 **기존 Guided 상태**, 사례·문항·정답 해설은 **신규 Clinical State**가 각각 소유한다.
- **탭 이동 ≠ 사례 종료**. 진행 중인 사례, 문제 위치, 제출한 응답, 판단/행동 단계, 공개된 임상 자료와 피드백은 그대로 유지한다.
- **사례 다시 풀기**는 해당 사례 답안·해설·진도만 초기화한다. **다른 사례 선택**과 **학습 종료**는 별도의 명시적 종료/초기화 동작으로 둔다.
- **오답 → 관련 학습 이동 → 임상 복귀**는 동일한 문제·해설 위치로 돌아온다.
- 페이지 새로고침 시 초기 버전의 학습·임상 진행 기록은 초기화한다. `localStorage`, IndexedDB, 서버 저장은 이번 범위에서 제외한다.
- 초기 Clinical Case 데이터는 식별자·학습 목표·검토된 가상 환자 정보·활력징후·ECG 자료·Lab 결과(검사명/수치/단위/참고범위/채취 시각)·문항·선택지별 피드백·근거를 갖는다. 콘텐츠 검증은 UI 개발과 분리한다.

## 5. 구현 경계 및 권장 구조

- `script.js`: A/B 시계·Play/Pause/Reset·Timeline의 단일 원본. 필요 시 정식 Pause를 호출하는 작고 검증 가능한 연결부만 허용한다.
- `dashboard-v111.js`: 기존 Dashboard, Electrical/Mechanical/Wiggers, DOM 원본 및 실시간 설명 보호.
- `guided-learning.js`, `guided-content.js`, `guided-questions.js`: 기존 5단계·10문항·선택/관찰 동작 보호. 독립 학습 탭을 위한 최소 표시 어댑터만 단계적으로 분리한다.
- **신규 상위 내비게이션:** 상위 화면 `hidden`/선택 상태·포커스 관리와 기존 Pause 호출 담당. 모델 시계 및 학습·임상 데이터 소유 금지.
- **신규 임상 모듈:** 정적 검증된 사례 데이터와 독립 임상 진행·채점·해설 관리. 실제 혈압·EF·심박출량·검사 수치 예측 금지.
- 별도의 최상위 탭 컴포넌트에서 UI를 숨기더라도 기존 Canvas/SVG 노드를 **복제·파기·재생성하지 않는다**. 복귀 시 필요한 경우 기존 정적 렌더링/크기 동기화만 수행하며 A/B 시간은 유지한다.
- 최상위 메뉴는 RAAS와 같이 실제 버튼 및 `aria-pressed`·`aria-controls`를 이용한 명료한 동작부터 시작한다. 표준 ARIA `tab` 패턴을 택한다면 화살표 키·`aria-selected`·포커스 이동까지 **전부** 구현해야 하므로 단순히 역할만 부여하지 않는다.

## 6. 위험 우선순위 및 방지책

| 우선순위 | 예상 위험 | 방지책 |
|---|---|---|
| 높음 | 탭 클릭→Guided 첫 시작/단계 이동→예기치 않은 Seek | 상위 탭 컨트롤러에서 학습 `setOpen`/Timeline을 호출하지 않기; Ready·재진입 테스트 |
| 높음 | 재생 중 숨김 화면의 RAF 지속 또는 복귀 시 자동 재생 | 기존 `pause()` 1회 사용, 세대 토큰 무효화, 복귀 시 Play 명시 |
| 높음 | 임상 세션이 탭 이동만으로 초기화 | 화면 선택과 Clinical State 분리, 명시적 종료 액션만 초기화 |
| 높음 | Guided/ECG/SVG DOM 복제로 이중 이벤트·답안 유실 | 원본 노드·모듈 인스턴스 하나만 유지, 소규모 UI 분리 |
| 중간 | 숨김/재표시 후 Wiggers·ECG 크기/정지 프레임 오류 | 표시 복귀 시 계산 없는 기존 렌더 동기화, PC·모바일 확인 |
| 중간 | 가상 Lab 결과가 기존 동율동 엔진의 실측 파형처럼 오해됨 | 별도 임상 자료 표기, 모델 한계, 허위 자동 파형 생성 금지 |
| 중간 | 좁은 화면의 탭·자료·선택지 가독성 저하 | 360/390/768/900/1366px 검증, 조작 터치 타깃·스크롤 확인 |

## 7. 단계별 구현 계약

| 단계 | 허용 변경 | 완료 게이트 |
|---|---|---|
| v1.12 종료 전 | Patch 14 PC/모바일 사용자 검수 | 명시적 승인 전 v1.12 FINAL 금지 |
| v1.13 P1 | 상위 탭 라우터 + 정식 Pause 계약·UI 상태 | A/B·ECG·Mechanical·Wiggers·Reset·Timeline 회귀 없음; 미완성 빈 탭은 사용자 공개 금지 |
| P2 | 기존 5단계 Guided/10문항을 학습 화면에 안전하게 연결 | Ready 첫 시작·단계 선택·수준·해설·답안·재진입 보존 |
| P3 | 학습 코스·자유 탐색 기반 | 기존 콘텐츠/근거 재사용·중복 데이터 방지 |
| P4 | Clinical Case 데이터 구조 및 첫 검증된 임상 사례 | Lab 단위/참고범위/시각·근거·문항 정합성 |
| P5 | 사례 풀이·간호 행동·재평가·해설/복습 | 탭 왕복·정답/오답·초기화 경계·학습 환류 |
| P6 | 종합 PC/모바일/키보드 QA·회귀·문서 | 기존 전 스위트+신규 자동 테스트 통과, 사용자 실제 기기 확인 |

패치는 각 단계에서 **기준 코드 확인 → 영향 분석 → 작은 PR → 신규+기존 테스트 → 원격 `main` CI 확인 → 문서 반영** 순서로 진행한다. 대규모 한 번에 변경/버전 FINAL 선언은 하지 않는다.

## 8. 필수 자동 검증 시나리오 (수용 기준)

1. Ready(A=0,B=0)에서 **학습 탭만 클릭** → A/B=0, 자동 관찰 없음, Pause 유지.
2. HR 30/72/180에서 재생 중 임상 탭 이동 → `playing=false`, A/B/위상/HR/ECG sweep 위치 값 동일, 숨김 상태에서도 증가 없음.
3. 임상→학습→시뮬레이터 왕복 → 자동 Play/Seek 없음, 사용자가 Play를 눌러야 재개.
4. 동일 탭 재선택 및 빠른 반복 탭 전환 → RAF 중복 없음, 시간 점프 없음, 탭 포커스/표시 일관.
5. 최초 Ready에서 **명시적으로** 5단계 학습 시작 → 기존 승인된 1회 Timeline 관찰 동작만 실행.
6. Guided 이전/다음/드롭다운 → 기존 Pause+Seek 1회. 수준 선택·문항 답안·해설→시간 불변.
7. Guided 답안 제출 후 임상 탭 왕복 → 단계·수준·원문·제출한 문항 보존, 반복 Seek 없음.
8. 임상 사례 일부 풀이 후 다른 두 탭 왕복 → 동일 사례/문제/답안/해설/공개된 Lab/진도 보존.
9. 명시적 사례 다시 풀기·다른 사례·종료만 해당 기록 초기화. 시뮬레이터 Reset은 임상 기록을 지우지 않음.
10. Electrical/Mechanical/Wiggers 상태·차트, 6 Measurements, ECG Event, Timeline·Play/Pause/Reset, 모델 주의 및 도움말 기능의 전 회귀 통과.
11. 360/390/768/900/1024/1366px 실제 브라우저 화면·터치·키보드·포커스·숨김 화면 복귀 검증. 화면 캡처 자동 생성과 **실제 사용자 PC/모바일 확인**을 구별 기록.
12. 임상 데이터 스키마·검사 단위·참고범위·채취 시각·근거·정답/오답 해설을 콘텐츠 검토 체크리스트로 검증.

## 9. 확정·보류 사항

**확정:** RAAS 기반 3탭, A안(기존 10문항은 학습/새 사례 문항은 임상), 탭 전환 Pause + A/B 유지 + 수동 Play, 기존 Guided 동작 유지, 임상 세션 탭 왕복 보존, 모델·콘텐츠 분리.

**추후 세부 설계:** 학습 코스 표시 디자인, 임상 사례의 실제 검사·문항 데이터, 특정 교차 이동의 포커스 위치, 화면 크기별 최종 UI. 임상 콘텐츠는 출처 확인·간호/의학적 검토 후 확정한다.

**미수행:** v1.13 코드 구현·기능 배포, v1.12 실제 기기 FINAL 검수. GitHub에 이 설계 계약서를 등록하는 것은 기능 구현 완료/검증 완료의 증거가 아니다.

## 확인한 원본

- Cardiac: [`script.js`](https://github.com/pchjesus/cardiac-electrophysiology-simulator/blob/main/script.js), [`dashboard-v111.js`](https://github.com/pchjesus/cardiac-electrophysiology-simulator/blob/main/dashboard-v111.js), [`guided-learning.js`](https://github.com/pchjesus/cardiac-electrophysiology-simulator/blob/main/guided-learning.js), [`V1.12_START_HERE.md`](https://github.com/pchjesus/cardiac-electrophysiology-simulator/blob/main/V1.12_START_HERE.md), [`V1.12_PATCH14_REPORT.md`](https://github.com/pchjesus/cardiac-electrophysiology-simulator/blob/main/V1.12_PATCH14_REPORT.md)
- RAAS: [`index.html`](https://github.com/pchjesus/raas-simulator/blob/main/index.html), [`SPEC.md`](https://github.com/pchjesus/raas-simulator/blob/main/SPEC.md), [`ROADMAP.md`](https://github.com/pchjesus/raas-simulator/blob/main/ROADMAP.md)