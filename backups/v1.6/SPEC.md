# SPEC.md
# Cardiac Electrophysiology Simulator Specification

## 1. Project Overview

Cardiac Electrophysiology Simulator is an educational browser-based simulator that visualizes cardiac electrical conduction and its relationship to an ECG waveform.

Educational conduction flow:

SA Node → AV Node → His Bundle → Purkinje System

The project prioritizes visual clarity, synchronization between the conduction model and ECG, and incremental development.

## 2. Current Version

**v1.6**

v1.6 is the UI stabilization milestone. It reorganizes the interface into a compact single-screen layout while preserving the working simulation behavior.

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

## 5. Reserved Panels

### ECG Measurements

Currently a UI placeholder only.

Future candidates:
- HR
- RR interval
- PR interval
- QRS duration
- QT/QTc

No calculated clinical measurements are implemented in v1.6.

### ECG Event / Phase Indicator

Currently a UI placeholder only.

Future synchronization concept:
- SA Node → P wave
- AV Node → PR interval
- His/Purkinje → QRS
- Ventricular recovery → T wave

No separate event engine is implemented in v1.6.

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

## v1.7 — ECG Measurement Engine (Planned)

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
- Implementing ECG Event / Phase Indicator synchronization

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

