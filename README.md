> **Future UI/UX design baseline (2026-10-15):** [Educational UI Design Standard v1.1](docs/EDUCATIONAL_UI_DESIGN_STANDARD_v1.1.md) guides subsequent learner-first layouts and accessibility. Preserve the active v1.13 three-area design, A/B simulation clocks, original Guided state and clinical review gate. **Documentation only; no runtime redesign is implied.**

# README.md
# Cardiac Electrophysiology Simulator

An educational browser-based simulator that visualizes cardiac electrical conduction and its relationship to ECG waveform changes.

> **Current (2026-10-15): v1.13 UX Patch 3, NOT FINAL.** Simulator and six-unit Learning are available; the unreviewed fictional Clinical case remains disabled for ordinary users (QA preview only). The seven-topic Korean-first explanations are retained; UX Patch 3 also aligns visible ECG/conduction descriptions, Ready-state displays, user-guide and accessible names with official Korean terminology while allowing necessary medical abbreviations and proper names. [Current handoff verification](V1.13_HANDOFF_VERIFICATION_2026-10-15.md). Sections below that describe P1/P2–P6 as future work are historical development records, not today's implementation status.

## v1.13 P3/P4 student-first detailed design (historical specification)

See [V1.13_PATCH3_PATCH4_STUDENT_DESIGN.md](V1.13_PATCH3_PATCH4_STUDENT_DESIGN.md) for six-unit curriculum/readability/state/QA specification and the strict separate fictional symptomatic bradycardia-case authoring/validation pipeline. This was **design-only when written**. Current P3/P4 code exists, but **clinical approval/public release does not**.

## v1.13 Patch 2–6 engineering blueprint (historical specification)

The post-Patch-1 implementation gates, single-instance Guided migration, six-unit learning curriculum, first clinically reviewed static case, session preservation, and QA/release boundaries are documented in [V1.13_PATCH2_TO_PATCH6_IMPLEMENTATION_PLAN.md](V1.13_PATCH2_TO_PATCH6_IMPLEMENTATION_PLAN.md). This was **a plan at the time it was written**, before P2–P6 integration; current code and release gate are described in the current-version section above. It supplements without superseding the [approved v1.13 contract](Cardiac_v1.13_Three_Tab_Development_Contract.md).

## v1.13 Patch 1 — historical initial navigation foundation

At the **Patch 1 milestone**, only Simulator was active and Learning/Clinical were both disabled. **Current v1.13** enables Learning but keeps unreviewed Clinical disabled for ordinary users. The existing Guided 5-stage/3-level course and 10 questions remain available inside the original Simulator Inspector. A/B timing and approved Guided observation actions are unchanged.

For automated internal navigation regression only, `index.html?v113Preview=1` enables the two **clearly labeled nonclinical preview panels** to test tab switching. This flag is **not** a release of educational/clinical features or an access-control feature. Switching active tabs invokes the original `pause()` only when playing, never seeks, resets, or resumes automatically. Refresh starts in Simulator and discards session-only UI state. See [development contract](Cardiac_v1.13_Three_Tab_Development_Contract.md). v1.12 Patch 14 remains **NOT FINAL**, awaiting actual PC/mobile user signoff.

## v1.13 next-development contract (historical design handoff)

The approved **three-tab educational platform** (① 시뮬레이터 / ② 학습 / ③ 임상 적용) and tab-navigation policy are documented in [Cardiac v1.13 Three-Tab Development Contract](Cardiac_v1.13_Three_Tab_Development_Contract.md). **A안 is confirmed:** on top-level tab transitions, pause via the existing `script.js` mechanism while preserving physiological A/visualization B times and the current display position; never auto-play on return. Guided Learning's explicitly initiated first study/stage-seek behavior remains unchanged. Preserve independent clinical answers and guided study state across tabs. This is a **future implementation contract only**, not a v1.13 release; v1.12 Patch 14 remains NOT FINAL pending user PC/mobile signoff.

## Current Version

**Current implementation: v1.13 UX Patch 3 (2026-10-15), NOT FINAL.** P2–P6 integration, approved A1+B1+C1+D1+E1+F1 layout and Korean-first concept popup have been merged through PR #34. The unreviewed Clinical case is preview-only. User PC/mobile signoff and independent clinical review are pending.

**Historical baseline, v1.12 Patch 14 — NOT FINAL:** responsive mechanical readability and safe model disclosures; the v1.12 instructions below describe the preserved legacy engine/Guided behavior, not the current top-level navigation.

Default view is compact: ECG + controls, live three-part status, physiological/nursing summary, six measurements and synchronized Electrical/Mechanical/Wiggers visualization. The '자료 목록 보기' button opens a **categorized source index only**, not every long description. All original detailed clinical content and ten concept questions remain available.

Start from Reset/Ready and press **5단계 학습 시작**. The first deliberate entrance pauses and uses the original Timeline once to show modeled atrial systole. '이전/다음 단계' then auto-seeks once per selected stage; Play retains the chosen reading while ECG and live phase continue. Reopening later does not secretly pause/seek an active simulation. Optional level chooser, manual Wiggers shortcut and re-observe button are under **추가 도구**. Quizzes remain optional and answers are held only for the current browser session.

Desktop >=1200px keeps ECG and heart visualization together to the left of the learning card. Narrow and mobile widths stack sections, and the five ECG concept buttons wrap without horizontal swiping. Displayed normalized pressures/volumes and five stage boundaries are simplified educational models, not patient data or validated cardiac-output/EF predictions. P is electrical atrial depolarization that precedes mechanical atrial contraction; QRS is electrical ventricular depolarization.

See [V1.12_PATCH14_REPORT.md](V1.12_PATCH14_REPORT.md) for current implementation, remaining QA gates and checks. Older roadmap/version references in sections below are historical only. Run locally with `python -m http.server 8000` and open `http://localhost:8000`.

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


## v1.10 Patch 5 — Nursing and cardiac-cycle learning scenarios (2026-10-12)

### What's new
- Open **Wiggers Diagram** near the bottom. Inside it choose **Normal 72**, **Bradycardia 50** or **Tachycardia 120 bpm**. These buttons reuse the original Heart Rate slider, not a separate simulation mode. Move the slider directly to return to *Custom HR*.
- Open **심화 의학·간호 해설 보기** to read a full, phase-specific six-part lesson: **electrical activation → relative pressure/valves → relative LV volume → patient nursing observation → rate comparison → modeling limitations**. Timeline seek or playback changes the current phase automatically. The inner explanation remains opt-in so the ECG Monitor and Wiggers plot are not displaced by paragraphs.
- Use the top **▤ Patch notes** and **? User guide** buttons to open scrollable reference popups. Close using **×**, **Escape**, or by clicking elsewhere. They are independent of Play/Pause/Reset, and only one reference popup opens at once. Their content is included inline in the app; there is no network connection or external help dependency.

### How to study the five phases
1. **Ventricular filling:** the mitral valve is open when LV pressure is sufficiently low relative to LA. LV relative volume rises. Do not assume normal preload merely because the teaching trace rises.
2. **Atrial systole:** P-wave atrial depolarization comes before atrial contraction; atrial contraction adds the end-diastolic contribution to ventricular filling. A P wave is an electrical signal, not a direct proof of mechanical atrial function.
3. **Isovolumetric contraction:** QRS activation precedes contraction. Mitral/tricuspid valve closure is chiefly associated with S1; in the left-heart teaching model, mitral close starts a closed-valve interval when LV pressure increases and LV volume is flat.
4. **Ventricular ejection:** aortic opening permits forward flow; relative LV volume falls. T-wave repolarization may overlap late ejection, but no exact mechanical end is inferred from the T wave.
5. **Isovolumetric relaxation:** aortic/pulmonary closure is associated with S2; after aortic close and before mitral open, volume stays flat while LV pressure falls. The diagram does not synthesize S2 or left/right valve split sounds.

### Heart rate scenarios: how to interpret safely
- **Normal (72 bpm reference):** observe the sequence of ECG→pressure rise→valve opening→ejection→relaxation and compare electrical/mechanical offsets. Resting adult 60–100 bpm is a descriptive band, not a guarantee of healthy cardiac function.
- **Bradycardia (50 bpm example):** a longer RR permits a longer model cycle. In real care bradycardia may be physiological (sleep, training) or associated with symptoms; assess dizziness, fainting, consciousness, blood pressure, pulse, breathing and medication/underlying context. The model does not represent AV block or compromised output.
- **Tachycardia (120 bpm example):** a shorter RR commonly reduces available filling time, particularly in diastole; *this does not directly predict EDV, stroke volume, EF, perfusion or cardiac output*. Fever, pain, activity, anemia, dehydration and other causes demand contextual assessment, not automatically a decision to lower HR.

**Nursing learning sequence:** pick a rate → observe P/QRS/T → locate mitral close (S1), aortic open, aortic close (S2), mitral open → examine pressure/volume → identify the present phase in the deeper learning area → ask what signs/symptoms, perfusion and auscultation findings would be needed in a *real* clinical assessment.

### Scientific fidelity and important restrictions
The simulator uses a simplified normal sinus electrical timing model, an educational mechanical event schedule, relative left atrial/LV/aortic pressure **indexes** and normalized LV volume. These are **not** invasive blood-pressure readings (mmHg), ventricular measurements (mL), stroke volume, cardiac output or ejection fraction, nor patient-specific predictions. The plotted S1/S2 are event markers, not sounds or independently computed right-heart valve closures. HR changes affect the modeled timestamps but not a physiological cardiac output/Frank–Starling system. QTc correction/high-HR electrical intervals and older Mechanical floating-point boundary ties also have documented limitations.

**A vs B:** The Wiggers vertical cursor maps the current *physiological A-time phase within a single RR*. The ECG Monitor shows a separately paced, horizontally scrolling B-time visualization. Do not compare their x-coordinates pixel-for-pixel.

### Quick controls and user guide
- **Play / Pause / Reset:** start, hold and reset. Reset returns status labels to Ready but retains chosen view/disclosure.
- **Timeline:** seek to cardiac-cycle time while pausing playback.
- **Heart Rate:** change 30–180 bpm; manual changes return the learning preset to Custom.
- **Electrical / Mechanical:** switch between conduction animation and educational schematic valves/flow without disturbing time.
- **Wiggers / ? / deeper explanation:** optional panel, brief Wiggers help and longer physiologic/nursing guidance respectively.
- **Header Patch notes / User guide:** categorized changelog and self-contained operation guide. ×, Escape or click outside closes.

**Clinical context matters:** Abnormal HR alone is not a diagnosis. Never use these simulated curves to interpret clinical unstable rhythms or decide treatment. The simulator is intended for foundational ECG/heart-cycle learning, not emergency or medical-device use.

### References (APA 7th)
Pollock, J. D., & Makaryus, A. N. (2022). *Physiology, cardiac cycle*. In *StatPearls*. StatPearls Publishing. https://www.ncbi.nlm.nih.gov/books/NBK459327/

OpenStax. (n.d.). *19.4 Cardiac physiology*. In *Anatomy and physiology*. https://openstax.org/books/anatomy-and-physiology/pages/19-4-cardiac-physiology

American Heart Association. (2024, September 25). *Bradycardia: Slow heart rate*. https://www.heart.org/en/health-topics/arrhythmia/about-arrhythmia/bradycardia--slow-heart-rate

American Heart Association. (n.d.). *Tachycardia: Fast heart rate*. https://www.heart.org/en/health-topics/arrhythmia/about-arrhythmia/tachycardia--fast-heart-rate

These support qualitative human physiology and context, **not** the numeric simulator engine.

### Manual visual review
From the repository root after the new main is merged:

~~~bash
git switch main
git pull --ff-only origin main
python3 -m http.server 8000 --bind 0.0.0.0
~~~

Open http://localhost:8000 (or forward port 8000). Verify collapsed-by-default Wiggers and deep-education disclosures, three HR presets, changing full medical/nursing explanations, visible four valve/S1-S2 markers, long popup text scrolling, outside-click/X/Escape behavior and narrow-screen view. Automated CI/browser checks are distinct from inspection on an actual user device.

**Next:** Patch 6 mobile/a11y improvements, then Patch 7 FINAL. Neither is included in Patch 5.


## v1.11 CURRENT — Integrated Learning Dashboard (2026-10-12)

This is the **current** layout. Earlier v1.10 guide sections describe the historical UI; the underlying physiology is unchanged.

### Current operation
- The original ECG Monitor stays visible. The original Play, Pause, Reset, 30–180 bpm HR and Timeline controls, plus Normal 72 / Bradycardia 50 / Tachycardia 120 teaching presets, are gathered in one compact top command region. Moving the old buttons, not cloning them, preserves their original control paths.
- Select Electrical (original SA/AV/His/Purkinje animation), Mechanical (original four-chamber valve/flow animation) or Wiggers (ECG, relative LA/LV/aorta pressures, normalized LV volume and four S1/S2/valve markers) in the central view. Every selection reads the same existing physiological time A, without seeking/pausing/resetting. A smaller separate ECG visualization-time clock B preserves existing sweep speed.
- A paired **실시간 통합 해설** displays separate electrical and mechanical phases and a short source-derived nursing/physiology summary, alongside the original Current Phase and ECG Event content. Expand the adjacent **심화 의학·간호 해설** to read the complete six-part original lesson.
- Desktop Wiggers has an optional **⤢ Wiggers 확대 보기** button: use full width and move the explanation below, then **⤢ 분할 보기** to restore the two-column view. This toggle changes no physiological state. On phones everything stacks; only the 720px-minimum Wiggers SVG plot scrolls horizontally.
- View controls support keyboard Left/Right/Home/End when focused. The existing header patch notes, User guide, and Wiggers ? popup retain close button, Escape and outside click.

### Physiological and clinical meaning
ECG electrical depolarization and mechanical contraction are not identical events. The normal/brady/tachy presets classify example HRs, not pathological diagnoses. Wiggers relative pressures are not mmHg; normalized LV volume is not mL, EF, stroke volume or cardiac output, and S1/S2 are event markers not sound recordings. Mechanical and Wiggers exact-boundary rounding differ slightly, as already documented. At high HRs QT/QTc values reflect the original simplified teaching model, not validated clinical measurements. This release does not add patient diagnosis/treatment or any new physiological calculations.

### Manual verification
Use desktop 1366×768 / 1440×900, tablet 768 and phone 390 / 360 widths. Confirm that ECG is always visible; view tabs do not change A/B, HR or Play/Pause state; Electrical pulses and Mechanical flow remain usable; Wiggers re-entry immediately synchronizes all five traces and four markers; focus/split and Reset preserve correct states; full nursing explanation, guide/changelog popups and keyboard controls work; only the Wiggers chart has horizontal scroll. Automated GitHub Actions and headless screenshots are **not** target-device human visual acceptance.

The pre-v1.11 confirmed source and documents are archived in backups/v1.10-final/ (15 files, baseline f08e894ca6713d0828cf4739d33cd87ac0da46fa). Continue to use existing v1.10 reference citations for the unchanged medical descriptions.


### v1.12 guided learning — design prepared, NOT yet implemented

The current running version remains **v1.11.1**. The planned next release has a complete design in [V1.12_DESIGN.md](V1.12_DESIGN.md) and medically scoped teaching/quiz content in [V1.12_CLINICAL_CURRICULUM.md](V1.12_CLINICAL_CURRICULUM.md). These are **design documents only**, not active UI or released features.

The design recommends an opt-in five-stage guide within the existing learning inspector, preserving the compact default and original ECG/Mechanical/Wiggers. Stage selection never changes A/B time or playback; **only explicit user action** to seek through the existing Timeline does so. The current normalized filling profile has two disjoint stage intervals with different LV-volume behaviors, explicitly addressed in the curriculum. The major visible UX alternatives (inline inspector / extra tab / modal, automatic Wiggers switching or user-triggered switch) remain **subject to user confirmation** prior to v1.12 implementation.


### v1.12 design refinement (design only, no new runtime)

See [V1.12_DESIGN_REFINEMENT.md](V1.12_DESIGN_REFINEMENT.md) for the improved **replace-in-place compact learning inspector**, separate study-step and live physiological-phase labels, explicit user-only seek behavior, model-RR filling terminology correction, proposed five-patch QA criteria and the three user UX decisions. Earlier v1.12 documents remain the original design and nursing syllabus. Active application version is **v1.11.1**, not v1.12.


## v1.12 Patch 1 — active narrow development milestone

User-approved A/A/A guided learning foundations have been implemented. The original compact ECG dashboard remains the default, with a small `5단계 학습` button replacing the existing short nursing summary only when opened. The five-phase dropdown and labels use the original PHASES medical teaching dictionary and current Wiggers model. Selecting a study phase never seeks, pauses, switches Wiggers, or changes HR/A/B. The six-part original educational narrative remains separately accessible. See [V1.12_PATCH1_REPORT.md](V1.12_PATCH1_REPORT.md) for risks, explicit non-goals, tests and Patch 2 handoff. v1.12 FINAL is NOT claimed; device acceptance is pending.


### v1.12 Patch 2 — Guided navigation and explicit observation (incremental development)

Patch 2 adds native `이전 단계`/`다음 단계` buttons to the opt-in five-stage teaching inspector; the selected lesson changes without seeking or pausing the simulation. It also adds two deliberately separate buttons: `Wiggers에서 보기` switches only the visualization, while `이 단계 관찰 시점으로 이동` explicitly dispatches the existing Timeline slider `input` and therefore pauses and synchronizes physiological A / visualization B. No independent clock, patient physiology or timeline calculation is created. The first/last study buttons disable at the boundaries. This preserves the closed compact dashboard and all original clinical explanations. See [V1.12_PATCH2_REPORT.md](V1.12_PATCH2_REPORT.md) for regression and next patch. Beginner/advanced quizzes are Patch 3 work; **v1.12 FINAL is not declared**.


### v1.12 Patch 3 — Beginner/advanced and 10 source-grounded questions

Current milestone: **v1.12 Patch 3 (NOT v1.12 FINAL)**. The existing opt-in guided inspector now provides **초급 / 심화** level choice and optional expandable learning review. Basic has one concept question per stage; advanced uses the complete original PHASES/RATE learning source and adds the second question for that stage. The 10 A/B/C items are mapped to [V1.12_CLINICAL_CURRICULUM.md](V1.12_CLINICAL_CURRICULUM.md). An answer becomes visible only after **정답 확인**; **다시 풀기** clears that item alone. The learner's in-memory responses survive guide close, stage switch and cardiac Reset but **not reload**; nothing is saved to the browser, a server or an EMR. Difficulty, question answers and feedback cannot change ECG waveform, the original A/B times, HR, playing state or visualization. The default closed compact dashboard and separate original six-part nursing explanation remain. Implementation/risk/QA: [V1.12_PATCH3_REPORT.md](V1.12_PATCH3_REPORT.md).

Future Patch 4/5 will handle broader responsiveness, medical-text consistency and full release QA; user's actual-device touch/visual acceptance is scheduled separately for later.



### v1.12 Patch 4 — Novice-first progressive guided learning

**Current milestone: v1.12 Patch 4, not FINAL.** The optional five-stage inspector now begins at **1. 기초 이해** (one-sentence overview; ECG, valve and relative-volume basics), advances to **2. 간호 연결** (qualitative nursing assessment connections), and opens **3. 추가학습** only by user choice (complete existing PHASES/RATE nursing/physiology source, modeled midpoint and the second advanced question). A next-level button and native selector coexist. All original ten quiz questions and six-part nursing explanation remain intact. Educational interactions do not change A/B, HR, playback, Timeline, Wiggers or the ECG. Details: [V1.12_PATCH4_REPORT.md](V1.12_PATCH4_REPORT.md). Real-device touch/visual acceptance is deferred at user request.


### v1.12 Patch 5 — educational accuracy and final stabilization (not FINAL)

Current implemented version: **v1.12 Patch 5**. The default compact dashboard remains unchanged. Select **5단계 학습** in the existing live explanation and follow **1. 기초 이해 → 2. 간호 연결 → 3. 추가학습**. Study stages and levels modify instructional text only. Only the separately clicked **Wiggers에서 보기** changes view; only separately clicked **이 단계 관찰 시점으로 이동** pauses and seeks through the original Timeline. All ten source-aligned conceptual questions remain optional and editable within the current page session.

**Important model caveat:** The relative LV-volume trace under `filling` is flat at 0.88 in the beginning of the model RR cycle, and increases from 0.48 to 0.88 in its end segment. These dimensionless anchors are modeling choices rather than physiological fill fractions or patient EF/mL; actual filling may not pause when the drawn curve is flat. S1/S2 markers illustrate left-sided valve timing, not auscultatory sound reproduction.

The original advanced nursing explanation, Electrical/Mechanical/Wiggers, ECG, A/B clocks, HR, Timeline and playback are preserved. New browser regression tests include stage and volume boundary verification, keyboard checks and mobile screenshots, but **actual user PC/mobile manual review remains outstanding**; this release is not marked v1.12 FINAL. See [Patch 5 report](V1.12_PATCH5_REPORT.md).

**Selected references (APA 7):**
- OpenStax. (2013). *19.3 Cardiac cycle*. In *Anatomy and physiology*. https://openstax.org/books/anatomy-and-physiology/pages/19-3-cardiac-cycle
- Pollock, J. D., & Makaryus, A. N. (2022, October 3). *Physiology, cardiac cycle*. In *StatPearls*. StatPearls Publishing. https://www.ncbi.nlm.nih.gov/books/NBK459327/
- Dornbush, S., & Turnquest, A. E. (2023, July 17). *Physiology, heart sounds*. In *StatPearls*. StatPearls Publishing. https://www.ncbi.nlm.nih.gov/books/NBK541010/


## v1.12 Patch 9 — learning-focused workbench
At desktop widths the ECG sits beside concise live/guided explanations; the Electrical/Mechanical/Wiggers view is below. Use **5단계 학습** to select a cardiac stage; when already studying, previous/next or dropdown seeks once through the native Timeline and pauses. The selected reading remains fixed even when Play resumes; live stage indicators keep moving. An independent **자료 목록 보기** opens a directory of original conduction, ECG event and nursing sources without expanding everything at once. Click individual categories; ECG wave-specific P/PR/QRS/ST/T is accessible within the ECG Monitor. Three study levels and ten questions remain intact; nothing diagnoses or predicts patient physiology. Physical PC/mobile acceptance is still required before v1.12 FINAL.

## v1.13 integrated Patch 2–6 (implementation branch; NOT FINAL)
- Added the original single-instance Guided rehost in Learning, six-unit lesson course/free browsing, a schema-validated **unreviewed fictitious** clinical case, independent Clinical judgement/action/reassessment session, and Playwright integration tests. See [V1.13_INTEGRATED_PATCH2_TO_6_REPORT.md](V1.13_INTEGRATED_PATCH2_TO_6_REPORT.md).
- Clinical public tab remains **disabled** until expert case-content review; QA-only `?v113Preview=1` allows running the unfinished clinical educational scenario for testing, not patient care. Simulator and Learning are usable.
- Still NOT FINAL pending full CI, clinical reviewer, and physical PC/Android acceptance; v1.12 Patch 14 also remains NOT FINAL. No original physiological model or ten-question bank was edited.


## v1.13 Student UX audit / choices (design approval pending; NOT FINAL)
See [V1.13_STUDENT_UX_AUDIT_AND_CHOICES.md](V1.13_STUDENT_UX_AUDIT_AND_CHOICES.md) for current code inspection, minimally scoped accessibility and quiz/confirmation focus repairs, unreviewed clinical content boundary, and six explicit visual UX decision groups (A–F). No overall layout/palette/reading-order choice has been silently made. Preserve original A/B, ECG, Mechanical, Wiggers, original 10-question Guided and clinical release gate.


## v1.13 UX Patch 1 — Student-first A1+B1+C1+D1+E1+F1 (approved)
- The project owner selected the student-first responsive chapter reader, calm medical blue/teal palette, single-depth cards, goal→mechanism→nursing→observation→original Guided→references order, phase-focused fictitious patient snapshot/decision, and balanced 16px reading density.
- Implemented design and regression boundaries are documented in [V1.13_UX_PATCH1_IMPLEMENTATION_REPORT.md](V1.13_UX_PATCH1_IMPLEMENTATION_REPORT.md). Simulator heart clocks, original ECG/Mechanical/Wiggers and original 5-stage/10-question Guided remain canonical.
- Clinical still requires independent educational/medical review and is QA-only until approved. v1.13 and v1.12 Patch14 remain NOT FINAL until user PC/mobile testing.

## v1.13 UX Patch 2 — 학생 중심 한글 용어·개념 팝업
- 학생에게 노출되는 핵심 기능을 한글 우선으로 표기하며 영어 약어는 한글 뒤 괄호로 병기합니다. 위거스 도표(Wiggers), 심전도(ECG), 전기 전도, 기계적 심장주기 등의 **개념·중요성·관찰 방법·모델 한계**를 설명하는 읽기 전용 팝업을 제공합니다.
- 전체 변경사항과 QA 기준: [V1.13_UX_PATCH2_KOREAN_EDUCATION_REPORT.md](V1.13_UX_PATCH2_KOREAN_EDUCATION_REPORT.md). A/B, 원본 5단계·10문항, 임상 자료는 변경하지 않으며 전문가 검토/실기기 검수 전 **NOT FINAL**입니다.
