# DEVLOG.md
# Cardiac Electrophysiology Simulator Development Log

## v1.0 — Initial Simulator
- Established the basic cardiac electrophysiology simulator.
- Added ECG monitor.
- Added cardiac conduction SVG.
- Added Current Phase explanation.
- Added Play / Pause / Reset.
- Established the SA Node → AV Node → His Bundle → Purkinje educational flow.

## v1.1 — Sinus Rhythm ECG Engine
- Introduced programmatic sinus-rhythm ECG generation.
- Added P wave, QRS complex, and T wave modeling.
- Added conduction-step timing.
- Connected ECG progression with cardiac conduction phases.

## v1.2–v1.4 — Simulation / Presentation Refinement
- Refined ECG animation behavior.
- Refined cardiac conduction visualization.
- Improved phase synchronization and controls.
- Refined ECG presentation for educational use.

## v1.5 — ECG / UI Refinement
- Improved ECG canvas presentation and readability.
- Added ECG grid and component interpretation.
- Refined ECG animation speed for educational visibility.
- Corrected intended left-to-right ECG presentation.
- Established 30–180 bpm heart-rate range.
- Established 60–100 bpm normal range.
- Set 80 bpm as the normal reference display.
- Added rhythm labels:
  - Bradycardia <60 bpm
  - Normal Sinus Rhythm 60–100 bpm
  - Tachycardia >100 bpm
- Added/ refined conduction visualization.
- Began the single-screen UI direction.

## v1.6 — UI Stabilization

### Compact Controller
- Moved the controller into the lower area of the ECG Monitor.
- Changed Play / Pause / Reset to a compact vertical arrangement on the left.
- Placed Cardiac Cycle Timeline and Heart Rate controls on the right.
- Reduced slider and spacing dimensions to reduce controller height.
- Reallocated saved vertical space to the ECG display.

### ECG Display
- Increased the visible ECG waveform area.
- Moved the ECG drawing baseline downward to approximately 58% of canvas height.
- Purpose: prevent the large positive QRS deflection from being clipped.
- Waveform amplitude and simulation timing were preserved.

### Information Area
Added UI-only placeholder panels:
- ECG Measurements
- ECG Event / Phase Indicator

These are reserved for future educational functions and do not calculate or animate additional data in v1.6.

### Current Phase Refinement
- Increased Current Phase panel height.
- Increased overall internal padding.
- Increased spacing between:
  - panel title and phase title
  - phase title and description
  - description and ECG component row
- Positioned the ECG component row toward the lower portion of the panel.
- This was finalized as the successful **UI patch 4**.

### Final v1.6 UI Patch Record
Successful patch:
`Cardiac_Electrophysiology_Simulator_v1.6_UI_patch4_current_phase_spacing`

Earlier experimental Current Phase patches were superseded and are not treated as the final v1.6 state.

## v1.6 Final Status

v1.6 is now considered a stable UI milestone pending final user confirmation of the complete project package.

Primary accomplishments:
- Compact controller
- Larger ECG display
- Improved ECG baseline positioning
- Reserved ECG analysis/event panels
- Improved Current Phase spacing
- Single-screen-oriented layout
- Development documentation and backup structure

## Next Development Direction

Before implementing new functionality:
1. Review and prioritize future features.
2. Define the behavior in SPEC.md.
3. Implement one isolated feature at a time.
4. Test existing functions for regression.
5. Update DEVLOG.md.
6. Archive the confirmed version before moving to the next version.

## Patch Naming Convention

`Cardiac_Electrophysiology_Simulator_v[version]_UI_patch[number]_[short-description]`

Example:
`Cardiac_Electrophysiology_Simulator_v1.6_UI_patch4_current_phase_spacing`

Patch numbers restart for each new version.

---

## v1.6 UI Patch 8 — Heart Rate Scale Alignment

**Status:** Confirmed

Fixed the Heart Rate controller alignment so the scale labels and normal-range indicator align with the slider's effective thumb positions.

The patch was limited to the UI layer and did not alter ECG, conduction, timeline, or heart-rate simulation logic.

Earlier experimental alignment patches were superseded by the confirmed final patch.

---

## v1.7 — ECG Measurement Engine

**Status: Completed — patch2 confirmed**

### patch1 — Measurement Engine

Implemented the first functional ECG measurement layer:
- Heart Rate
- RR Interval
- PR Interval
- QRS Duration
- QT Interval
- QTc

The measurement layer uses the existing ECG timing/model information and does not replace the visualization timing system.

RR follows:

`RR (ms) = 60000 / HR (bpm)`

QTc uses the existing correction calculation.

### patch2 — Measurement Reference UI

Implemented:
- Removed the temporary `Simulated educational measurements based on the current ECG model.` user-facing note.
- Added a normal reference range beneath each measurement.
- Retained PR = **220 ms** because it is derived from the current model timing.
- QT is presented as **HR-dependent**.
- QTc displays adult sex-specific upper reference limits.

### patch2 — Final Layout

The two lower information areas are independent sibling panels:
- `ECG Measurements`
- `ECG Event / Phase Indicator`

The final layout gives `ECG Measurements` more horizontal space while keeping the Indicator as a separate panel.

Inside `ECG Measurements`:
- The two measurement columns are equal width.
- The QTc reference is displayed on one line.

Intermediate panel ratios used during UI tuning were superseded and are not current specifications.

### Regression / Preservation

The following were intentionally preserved:
- ECG visualization speed
- BPM-dependent visualization-speed behavior
- ECG waveform presentation
- Conduction animation
- Cardiac Cycle Timeline
- Play / Pause / Reset
- Current Phase
- Rhythm classification

No JavaScript/simulation logic was changed for the final patch2 UI adjustments.

### Known Model Limitation

The current ECG timing model is a simplified educational model rather than a fully physiological ECG timing engine. A model-derived PR value can therefore fall outside the displayed general adult reference range without indicating a software calculation error.

### Architecture Decision

The project intentionally separates the current visualization behavior from future physiological timing work.

A future architecture may define:
- **Physiological / Measurement Time (A)**
- **Visualization Time (B)**

The A/B mapping is deferred and must not be introduced incidentally into unrelated patches.

### Current Baseline

**v1.7 patch3** is the confirmed working baseline.

### Next Development Priority

**Explicit Conduction-Path Animation**

The next implementation should consume the existing ECG/simulation state and display the current ECG event/phase while avoiding a competing timer or animation loop.

### Future Feature Roadmap

1. ECG Event / Phase Indicator synchronization.
2. More explicit conduction-path animation and phase feedback.
3. Dedicated Physiological ECG Timing Model.
4. Explicit A/B mapping between physiological and visualization time.
5. More physiologically consistent HR-dependent interval behavior.
6. Expanded rhythm/ECG educational scenarios.
7. Interactive ECG component explanations and clearer simulation-state feedback.
8. Additional rhythm modes and broader cardiac physiology/arrhythmia expansion.

### Development Workflow Going Forward

Before each new feature:
1. Inspect the current implementation.
2. Identify affected files and state/rendering/event/layout paths.
3. Review regression risks and feature conflicts.
4. Implement the smallest reasonable change.
5. Test existing behavior.
6. Obtain user verification.
7. Update documentation.
8. Archive the confirmed version.

Intermediate experimental patches that were superseded during v1.7 patch2 layout tuning are not treated as confirmed versions.


---

## v1.7 patch3 — ECG Event / Phase Indicator Synchronization

Implemented the next v1.7 feature on top of the v1.7 patch2 baseline.

### Implementation
- Added a dedicated ECG event mapping based on the simulator's existing waveform timing.
- Connected the `ECG Event / Phase Indicator` panel to `heartState.ecgTime`.
- Added active conduction-stage feedback to the existing SA Node → AV Node → His Bundle → Purkinje flow.
- Updated ECG interpretation highlighting from the current ECG event rather than only the broader conduction step.
- Removed the placeholder synchronization note and replaced it with a live synchronization status.
- Preserved the existing `requestAnimationFrame` animation loop and did not add a competing timer or animation loop.
- Kept the existing BPM-dependent visualization speed, waveform timing, conduction animation, timeline, playback, and measurement behavior unchanged.

### ECG Event Mapping
- 0–80 ms: Baseline
- 80–160 ms: P Wave
- 160–300 ms: PR Interval
- 300–380 ms: QRS Complex
- 380–500 ms: ST Segment
- 500–680 ms: T Wave
- 680 ms–end of cycle: Baseline

### Boundary Handling
The existing conduction model ends at 700 ms while the 72-bpm cardiac cycle is approximately 833 ms. The new Event Indicator treats the remaining cycle as baseline/resting and does not redesign the existing Current Phase behavior.

### Verification Status
Static JavaScript syntax validation passed. Manual browser verification is still required for visual behavior and interaction regression before v1.7 is considered confirmed.

### Version Boundary
v1.7 remains focused on completing the current educational visualization model. Physiological ECG timing redesign and Physiological Time (A) / Visualization Time (B) separation remain deferred to v1.8.

---

## v1.7 patch4 — Explicit Conduction-Path Animation

Implemented on top of the user-verified v1.7 patch3 build.

### Implementation
- Added separate right- and left-sided conduction pulse elements.
- During the Purkinje activation interval (380–450 ms), the visual pulse now propagates simultaneously toward the right and left bundle branch endpoints.
- The existing single pulse remains responsible for SA → AV → His → bifurcation movement.
- Branch pulse position and visibility are driven by the existing `heartState.ecgTime` update path.
- No new timer, animation loop, or simulation clock was introduced.
- Reset explicitly hides and re-centers both branch pulses.

### Educational Intent
The impulse is now visually represented as splitting into the right and left ventricular conduction pathways rather than appearing to move sequentially across the lower heart.

### Regression Scope
The ECG waveform, measurement engine, BPM-dependent visualization speed, ECG Event / Phase Indicator, Timeline, Play/Pause/Reset behavior, and existing conduction timing remain unchanged.

### Version Status
**v1.7 patch4** is the current development build pending user verification.

## v1.7 patch5 — Interactive ECG Component Explanation

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
- Restored the ECG component button font sizing to the v1.7 patch4 scale after the button conversion had overridden the responsive font-size.
- The explanation is inline to avoid modal focus/transition issues.

### Version Status
**v1.7 patch5** is the current development build pending user verification.



## v1.7 patch6 — Simulation State Feedback / Current Phase Integration

Implemented on top of the user-verified v1.7 patch5 build.

### Implementation
- Kept `heartState.ecgTime` as the sole simulation clock.
- Unified visible feedback so Current Phase, ECG Event, ECG explanation, and existing conduction animation all derive from the same time position.
- Replaced the Current Phase ECG label's dependency on the broader conduction step with the canonical ECG event label.
- Added forced synchronization for timeline seeks, including seeks that remain within the same conduction step but cross an ECG-event boundary.
- Reset now clears manual ECG selection and restores the pre-playback Ready state consistently.
- Consolidated duplicate `.ecg-item` font-size declarations without changing the intended patch5 visual scale.

### Important Boundary Note
The existing model intentionally has conduction and ECG-event boundaries that do not map one-to-one. For example, Purkinje activation spans 380–450 ms while the QRS event ends at 380 ms and ST begins at 380 ms. Patch6 does not change that timing model; physiological timing redesign remains deferred to v1.8.

### Regression Review
- No competing timer or animation loop introduced.
- No changes to ECG waveform generation, measurement engine, BPM-dependent visualization speed, or patch4 branch pulse animation.
- Timeline, reset, manual explanation selection, and responsive ECG component controls require browser verification at all event/phase boundaries.

**v1.7 patch6** is the current development build pending user verification.


## v1.7 patch7 — Educational Rate Scenarios

Implemented on top of the user-verified patch6 build.

### Implementation
- Added educational rate presets:
  - Normal Sinus Rhythm — 72 bpm
  - Bradycardia — 50 bpm
  - Tachycardia — 120 bpm
- Existing heart-rate control remains available.
- Direct heart-rate changes switch the scenario state to Custom.
- Reset returns to the Normal preset.
- Scenario descriptions are educational and focus on rate/cycle-speed differences.

### Scope
The patch does not introduce HR-dependent physiological changes to PR, QRS, QT, or QTc. Those relationships are deferred to the v1.8 physiological timing model.

### Regression Review
- Reused the existing heart-rate state and `heartState.ecgTime`.
- No new timer or animation loop introduced.
- Existing ECG waveform, measurements, conduction animation, Current Phase, ECG Event, Explanation, Timeline, and playback controls remain the same.

**v1.7 patch7** was user-tested as the final development build.

## v1.7 FINAL — Version Closure

v1.7 is closed after patch7.

The version establishes a complete educational ECG/conduction learning flow:
- measurement
- ECG event synchronization
- explicit conduction-path animation
- interactive/automatic ECG component explanation
- unified simulation-state feedback
- educational rate scenarios

### Final Known Limitation

The timing model remains intentionally simplified. In particular, Purkinje activation and ECG-event boundaries are not a complete physiological electromechanical representation. This is documented as a v1.8 redesign target rather than patched into v1.7.

### Next Version

v1.8 begins with physiological timing architecture:
- Physiological / Measurement Time
- Visualization Time
- HR-dependent timing
- preserved v1.7 UI and state flow

Later work can then add Cardiac Cycle & Hemodynamics, including valve motion, chamber filling/ejection, and blood-flow visualization.

## v1.8 — Patch 1: Central Timing Model Foundation (2026-10-09)

### Added
- `CARDIAC_TIMING_MODEL` holds v1.7's existing ECG and conduction timings.
- `getCardiacTimingModel()` is the initial access point for later HR-dependent timing logic.
- v1.7-compatible `baseCycleLength` alias remains available.
- `backups/v1.8/patch1_baseline/` preserves the original v1.7 runtime files.

### Changed
- ECG measurement timing, ECG event intervals and conduction-step timing now reference the central static model.

### Preserved
- No changes to heart-rate physiology, A/B time separation, animation speed, visual waveform morphology, HTML, CSS, interaction controls, or runtime screen behavior.

### Verification (scope)
- `node --check script.js` succeeded.
- Headless Chromium/Playwright compared **110 deterministic states** between v1.7 and Patch 1 (heart-rate values 30–180 bpm, Timeline positions, measurements, ECG canvas, conduction state, event/phase, explanations, selection, Play/Pause/Reset); **0 differences** for stable comparable states, **0 page errors**. Dynamic elapsed-time fields during active playback were excluded from exact equality.
- Browser test used injected HTML/CSS/JS because opening local files and localhost was blocked by the test environment; physical-device UX and deployed GitHub Pages were not verified.

### Known limitations / next
- ECG waveform generation still includes v1.7 absolute-time boundaries.
- The current static cycle and HR-to-animation-speed coupling remain by design until the physiological clock and visualization clock are safely separated.
- Plan next patch carefully: avoid HR double application, preserve the v1.7 pace, and test RR/cycle-boundary interactions, Timeline seeking and sweep synchronization.
