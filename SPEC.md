# SPEC.md
# Cardiac Electrophysiology Simulator Specification

## 1. Project Overview

Cardiac Electrophysiology Simulator is an educational browser-based simulator that visualizes cardiac electrical conduction and its relationship to an ECG waveform.

Educational conduction flow:

SA Node → AV Node → His Bundle → Purkinje System

The project prioritizes visual clarity, synchronization between the conduction model and ECG, and incremental development.

## 2. Current Version

**v1.7 FINAL**

v1.6 was the UI stabilization milestone. v1.7 patch2 was the confirmed measurement baseline. v1.7 is now complete through patch7.

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
