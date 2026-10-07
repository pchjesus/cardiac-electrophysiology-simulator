# AGENTS.md
# Development Rules — Cardiac Electrophysiology Simulator

## 1. Preserve Existing Behavior

This is an educational simulator. Existing working behavior must be preserved unless a change explicitly requires otherwise.

Always inspect the current code before modifying it. Do not assume the current files match an earlier version.

## 2. Isolate Changes

Prefer small, isolated patches.

UI-only change:
- Prefer HTML/CSS.
- Do not modify JavaScript unless required.

Simulation change:
- Modify only the logic required.
- Keep the UI stable where practical.

## 3. Regression Review

After changes, verify:
- Play
- Pause
- Reset
- Timeline
- Heart-rate control
- ECG animation
- ECG direction
- ECG visibility
- Rhythm classification
- Cardiac conduction animation
- Current Phase updates

Ensure all JavaScript-referenced DOM IDs remain intact.

## 4. State and Animation

Avoid competing timers or animation loops.

ECG cycle, conduction phase, playback state, and controls should remain synchronized.

## 5. ECG Canvas

HTML canvas dimensions control drawing resolution; CSS dimensions control displayed size.

Do not change waveform amplitude/timing merely to solve a UI problem.

For clipping, prefer adjusting the drawing baseline or display area before altering the physiological model.

## 6. Educational Accuracy

The simulator is educational, not a clinical diagnostic tool.

Simulated measurements must not be presented as real patient data.

Future ECG measurements should clearly originate from the simulator model.

## 7. Placeholder Panels

Current placeholders:
- ECG Measurements
- ECG Event / Phase Indicator

Do not insert fake dynamic values.

Implement these panels only after their expected behavior and relationship to the ECG model are specified.

## 8. UI Principles

- ECG remains visually dominant.
- Avoid unnecessary vertical padding.
- Do not fill empty space with low-value features.
- Maintain readable labels and controls.
- Prefer consistent spacing.
- Aim for practical single-screen desktop use.
- Preserve responsive behavior.

## 9. Patch Naming

Use:

`Cardiac_Electrophysiology_Simulator_v[version]_UI_patch[number]_[short-description]`

Example:
`Cardiac_Electrophysiology_Simulator_v1.6_UI_patch4_current_phase_spacing`

Patch numbers restart for each new version.

## 10. Backups

Never overwrite a confirmed backup.

Before moving to a new version, archive the confirmed build under:

`backups/v[version]/`

At minimum:
- index.html
- style.css
- script.js

Documentation should also be archived when it represents that version's confirmed state.

## 11. Documentation

When a version is confirmed:
- Update SPEC.md.
- Update DEVLOG.md.
- Update README.md when user-facing behavior changes.
- Update AGENTS.md only when development rules or architecture change.

Documentation must describe the actual current behavior separately from future plans.

## 12. Standard Workflow

1. Inspect current code.
2. Identify affected files.
3. Review regression risks.
4. Implement the smallest reasonable change.
5. Test existing behavior.
6. Have the user visually/behaviorally verify the result.
7. Update documentation.
8. Archive the confirmed version.

---

## Current Project Baseline — v1.7 FINAL

Treat **v1.7 FINAL** as the confirmed baseline for the next version.

Completed v1.7 features:
- ECG Measurement Engine: HR, RR, PR, QRS, QT, QTc.
- Measurement normal-reference UI.
- ECG Event / Phase Indicator synchronization.
- Explicit conduction-path animation, including simultaneous RBB/LBB branching.
- Interactive ECG Component Explanation for P / PR / QRS / ST / T.
- Unified State Feedback using `heartState.ecgTime` as the sole simulation time source.
- Educational rate scenarios: Normal 72 bpm, Bradycardia 50 bpm, Tachycardia 120 bpm, and Custom after direct BPM adjustment.

### Protected v1.7 Behavior

When developing v1.8, preserve unless the change is explicitly part of the new physiological model:
- ECG visualization and waveform presentation
- ECG measurements and UI
- conduction animation
- Current Phase / ECG Event / Explanation synchronization
- Play / Pause / Reset
- Cardiac Cycle Timeline
- heart-rate control and scenario UI
- responsive behavior

### v1.7 Timing Limitation

The current model is intentionally simplified for education. Conduction phases and ECG events do not form a complete physiological electromechanical timing model. For example, Purkinje activation currently spans 380–450 ms while the QRS event ends at 380 ms. Do not silently "fix" such boundaries during unrelated work.

### v1.8 Architecture Direction

The first v1.8 task should be analysis and design of a physiological timing model before large UI changes.

Target architecture:
- **Physiological / Measurement Time (A):** source for modeled cardiac electrical timing and measurements.
- **Visualization Time (B):** controls how the model is presented/animated on screen.

The A/B separation must be introduced deliberately and centrally, not through competing timers.

Future cardiac-cycle/hemodynamic visualization should be designed to consume this model:
- valve opening/closing
- chamber filling
- ventricular ejection
- blood-flow direction

### Development Rule for v1.8+

Before implementation:
1. Inspect the confirmed v1.7 code and state flow.
2. Define the physiological model and timing dependencies.
3. Identify regression and state-synchronization risks.
4. Implement in small isolated patches.
5. Test boundary transitions, timeline seeking, playback, reset, and BPM changes.
6. Update SPEC/DEVLOG/README when the behavior is confirmed.
7. Archive the confirmed build before moving to the next version.

Do not claim physiological accuracy where the model has not implemented it.
