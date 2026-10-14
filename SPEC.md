# SPEC.md
# Cardiac Electrophysiology Simulator Specification

## 1. Project Overview

Cardiac Electrophysiology Simulator is an educational browser-based simulator that visualizes cardiac electrical conduction and its relationship to an ECG waveform.

Educational conduction flow:

SA Node → AV Node → His Bundle → Purkinje System

The project prioritizes visual clarity, synchronization between the conduction model and ECG, and incremental development.

## 2. Current Version

**Current development: v1.13 Patch 1 (top-level navigation scaffold; NOT FINAL). The underlying v1.12 Patch 14 simulator also remains NOT FINAL pending user PC/mobile signoff.** v1.7 FINAL is an archived confirmed milestone, not the active build.

v1.6 was the UI stabilization milestone. v1.7 patch2 was the confirmed measurement baseline. v1.7 is now complete through patch7.

## v1.13 Patch 2–6 implementation plan (design only)

The approved three-tab contract is elaborated in [V1.13_PATCH2_TO_PATCH6_IMPLEMENTATION_PLAN.md](V1.13_PATCH2_TO_PATCH6_IMPLEMENTATION_PLAN.md): P2 single original Guided instance in Learning, P3 six-unit course, P4 clinically reviewed static case data, P5 independent clinical sessions, P6 accessibility/QA gates. **These follow-on features are not yet implemented and must not be reported as released.**

## v1.13 Patch 1 scope and acceptance contract

- Original `main.main-container` remains the single Simulator DOM, moved nowhere and never cloned.
- `main-tabs-v113.js` owns only a selected top-level screen (simulator/learning/clinical), hidden and pressed state, and optional display synchronization. It owns **no A/B time**, quiz answers, cases, RAF or timer.
- Normal interface exposes Simulator as usable; Learning and Clinical buttons are **disabled** until real content lands. Internal automated preview is enabled with `?v113Preview=1`; preview panels are explicitly marked nonfunctional.
- On an actual top-level change from playback, call canonical `pause()` once before hiding the Simulator. A/B time, cycle anchor, ECG sweep, HR, current step, native Timeline value and Guided learner state must remain unchanged. Return never autoplays.
- Selecting Learning must never call `setOpen`, `observeSelected` or native Timeline input. Existing explicit Guided start and step selection retain original timeline-seek behavior.
- A simulator Reset remains a simulator action, not an educational session clear. Clinical engine, data and public learning relocation are future patches, not Patch 1.
- Regression includes internal 3-way route testing, Ready A/B=0, HR 30/72/180, repeated switches, Guided answered state, no hidden progression, keyboard focus, 360/390/768/900/1024/1366 desktop/mobile viewport screenshot checks. All preexisting test suites remain mandatory.

## 3. Current Features

### ECG Monitor
- Animated sinus-rhythm ECG waveform.
- Left-to-right waveform presentation.
- ECG grid/background presentation.
- P / PR / QRS / ST / T interpretation indicators.
- Heart-rate display.
- Rhythm classification:
  - <60 bpm: Bradycardia
  - 60–100 bpm: Normal Sinus Rhythm
  - >100 bpm: Tachycardia
- ECG baseline positioned below the vertical center to reduce QRS clipping.

### Cardiac Conduction
- SVG heart/conduction visualization.
- SA Node, AV Node, His Bundle, RBB, LBB, and Purkinje structures.
- Active conduction highlighting.
- Conduction animation synchronized with the cardiac cycle.

### Controls
- Play
- Pause
- Reset
- Cardiac Cycle Timeline
- Heart-rate slider
- Heart-rate range: 30–180 bpm
- Normal range markers: 60–100 bpm
- Normal reference display: 80 bpm

### Current Phase
- Current phase title.
- Educational description.
- Associated ECG component.
- v1.6 UI provides additional vertical space and internal spacing for readability.

## 4. v1.6 Layout

Desktop layout:

- Left: ECG Monitor
- Right: Cardiac Conduction
- Control panel embedded beneath the ECG monitor.
- Play / Pause / Reset arranged vertically on the left side of the compact controller.
- Timeline and Heart Rate controls arranged on the right.
- Lower information area contains:
  - ECG Measurements placeholder
  - ECG Event / Phase Indicator placeholder
- Current Phase remains a separate full-width information panel.

The ECG display remains the visual priority.

## 5. Reserved / Functional Panels

### ECG Measurements

Implemented in v1.7:
- HR
- RR interval
- PR interval
- QRS duration
- QT interval
- QTc
- Normal reference ranges

These are simulated educational measurements derived from the simulator model, not patient data.

### ECG Event / Phase Indicator

Implemented in v1.7. The current ECG event is synchronized with the conduction state through the shared `heartState.ecgTime` source.

### ECG Component Explanation

Implemented in v1.7 for:
- P Wave
- PR Interval
- QRS Complex
- ST Segment
- T Wave

During playback, explanation follows the current ECG event. Manual component selection remains available while paused.

### Simulation State Feedback

Current Phase, ECG Event, ECG explanation, and conduction animation share the same simulation time source. Timeline seeking and Reset force the related feedback state to remain consistent.

### Educational Rate Scenarios

Implemented in v1.7:
- Normal Sinus Rhythm: 72 bpm
- Bradycardia: 50 bpm
- Tachycardia: 120 bpm
- Custom: entered by direct heart-rate adjustment

The scenarios demonstrate rate/cycle-speed behavior only; physiological HR-dependent interval changes remain a v1.8 concern.

## 6. Design Principles

- Preserve existing behavior during UI changes.
- Prefer isolated patches.
- Keep ECG visually dominant.
- Avoid excessive vertical padding.
- Do not add features merely to fill empty space.
- Reserve space for clearly useful future educational functions.
- Keep desktop use practical within one screen where possible.
- Preserve responsive behavior.

## 7. Future Feature Priority

### Priority A
1. ECG Measurement Engine
2. ECG Event / Phase Indicator synchronization
3. More explicit conduction-path animation

### Priority B
4. Interactive ECG component explanations
5. Clearer simulation state feedback
6. Basic bradycardia/tachycardia educational scenarios

### Priority C
7. Additional rhythm modes
8. More detailed cardiac physiology
9. Broader ECG/arrhythmia expansion

These are future plans, not v1.6 requirements.

## 8. Versioning

UI patch naming:

`Cardiac_Electrophysiology_Simulator_v[version]_UI_patch[number]_[short-description]`

Example:
`Cardiac_Electrophysiology_Simulator_v1.6_UI_patch4_current_phase_spacing`

Patch numbering restarts for each new version.

Confirmed versions are archived under `backups/v[version]/`.

---

## v1.7 — ECG Measurement Engine (Historical Plan → Completed)

### Scope

v1.7 introduces the first functional ECG measurement layer. The planned measurements are:

- Heart Rate (HR)
- RR interval
- PR interval
- QRS duration
- QT interval
- QTc

The existing `ECG Measurements` placeholder UI will be connected to these simulated measurements.

### Visualization Preservation

The existing v1.6 visualization behavior is preserved in v1.7.

In particular:

- Existing ECG animation speed must remain unchanged.
- Existing BPM-dependent animation-speed behavior must remain unchanged.
- Existing ECG waveform presentation must remain unchanged.
- Existing conduction animation must remain unchanged.
- Existing Cardiac Cycle Timeline behavior must remain unchanged.
- Play, Pause, Reset, Current Phase, and rhythm classification behavior must remain unchanged.

The measurement engine is an additional calculation layer. It must not redefine the existing visualization timing model.

### Measurement Basis

Measurements are simulated educational values derived from the simulator's configured heart-rate state and ECG timing model. They are not measurements from a real patient ECG.

RR interval may be calculated from the selected heart rate:

`RR (ms) = 60000 / HR (bpm)`

Other intervals should be derived from the simulator's defined ECG timing model rather than duplicating unrelated timing constants in the UI layer.

### Architecture

The measurement layer should remain logically separated from:

- ECG waveform rendering
- animation-speed calculation
- conduction animation
- Cardiac Cycle Timeline
- UI control state

Where practical, measurement functions should consume shared timing/model information rather than independently duplicating waveform definitions.

### Out of Scope for v1.7

The following are explicitly outside the v1.7 scope:

- Redesigning the current visualization speed
- Recalibrating BPM-dependent animation speed
- Rebuilding the physiological timing model
- Introducing new rhythm modes
- Introducing arrhythmia simulation
- Dedicated Physiological ECG Timing Model
- Explicit Physiological Time (A) / Visualization Time (B) architecture

These may be addressed in later versions after the measurement layer is stable.

### Validation and Regression

Before v1.7 is considered complete, verify at minimum:

- HR display
- RR calculation at multiple BPM values
- PR interval
- QRS duration
- QT interval
- QTc calculation
- ECG waveform animation
- BPM-dependent animation speed
- Cardiac Cycle Timeline
- Play / Pause / Reset
- Conduction animation
- Current Phase
- Rhythm classification



---

## v1.7 patch2 — Confirmed Current Specification

### ECG Measurements

The former placeholder is now functional and displays:
- Heart Rate (HR)
- RR interval
- PR interval
- QRS duration
- QT interval
- QTc

A normal reference range is displayed beneath each measurement.

The measurement layer remains an educational model derived from the simulator's existing ECG timing model. It is not a real patient ECG measurement system.

### Reference-Range Presentation

- HR: normal range 60–100 bpm
- RR: reference corresponding to the normal-rate context
- PR: normal range 120–200 ms
- QRS: normal range 70–120 ms
- QT: HR-dependent
- QTc: adult sex-specific upper reference limits

The current PR result of **220 ms** is intentionally retained because it is derived from the existing model timing. It is not treated as a UI or arithmetic error.

### v1.7 patch2 Layout

`ECG Measurements` and `ECG Event / Phase Indicator` are separate sibling panels.

The Measurement panel was widened relative to the Indicator panel. The two internal Measurement columns are equal-width, and the QTc reference is kept on one line.

### Timing Preservation

The following remain unchanged:
- ECG visualization speed
- BPM-dependent visualization-speed behavior
- ECG waveform timing/presentation
- Conduction animation
- Cardiac Cycle Timeline
- Play / Pause / Reset
- Current Phase
- Rhythm classification

### v1.7 patch3 Regression Requirements

Before v1.7 is confirmed, verify at minimum:
- ECG Event changes at the defined waveform boundaries.
- Conduction indicator follows the existing conduction phase.
- Play/Pause does not create a second animation path.
- Reset returns Event/Phase Indicator to its initial state.
- Timeline movement updates the Event/Phase Indicator immediately.
- Heart-rate changes preserve the existing animation-speed relationship.
- Existing ECG waveform, measurements, rhythm classification, conduction animation, and Current Phase remain unchanged.
- The responsive event flow remains horizontally usable on small screens.

### Deferred Architecture

The Physiological Time (A) / Visualization Time (B) split is a future architecture task. It is not implemented in v1.7 and remains deferred to v1.8.

### v1.7 patch3 — ECG Event / Phase Indicator Synchronization

The `ECG Event / Phase Indicator` panel now consumes the existing cardiac-cycle time (`heartState.ecgTime`) and displays the current ECG event and conduction stage.

ECG event mapping follows the simulator's existing waveform timing:
- 0–80 ms: Baseline
- 80–160 ms: P Wave
- 160–300 ms: PR Interval
- 300–380 ms: QRS Complex
- 380–500 ms: ST Segment
- 500–680 ms: T Wave
- 680 ms–end of cycle: Baseline

The conduction flow indicator uses the existing `currentStep` state. Bundle Branch Activation and Purkinje Activation are represented by the Purkinje-stage indicator because the current panel presents the conduction pathway at a high level.

The synchronization is driven by the existing animation/update path. No competing timer or animation loop was introduced. Timeline changes and Reset reuse the same state path.

### v1.7 patch3 Timing Note

The ECG Event indicator follows the current simplified educational waveform timing. It does not introduce or imply a new physiological timing model. The 700–833 ms portion of the normal 72-bpm cycle remains a baseline/resting portion for the event indicator, while the existing Current Phase behavior is preserved.

### v1.7 Completion Boundary

v1.7 is intended to finish the current educational simulator model. A dedicated Physiological ECG Timing Model and the separation of Physiological/Measurement Time (A) from Visualization Time (B) are deferred to v1.8.

### Current Development Build

**v1.7 patch4** is the current development build pending user verification.

### v1.7 patch4 — Explicit Conduction-Path Animation

The ventricular conduction visualization now makes the right/left bundle branch split explicit.

- The existing conduction pulse continues through SA Node → AV Node → His Bundle using `heartState.ecgTime`.
- During the 380–450 ms Purkinje activation interval, the visual pulse divides into simultaneous right- and left-sided pulses traveling along the RBB and LBB paths.
- Branch pulse visibility and position are controlled by the existing `updateElectricalPulse()` call in the main simulation loop.
- No additional timer, animation loop, or independent clock is introduced.
- Reset explicitly hides and re-centers both branch pulses.
- The change is visual/educational and does not alter ECG waveform timing, measurement calculations, BPM-dependent visualization speed, or the future physiological timing architecture.

### v1.7 patch4 Regression Requirements

Verify:
- SA → AV → His pulse movement remains functional.
- The ventricular pulse visibly splits into RBB and LBB propagation.
- Branch pulses disappear during recovery/rest.
- Play/Pause continues to use the existing animation loop.
- Reset restores the SA starting state and removes branch pulses.
- Timeline movement updates the branch pulse position immediately.
- BPM changes preserve event ordering and existing speed behavior.
- ECG waveform, measurements, Current Phase, ECG Event Indicator, and path highlighting remain functional.
- Narrow/mobile layouts remain usable.

### v1.7 patch5 — Interactive ECG Component Explanation

Implemented on top of the user-verified v1.7 patch4 build.

### Implementation
- Converted the ECG interpretation items for P, PR, QRS, ST, and T into accessible buttons.
- Added an inline `ECG Component Explanation` panel instead of a modal, keeping the main simulator view compact.
- Clicking an ECG component shows an educational explanation and its related conduction/activity path.
- Clicking an ECG component shows its explanation for manual inspection while paused.
- During playback, the explanation automatically follows the current ECG event (P → PR → QRS → ST → T), giving the simulation timeline priority over manual selection.
- Reset/timeline movement also returns the explanation to the corresponding current ECG event.
- Reused the existing ECG event/conduction model; no new timer, animation loop, or simulation clock was introduced.

### Educational Scope
- P: atrial depolarization / SA Node → atria
- PR: atrial-to-ventricular conduction interval / AV Node → His Bundle
- QRS: ventricular depolarization / His → RBB/LBB → Purkinje
- ST: simplified early ventricular recovery portion
- T: ventricular repolarization

### Regression / UX Review
- Current ECG event highlighting and selected explanation use separate CSS states.
- Timeline changes continue to use the existing `updateConduction()` path.
- No competing animation or event loop was added.
- Buttons retain keyboard focus behavior and mobile horizontal scrolling of the ECG interpretation row.
- The explanation is inline to avoid modal focus/transition issues.

### Version Status
**v1.7 patch5** is the current development build pending user verification.



## v1.7 patch6 — Simulation State Feedback / Current Phase Integration

Implemented on top of the user-verified v1.7 patch5 build.

### State Model
- `heartState.ecgTime` remains the single simulation time source.
- Current Phase is derived from the existing `conductionSteps`.
- ECG Event is derived from the existing `ecgEvents`.
- The Current Phase ECG label now follows the canonical current ECG Event rather than the broader conduction step's static `step.ecg` value.
- ECG explanation continues to follow the current ECG Event during playback, while manual component selection remains available when paused.

### Synchronization Improvements
- `updateConduction()` now supports an explicit synchronization request for timeline seeking.
- ECG Event changes update the Current Phase ECG label even when the conduction step itself has not changed (for example, ST → T within the Recovery step).
- Timeline seeking forces the complete feedback state to refresh, preventing stale explanation/selection state when the selected time remains inside the same conduction step.
- Reset returns the interface to a consistent pre-playback Ready state and clears manual ECG component selection.

### Scope / Non-Goals
- No new timer, animation loop, simulation clock, or physiological timing model was introduced.
- ECG waveform timing, measurement values, BPM-dependent visualization speed, conduction durations, and patch4 pulse animation remain unchanged.
- The known 380–450 ms Purkinje interval versus ECG-event boundary is retained as part of the current educational timing model and remains a v1.8 physiological-model concern.

### CSS Cleanup
- Consolidated duplicate `.ecg-item` font-size declarations so the interactive ECG buttons retain the intended patch5 responsive scale without a later rule unexpectedly overriding it.

### Regression Requirements
Verify at minimum: Play/Pause/Reset, timeline movement across every ECG/conduction boundary, P→PR→QRS→ST→T explanation synchronization, manual component selection while paused, BPM slider behavior, ECG measurements, conduction pulse branching, and responsive ECG component button layout.

**v1.7 patch6** is the current development build pending user verification.


## v1.7 FINAL — Completed Scope

v1.7 is complete through patch7.

Patch sequence:
1. patch1 — ECG Measurement Engine
2. patch2 — Measurement UI refinement and normal-reference display
3. patch3 — ECG Event / Phase Indicator synchronization
4. patch4 — Explicit conduction-path animation with RBB/LBB branching
5. patch5 — Interactive ECG Component Explanation
6. patch6 — Simulation State Feedback / Current Phase integration
7. patch7 — Educational Rate Scenarios

### Known Model Limitation

The v1.7 ECG/conduction timing model is intentionally simplified for educational visualization. Conduction-phase and ECG-event boundaries are not a complete physiological electromechanical model. For example, the current Purkinje phase spans 380–450 ms while the QRS ECG event ends at 380 ms. This is retained intentionally for v1.7 and should not be silently recalibrated during unrelated changes.

## v1.8 Roadmap

The next version focuses on a **Physiological ECG Model**:
- Physiological / Measurement Time (A)
- Visualization Time (B)
- HR-dependent physiological timing relationships
- more coherent RR, PR, QRS, QT and QTc behavior
- architecture that can later drive mechanical and hemodynamic visualization

Do not introduce A/B timing through competing timers. Build it as a central model/state architecture.

## Later Roadmap

### Cardiac Cycle & Hemodynamics
Build on the v1.8 physiological timing model:
- four-valve opening/closing
- chamber filling
- ventricular ejection
- blood-flow direction and visualization
- electrical → mechanical → hemodynamic synchronization

### 12-Lead ECG
- I, II, III, aVR, aVL, aVF, V1–V6
- lead-specific waveform visualization
- representative cardiac observation territories
- lead direction/vector explanation

### ECG Interpretation
- normal vs abnormal ECG
- ST/T changes
- introductory ischemia/infarction localization

### Case / Quiz Engine
- rhythm identification
- ST/T pattern identification
- territory localization
- case-based explanations

## v1.8 Development Status — Patch 1 (Timing Model Foundation, 2026-10-09)

Implementation status: **Patch 1 implemented and browser-regression checked; physiological HR-dependence is not yet implemented.**

- Added `CARDIAC_TIMING_MODEL` and `getCardiacTimingModel()` with the unchanged v1.7 timing boundaries.
- Measurement timing, conduction steps, and ECG event interval definitions reference this central static model.
- `baseCycleLength` remains a compatibility alias at 60000/72 ms.
- `ecgValue()` and several rendering/state consumers still contain v1.7 timing logic; this patch **does not** complete single-source timing migration.
- Playback speed, ECG morphology, Heart Rate control, Timeline, Play/Pause/Reset, and UI are intentionally unchanged.
- Future work: define safe cycle semantics and A/B (physiological/visualization) time separation before changing RR and time-dependent consumers; maintain v1.7 visual pacing.
- Known v1.7 limitation: Purkinje conduction and QRS timing boundaries require a later deliberate physiological alignment patch.

## v1.8 Development Status — Patch 2 (A/B Clock Foundation, 2026-10-09)

**Implemented in the v1.8 development line; HR-dependent physiological cycle timing is not yet enabled.**

- A (physiological/model clock): `heartState.physiologicalTime` is now the authoritative time for ECG waveform sampling, conduction phases, events, Current Phase, Timeline and seek reconstruction.
- B (visualization clock): `heartState.visualizationTime` accumulates the v1.7-calibrated playback delta. The ECG sweep consumes exactly that pre-scaled delta without a second HR-speed multiplier.
- One `requestAnimationFrame` loop remains the shared update driver. `heartState.ecgTime` is a synchronized compatibility mirror, not an independent timer.
- `getVisualizationDelta(realDelta)` applies the legacy `animationSpeed * BASE_SPEED_FACTOR` once; `getPhysiologicalDelta(visualDelta)` is **identity mapping in Patch 2**, so A = B and observed timing stays the same as Patch 1.
- `getPhysiologicalRR(hr)` provides `60000 / hr` independently of playback speed. It is currently used for the existing RR measurement, **not** for active event/cycle boundaries.
- Reset zeros A, B and compatibility time. Timeline seek atomically assigns A and B to the same reference phase; pause/resume preserves both.
- Unchanged: fixed 72-bpm reference cycle, PR/QRS/QT model, morphology, ECG event/conduction timing, HR-to-animation-speed mapping, HTML/CSS and user-visible presentation.
- Future Patch 3: introduce HR-dependent cycle length and its mapped physiological interval boundaries together, **never** update `baseCycleLength` alone without event/waveform/conduction migration. Preserve the v1.7-calibrated visual cycle pacing through the A/B converter.
- v1.9: keep electrical event timing as extensible structured data for mechanical and hemodynamic components sharing the same A clock.


## v1.8 Development Status — Patch 3 (Physiological RR / Cycle Projection, 2026-10-09)

**Status: Implemented and automated-browser regression tested.**

- The physiological clock (A) now advances in milliseconds relative to the active RR: `RR = 60000 / heartRate`. `getActiveCycleLength()` returns the physical cycle duration, while `baseCycleLength` remains a **fixed, visualization-only v1.7 template duration** (60000/72 ms). Do not confuse these.
- The existing visual clock (B) continues using the v1.7-calibrated `heartRateToSpeed * BASE_SPEED_FACTOR` exactly once, so the **overall screen playback cadence is preserved**.
- `getPhysiologicalDelta(B_delta) = B_delta * RR / baseCycleLength`. Physiological cycle boundaries and Timeline percentages use real RR via `cycleStartTime`; the mapped v1.7 reference phase is used for ECG waveform, conduction, cardiac regions, pulse, event, Current Phase and labels.
- On mid-cycle HR changes, `synchronizeCycleLength()` retains the current beat fraction without rewinding monotonic A; the anchor `cycleStartTime` shifts as needed. After a Timeline seek, A is set to `RR*percent`, B to `referenceCycle*percent` in one operation.
- Preserve `ecgTime` only as a temporary compatibility mirror. One animation loop remains. Reset rebuilds A, B, the RR anchor, and the existing Ready state.
- The preserved v1.7 **intra-cycle ECG boundaries** are still projected by normalized cycle position. **IMPORTANT: PR/QRS/QT readouts remain v1.7 educational reference values and are not yet physically timed HR-adaptive intervals.** Patch 4 must replace this normalized reference projection with a scientifically justified interval model and update waveform, conduction, event and measurement consumers together.
- The simulator **must not** be described as having a fully physiologically accurate ECG model at Patch 3. At extreme HRs, proportional reference projection is only a temporary display compatibility technique.
- Known v1.7 Purkinje/QRS timing limitation remains until the dedicated conduction-alignment patch; no changes were made to branching animation or its educational labels.
- Keep room for v1.9 valve/chamber/blood-flow events driven by the same physiological clock, without a second animation driver.

## v1.8 FINAL — Dynamic Timing Contract (2026-10-09)

- `getPhysiologicalTiming(hr)` is the active source of RR, P, PR, QRS, ST, T, QT/QTc and conduction boundaries. `getPhysiologicalCyclePhase()` is the A-clock event location. `getReferenceCyclePhase()` and `baseCycleLength = 60000/72` are legacy visualization reference helpers, **not** physiological timing values.
- One animation loop advances B using the protected v1.7 `heartRateToSpeed() * BASE_SPEED_FACTOR` mapping, then advances A with `RR / baseCycleLength`. This avoids double-counting HR.
- Events, waveform, conduction, cardiac regions, electrical pulses, Current Phase, Timeline and measurements use the same dynamic physical intervals. Reset, pause, HR transitions and seek synchronize states.
- `RR(ms)=60000/hr`. P start: `clamp((RR-320)*0.18,8,80)`. PR: `clamp(185+0.13*(RR-750),125,200)`. QRS: fixed 80 ms. P end: `pStart+min(clamp(RR*0.145,55,80),PR-40)`. QRS start = pStart + PR.
- Nominal QT: `clamp(380*(RR/(60000/72))^0.35,225,525)`; effective QT: `min(nominalQT,RR-QRSstart-8)` to prevent next-cycle overlap within the simplified SA-first rendering model. ST duration: `clamp((QT-80)*0.27,15,80)`. T end = QRSstart+QT.
- `QTc (Bazett)=QT/sqrt(RR/1000)` (ms). The printed values are derived from *simulated* boundaries, not measured patient ECG.
- RBB/LBB simultaneous branching is retained. Purkinje now ends with QRS: this is a deliberate correction of the documented v1.7 phase mismatch.
- This is a teaching approximation: coefficients are modeling choices without clinical validation. At high HR QT clipping creates unrealistically short intervals; do not use output for clinical diagnosis or treatment. Bazett has known overcorrection/undercorrection at high/low rates.
- Validated: 239 browser-regression assertions, 13,741 interval/event/seek assertions for 151 HR points (30–180 bpm), 4,077 event sample checks, 1,208 seek states; zero browser script errors. Actual device UX approval remains pending.
- Known inherited issue: approximately 47px horizontal scrolling at width 390px. This also exists in the tested Patch 3 and was left unchanged intentionally.
- v1.9 should attach mechanical/hemodynamic phases to physiological clock A, not to CSS animation timers or normalized canvas positions. See `V1.9_START_HERE.md`.

### Clinical / scientific source context (APA 7th)

Rautaharju, P. M., Surawicz, B., & Gettes, L. S. (2009). AHA/ACCF/HRS recommendations for the standardization and interpretation of the electrocardiogram: Part IV: The ST segment, T and U waves, and the QT interval. *Journal of the American College of Cardiology, 53*(11), 982–991. https://doi.org/10.1016/j.jacc.2008.12.014

Luo, S., Michler, K., Johnston, P., & Macfarlane, P. W. (2004). A comparison of commonly used QT correction formulae: The effect of heart rate on the QTc of normal ECGs. *Journal of Electrocardiology, 37*(Suppl.), 81–90. https://doi.org/10.1016/j.jelectrocard.2004.08.030

These works ground the discussion of QT/QTc and correction limitations, **not** the simulator's chosen heuristic coefficients.


## v1.9 FINAL — Electrical/Mechanical Modes and Domain Contract

### UI contract
- ECG monitor, explanation, measurements, event/phase indicators, HR controls and playback timeline are ALWAYS visible.
- Only the heart-visualization region switches between Electrical (the v1.8 `heartSVG`) and Mechanical (`mechanicalView`). View switching never changes time, HR, selection, playback or sweep data. `aria-pressed` communicates active mode; default is Electrical.
- View mode persists through Reset (UI preference) while the Mechanical indicator returns to Ready. Timelines and HR changes immediately reconstruct the current mechanical state.

### Shared timing contract
- One existing requestAnimationFrame (no added timer). `script.js/updateConduction()` calls `window.CardiacMechanical?.sync()` after obtaining the current A time. `script.js/reset()` calls `window.CardiacMechanical?.reset()`.
- `mechanics.js/getMechanicalTiming(electrical)` derives atrialStart from P-wave onset + small lag, ventricular isovolumetric contraction from QRS onset + small lag, ejection from contraction plus a ramp, and relaxation after ejection; it does **not** depend on the v1.8 T end (clipped in extreme tachycardia).
- `getMechanicalState(phase,electrical)` is pure, accepts an explicit phase, and returns stage/progress, qualitative relative pressure indexes, four valve booleans, forward flow category, normalized ventricular volume, and the timing boundaries. No second mutable clock or cached phase is authoritative.

### Mechanical stage/state requirements
- Filling: AV (mitral/tricuspid) open, semilunar closed, ventricular volume rises. Atrial systole adds late filling.
- Isovolumetric contraction: both valve groups closed, ventricular volume constant while the qualitative ventricular pressure rises.
- Ejection: semilunar group open, AV closed; ventricular volume decreases and flow goes toward the arteries.
- Isovolumetric relaxation: both groups closed, ventricular volume constant, then next-cycle filling resumes.
- Valve states are derived from relative pressure *ordering*: AV open iff atrial > ventricular, semilunar open iff ventricular > arterial. The illustrative pressure values are synthetic indexes (NOT mmHg). The same conceptual pressure comparisons are reused on both sides, not full separate right/left hemodynamic calculations.
- Blood particle positions use SVG path geometry as a deterministic function of stage progression. No CSS keyframe, timeout or additional animation loop.

### Verification and limitations
- `tests/test_v19.py` covers 151 heart rates, six representative phase points per rate, valve/pressure invariants, volume, v1.8 A/B/rhythm/waveform/measurement equality, seek/Reset/Play/Pause, mode switching and mobile overflow comparison (4,711 checks, no JS errors).
- Inherited v1.8 clinical issue: high-HR QT clipping and Bazett rate bias. New v1.9 model has no measured chamber pressure, volume, cardiac output or ejection-fraction prediction; phase coefficients represent a chosen teaching approximation, not validated human physiology. Anatomical direction and chambers are schematic.

### Source context (APA 7th)
Pollock, J. D., & Makaryus, A. N. (2022). *Physiology, cardiac cycle*. In *StatPearls*. StatPearls Publishing. https://www.ncbi.nlm.nih.gov/books/NBK459327/

OpenStax. (n.d.). *19.3 Cardiac cycle*. In *Anatomy and physiology*. https://openstax.org/books/anatomy-and-physiology/pages/19-3-cardiac-cycle

These sources support the **sequence** of events and pressure/valve principles, not the simulator's invented interval coefficients or numerical relative-pressure indexes.


## v1.10 Patch 1 — Wiggers Model Foundation (development)

**Baseline:** v1.9 FINAL at commit `dbfb60e84ef7919f7a65ec45bcab322b8895995a`. Preserve the archived v1.9 runtime at `backups/v1.9/FINAL/`.

### Scope and requirement traceability

- **WIG-001**: Add `wiggers.js` as a passive read-only model consumer of the existing v1.8 physiological electrical timing and v1.9 pure mechanical functions.
- **WIG-002**: Represent ECG boundaries, mechanical phase/boundaries, left-heart *conceptual* pressure indexes, normalized ventricular volume, and valve/flow states in a deterministic snapshot for an explicitly supplied physiological phase.
- **WIG-003**: Define representative mitral closure (S1), aortic opening, aortic closure (S2), and mitral opening at the **existing** v1.9 mechanical boundaries, not at arbitrary ECG waveform pixels. The S1/S2 objects are *event markers*, not synthesized heart sounds, and do not represent split S1/S2 or independently validated right-sided valve timing.
- **WIG-004**: Audit discontinuities at the existing v1.9 pressure-stage boundaries via `inspectPressureBoundaries()`. Do **not** interpolate those stage values or label them measured mmHg. Continuous pressure curves and valve-pressure consistency are explicitly deferred to Patch 2.
- **WIG-005**: Preserve v1.9 display, animation and electrical/mechanical model behavior byte-for-byte except loading the new passive script; no new animation driver, timers, CSS or panel.
- **WIG-006**: Validate 151 integer HRs (30–180), valve/S1/S2 ordering, reproducible seek positions, untouched app state, exactly equivalent v1.9 ECG/Mechanical outputs and responsive width using `tests/test_v110.py`. Continue running `tests/test_v18.py`, `tests/stress_v18.py`, and `tests/test_v19.py`.

### Public browser contract

`window.CardiacWiggers.getSnapshot(phaseMs, getActiveTiming())`

Returned contract:
- `metadata`: version, educational units, non-clinical caveat, current v1.9 pressure-profile identifier.
- `cycle`: `rrMs`, normalized `phaseMs`, derived `heartRateBpm`.
- `electrical`: P/QRS/ST/T boundary timestamps in physiological milliseconds.
- `mechanical`: stage, progress and `boundaries`.
- `pressure`: `leftAtrial`, `leftVentricular`, `aortic`, `representation`; these are aliases of the v1.9 **shared qualitative pressure proxies** and are not separately modeled left/right chamber pressures.
- `ventricularVolume.relativeValue`: the unchanged v1.9 normalized educational volume.
- `valves` and `flow`: unchanged v1.9 valve and flow states.
- `valveEvents` and `heartSoundEvents`: time-stamped event definitions derived from `getMechanicalTiming()`.

Pure query helpers: `getValveEvents(electricalTiming)`, `getHeartSoundEvents(electricalTiming)`, `inspectPressureBoundaries(electricalTiming, epsilonMs?)`.

The module does **not** subscribe to rAF or mutate `heartState`. The Wiggers graph and UI are deferred. Graph cursors must later consume `getPhysiologicalCyclePhase()`; A and B playback rules remain unchanged.

### Next: Patch 2

Define and validate a continuous educational *left-sided relative* pressure and volume profile with coherent valve state inequalities, event timing, isovolumetric volume invariants and explicit boundary continuity checks. Decide whether the verified new shared profile can replace the current stage pressure implementation without changing existing Mechanical presentation. Retain a safe v1.9 rollback and separate model-validation acceptance from display appearance.

### Physiological sources (APA 7th)

Pollock, J. D., & Makaryus, A. N. (2022). *Physiology, cardiac cycle*. In *StatPearls*. StatPearls Publishing. https://www.ncbi.nlm.nih.gov/books/NBK459327/

OpenStax. (n.d.). *19.3 Cardiac cycle*. In *Anatomy and physiology*. https://openstax.org/books/anatomy-and-physiology/pages/19-3-cardiac-cycle

These sources substantiate the **sequence and relationships** among cardiac-cycle events; they do not validate the simulator's heuristically selected numerical pressures, volume normalization or event timing delays.


## v1.10 Patch 2 — Continuous Relative Pressure / Volume Profile

**Scope:** Preserve v1.9 `mechanics.js` and the Patch 1 `window.CardiacWiggers.getSnapshot()` contract. Add `wiggers-profile.js` as a **parallel, read-only teaching profile** for the later optional Wiggers panel. No user-facing graph, physical pressure or sound is introduced in Patch 2.

### Data and model contract

- New API: `window.CardiacWiggersProfile.getSnapshot(phaseMs,getActiveTiming())` returns a pure snapshot with `cycle`, mechanical stage/boundaries, a continuous illustrative relative pressure triple (`leftAtrial`, `leftVentricular`, `aortic`), normalized relative ventricular volume, gradient signs, valves/flow and the Patch 1 valve/S1/S2 event objects.
- Helpers: `getLandmarks(timing)` supplies labelled conceptual pressure/volume anchors, `phaseWithinCycle(phase,RR)` normalizes an explicit finite physiological time.
- Pressures are **dimensionless educational values**: `relative-teaching-index`. No mmHg, pressure calibration, patient-specific vascular compliance, right-sided chamber pressures, or measured cardiac output.
- Common phase boundaries come from the unchanged `CardiacMechanical.getMechanicalTiming()`, based on A/physiological time. QT clipping is not used as a new mechanical event anchor.
- Each stage blends adjacent illustrative landmark pressures via cubic smoothstep. Ejection adds a smooth illustrative arch and a positive LV-to-aortic gradient that is zero at valve-opening and valve-closing boundaries. Relative volume is C1 smooth with isovolumetric plateaus at 1.00 and 0.48, ejection drop 1.00→0.48, early/late filling and atrial contribution. These numbers are **modelling choices, not measured norms**.
- Adjacent pressure and volume curves have matching endpoint values and zero slope at phase boundaries, including cycle wrap (C1 by design); the model does not claim physiological waveform calibration.

### Valve event tie-break contract

- Stages are **half-open intervals** `[start,end)`, with the event at its exact named boundary belonging to the following stage. The event schedule owns equality at valve crossing.
- Mitral valve is open during `[0,contractionStart)` and `[relaxationEnd,rr)`; aortic valve is open during `[ejectionStart,ejectionEnd)`.
- At the exact event, the relevant relative pressures are equal and the prescribed post-event valve state wins; between boundaries pressure gradients must support the modelled valve state.
- **Important numerical note:** this profile uses one modulo for positive phases and a bounded IEEE-754-scale tie tolerance (at most 1e-8 ms) to canonicalize mathematically identical event positions across cycles. The original v1.9 Mechanical mode remains **unchanged**, so the two models may classify a floating-point event tie differently at an exact boundary. This distinction must remain explicit until a separately tested shared timing boundary policy is adopted; do not silently use new pressures to toggle v1.9 valves.

### Regression and release gate

- v1.9 Electrical/Mechanical display, animation speed, A/B clocks, HR, Timeline, Play/Pause/Reset and ECG readouts must be bitwise/deterministically comparable against the archived v1.9 baseline where appropriate.
- Use `tests/test_v110_patch2.py` over all integer HR 30–180, thousands of phase samples, pressure-gradient signs, event-boundary left/right limits, equal-pressure tie-break, constant isovolumetric volume, wrap continuity, invalid input and 390px overflow. Preserve earlier `tests/test_v18.py`, `tests/stress_v18.py`, `tests/test_v19.py` and `tests/test_v110.py`.
- Test results and CI status must be recorded **after actual execution**; no manual physical-browser or clinical validation is claimed. 
- Rollback: original v1.9 FINAL remains in `backups/v1.9/FINAL/`; verified Patch 1 is pinned by commit `d46a6a30b10e766d9dd6da05f795b8dacb8a9e2f` and branch `backup/v1.10-patch1-verified`.

### Next — Patch 3

Build a **user-controlled optional expand/collapse Wiggers panel** consuming the verified continuous profile and unchanged electrical timing, with ECG, three relative pressure traces, ventricular relative volume and discrete valve/S1/S2 event markers. Avoid an independent animation loop and protect single-screen desktop layout; manually verify actual visual presentation on the user's local server. Consider a model consistency comparison against v1.9 at event ties before wiring live cursors.

### References (APA 7th)

Pollock, J. D., & Makaryus, A. N. (2022). *Physiology, cardiac cycle*. In *StatPearls*. StatPearls Publishing. https://www.ncbi.nlm.nih.gov/books/NBK459327/

OpenStax. (n.d.). *19.3 Cardiac cycle*. In *Anatomy and physiology*. https://openstax.org/books/anatomy-and-physiology/pages/19-3-cardiac-cycle

These references justify the qualitative cardiac-cycle sequence and valve-pressure relationship, not the new smoothstep curves, illustrative amplitudes, or normalized volume anchors.


## v1.10 Patch 3 — Optional Wiggers Visualization Integration

### User-facing scope

- **Selected UX A:** one expandable native `<details>` Wiggers Diagram panel placed **after all v1.9 information panels**, collapsed by default. The top ECG monitor and Electrical/Mechanical diagram retain their existing placement, controls and animation speed.
- Opening the panel displays **one physiological RR cycle**, not the existing ~3-second monitor sweep; the plot's horizontal fraction is `phaseMs / rrMs`. All five traces come from the existing v1.8 ECG function `ecgValue(phase,timing)` and the independently verified v1.10 Patch 2 `CardiacWiggersProfile.getSnapshot()` (left atrial pressure, left ventricular pressure, aortic pressure, normalized LV volume).
- Four valve event markers are obtained from the Patch 2 snapshot's Patch 1 event schedule, with a key for mitral closing/S1, aortic opening, aortic closing/S2 and mitral opening. These represent **event labels**, not audio or separately modelled right-sided heart sounds.
- A vertical cursor and status labels reflect **A clock** via `getPhysiologicalCyclePhase()`, preserving B visual pacing. No competing `requestAnimationFrame`, timer, independently advancing graphics state or ECG-calculation logic.
- Panel visibility is user-controlled and persists through Play, Pause, Timeline, HR slider, Reset and Electrical/Mechanical mode switches. Reset restores the panel readout to Ready while keeping disclosure preference.
- Rebuild the static SVG traces/events **only** on first open or when ECG timing/HR changes. On ongoing simulation frames, update just the cursor and minimal status. While the panel is closed, `sync()` makes no chart changes.
- Use a keyboard-operable native disclosure, SVG accessible descriptions, event SVG titles and a horizontally scrolling **local chart region** at narrow widths. Do not change the inherited v1.9 mobile overflow in this patch; do not make it worse.

### Architecture, data and safety

- New `wiggers-view.js` is only a presentation adapter. It relies on `script.js`'s existing A-clock and pure Wiggers domain models; diagram coordinates derive from the source data at 481 samples per RR. Pressure traces have **relative-index**, volume has **normalized-relative** units, and ECG is the simulator's modeled waveform, not a measured lead II ECG.
- Three **optional hooks** in `script.js`: after `updateConduction()`'s mechanical sync, when HR changes (even in Ready), and after Reset. All use `window.CardiacWiggersView?.sync/reset` so legacy baseline pages without the new module continue functioning.
- Existing `mechanics.js`, `wiggers.js`, `wiggers-profile.js` are untouched. Wiggers uses the Patch 2 explicit event-boundary tie policy, while v1.9 Mechanical may show its known floating-point near-boundary difference; do **not** silently merge pressure models.
- Do not claim numeric pressure (mmHg), volume (mL), ejection fraction, patient diagnostic values or validated clinical haemodynamic predictions.

### Verification gate

Run full v1.8–v1.10 Patch 2 regression plus `tests/test_v110_patch3.py` for disclosure keyboard operation, 5 source-backed SVG paths, valve event markers, HR 30–180 sample points, seek-based A-cursor, Play/Pause/Reset, mode switches, single-loop behavior, mobile scroll width and JS exceptions. This is automated QA only; **manual visual acceptance** is needed from the user on local `http://localhost:8000` for readability, scaling, markers and synchronized movement.

Next Patch 4: add state-aware cardiac event/valve/S1/S2 educational explanations to Wiggers and clarify event-crossing tie semantics, without changing the validated physiological graphics/legacy Mechanical presentation.


## v1.10 Patch 4 — Valve/S1/S2 educational explanations and nonmodal help

### Scope and architecture
- **WIG-401:** Keep the native `<details>` panel, A/B clocks and existing Wiggers traces exactly as implemented in Patch 3. Add a separate sibling `?` button in a positioned shell, *outside* `<summary>`, so clicking help cannot trigger the panel's native disclosure.
- **WIG-402:** Show a small, anchored nonmodal `role="group"` popover with an accessible title, short ECG→pressure→valve→volume guide, close button, Escape handling and outside pointer click dismissal. Focus close button on open and restore trigger focus after explicit close/Escape. Do not trap focus or interfere with other controls.
- **WIG-403:** Put phase-dependent educational text immediately under Wiggers status. Add contextual text for the most recent valve event, differentiating exact-event timestamps from the intervening stage. Dynamic text must be sourced from `CardiacWiggersProfile.getSnapshot(A,getActiveTiming())` rather than recomputing pressures or asking v1.9 Mechanical for stage.
- **WIG-404:** Reuse `CardiacWiggersProfile`'s event IDs and `CardiacWiggers`'s four timestamps for SVG title and text. At a precise event tie the Patch 2 half-open stage / explicit valve-state rule is authoritative; the older Mechanical view may round differently and must remain unchanged.
- **WIG-405:** Reset restores educational readouts to Ready. Collapse stops graph/educational updates. Opening help does not alter the `<details>` state, HR, Timeline, A/B clocks, animation, Electrical/Mechanical selection or chart plot cache. Outside click on playback controls dismisses help while letting those controls execute normally.
- **WIG-406:** The help and learning presentation uses no new ticker, rAF or domain model. `wiggers-help.js` registers click/keydown listeners once on load; `wiggers-view.js` compares texts before DOM writes.
- **WIG-407:** Full nurse-facing educational guide and APA 7th sources are provided in README, including nonclinical limitations, relative-unit conventions, A/B cursor distinction, S1/S2 associations and stage interpretation.

### Verification
- Retain all six previous browser suites and add `tests/test_v110_patch4.py`: keyboard & mouse popover operation, independent disclosure, focus/aria, outside click, exact-event tie/marker/readout consistency for HR 30/50/80/120/180, all five phase narratives, Reset/Play/Pause/Mechanical/Electrical, 1366/768/390/360 viewport clipping and JavaScript errors.
- Run on CI using the existing single browser-regression workflow; separate CI functional verification from target-device **manual visual** acceptance.
- **Excluded:** independent right-heart physiology, audio synthesis, clinical mmHg/mL/EF numbers, modifying v1.9 Mechanical pressure rules, heart-disease scenarios and Patch 5–7 features.
- **Known carryovers:** inherited narrow screen overflow, high-HR educational interval fidelity/Bazett QTc bias, and possible legacy Mechanical exact-boundary rounding mismatch.

### References (APA 7th)
See the cardiac-cycle physiology references listed in this SPEC under v1.10 Patch 2 and in README's Patch 4 guide. Those sources justify the qualitative event sequence, not exact synthetic plots or pressures.


## v1.10 Patch 5 — High-fidelity *explanations*, not higher-fidelity hemodynamic calculations

**Starting base:** main v1.10 Patch 4 commit `b419506ea4ca79b088ec39703954f60f635b6e10`. This patch preserves physiological A time, visualization B pacing, mechanical state, ECG model, continuous Wiggers profile, normalized volume, static 481-point curves and the protected Electrical/Mechanical views.

### Feature requirements
- **WIG-501 — Presets:** Add Normal 72 bpm, Bradycardia 50 bpm, Tachycardia 120 bpm buttons inside the optional Wiggers panel. They assign the *existing* #heartRateSlider and dispatch the original input event. Do not add a competing HR source. Slider use returns educational preset selection to Custom; rhythm *classification* remains derived solely from HR (<60, 60–100, >100).
- **WIG-502 — Stage education:** Add a second optional native disclosure below the Wiggers profile, initially collapsed, with five narratives for filling, atrial systole, isovolumetric contraction, ejection and isovolumetric relaxation. Each narrative has: electrical event, pressure/valve principle, ventricular volume, nursing observation, rate comparison, and limitations. Use `CardiacWiggersProfile.getSnapshot(getPhysiologicalCyclePhase(),getActiveTiming())` and canonical phase boundaries. Reuse existing `getMechanicalTiming()` strictly to describe *model* cycle/filling-window duration.
- **WIG-503 — Rate-appropriate messaging:** Describe a reduced *available filling interval* at higher rates as a conditional physiological consideration, not measured preload, cardiac output or disease. Bradycardia alone need not be pathological; tachycardia can be a physiological response. Do not infer EF, stroke volume, blood pressure, cardiac output or patient stability from normalized profiles.
- **WIG-504 — Interaction:** Respect Reset Ready semantics, original disclosure/deep-disclosure preference, Play/Pause, Timeline seek, current mode and HR change without rewinding clocks. `wiggers-learning.js` reads the existing model; sync occurs only via existing control/update hooks, using no second rAF or timer. Detailed text is updated on change, not every identical animation frame.

### Document/UX requirements
- **WIG-505 — Patch notes:** Header icon opens a nonmodal, scrollable, accessible patch-history popup categorized as Features / Medical and nursing education / UI-UX / Safety-QA-Documentation. Claims are tied to actual shipped v1.8–v1.10 changes.
- **WIG-506 — User guide:** Second header icon opens a nonmodal user guide with controls, Electrical/Mechanical, Wiggers, scenario learning and clinical limitations. Both overlays have X, Escape, outside click; only one open at once, close with focus restoration for Escape/X, do not interfere with outside controls.
- **WIG-507 — Limited layout change:** Keep original ECG Monitor, Current Phase, control panels and Electrical/Mechanical modes unchanged. Add a small header toolbar and place detailed explanations inside the existing optional Wiggers view to avoid growing the default single-screen layout. Mobile popup positions are viewport-relative, not document-relative (existing narrow-screen overflow remains a separate Patch 6 task).

### Verification and clinical guardrails
- Keep all 7 previous suites, add `tests/test_v110_patch5.py` (3 preset values, 7 HR classification boundaries, exact source-backed 5-stage data display, Reset/Timeline/play/modes, help popover state/focus/outside clicks, desktop/390/360px popup geometry, no JS errors). Run 8 suites via CI.
- Illustrative relative pressures are not mmHg, normalized LV volume not mL or EF, S1/S2 markers not audio. At high HR the existing PR/QT/QTc approximations may be nonclinical. Do not claim independent ventricular hemodynamic adaptation to HR: rate changes shift event timing but the model does not calculate Frank–Starling response.
- Maintain Patch 4's Wiggers-profile vs v1.9 Mechanical exact-boundary rounding note; no forcing their outputs to match at a floating-point event tie.
- Clinical claims separated into established physiology (electrical activation preceding contraction; pressure-related valve transitions; cardiac-cycle phases), educational conventions (72/50/120 representative HR presets), and unsupported inference (numeric blood pressures, perfusion and output).

### Supporting physiology (APA 7th)
Pollock, J. D., & Makaryus, A. N. (2022). *Physiology, cardiac cycle*. In *StatPearls*. StatPearls Publishing. https://www.ncbi.nlm.nih.gov/books/NBK459327/

OpenStax. (n.d.). *19.4 Cardiac physiology*. In *Anatomy and physiology*. https://openstax.org/books/anatomy-and-physiology/pages/19-4-cardiac-physiology

American Heart Association. (2024, September 25). *Bradycardia: Slow heart rate*. https://www.heart.org/en/health-topics/arrhythmia/about-arrhythmia/bradycardia--slow-heart-rate

American Heart Association. (n.d.). *Tachycardia: Fast heart rate*. https://www.heart.org/en/health-topics/arrhythmia/about-arrhythmia/tachycardia--fast-heart-rate

These references ground descriptive adult HR ranges, cardiac-cycle sequence, and nursing-context symptom awareness; they do not validate this application's mathematical curves.


## v1.11 — Approved integrated dashboard implementation contract

**DASH-1101:** Move original Play/Pause/Reset, Timeline, 30–180 bpm HR and three teaching presets into a shared command area. Never clone IDs or create independent HR/clock/slider handlers.

**DASH-1102:** Keep the existing ECG Canvas and component explanation visible above all visualization views. CSS may adjust display dimensions but must not change Canvas waveform generation, ECG timing or A/B pacing.

**DASH-1103:** Central visualization has Electrical (original conduction SVG), Mechanical (original Mechanical mode) and Wiggers (original native details/graph). Switching view must not alter any heartState A/B time, cycle origin, sweep position, HR or playback state. Preserve existing Mechanical.selectMode logic and buttons.

**DASH-1104:** Keep Wiggers native details as rendering gate. On leaving Wiggers close details to prevent offscreen continuous SVG work; on reentering reopen and sync to the current physiological phase. Full clinical-learning disclosure stays independent and retains user choice. Optional desktop Wiggers focus/split changes layout only.

**DASH-1105:** Present electrical and mechanical phases distinctly next to the visualization, together with source-derived concise physiology/nursing messages. Move, not discard, the Current Phase and ECG Event DOM panels. The full six-part v1.10 explanation and clinical-model caveats must remain accessible.

**DASH-1106:** Wide screen 2-column visualization/inspector; below 1200px single-column; 390/360px no document horizontal overflow; bounded internal Wiggers graph scroll at its original minimum 720px. Three view controls have ARIA pressed states and keyboard Left/Right/Home/End navigation. Keep existing independent Wiggers and header help popups.

**DASH-1107:** Use load-last dashboard-v111.js progressive DOM relocation. Existing JS modules bind to original DOM before relocation, with no second rAF/timer. Only optional Dashboard.sync calls are added to existing update paths, plus read-only inspector narrative from the existing learning dictionary. Backup 15 v1.10 files in backups/v1.10-final/.

**Tests:** All eight historical v1.8–v1.10 tests remain unchanged and runnable; tests/test_v111.py loads the real index.html and verifies A/B identity, 3 modes, focus/split, HR presets/custom slider, Play/Pause/Reset/Timeline, popup keyboard interactions, original content and six viewport widths. The independent screenshot workflow supports visual review but is not human device acceptance.

**Known scientific limitations:** no actual mmHg, mL, EF, stroke volume, output, patient perfusion or validated high-HR QTc interpretation; distinct Mechanical vs Wiggers exact event ties; deliberately simplified ECG/pressure/volume teaching relationships. Short screens require some vertical scrolling rather than shrinking explanations into illegibility.


## v1.11.1 — Compact-first educational UI stabilization contract

**SCOPE:** presentation, accessibility and QA. No physiology, ECG shape, simulation timer/rAF, mechanical calculation, Wiggers event boundary, pressure/volume profile or clinical diagnostic model changes.

**DASH-1111-01** Initial compact view keeps ECG, native Play/Pause/Reset, HR (30–180 bpm), Timeline, three rate presets, six measured interval values, Electrical/Mechanical/Wiggers controls, electrical phase, mechanical phase, ECG Event and short nursing/physiology explanations visible. The three original detailed text panels must remain in the DOM in independent native details, initially collapsed.

**DASH-1111-02** Full information toggle opens original ECG-component, Current Phase, ECG Event details and references. It closes them when restored to compact and cannot alter any simulation model or canonical clock. The independent six-part nursing/physiology deep disclosure is not automatically opened or closed by density changes.

**DASH-1111-03** Clicking an existing P/PR/QRS/ST/T item reveals its original explanatory DOM node even in compact mode without auto-opening unrelated panels. UI view state must not compete with ECG selected-component state.

**DASH-1111-04** At >=1200px, compact mode arranges original shared controls alongside the original ECG Canvas without cloning nodes. Expanded mode and smaller screens retain stacked layout. Do not make the canvas, Wiggers graph or clinical text unreadably small for first-viewport fitting.

**DASH-1111-05** Measurements remain visible in compact mode; their historical normal-range footnotes are accessible in expanded mode and must not be represented as clinically calibrated output. Wiggers alone may scroll horizontally within its bounded plot.

**DASH-1111-06** Preserve the protected nine v1.8–v1.11 suites and add a 98-assertion real-page v1.11.1 suite. Test full/compact document height, visible core info, complete nursing text, original mode and control bindings, A/B identity, Reset/Play/Pause/Timeline, help popups and widths 1440/1366/1024/768/390/360. Native toggle-associated content assertions wait on content rather than merely disclosure-open state. Record actual screenshots separately from physical-device acceptance.

**Clinical guardrails:** ECG vs mechanical phases remain distinct. Pressure and volume are illustrative relative/normalized values, not mmHg/mL/EF/CO; S1/S2 are markers not audio. High-HR QT/QTc limitations and v1.9 Mechanical vs Wiggers exact-boundary ties are documented, not fixed through UI code.

**NEXT:** v1.12 plans are in V1.12_START_HERE.md. Do not silently begin disease/rhythm-model additions in the stabilization patch.


## v1.12 PLANNED DESIGN — NOT IMPLEMENTED

Detailed architecture, user-visible UX alternatives, state transition table, validated source mapping, phase interval targets, tests and risks: [V1.12_DESIGN.md](V1.12_DESIGN.md).
Detailed nursing/medical teaching curriculum and 10 qualitative practice questions: [V1.12_CLINICAL_CURRICULUM.md](V1.12_CLINICAL_CURRICULUM.md).

**GUIDE-1201 (pending UX confirmation):** Keep v1.11.1 compact view and clinical inspector unchanged by default. An explicit opt-in guide covers five currently modeled stages. Recommended location: existing inspector rather than a fourth visualization mode or blocking popup.

**GUIDE-1202 (protected state):** Guided open/close/step/question/level actions never change A/B, HR, Timeline, ECG, Play/Pause, Electrical/Mechanical mode, Wiggers plot or Reset behavior. Optional explicit “move to this phase” action must invoke original Timeline input and clearly disclose that it pauses/seeks.

**GUIDE-1203 (scientific integrity):** Canonical profile and valve events from existing CardiacWiggersProfile, model segment boundaries from CardiacMechanical.getMechanicalTiming. Handle the two disjoint `filling` segments correctly: initial [0,atrialStart) relative LV volume remains 0.88, while late [relaxationEnd,RR) increases 0.48→0.88. Mid-stage guide target for filling must be in late filling. No medical parameters or numerical clinical inferences.

**GUIDE-1204 (teaching):** electrical event, mechanical activity, valve/pressure, relative LV volume, qualitative nursing assessment and current model limitation per stage; original source text reused, beginner/advanced selectable, test conceptual understanding without clinical prediction.

**GUIDE-1205 (regression):** preserve prior ten automation suites, add v1.12 real-browser tests at HR 30/50/60/72/80/100/120/180 and stage-event boundaries, seek-only-on-explicit-click, no default viewport height increase, mobile graph-local scrolling and keyboard operation. Physical-device QA is not asserted by automated tests.

**Release gate:** User-visible guide location and automatic tab-switch choice require user approval; no v1.12 runtime implementation in this design-only change.


### v1.12 design v2 contract — planned, not implemented

See [V1.12_DESIGN_REFINEMENT.md](V1.12_DESIGN_REFINEMENT.md). The default dashboard must have no additional permanently visible learning card; instead a small header-row entry exchanges the live explanation with opt-in guided learning, retaining original DOM and all ECG/Wiggers views. Guided selected stage and the model's current stage are distinct. Previous/next steps have zero A/B, HR or playback effects. Explicit phase-seek alone uses the existing Timeline input and pauses. `filling` has two **model-RR** intervals; never mislabel the latter as clinically 'late diastolic filling'. No v1.12 code is authorized before the three user-visible UX decisions are confirmed.


## v1.12 Patch 1 — implemented scope

- Approved UX A/A/A: existing inspector in-place learning replacement; stage selection is informational only; no automatic Wiggers/tab changes.
- Added `guided-content.js` (exactly five stage IDs, read-only representative midpoints checked against existing Mechanical/Wiggers interval rules), `guided-learning.js` (open/selected-stage state only), and a `CardiacLearning.getStageNarrative` read-only source method. Default closed; original ECG/short clinical/full six-part descriptions preserved.
- Added an optional passive sync hook to the existing dashboard, no new timer/rAF or model/HR/A-B mutation; guidance entry does not resize the original first screen beyond the 16px budget at 1366x768.
- In model-RR later-segment filling the representative midpoint is selected within `[relaxationEnd,RR)`; the earlier `[0,atrialStart)` filling stage's relative LV volume is flat 0.88. This is not clinical late-diastolic filling or a patient measurement.
- Added `tests/test_v112_patch1.py` on top of the historical 10 suites. Previous/next, explicit guided seek/Wiggers-view buttons, difficulty levels and quizzes remain future Patch 2/3 work. Source-of-truth and handoff: [V1.12_PATCH1_REPORT.md](V1.12_PATCH1_REPORT.md).


## v1.12 Patch 2 — approved explicit-interaction contract

**Implemented scope:** only three incremental actions inside the existing optional learning inspector:

1. `guidedV112Previous` / `guidedV112Next` change the selected study index (bounded 1–5) and update native select, text and aria states. First/last buttons disabled. No mutation of A/B time, HR, player state, view or timeSlider.
2. `guidedV112ViewWiggers` calls `CardiacDashboard.setView('wiggers')` on a **direct user click only**. No hidden seek, Pause or new Wiggers model.
3. `guidedV112Seek` is a separate, prominently described user click. Calculate the midpoint of the currently selected stage from original Mechanical timing, verified by Wiggers profile; quantize 100 × midpoint / RR to the existing 0.1%-step Timeline; dispatch **one** original slider input event. The original handler pauses and synchronizes A/B. Current active view and HR remain intact.

**Prohibitions:** no automatic timeline seek, automatic Wiggers tab switch, new animation loop, new pressure/volume model, change to source nursing/ECG explanation, model-RR filling misinterpretation, or new patient-safety inference.

**QA:** preserve all previous 11 suites and add `tests/test_v112_patch2.py`, including 50 real 10-HR × five-stage Timeline seeks and explicit event-counter verification. Default compact height must stay at or below 908px on 1366×768, full teaching and 360/390px mobile layout must remain. Read [V1.12_PATCH2_REPORT.md](V1.12_PATCH2_REPORT.md). This does not indicate clinical or real-device validation.


## v1.12 Patch 3 — curriculum-driven questions and information depth

- Adds `guided-questions.js`: exactly 5 stages × 2 independent, immutable A/B/C conceptual questions transcribed from the project-approved V1.12_CLINICAL_CURRICULUM.md. No numerical patient prediction, EF/CO calculation or clinical proficiency certification.
- Extends `guided-learning.js` only with `detailLevel=basic|advanced` and a transient `answers[stageId-level]` map; **not** with an alternate physiological clock or persistence. Basic is the initial level; selecting advanced exposes a separately collapsible original PHASES/RATE read-only explanation and the stage's second question.
- Quiz `details` begins closed; before clicking `정답 확인` it shows neither the answer nor feedback. Submission locks the chosen radio and shows grounded correct/incorrect explanation; `다시 풀기` resets **only the active question**. Switching stages/levels or closing the guide preserves the transient answers. Original simulator Reset must not clear learning progress, but a new page load must.
- All existing 12 regression suites and `tests/test_v112_patch3.py` must pass; test question bank/correct key, source text exact equality, retry, answer state isolation, A/B/HR/TIimeline/player unchanged from any quiz control, accessibility/390px no overflow and default 1366×768 ≤910px.
- No extra permanent dashboard panels, timers, network APIs, localStorage/sessionStorage or alteration of the user-approved A/A/A study/Wiggers/seek behavior. Details: [V1.12_PATCH3_REPORT.md](V1.12_PATCH3_REPORT.md).



## v1.12 Patch 4 — student progressive teaching contract

- **basic (1. 기초 이해)**: one simple heart-cycle sentence; concise ECG, valve/pressure and relative LV-volume direction; optional basic concept question. Hide long numeric model midpoint and advanced nursing detail.
- **intermediate (2. 간호 연결)**: reveal short qualitative nursing observation with prior basics; retains the explicit model-RR beginning/end filling difference and relative-value warning.
- **advanced (3. 추가학습)**: only by explicit selection, expose the unchanged original full PHASES/RATE source, limitations, model timing and extra quiz question. Do not delete or alter ten questions or the independent six-part long teaching.
- Next-level button advances one level, native selector may choose any. Level state is separate from five cardiac stages and A/B simulation, preserving existing manual Wiggers view and explicit original Timeline seek.
- No permanently stacked card/default height increase beyond <=910px at 1366x768. Require prior 13 stages plus Patch 4 browser progression/overflow tests; device manual acceptance separately deferred.


## v1.12 Patch 5 — educational consistency & QA contract (2026-10-12)

- **Scope**: clinical-language consistency, explanatory Wiggers filling caveat, current three-level user documentation, readability and boundary regression. No new cardiac physiology, algorithms, animation timers, automatic navigation or persistence.
- **Model fidelity**: retained `wiggers-profile.js` anchor volumes [0.88,0.88,1.00,1.00,0.48,0.48,0.88] and original `mechanics.js` stage boundaries. Initial RR filling is flat 0.88; final RR filling rises 0.48→0.88. Neither is mL, stroke volume or EF; relative pressure never represents patient mmHg.
- **Educational categories**: established physiology (P/QRS/T versus subsequent contraction, pressure gradients, valve transitions, S1/S2); model-specific relative quantities and stage/event boundaries; qualitative nursing observation of ECG, vital signs, perfusion and symptoms.
- **Presentation**: default compact layout unchanged; optional guide still basic → intermediate nursing → advanced source/quiz; mobile caution text increased without shortening old education. Wiggers, source PHASES and ten questions remain accessible.
- **QA gate**: 14 earlier suites plus `tests/test_v112_patch5.py` via `.github/workflows/regression.yml`; test HR list 30/50/59/60/72/80/100/101/120/180, all five stage midpoints and exact boundaries, two filling intervals, keyboard, 360/390/768/1024/1366/1440 widths and automatic screenshots. Browser automation is not user device acceptance.
- **Release**: Patch 5 can be merged only on passing CI; **v1.12 FINAL** label remains deferred until requested real-device manual review and declared scope review. See [V1.12_PATCH5_REPORT.md](V1.12_PATCH5_REPORT.md).


## v1.12 Patch 9 accepted UX contract
- ECG + concise Inspector adjacent on desktop; visuals follow, categorized source index last. Mobile is vertically stacked.
- Free mode retains original A/B, Timeline, controls and views. Guided mode uses native Timeline to pause/seek on explicit previous/next/stage selection; guided reading stays fixed through playback while live statuses keep updating.
- '자료 목록 보기' reveals categories, not every narrative. Each source disclosure is optional. Preserve original clinical six-part source and ten quizzes. No new biomedical outputs.
- Native source-index summary and header control reflect the same open/closed state. No P/PR/QRS/ST/T, Mechanical, Wiggers or ECG canvas duplication.


## v1.12 Patch 10–12 — accepted B-plan education UX (current)
- P10: P/QRS/T annotations show only waveform traversed by the sweep, and inactive highlighted conduction is not confused with pre-playback Ready; no new timing source.
- P11: learner-first 5-stage guided entry from Ready auto-Pauses/Seeks once through native Timeline; step Previous/Next continues guided-only Pause/Seek. Core/gist/navigation precede optional manual tools. Re-entry during free playback never seeks.
- P12: readable 15–16px guided body; mobile ECG component buttons all discoverable without internal side-scroll; clear focus affordance, updated user and developer docs.
- Original A/B clocks, ECG waveform, Electrical/Mechanical/Wiggers, all six-source clinical narratives, ten qualitative quiz questions/feedback, and complete native controls are preserved. No disease/clinical prediction model introduced. v1.12 FINAL requires separate real-device user review.


## v1.12 Patch 13 — quieter educational visualization
- Existing mechanical chamber SVG and mechanical phase/readout appear beside each other at >=900px; mobile stack remains intact. No simulation model or animation update behavior changed.
- Repeated caveats are removed from the default reading flow but accessible through native keyboard/touch expandable educational-model information beside the phase title and the guided study details. Original wording and ten quizzes retained.
- Await real-device visual checks before v1.12 FINAL.


## v1.12 Patch 14 — responsive mechanical usability
- Preserve the original Mechanical SVG, live phase/readout, A/B timing, valve/flow/volume calculations, source notes and all ten guided questions.
- At >=900 CSS px, use an available-space auto-fitting two-column grid for the original SVG and readout; stack if their actual content area cannot fit 320px per cell. Below 900px preserve stacked display.
- Native model note expands inside the readout rather than overlaying adjacent education cards. Both contextual ⓘ notes keep keyboard/touch focus and original caution text.
- Improve live mechanical explanation to 14px and valve/flow/volume readouts to 13px. At small mobile widths, disclosure touch targets are at least 44px high.
- This is a display-only change. Real-device PC/mobile acceptance and v1.12 FINAL remain pending.

## v1.13 integrated Patch 2–6 (implementation branch; NOT FINAL)
- Added the original single-instance Guided rehost in Learning, six-unit lesson course/free browsing, a schema-validated **unreviewed fictitious** clinical case, independent Clinical judgement/action/reassessment session, and Playwright integration tests. See [V1.13_INTEGRATED_PATCH2_TO_6_REPORT.md](V1.13_INTEGRATED_PATCH2_TO_6_REPORT.md).
- Clinical public tab remains **disabled** until expert case-content review; QA-only `?v113Preview=1` allows running the unfinished clinical educational scenario for testing, not patient care. Simulator and Learning are usable.
- Still NOT FINAL pending full CI, clinical reviewer, and physical PC/Android acceptance; v1.12 Patch 14 also remains NOT FINAL. No original physiological model or ten-question bank was edited.
