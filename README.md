# README.md
# Cardiac Electrophysiology Simulator

An educational browser-based simulator that visualizes cardiac electrical conduction and its relationship to ECG waveform changes.

## Current Version

**v1.9 FINAL — automated tests complete; user visual acceptance pending**

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
Displays:
- HR
- RR interval
- PR interval
- QRS duration
- QT interval
- QTc
- Normal reference ranges

### ECG Event / Phase Indicator
Synchronizes the current ECG event with the cardiac conduction state.

### ECG Component Explanation
Interactive P / PR / QRS / ST / T components provide educational explanations. During playback, the explanation follows the current ECG event; manual selection remains available while paused.

### Simulation State Feedback
Current Phase, ECG Event, ECG explanation, and conduction animation derive from the same `heartState.ecgTime` source. Timeline seeking and Reset keep these states synchronized.

### Educational Rate Scenarios
Provides:
- Normal Sinus Rhythm preset: 72 bpm
- Bradycardia preset: 50 bpm
- Tachycardia preset: 120 bpm
- Direct heart-rate adjustment switches the scenario to Custom
- Reset returns to the Normal preset

The v1.7 scenarios demonstrate rate/cycle-speed differences only; they do not claim physiological HR-dependent interval changes.

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

## v1.7 FINAL Status

v1.7 is the confirmed completion of the ECG-focused educational simulator milestone.

Completed:
- ECG Measurement Engine
- Measurement normal-reference UI
- ECG Event / Phase synchronization
- Explicit His → RBB/LBB conduction-path animation
- Interactive ECG Component Explanation
- Simulation State Feedback / Current Phase integration
- Educational Normal / Bradycardia / Tachycardia scenarios with Custom heart-rate adjustment

The current simulation still uses a simplified educational ECG timing model. In particular, conduction-phase boundaries and ECG-event boundaries are not intended to represent a complete physiological electromechanical model. Physiological timing redesign is deferred to v1.8.

## Next Version — v1.8

v1.8 will focus on the **Physiological ECG Model**, including:
- separation of Physiological / Measurement Time and Visualization Time
- HR-dependent physiological timing relationships
- refinement of RR, PR, QRS, QT and QTc relationships
- preservation of the v1.7 UI and learning flow where practical

Future **Cardiac Cycle & Hemodynamics** work (valve opening/closing, chamber filling/ejection, and blood-flow visualization) should be built on the physiological timing architecture rather than added prematurely to v1.7.

Later roadmap:
- 12-Lead ECG
- ECG interpretation / myocardial ischemia learning
- case and quiz engine

## v1.8 Development Branch Status (2026-10-09)

The current `main` branch contains **v1.8 Patch 2 (A/B time foundation)**. The last fully finalized product baseline is **v1.7 FINAL**. Patch 2 is designed to look and behave exactly like v1.7: the new internal model and visualization clock are separate but use an identity mapping for now. HR-dependent physiological cycle timing is planned for Patch 3, not yet active.

For change details and verification scope, see `SPEC.md` and `DEVLOG.md`.


## Current Development Status — v1.8 Patch 3 (2026-10-09)

Patch 3 is implemented on the development branch (main). The last fully finalized product remains **v1.7 FINAL**. Its visual animation speed and existing UI are intentionally preserved.

- A (Physiological Time) follows the HR-specific beat duration `RR = 60000/HR`.
- B (Visualization Time) uses the existing v1.7 animation pacing. A presentation-phase adapter synchronizes the ECG waveform, conduction, Current Phase, events and Timeline to the real beat fraction.
- **Limit:** PR/QRS/QT still use v1.7 reference timing and are not yet HR-dependent physiological measurements. They will be migrated together in Patch 4; do not interpret them as clinically validated at non-reference heart rates.
- See `SPEC.md` / `DEVLOG.md` for detailed design, verification status and known limitations.

## v1.8 FINAL — A/B Time + Educational Physiological ECG (2026-10-09)

- Physiological Time (A) uses `RR = 60000 / HR` and drives the active P, PR, QRS, ST, T, conduction, ECG event and measurements.
- Visualization Time (B) preserves the calibrated v1.7 HR-based playback rate and existing overall sweep pace; one requestAnimationFrame loop drives both.
- Dynamic PR/QRS/QT/QTc, ECG waveform, Current Phase, events, conduction, cardiac regions, electrical pulses and Timeline share the active timing model.
- ECG morphology amplitudes and dual RBB/LBB conduction pulses remain present. Play, Pause, Reset, manual explanation and HR scenarios are retained.
- **Educational model, not clinical data.** Model coefficients are hand-chosen approximations, not calibrated to patients. At high HR (especially >140 bpm), QT is clipped to avoid overlapping beats; the resulting QT/QTc can be physiologically unrealistic. Bazett QTc also has known rate bias.
- Testing: syntax verified; 239 Chromium end-to-end assertions; 13,741 additional interval/event/seek checks across integer HR 30–180; no JavaScript page errors. User physical-browser visual acceptance is pending.
- Inherited limitation: at 390px mobile viewport there is approximately 47px horizontal overflow, also present in v1.8 Patch 3. It was not worsened or redesigned during the physiological changes.
- v1.8 FINAL runtime backup and Patch 3 reference are stored in `backups/v1.8/`. Start v1.9 from `V1.9_START_HERE.md`.


## v1.9 FINAL — Cardiac Cycle & Hemodynamics (2026-10-09)

Two heart views share the same ECG panel, HR control, Timeline and Play/Pause/Reset:

- **Electrical** (default) shows the unchanged v1.8 conduction SVG, RBB/LBB pulses, ECG waveform, measurements, events and explanations.
- **Mechanical** shows a simplified four-chamber diagram and four valve states (mitral, tricuspid, aortic and pulmonary), filling/ejection animations and contextual explanatory text. The user selects the mode manually; Reset preserves this view preference while clearing simulation state.
- Both views share the *physiological A clock* from `script.js`. A new `mechanics.js` module computes all states as pure functions of physiological phase and the existing electrical timing model. The only animation loop remains the existing requestAnimationFrame driver and B visualization pacing remains unchanged.
- `getMechanicalTiming` derives an educational electrical-to-mechanical lag and the phases atrial systole, isovolumetric contraction, ejection, isovolumetric relaxation and ventricular filling. Qualitative pressure comparisons control both AV and semilunar valve groups. Chamber volume is a relative illustrative scale, **not actual milliliters or ejection fraction**. Blood particles move only while the appropriate valves are open.
- Limitations: the same relative pressure-state profile is used for right/left heart **only for showing valve order**, not realistic right-vs-left pressure magnitudes; phase delays are heuristic; at high HR the existing QT approximation is not validated; flow and valve drawing is schematic (not anatomically scaled); no patient-specific measurements or disease simulation.
- Automatic regression: `python tests/test_v18.py`, `python tests/stress_v18.py`, and `python tests/test_v19.py` all pass. v1.9 testing included 4,711 model/regression assertions over integer HR 30–180; the 239 v1.8 functional and 13,741 stress assertions still pass. JavaScript page errors = 0. Physical-browser visual acceptance remains pending; the inherited 390px horizontal overflow is 437px total width in both v1.8 and v1.9 and was not worsened.
- Start further development using `V1.10_START_HERE.md`.
