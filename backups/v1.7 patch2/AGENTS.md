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
