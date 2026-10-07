# README.md
# Cardiac Electrophysiology Simulator

An educational browser-based simulator that visualizes cardiac electrical conduction and its relationship to ECG waveform changes.

## Current Version

**v1.6**

## Educational Flow

SA Node → AV Node → His Bundle → Purkinje System

The simulator combines an animated ECG with a cardiac conduction visualization to help learners connect electrical conduction events with ECG components.

## Main Interface

### ECG Monitor
Displays:
- ECG waveform
- Heart rate
- Rhythm classification
- P / PR / QRS / ST / T interpretation

### Cardiac Conduction
Displays the heart conduction pathway and highlights the current conduction stage.

### Compact Controller
Provides:
- Play
- Pause
- Reset
- Cardiac Cycle Timeline
- Heart Rate control

### ECG Measurements
Reserved UI panel for future quantitative ECG measurements.

### ECG Event / Phase Indicator
Reserved UI panel for future synchronization between conduction events and ECG components.

### Current Phase
Displays the active conduction phase, educational explanation, and associated ECG component.

## Heart Rate

Supported range:
**30–180 bpm**

Normal range:
**60–100 bpm**

Normal reference display:
**80 bpm**

Rhythm labels:
- <60 bpm: Bradycardia
- 60–100 bpm: Normal Sinus Rhythm
- >100 bpm: Tachycardia

## Running

No build system is required for the current version.

Open `index.html` in a modern web browser.

## Files

- `index.html` — page structure
- `style.css` — UI/layout styling
- `script.js` — simulation and interaction logic
- `SPEC.md` — specification and roadmap
- `DEVLOG.md` — development history
- `AGENTS.md` — development rules
- `backups/` — confirmed version archives

## Development Philosophy

The project prioritizes:
1. Educational clarity
2. Existing-function stability
3. Incremental changes
4. Readable UI
5. Easy rollback

For substantial changes, inspect the current implementation first, isolate the change, test for regressions, then document and archive the result.

## Versioning

Patch files use:

`Cardiac_Electrophysiology_Simulator_v[version]_UI_patch[number]_[short-description]`

Confirmed versions are archived under `backups/v[version]/`.

---

## v1.7 Development Plan

The next planned version is **v1.7 — ECG Measurement Engine**.

The first functional measurement layer will add:

- HR
- RR interval
- PR interval
- QRS duration
- QT interval
- QTc

These values are simulated educational measurements derived from the simulator model.

### Compatibility Principle

v1.7 preserves the existing v1.6 visualization behavior. In particular, the current ECG animation speed and the existing change in animation speed according to BPM will not be redesigned as part of the measurement implementation.

The measurement engine is an additional calculation layer rather than a replacement for the current visualization timing model.

### Development Sequence

1. Inspect and formalize the existing ECG timing model.
2. Implement the measurement calculation layer.
3. Connect the measurements to the existing `ECG Measurements` UI.
4. Test multiple BPM values.
5. Run regression checks against the existing v1.6 simulation behavior.
6. Confirm v1.7 before archiving the version.

ECG Event / Phase synchronization and expanded conduction-path visualization remain later priorities.
