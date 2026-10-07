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

**Status:** Planning

### Planned Scope

Add the first functional ECG measurement layer:

- HR
- RR interval
- PR interval
- QRS duration
- QT interval
- QTc

The existing `ECG Measurements` placeholder will be replaced with simulated educational values.

### Core Implementation Principle

v1.7 will **not** redesign the existing visualization timing.

The following v1.6 behaviors are explicitly preserved:

- Current ECG animation speed
- BPM-dependent animation-speed changes
- ECG waveform presentation
- Conduction animation
- Cardiac Cycle Timeline
- Play / Pause / Reset
- Current Phase
- Rhythm classification

The measurement layer will be added independently from the visualization/animation layer.

### Measurement Interpretation

The measurements represent the simulator's calculated educational model values, not real patient ECG measurements.

RR may be calculated from the selected heart rate:

`RR (ms) = 60000 / HR (bpm)`

Other interval measurements will use the simulator's defined ECG timing model.

### Regression Priority

Before finalizing v1.7, verify:

1. HR changes still produce the same visual speed behavior as v1.6.
2. ECG waveform animation remains stable.
3. Conduction animation remains synchronized with the existing simulator behavior.
4. Cardiac Cycle Timeline remains unchanged.
5. Play / Pause / Reset remain functional.
6. Current Phase and rhythm classification remain functional.
7. Measurement values update correctly without altering visualization behavior.

### Future Timing Model

A future version may revise the relationship between physiological timing and visualization timing. Such a redesign is intentionally outside the scope of v1.7.


---

## v1.7 UI Patch 2 — Measurement Reference Ranges

**Status:** Implemented

### Changes
- Removed the temporary measurement-panel note describing the values as simulated educational measurements.
- Added a normal reference range beneath each ECG measurement.
- Kept the existing HR, RR, PR, QRS, QT, and QTc calculation logic unchanged.
- Kept the current PR result of 220 ms unchanged; no waveform timing was modified.
- QT is labeled as HR-dependent rather than being assigned a fixed normal range.
- QTc reference is displayed with sex-specific adult upper limits.

### Explicitly Not Changed
- ECG visualization speed
- BPM-dependent animation-speed behavior
- ECG waveform timing
- Conduction animation
- Cardiac Cycle Timeline
- Play / Pause / Reset behavior
- Physiological Time / Visualization Time A/B separation

### Future Work
A dedicated Physiological ECG Timing Model and explicit A/B time mapping remain future work and are not part of v1.7 patch2.


### v1.7 UI Patch 2 Final — Measurement Panel Width

**Status:** Confirmed for testing

Adjusted the lower two-panel layout so `ECG Measurements` receives approximately 35% more horizontal space relative to `ECG Event / Phase Indicator`.

- Measurement column: `1.35fr`
- Event / Phase column: `1fr`
- Existing measurement calculations remain unchanged.
- Existing ECG visualization and animation behavior remain unchanged.
- The adjustment is made at the parent grid level to avoid fixed-width overflow.
- Mobile behavior remains governed by the existing responsive layout.

This is a presentation-only adjustment within v1.7 patch2.


### v1.7 UI Patch 2 Final — Information Panel Proportion

**Status:** Final revision for user testing

The two independent information panels were resized at their parent layout level:

- ECG Measurements: `1.1fr` (approximately 36.7% of the available panel width)
- ECG Event / Phase Indicator: `1.9fr` (approximately 63.3%)

This increases the Measurement panel by approximately 37.5% relative to its previous width while reducing the Indicator panel proportionally.

The existing two-column measurement content remains responsive inside the wider Measurement panel, so its internal items expand with the panel rather than using a fixed width.

No JavaScript, measurement calculations, ECG animation, conduction behavior, or timeline behavior were changed.


### v1.7 UI Patch 2 Final Adjustment — Equal Measurement Columns

**Status:** Final revision for testing

The two cards/columns inside `ECG Measurements` now have equal widths.

- Measurement panel outer width remains the widened `1.1fr : 1.9fr` layout.
- Internal measurement columns are `minmax(0, 1fr) : minmax(0, 1fr)`.
- Each measurement item uses `min-width: 0` so long QTc reference text cannot widen one column.
- No JavaScript or simulation behavior changed.


### v1.7 UI Patch 2 Final Adjustment — QTc Reference Single Line

**Status:** Final revision for testing

The sibling panel ratio was adjusted to give `ECG Measurements` additional horizontal space:

- ECG Measurements: `1.25fr` (approximately 41.7%)
- ECG Event / Phase Indicator: `1.75fr` (approximately 58.3%)

The two internal measurement columns remain equal-width. Reference text is kept on one line so the QTc reference does not wrap.

No JavaScript or simulation behavior was changed.
