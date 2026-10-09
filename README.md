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


## v1.10 Patch 1 Development — Wiggers Model Foundation

The confirmed visible baseline remains **v1.9 FINAL**. This patch adds a passive `wiggers.js` model with no new UI panel and no changes to ECG, Mechanical mode, playback or animation speed.

The browser API `window.CardiacWiggers.getSnapshot(phaseMs, getActiveTiming())` exposes consistent electrical/mechanical timestamps, current v1.9 *relative educational* pressure and ventricular volume, left-sided conceptual valve markers, and S1/S2 event markers. `inspectPressureBoundaries()` explicitly reports discontinuities in the existing v1.9 pressure indexes. These are **not calibrated physiological pressure traces**. Do not interpret the values as mmHg, mL, ejection fraction or patient data.

Files: `wiggers.js` (model), `tests/test_v110.py` (contract and v1.9 regression), `.github/workflows/regression.yml` (automated browser regression). Run all v1.8, v1.9 and v1.10 tests before accepting this patch. The synchronized visual Wiggers panel is planned for a later patch; user-device visual acceptance remains pending.

Next: v1.10 Patch 2 pressure/volume continuity and shared valve-state consistency.


## v1.10 Patch 2 — Continuous Teaching Profile (internal)

`wiggers-profile.js` adds a **separate, passive** continuous relative-pressure and ventricular-volume profile for future Wiggers visualization. It is NOT a user-visible panel and does NOT replace the v1.9 Electrical/Mechanical controls or alter their animation speed. The original `wiggers.js` snapshot remains available for comparison.

The new `window.CardiacWiggersProfile.getSnapshot(physiologicalPhaseMs,getActiveTiming())` returns educational relative pressure, normalized ventricular volume, valve states, event markers and pressure-gradient signs. These are heuristic teaching values, **not mmHg, mL, EF or patient measurements**. An explicit half-open event boundary convention handles exact event ties for the new profile only.

See `SPEC.md`, `DEVLOG.md`, `tests/test_v110_patch2.py` and GitHub Actions for implementation and verification. Manual browser visual acceptance remains pending. Next: v1.10 Patch 3 optional Wiggers graph UI.


## v1.10 Patch 3 — Wiggers Diagram (optional)

A collapsed **Wiggers Diagram** section now appears below the existing ECG, Electrical/Mechanical, measurement and phase panels. Open it to compare one physiological RR interval of the **modeled ECG** with illustrative relative left-atrial/left-ventricular/aortic pressure, normalized ventricular volume, four valve events and S1/S2 event markers. The vertical cursor follows the existing A time while the familiar monitor animation speed stays unchanged.

The diagram is **educational only**: pressure is not mmHg, volume is not mL or ejection fraction, and S1/S2 labels are not audio. The horizontal axis is one complete physiological heartbeat, **not** the existing ECG monitor's scrolling time span.

The optional panel is closed by default and preserves its open/closed state through playback, seek, reset and heart mode switches. On a narrow screen, scroll the chart horizontally within its own region. See `SPEC.md` / `DEVLOG.md` and `tests/test_v110_patch3.py`.

### Local visual review after GitHub main is updated

From the repository root:

```bash
git switch main
git pull --ff-only origin main
python3 -m http.server 8000 --bind 0.0.0.0
```

Open `http://localhost:8000` (or forward port 8000 from a remote development environment). Verify the default collapsed section, keyboard disclosure, chart labels and relative values, moving cursor, HR change, Timeline seek, reset and existing Electrical/Mechanical views.


## v1.10 Patch 4 — Wiggers Diagram learning guide and help (2026-10-10)

**Open the Wiggers Diagram panel, then press the separate `?` button beside its title for a quick guide.** The small non-modal help popover works even while the graph is collapsed. Close with ×, Escape, or a click outside the popup; keyboard focus returns to the help button when closed via ×/Escape. Other controls remain usable; clicking them dismisses the popup without interfering with their normal behavior.

### Why learn this diagram?

The Wiggers Diagram aligns **electrical activation (ECG), mechanical contraction/relaxation, pressure relationships, valve events, and ventricular volume** within one cardiac cycle. It helps nursing learners reason from a monitor waveform to *what the chambers and valves are doing*, rather than memorize disconnected terms. This simulator illustrates **one simplified left-heart sinus cycle**, not an individual patient's cardiac function or a diagnostic waveform.

**Suggested reading order: ECG → pressure → valve → volume → cardiac phase.**

1. **ECG and chamber activity.** The P wave indicates atrial depolarization and precedes atrial contraction. The QRS complex represents ventricular depolarization and precedes the pressure rise associated with ventricular contraction. The T wave represents ventricular repolarization; electrical recovery and mechanical relaxation are related but not identical in timing. A wave is not itself a mechanical contraction.
2. **Relative LA/LV/aortic pressure.** Compare the *heights and directions* of the left atrial, left ventricular and aortic curves. A mitral valve permits flow when atrial pressure is higher than ventricular pressure; an aortic valve permits ejection when ventricular pressure exceeds arterial pressure. In this teaching model, exact equality at a scheduled event is resolved by an explicit valve event rule. Do not read the plotted numbers as mmHg.
3. **Relative left-ventricular volume.** Its curve rises as the ventricle fills, remains level while inlet and outlet valves are closed (isovolumetric phases), falls during ejection and reaches a relative low point before filling resumes. The normalized curve is **not** a measured mL volume or an ejection fraction (EF); a relative decrease does not quantify stroke volume.
4. **The four valve markers.** *Mitral closes* at the beginning of isovolumetric contraction; *aortic opens* at the beginning of ejection; *aortic closes* at the beginning of isovolumetric relaxation; *mitral opens* when ventricular filling resumes. Each labeled event comes from the same schedule as the diagram's marker position and phase explanation.
5. **S1 and S2.** S1 is mainly associated with **mitral and tricuspid closure**, while S2 is associated with **aortic and pulmonary closure**. Here S1 is linked to the *mitral-close* marker, and S2 to the *aortic-close* marker as conceptual left-sided references. There are no simulated sounds, physiologic splits or distinct right-heart event timings.
6. **The cardiac phases.** During *atrial systole*, atrial contraction completes filling. During *isovolumetric contraction*, both left valves are closed, pressure rises and volume is constant. During *ventricular ejection*, the aortic valve is open and LV volume falls. During *isovolumetric relaxation*, both valves close and pressure falls at constant volume. During *ventricular filling*, the mitral valve is open and volume rises.

The **vertical cursor** points to the current **physiological A-time fraction of one RR beat** in the Wiggers diagram. The existing ECG Monitor shows a longer, scrolling view paced by **visualization B time**. Their horizontal coordinates should **not** be compared pixel-for-pixel, even though they share the same underlying electrical cycle. Heart-rate changes alter the length of RR in A while the familiar animation pacing remains unchanged.

**Practical nursing application:** Use the model to connect an observed ECG sequence with anticipated phases of valve closure, contraction, filling and heart sounds, and to learn why a waveform or single sound is only one part of a cardiac assessment. This does **not** diagnose murmur etiology, calculate cardiac output, assess valve disease, interpret invasively measured pressure or predict clinical deterioration. At high heart rates the existing HR-dependent intervals and Bazett QTc also retain known educational limitations.

**Model boundary warning:** This graph uses the v1.10 Patch 2 continuous illustrative profile, whose event timestamps explicitly determine equality ties. The older v1.9 Mechanical graphic uses a different simplified pressure calculation and can disagree within a floating-point epsilon at an exact boundary. Patch 4 explains this difference without rewriting either model.

### References (APA 7th)

Pollock, J. D., & Makaryus, A. N. (2022). *Physiology, cardiac cycle*. In *StatPearls*. StatPearls Publishing. https://www.ncbi.nlm.nih.gov/books/NBK459327/

OpenStax. (n.d.). *19.3 Cardiac cycle*. In *Anatomy and physiology*. https://openstax.org/books/anatomy-and-physiology/pages/19-3-cardiac-cycle

These sources support the *qualitative physiologic relationships*, not the project's chosen relative magnitudes, smoothstep interpolation, event rendering or high-HR numerical fidelity.

### Visual verification and limitations

From the repository root run:

~~~bash
git switch main
git pull --ff-only origin main
python3 -m http.server 8000 --bind 0.0.0.0
~~~

Open http://localhost:8000 (or forward port 8000), try `?` both with the Wiggers panel collapsed and expanded, test Escape/×/outside click, compare five traces and four markers to changing phase lessons, and repeat on a phone-sized browser. Automated browser tests cannot replace visual acceptance on the user's actual device. **The inherited narrow-screen page overflow is reserved for Patch 6.**

Next: Patch 5 focuses on normal/bradycardia/tachycardia educational scenarios. Patch 6 mobile/a11y improvements and Patch 7 final release remain out of scope.
