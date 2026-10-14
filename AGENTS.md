# AGENTS.md
# Development Rules — Cardiac Electrophysiology Simulator

## 1. Preserve Existing Behavior

This is an educational simulator. Existing working behavior must be preserved unless a change explicitly requires otherwise.

Always inspect the current code before modifying it. Do not assume the current files match an earlier version.

## 2. Isolate Changes

Prefer small, isolated patches.

UI-only change:
- Prefer HTML/CSS.
- Do not modify JavaScript unless required.

Simulation change:
- Modify only the logic required.
- Keep the UI stable where practical.

## 3. Regression Review

After changes, verify:
- Play
- Pause
- Reset
- Timeline
- Heart-rate control
- ECG animation
- ECG direction
- ECG visibility
- Rhythm classification
- Cardiac conduction animation
- Current Phase updates

Ensure all JavaScript-referenced DOM IDs remain intact.

## 4. State and Animation

Avoid competing timers or animation loops.

ECG cycle, conduction phase, playback state, and controls should remain synchronized.

## 5. ECG Canvas

HTML canvas dimensions control drawing resolution; CSS dimensions control displayed size.

Do not change waveform amplitude/timing merely to solve a UI problem.

For clipping, prefer adjusting the drawing baseline or display area before altering the physiological model.

## 6. Educational Accuracy

The simulator is educational, not a clinical diagnostic tool.

Simulated measurements must not be presented as real patient data.

Future ECG measurements should clearly originate from the simulator model.

## 7. Placeholder Panels

Current placeholders:
- ECG Measurements
- ECG Event / Phase Indicator

Do not insert fake dynamic values.

Implement these panels only after their expected behavior and relationship to the ECG model are specified.

## 8. UI Principles

- ECG remains visually dominant.
- Avoid unnecessary vertical padding.
- Do not fill empty space with low-value features.
- Maintain readable labels and controls.
- Prefer consistent spacing.
- Aim for practical single-screen desktop use.
- Preserve responsive behavior.

## 9. Patch Naming

Use:

`Cardiac_Electrophysiology_Simulator_v[version]_UI_patch[number]_[short-description]`

Example:
`Cardiac_Electrophysiology_Simulator_v1.6_UI_patch4_current_phase_spacing`

Patch numbers restart for each new version.

## 10. Backups

Never overwrite a confirmed backup.

Before moving to a new version, archive the confirmed build under:

`backups/v[version]/`

At minimum:
- index.html
- style.css
- script.js

Documentation should also be archived when it represents that version's confirmed state.

## 11. Documentation

When a version is confirmed:
- Update SPEC.md.
- Update DEVLOG.md.
- Update README.md when user-facing behavior changes.
- Update AGENTS.md only when development rules or architecture change.

Documentation must describe the actual current behavior separately from future plans.

## 12. Standard Workflow

1. Inspect current code.
2. Identify affected files.
3. Review regression risks.
4. Implement the smallest reasonable change.
5. Test existing behavior.
6. Have the user visually/behaviorally verify the result.
7. Update documentation.
8. Archive the confirmed version.

---

## Current Project Baseline — v1.7 FINAL

Treat **v1.7 FINAL** as the confirmed baseline for the next version.

Completed v1.7 features:
- ECG Measurement Engine: HR, RR, PR, QRS, QT, QTc.
- Measurement normal-reference UI.
- ECG Event / Phase Indicator synchronization.
- Explicit conduction-path animation, including simultaneous RBB/LBB branching.
- Interactive ECG Component Explanation for P / PR / QRS / ST / T.
- Unified State Feedback using `heartState.ecgTime` as the sole simulation time source.
- Educational rate scenarios: Normal 72 bpm, Bradycardia 50 bpm, Tachycardia 120 bpm, and Custom after direct BPM adjustment.

### Protected v1.7 Behavior

When developing v1.8, preserve unless the change is explicitly part of the new physiological model:
- ECG visualization and waveform presentation
- ECG measurements and UI
- conduction animation
- Current Phase / ECG Event / Explanation synchronization
- Play / Pause / Reset
- Cardiac Cycle Timeline
- heart-rate control and scenario UI
- responsive behavior

### v1.7 Timing Limitation

The current model is intentionally simplified for education. Conduction phases and ECG events do not form a complete physiological electromechanical timing model. For example, Purkinje activation currently spans 380–450 ms while the QRS event ends at 380 ms. Do not silently "fix" such boundaries during unrelated work.

### v1.8 Architecture Direction

The first v1.8 task should be analysis and design of a physiological timing model before large UI changes.

Target architecture:
- **Physiological / Measurement Time (A):** source for modeled cardiac electrical timing and measurements.
- **Visualization Time (B):** controls how the model is presented/animated on screen.

The A/B separation must be introduced deliberately and centrally, not through competing timers.

Future cardiac-cycle/hemodynamic visualization should be designed to consume this model:
- valve opening/closing
- chamber filling
- ventricular ejection
- blood-flow direction

### Development Rule for v1.8+

Before implementation:
1. Inspect the confirmed v1.7 code and state flow.
2. Define the physiological model and timing dependencies.
3. Identify regression and state-synchronization risks.
4. Implement in small isolated patches.
5. Test boundary transitions, timeline seeking, playback, reset, and BPM changes.
6. Update SPEC/DEVLOG/README when the behavior is confirmed.
7. Archive the confirmed build before moving to the next version.

Do not claim physiological accuracy where the model has not implemented it.

## v1.8 FINAL Development Rules — Transition (2026-10-09)

The historical v1.7 requirements above are the protected behavior/regression baseline, not the current internal state model. v1.8 uses A physiological time and B visualization time with a single rAF driver, active `getPhysiologicalTiming()` and HR-based RR.

When changing timing, re-verify ECG waveform, measurements, ECG Event, Current Phase, conduction phases, RBB/LBB pulses, cardiac regions, Timeline, manual explanations, and Play/Pause/Reset. Never add competing timers or apply HR speed twice.

PR/QRS/QT coefficients are educational model assumptions, not clinical constants. High-rate QT clipping and Bazett QTc require explicit caveats. v1.9 mechanical events must consume A and preserve B's established pacing.

Automated v1.8 regression is complete; user physical-browser visual acceptance is pending. See `V1.9_START_HERE.md`.


## v1.9 / v1.10 Development Guardrails

- v1.9 adds a separate `mechanics.js` module and mode buttons. Do not remove or merge the original `heartSVG`; it remains the Electrical reference view.
- Never add another animation driver. All electrical and mechanical time derives from `heartState.physiologicalTime` (A). Leave `animationSpeed`, B clock and existing ECG canvas/sweep behavior untouched unless there is an explicit requirement.
- For mechanical changes test valve pressure inequalities, flow gating, constant volume during isovolumetric phases, full HR range, Timeline seek/Reset and Electrical baseline equality.
- Preserve selected view when resetting simulation; clear the Mechanical ready/phase feedback appropriately.
- Medical data is illustrative; do not present synthetic pressure indexes/volume ratio as clinical values. Keep high-HR QT and mobile overflow known limitations visible.
- Run `tests/test_v18.py`, `tests/stress_v18.py` and `tests/test_v19.py` after changes. Next design handoff: `V1.10_START_HERE.md`.


## v1.11 dashboard development guardrails
- The confirmed baseline is preserved in backups/v1.10-final/ (15 files); do not overwrite it.
- dashboard-v111.js loads last and only relocates original attached DOM elements. Never clone Canvas/SVG/HR/Timeline/Mechanical controls or duplicate IDs.
- Maintain one original A/B animation driver with no additional timer; mode/focus selection is UI state and cannot alter heartState, HR, Timeline, playback, ECG sampling, Mechanical or Wiggers domain models.
- When Wiggers is offscreen its native details closes to avoid wasted render work. On return open/sync with current A phase. The full deep-learning disclosure keeps its separate open state.
- The inspector distinguishes electrical conduction vs mechanical phase and uses the existing scientific/nursing description source. Do not derive clinical blood pressure, actual stroke volume, EF, CO, prognosis or therapeutic advice from illustrative curves.
- Run eight legacy suites plus the new real-entry v1.11 suite; check all six viewport widths, keyboard controls, popup dismissal, A/B equality and graph focus mode. Target-device manual visual sign-off is separate.


## v1.11.1 stabilization and v1.12 transition guardrails

- Default is compact, with explicit reversible full information mode. Never delete old teaching/ECG/Event/Current Phase DOM nodes merely to shorten the page; preserve native details and the independent long-form six-part clinical disclosure.
- Do not clone Play/Pause/Reset, HR, Timeline, ECG, Electrical/Mechanical/Wiggers or graph nodes; the dashboard remains a load-last presentation-only adapter. Compact mode cannot mutate A/B clocks or any model.
- Preserve graph and clinical text readability. Desktop controls/ECG may share a row when >=1200px; mobile remains stacked with Wiggers-only internal horizontal scrolling.
- Historical nine CI suites plus the v1.11.1 real-page suite are mandatory. Native details-toggle events are async; tests should wait for the actual dependent content/state, not arbitrary sleeps.
- Before v1.12 feature work read V1.11.1_RELEASE_NOTES.md and V1.12_START_HERE.md. No diagnosis or patient hemodynamic prediction from relative plots and no unreviewed arrhythmia engine. Document meaningful UX options and obtain user choice first.


## v1.12 planned guided-learning design (NOT YET CODE)

- Read V1.12_DESIGN.md and V1.12_CLINICAL_CURRICULUM.md before starting new feature work. Do not redo the completed scientific/model/architecture inventory.
- Important UX decision is pending explicit user approval: default recommend optional in-inspector guide and user-triggered, not automatic, Wiggers tab switch. No runtime Guided Learning code until decided.
- Follow the existing five-stage Wiggers profile (including two noncontiguous filling segments); never invent new event times or use normalized pressure/volume as real patient metrics.
- Learning navigation/answers are isolated presentation/progress state; no HR/clock/Timeline/playback side effects. Any seek is an explicitly labeled user action through the original Timeline. Preserve compact height, medical/nursing source content and Wiggers SVG scroll.
- Release new functionality only after old ten CI test stages and new v1.12 scientific/interaction/regression tests; manual target-device acceptance remains a separate review.


### v1.12 refined design mandatory handoff

Before implementing Guided Learning, read [V1.12_DESIGN_REFINEMENT.md](V1.12_DESIGN_REFINEMENT.md) in addition to V1.12_DESIGN.md and V1.12_CLINICAL_CURRICULUM.md. The default compact Inspector keeps its height, the guide **replaces** rather than stacks with the existing summary, educational selection and live model time must be labeled distinctly, and only a visibly confirmed original Timeline action may seek/pause. 'RR latter-half filling' must not be presented as a clinical late-diastolic physiological stage. Seek/view/guide UX must be explicitly approved before coding.


## v1.12 Patch 1 implementation guardrails

A/A/A are APPROVED: in-place inspector learning, study phase changes only text, Wiggers never switches automatically. Keep `guided-content.js` stage IDs and observation timing read-only from existing Mechanical/Wiggers, and `getStageNarrative` bound to existing PHASES data. Do not mutate A/B, HR, Timeline, Playback or views or clone original DOM. Original short nursing summary is hidden only during guided mode, then restored; native six-part deep dive stays independent. Patch 1 contains no previous/next, explicit seek/view, quizzes or difficulty; use separate Patch 2/3 PRs. Run prior ten suites plus the v1.12 Patch 1 real-browser regression; do not claim physical-device QA or medical validation from CI.


## v1.12 Patch 2 guardrails — latest implementation

The user has approved A/A/A and Patch 1/2 are implemented on the development line. Study previous/next and native dropdown are **UI-only**; Wiggers switches only on direct click of its own button; native Timeline seeks and pauses only on separate explicitly labeled `이 단계 관찰 시점으로 이동` button. Keep the original source-of-truth A/B clock, 0.1%-step Timeline event handler, model-relative units, full nursing text and existing first-viewport height. Never merge view and seek actions or add an alternate timer. Run 12 full regression steps including the 718-check Patch 2 real-browser test and confirm both branch and merged-main CI. Before Patch 3 read V1.12_PATCH2_REPORT.md and V1.12_CLINICAL_CURRICULUM.md; difficulty and quizzes are NOT yet implemented.


## v1.12 Patch 3: scientific learning and quiz guardrails

The approved A/A/A UX remains unchanged: no automatic Wiggers switching or seek, study navigation only edits selected stage, and only the Patch 2 explicit seek calls the original Timeline handler. `guided-questions.js` is a read-only bank of ten qualitative questions from V1.12_CLINICAL_CURRICULUM.md; do not invent patient metrics, diagnoses, treatment or clinical skill assessment from quiz completion. The new guided basic/advanced selection and answer state is **presentation/progress state only**, strictly isolated from A/B clocks, HR, Play/Pause, Wiggers/Mechanical domains and ECG. Quiz results must not leak before submission; answers reset only on a deliberate per-item retry or reload, not on cardiac Reset, stage or guide close. Complete PHASES/RATE source explanations and full original nursing disclosure must remain available. Never use localStorage, sessionStorage or server persistence for learning answers in v1.12 Patch 3. Preserve the previous 12 CI stages plus the Patch 3 real browser test, with exact-source nursing comparisons and six viewports. Actual device QA remains deferred by user request.



## v1.12 Patch 4 learning scope

Begin with a single phase concept plus ECG, valve and flow essentials for novice students. Add nursing observations only at the next learning level, and full source clinical narratives, model limits and the extra question through optional additional learning. Never delete the six-part full explanation, any of the original ten questions, or the two-segment model filling caution. Education-only transitions must not mutate A/B time, HR, playback, Timeline, ECG or modes; the user-approved A/A/A view and explicit seek remain unchanged. Run 14 CI stages (13 old + Patch 4), including six viewport widths and source-text parity. Actual device inspection remains user-deferred.


## v1.12 Patch 5 — clinical/UX closeout guardrails (2026-10-12)

- Keep v1.12 Patch 4 A/A/A behavior and three learning levels. Study-level/stage changes are view-only; only explicitly clicked native Timeline seek may pause/move A/B; Wiggers view switches only on direct action.
- The profile has **two distinct model-RR filling intervals**: early [0,atrialStart) is 0.88 flat, late [relaxationEnd,RR) rises 0.48→0.88. Even if both read `filling` and mitral open, do not imply an increasing plotted volume throughout both intervals or clinical late-diastolic correspondence.
- Teaching source text may be clarified without touching the established ECG, Mechanical, Wiggers physical proxy calculations. Treat source prose, model assumptions and clinical facts as distinct.
- Preserve 10 existing quizzes and six-part original nursing explanation; keep compact startup and native keyboard/mobile controls. Tests now consist of 15 CI steps (14 historical + Patch 5) including clinical interval checks across HR 30–180 bpm.
- This is **not v1.12 FINAL** until explicit user PC/mobile hands-on acceptance and remaining release criteria are met. No external independent clinical expert audit is claimed.


## v1.12 Patch 8 guided-only seek rule
Previous A/A/A no-seek navigation assertions in historical tests are intentionally replaced by B-mode tests. Guided course must only change A/B and Pause on deliberate stage selection (dropdown or previous/next), through original Timeline input; learning level/quiz/source/closing remain non-seeking. A fixed chosen-stage explanation is distinct from rapidly updating live model status. Free Play/Pause/HR and A/B remain original.


## v1.12 Patch 9 UX closeout rules
P6-8 are already merged with validated CI. New changes only consolidate the source directory and user-facing documentation, not original PHASES/RATE source text, native A/B clock, ECG/Mechanical/Wiggers profiles, or ten question bank. Header source-index toggle and native details summary must synchronize. No bulk-open on '자료 목록 보기'. Full original long-form source text available through the user's selected disclosure. Run all 18 legacy/current stages + Patch 9 Chromium six-view tests, verify branch PR and merged main. Version remains Patch 9, **NOT FINAL** without PC/mobile user acceptance.


## Current v1.12 Patch 12 development contract (supersedes historical A/A/A)
B/B/B/B guided ECG-first interface + student-first adjustments P10–12 are active. Only a deliberate first guided launch from canonical Ready seeks stage 1 once; subsequent free playback entry is non-seeking. Later guided stage changes Pause/Seek via native Timeline only. All ten questions and original clinical sources are protected data. No duplicate canvases/SVG/timers, no physiological model changes for presentation. New UX modifications must verify source availability, first-use/focus, six widths including narrow 200%-equivalent CSS viewports, old regression suites, and user device signoff. Do not claim FINAL from CI only.


## v1.12 Patch 13 source/display boundary
In compact study views, keep only the learner-relevant phase, valve, flow and relative volume visible. Retain qualitative model limits and non-patient values in contextual `ⓘ` native disclosures. Do not erase original pedagogic source texts or copy the SVG/DOM/animation clocks. PC mechanical SVG and live readout are side-by-side from 900 CSS pixels; mobile stacks. Preserve all tests and physical-device signoff before FINAL.


## v1.12 Patch 14 current usability guardrail
- Mechanical's original SVG/readout uses auto-fitting columns with >=320px minimum at viewport widths >=900px; if actual work area is too narrow it stacks. Mobile remains stacked. Do not base future width decisions solely on viewport width.
- Keep model note inside the readout in normal layout flow when open, never covering adjacent cards. Retain all established note/source wording, and protect disclosure keyboard and touch access.
- No new timers, DOM clones or changes to model, clinical text, ten questions or original A/B time. Before FINAL, confirm new Patch 14 automated browser checks and physical PC/mobile visual acceptance separately.

## v1.13 approved development contract — document registered, implementation pending
- Before any v1.13 code change, read **[Cardiac_v1.13_Three_Tab_Development_Contract.md](Cardiac_v1.13_Three_Tab_Development_Contract.md)** and check its rules against live `main` and current code. This approved new contract governs v1.13; historical v1.12 notes still apply as regression guardrails.
- Approved three top-level areas: Simulator / Learning (existing 5 stages and ten questions) / Clinical Application (new, separate cases). Electrical/Mechanical/Wiggers remain the simulator's internal views.
- **A안:** top-level tab changes use the current canonical Pause, preserve both A/B clocks, phase/ECG sweep/HR/current visualization and guided/clinical answers; returning never autoplays. Tab clicks must not invoke Timeline input, Reset or Guided first-start/step seek. Explicit Guided Learning start/step changes retain their existing native seek behavior.
- RAAS v5.5.1 three-tab session isolation (retained in v5.5.2) is a reference; tab navigation must never delete a clinical session. Study/clinical progress is in-memory initially, with explicit scenario reset only.
- **Documentation-only handoff:** no v1.13 UI implementation, medical model change or QA is claimed. v1.12 Patch 14 remains NOT FINAL pending real PC/mobile user signoff. Implement incrementally on separately reviewed PRs with regressions.

## v1.13 Patch 1 route adapter guardrails (2026-10-14)
- `main-tabs-v113.js` owns only UI route/pressed/hidden state. Native `pause()` must run only for actual top-level transitions while playing; no new engine, timer, RAF, reset, seek, Guided opening, or clinical session mutations.
- Do not move/clone the existing Inspector learning UI yet. The normal interface disables incomplete Learning/Clinical routes; `?v113Preview=1` is test-only, not a clinical-content release.
- All future routes must preserve exact A/B clocks, phase, HR, sweep, native input and Guided answers. v1.12 Patch 14 remains NOT FINAL pending user PC/mobile QA.

## v1.13 P2–P6 design handoff (2026-10-14)
- Before Patch 2, read [V1.13_PATCH2_TO_PATCH6_IMPLEMENTATION_PLAN.md](V1.13_PATCH2_TO_PATCH6_IMPLEMENTATION_PLAN.md) and the higher-priority approved 3-tab contract. Current implementation remains P1 only; this is a design update.
- P2: original Guided DOM/questions/answers exactly one instance; never make mere tab navigation trigger first study or Timeline seek. Simulator Live Inspector survives. P4/P5: static reviewed case content and Clinical State remain isolated from the sinus simulation.
- Preserve v1.12 Patch 14 NOT FINAL and separate app CI/automated screenshots from actual user device acceptance.

## 2026-10-14 — Detailed P3/P4 student-first design (design only)
- [V1.13_PATCH3_PATCH4_STUDENT_DESIGN.md](V1.13_PATCH3_PATCH4_STUDENT_DESIGN.md) specifies six-unit/5-stage mental model, guided/free unit/course state, no unit-navigation Seek, mobile/accessibility/readability, and strict fictitious bradycardia case content/validator/review policy.
- Clinical sample vital signs are **unreviewed design illustrations**, not approved data, and Clinical stays disabled until P5. Original ten questions, Guide instance, A/B heart engine and v1.12 Patch 14 NOT FINAL status are preserved.
- User intends later coordinated P2–P6 implementation on an integration branch with per-patch commits/tests before one final merged stable result; this commit changes documentation only.

## v1.13 integrated Patch 2–6 (implementation branch; NOT FINAL)
- Added the original single-instance Guided rehost in Learning, six-unit lesson course/free browsing, a schema-validated **unreviewed fictitious** clinical case, independent Clinical judgement/action/reassessment session, and Playwright integration tests. See [V1.13_INTEGRATED_PATCH2_TO_6_REPORT.md](V1.13_INTEGRATED_PATCH2_TO_6_REPORT.md).
- Clinical public tab remains **disabled** until expert case-content review; QA-only `?v113Preview=1` allows running the unfinished clinical educational scenario for testing, not patient care. Simulator and Learning are usable.
- Still NOT FINAL pending full CI, clinical reviewer, and physical PC/Android acceptance; v1.12 Patch 14 also remains NOT FINAL. No original physiological model or ten-question bank was edited.


## v1.13 Student UX audit / choices (design approval pending; NOT FINAL)
See [V1.13_STUDENT_UX_AUDIT_AND_CHOICES.md](V1.13_STUDENT_UX_AUDIT_AND_CHOICES.md) for current code inspection, minimally scoped accessibility and quiz/confirmation focus repairs, unreviewed clinical content boundary, and six explicit visual UX decision groups (A–F). No overall layout/palette/reading-order choice has been silently made. Preserve original A/B, ECG, Mechanical, Wiggers, original 10-question Guided and clinical release gate.


## v1.13 UX Patch 1 — Student-first A1+B1+C1+D1+E1+F1 (approved)
- The project owner selected the student-first responsive chapter reader, calm medical blue/teal palette, single-depth cards, goal→mechanism→nursing→observation→original Guided→references order, phase-focused fictitious patient snapshot/decision, and balanced 16px reading density.
- Implemented design and regression boundaries are documented in [V1.13_UX_PATCH1_IMPLEMENTATION_REPORT.md](V1.13_UX_PATCH1_IMPLEMENTATION_REPORT.md). Simulator heart clocks, original ECG/Mechanical/Wiggers and original 5-stage/10-question Guided remain canonical.
- Clinical still requires independent educational/medical review and is QA-only until approved. v1.13 and v1.12 Patch14 remain NOT FINAL until user PC/mobile testing.
