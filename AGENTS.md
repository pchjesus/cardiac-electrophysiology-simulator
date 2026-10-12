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
