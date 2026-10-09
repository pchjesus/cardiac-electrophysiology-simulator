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

## v1.8 — Patch 2: Physiological / Visualization Time Adapter (2026-10-09)

### Added
- `heartState.physiologicalTime` (A), `heartState.visualizationTime` (B), and a synchronized deprecated `ecgTime` compatibility mirror.
- Explicit adapter functions: `getVisualizationDelta()`, `getPhysiologicalDelta()`, `advanceSimulationClocks()`.
- Pure `getPhysiologicalRR(hr)` reused in measurement calculation.
- `backups/v1.8/patch2_baseline/script.js` stores the verified Patch 1 script.

### Changed
- ECG sampling, conduction, Current Phase/Event, Timeline, and seek reconstruction read A instead of the legacy alias.
- Sweep consumes B's already HR-scaled delta; HR multiplier is applied only once.
- Reset, seek and frame update synchronize A/B and legacy alias.

### Intentionally unchanged
- A and B have equal elapsed values in Patch 2 (identity adapter). **This is preparation for physiological RR in Patch 3, not its activation.**
- Existing fixed cycle/event boundaries, ECG waveform morphology, conduction stages, HR-to-speed curve, single animation loop, UI, Play/Pause and Reset behavior.

### Verification performed
- `node --check script.js` passed.
- Headless Chromium / Playwright compared **237 deterministic Patch 1 vs Patch 2 states**: HR 30,50,60,72,80,100,120,180; twelve Timeline positions at each HR; simulated elapsed frames; ECG canvas and cursor; conduction state; Current Phase/ECG Event; manual QRS explanation; Play/Pause/Reset.
- Additional 3 long frame runs (275 simulated 50-ms frames each) exercised cycle/sweep wrapping, with periodic state comparisons.
- A = B = legacy alias after frame advances, Timeline seek, reset and actual rAF live playback: verified.
- RR calculation evaluated at 8 HR values: expected `60000/hr`.
- JavaScript page errors: 0 in both baseline and updated browser pages.
- The first exact comparison during Play encountered ordinary rAF scheduling differences between two browser pages; the test harness then disabled rAF **only during synchronous Play/Pause snapshots**, re-enabled it for live playback, and completed without mismatches. This was a test-harness timing issue, not an observed application regression.

### Known issues / next
- Visually calibrated on automated browser snapshots, not manually assessed on every physical device.
- Patch 3 requires physiological RR, phase boundaries and waveform durations to be changed coherently, avoiding HR double-speed and temporary clinically misleading interval values.
- No new functionality in Patch 2 changes educational clinical outputs beyond centralizing the existing RR calculation.


## v1.8 — Patch 3: HR-Dependent Physiological RR and Phase Adapter (2026-10-09)

### Added
- Active physiological cycle length `getActiveCycleLength()`, cycle-position resolver `getPhysiologicalCyclePhase()`, and reference presentation resolver `getReferenceCyclePhase()`.
- Beat anchor `heartState.cycleStartTime` to allow changes to HR without resetting elapsed A.
- `synchronizeCycleLength()` reanchors the beat on HR slider changes while preserving the current normalized phase.
- Backup `backups/v1.8/patch3_baseline/script.js` of the verified previous Patch 2 script.

### Changed
- A now advances by the dynamic `RR / baseCycleLength` conversion from B; HR-to-speed is still applied only in B.
- Timeline/seek, ECG sampling/history reconstruction, conduction, Current Phase and event status all use the consistent physiological-to-reference phase adapter.
- Reset and HR changes reconcile A, B, and the cycle anchor.

### Explicitly not changed
- The v1.7 perceived visual cycle cadence, RBB/LBB branching, ECG morphology and amplitudes, UI, CSS, original event segmentation, PR/QRS/QT measurement values or QTc formula.
- These interval labels are **provisional baseline reference values**, not dynamically calibrated physical intervals. Patch 4 is required.

### Verification
- `node --check script.js`: PASS.
- Headless Chromium via Playwright, injecting unchanged HTML/CSS and Patch 2/3 scripts: **312 deterministic comparison states** covering HR 30,50,60,72,80,100,120,180 bpm; seek at 13 percentages; repeated delta steps; 3 long-run wrap sequences; mid-beat HR swaps, manual ECG explanation, Play/Pause/Reset and actual requestAnimationFrame playback.
- ECG canvas image comparisons: **0 differences** across 312 states; ECG sample x/y max difference about 3.3e-11 pixels; 0 JavaScript errors.
- Found **3 tiny boundary-classification differences** at an exact event boundary during long runs due to floating-point rounding (e.g. near 380 ms): no missing phase/event, but a one-frame edge case to stabilize during the dedicated boundary/event patch.
- Assertions verified physiological RR=60000/HR, physical phase fraction = presentation reference phase fraction, and A/legacy mirror consistency.
- Manual visual verification in the end user's browser and dedicated high-rate clinical interval verification are not yet completed.

### Next: Patch 4
- Scientific HR-dependent PR/QRS/QT model; keep QRS relatively stable, explicitly justify QT correction assumptions, and replace temporary reference interval projection so measurements and physical waveform represent the same model.
- Preserve animation pacing, verify ECG labels/events/conduction, and test transitions/seek/wrap at HR extremes.

## v1.8 Patch 4 — HR-Dependent Electrical Interval Model (2026-10-09)
Added `getPhysiologicalTiming()` with RR/PR/QRS/QT, ST, P and conduction boundaries. The chosen coefficients are educational approximations, not calibrated to clinical data. No visible changes at this isolated foundation stage.

## v1.8 Patch 5 — ECG Waveform and Measurement Alignment
ECG waveform samples and PR/QRS/QT/QTc now consume the active interval model. P/QRS/T amplitudes remain unchanged. Interval display values rounded to milliseconds.

## v1.8 Patch 6 — Conduction Timing Alignment
SA, AV, His, bundle branches, Purkinje and recovery use the active physical timing model; RBB/LBB dual pulse paths preserved. Purkinje deliberately ends with QRS instead of extending beyond it.

## v1.8 Patch 7 — ECG Events, Current Phase and Timeline
Physical beat intervals now drive event classification, Current Phase labels, conduction visual steps, ECG label positions, Timeline and seek. Presentation positions are mapped to the B clock.

## v1.8 Patch 8 — Playback/Reset/Seek Robustness
Added a playback-generation guard to prevent stale queued rAF callbacks after rapid pause/play transitions, constant-time cardiac-cycle wrap logic, and safe 100% seek bounds.

## v1.8 Patch 9 — Sweep Calibration
Preserved fractional sweep overshoot across screen wrap, corrected Timeline-reconstructed ECG baseline to the actual canvas baseline. Preserved the v1.7 rate-to-display curve.

## v1.8 Patch 10 — FINAL Automated Regression / Documentation / Archive
Removed unused static measurement table, revised stale reference comments and updated HTML version to v1.8 FINAL. Consolidated docs and prepared V1.9_START_HERE.md.
- Syntax: node --check script.js PASS.
- Browser: 239 assertions across HR 30,50,60,72,80,100,120,150,180; Play/Pause/Reset, HR swaps, Timeline seek, ECG event, conduction, measurements, current phase, sweep, live rAF; page errors 0.
- Full HR sweep: 13,741 assertions across all integer HR 30–180, including 4,077 event boundary samples and 1,208 seek states; errors 0.
- Presentation speed B and sweep position matched the verified Patch 3 at tested rates; dynamic waveform/interval timing intentionally differs.
- Known limits: high-rate QT clipping to non-overlap SA-first beats (not clinically validated); Bazett rate bias; inherited 390px mobile horizontal overflow (~47px); manual physical browser acceptance pending.
- New next-version handoff: V1.9_START_HERE.md.


## v1.9 FINAL — Cardiac Mechanics & Hemodynamics (2026-10-09)

- **Patch 1 — Requirements/impact analysis:** protected v1.8 A/B pacing, electrical view, ECG and all controls. UX selected: mode switch only within heart-visualization region.
- **Patch 2 — Mechanical timing engine:** implemented phase boundaries from ECG events with deliberate electrical-to-mechanical lags; high-HR QT is not used as the mechanical timing anchor.
- **Patch 3 — Pressure/valve model:** modeled pressure-gradient rules (conceptual indexes), synchronizing mitral/tricuspid and aortic/pulmonary valve groups. No independent right/left pressure magnitudes.
- **Patch 4 — Chamber filling/ejection:** relative ventricular volume stays constant in isovolumetric phases, increases with filling, and falls during ejection. Atria visually contract in atrial systole.
- **Patch 5 — Blood-flow visualization:** color-coded forward-flow paths and deterministic particles, visible only when the matching valves are open.
- **Patch 6 — Educational explanation:** phase explanation, valve statuses, flow and normalized volume in the Mechanical view.
- **Patch 7 — UI mode integration:** Electrical/Mechanical buttons; unchanged ECG monitor and original electrical SVG, keyboard focus and aria-pressed semantics.
- **Patch 8 — A/B state synchronization:** current physiological phase is recomputed during Play/Pause, Timeline seek, HR update, mode switching and Reset; UI preference persists after Reset. No new requestAnimationFrame.
- **Patch 9 — Automated regression:** 4,711 v1.9 assertions (HR 30–180 incl. interval/valve/flow constraints and baseline equivalence), inherited 239 v1.8 functional assertions, and 13,741 v1.8 stress assertions PASS; 0 JavaScript execution errors; mobile overflow unchanged (437px content width on 390px viewport).

**Verified:** code syntax, headless Chromium application runs, responsive smoke, replay/seek/reset, pressure/valve consistency and baseline ECG timing/measurements.
**Not verified:** actual user-device acceptance, physiological calibration of numeric pressure/volume or extreme tachycardia behavior, clinical interpretation. This remains a teaching simulator only.
**Design compromises:** separate diagrams by user-selected mode, same modeled valve timing on left/right sides, approximate chamber ellipse changes (not actual mechanical deformation), synthetic pressure indexes and heuristic delays. No unrequested ECG or controller redesign.


## v1.10 Patch 1 — Passive Wiggers Foundation (implementation)

- Confirmed `main` baseline `dbfb60e84ef7919f7a65ec45bcab322b8895995a` and v1.9 backup.
- Added `wiggers.js` as a read-only consumer of `getMechanicalTiming()` / `getMechanicalState()` with explicit physiological-time inputs; the new script is loaded after `mechanics.js`.
- Added a deterministic Wiggers snapshot contract for electrical timing boundaries, mechanical stages, existing qualitative pressure, unchanged normalized ventricular volume, left-side reference valve events and S1/S2 markers.
- Added `inspectPressureBoundaries()` to expose the pre-existing pressure jumps instead of hiding them behind an invented smooth curve.
- Kept `script.js`, `mechanics.js`, `style.css`, and archived v1.9 files untouched. No Wiggers UI, new timer/rAF, sound player, clinical pressure units, or independent RH/LH physiology.
- Added `tests/test_v110.py` for HR 30–180, event boundaries, model purity, pressure/valve/volume consistency, v1.9 runtime equivalence and basic UI interactions. Added GitHub Actions regression workflow for v1.8–v1.10 checks.
- **Verification reporting:** Record final executed test results independently. Newly committed test code and workflow presence alone do not mean automatic or device verification passed.
- **Next:** Patch 2 validated continuous pressure/volume profile; protect the existing Mechanical display and clarify whether derived valve events or pressure-crossing logic becomes authoritative.


### Patch 1 verification (GitHub Actions run 37895290190)

- `tests/test_v18.py`: **239 PASS**.
- `tests/stress_v18.py`: **13,741 PASS**.
- `tests/test_v19.py`: **4,711 PASS**.
- `tests/test_v110.py`: **7,167 PASS**.
- Chromium page errors: **0**. Total: **25,858** assertions/checks. This is automated, not user-device/clinical acceptance.
- The initial CI runner failure was an existing `/usr/bin/chromium` symlink collision (fixed in the CI workflow, unrelated to application code).
- First v1.10 test revealed a **pre-existing v1.9 exact-boundary rounding issue**: the double modulo in the mechanical phase calculation can round a mathematical boundary to the preceding interval when RR is fractional (reproduced at HR 33). The test now checks representative valve states immediately *before and after* each transition (±0.0001 ms), rather than requiring one arbitrary outcome at an exact floating-point tie. Do not silently change the v1.9 mechanical domain engine in Patch 1.
- **Patch 2 requirement:** define an explicit half-open interval/event tie-break contract before introducing smooth relative pressure curves; verify pressure equalities/crossings, valve switching and volume invariants at both sides of every boundary.
- User physical-browser visual review and calibration/clinical validation are still pending.


## v1.10 Patch 2 — Continuous Relative Pressure / Volume Profile

- Confirmed start `main` / v1.10 Patch 1 SHA `d46a6a30b10e766d9dd6da05f795b8dacb8a9e2f`. Saved immutable rollback branch `backup/v1.10-patch1-verified`.
- Added `wiggers-profile.js`: independent, read-only continuous educational left-heart pressure and normalized volume functions. It reuses the existing A-time and `CardiacMechanical.getMechanicalTiming()` but does NOT change `script.js`, `mechanics.js`, or the first `wiggers.js` foundation.
- Built consistent C1-smooth stage pressure joins (including cycle wrap), an illustrative ventricular ejection pressure arch, smooth relative volume changes, fixed isovolumetric volumes and event/gradient-consistent valve states.
- Adopted explicit event-tie contract for **new profile only**. At equal pressure the named valve event determines the post-event state, rather than relying on floating-point comparisons. v1.9 retains its known exact-boundary double-modulo behavior.
- Loaded `wiggers-profile.js` after `wiggers.js`, no new UI, timer or rAF. Existing Mechanical display continues consuming legacy `getMechanicalState()`; new profile is **not** advertised as a user-facing change.
- Added `tests/test_v110_patch2.py`, extended regression workflow, specified scope and limits in `SPEC.md`. Full CI result to be appended after execution.
- Known limitations: high-HR ECG QT clipping and Bazett rate bias remain; volume/pressure values are synthetic and uncalibrated; no dedicated right heart or independent vascular mechanics; legacy 390px overflow remains; actual user-device visual and clinical validation outstanding.
- **Next:** Patch 3 expandable Wiggers teaching panel (chosen A UX), synced via single existing A/B playback adapter, with keyboard/viewport review and graph/event mismatch checks.


### Patch 2 executed regression evidence

GitHub Actions PR run: https://github.com/pchjesus/cardiac-electrophysiology-simulator/actions/runs/37953779360 — **all five steps passed**.
- v1.8 functional: **239 checks PASS**
- v1.8 HR stress: **13,741 checks PASS**
- v1.9 mechanical: **4,711 checks PASS**
- v1.10 Patch 1: **7,167 checks PASS**
- v1.10 Patch 2: **422,404 checks PASS** (151 integer HR inputs, pressure/volume continuity, relative gradient direction, event tie and periodicity, isovolumetric invariants and v1.9 deterministic state comparison)
- JavaScript page errors: **0** in new and baseline browser pages.
- Combined check count: **448,262**. This is automated test coverage, not clinical validation or human-device visual acceptance.
- Diagnostic finding and fix: initial static review showed 78/151 HR values produced a floating-point event-boundary mismatch when querying a mathematically equivalent phase at `phase+RR`. The new profile now canonicalizes only IEEE-754-scale ties (capped at 1e-8 ms); the rechecked cycle-equivalence scan found 0 mismatches over HR 30–180. v1.9 Mechanical code is unchanged.
- Graph UI remains unimplemented; no user browser visual inspection required for this passive model-only patch. Human acceptance is still pending for v1.9 and future graphical Wiggers Patch 3.


## v1.10 Patch 3 — Optional Wiggers Diagram

- Baseline verified as v1.10 Patch 2 `main` SHA `65f984196ce1ede0e2eaa2ce9570d689060aeeb0`.
- Added native collapsed `<details>` panel after existing user information, with separate single-RR ECG, left atrial/LV/aortic **relative** pressure traces, normalized LV volume, valve events and S1/S2 *marker labels*. Existing monitor sweep and heart diagram are unchanged.
- Added `wiggers-view.js`, a source-backed SVG renderer querying existing `ecgValue` and `CardiacWiggersProfile` with 481 points per beat. Uses only existing A-clock phase; it does not own a timer/rAF and skips rendering when closed. Cached plots rebuild only on HR/timing changes.
- Added three optional hooks for frame synchronization, HR change and Reset in `script.js`. Existing `mechanics.js`, Wiggers domain models and legacy CSS selectors remain unchanged; new styles are namespaced.
- Added keyboard-accessible disclosure, text readouts without per-frame `aria-live` announcements, local horizontal SVG scroll, clear unit warning and explicit single RR/monitor sweep distinction.
- Tests: `tests/test_v110_patch3.py` and the full 6-step workflow; execution results must be appended **after successful CI**. Browser rendering and manual user visual acceptance are separate from automatic functional validation.
- Known inherited issues: 390px horizontal overflow, extreme-HR clinical interval limits, Bazett bias and v1.9 exact-boundary floating-point Mechanical tie. Pressure/volume are heuristic non-clinical indexes. Follow-on Patch 4 explains valve transitions and S1/S2 more deeply.
