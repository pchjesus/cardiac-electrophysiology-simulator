# CARDIA v8 — Inquiry-first Learning & Spatial Motion

**Status:** Draft design preview, not approved for merge or GitHub Pages deployment.

## Product decision
The reviewed CARDIA v7 standalone design remains the starting point. The v8
learning tab is a **new instructional workflow**, not a recolor of the v7 course.

- **01 생각하기:** start with one scientific question and its event sequence
- **02 관찰하기:** open the *same native engine* in a relevant electrical / mechanical / optional Wiggers view
- **03 이해 확인:** answer one formative question with immediate explanation; this is **not** an official completion
- **원문·심화:** preserve the full, original course content, citations, interactive questions and completion controls in a clearly disclosed source section

Progress counts only the native `CardiacCourseV113.completedUnitIds` data.
The user's quiz selection is only ephemeral in the v8 UI and does not change
the native course completion record.

## Motion design decisions
From `pchjesus/design-kkakgi`:
- `references/MOTION_INDICATOR_ATLAS_v0.1_20261105.md`
- `references/UI_MOTION_BEHAVIOR_ADDENDUM_v0.1_20261108.md`
- `references/UI_PATTERN_FIELD_ATLAS_v0.1_20261105.md`
- `references/COLOR_BALANCE_CONTRAST_NOTE_v0.1_20261110.md`

A moving left navigation surface indicates the selected destination. Moving
between simulator and learning uses direction-aware View Transitions.
Inside one learning page, the active step underline slides and new content
enters with a brief, interruptible fade-up, rather than an expensive full-screen
transition. All animation respects `prefers-reduced-motion`.

## Engineering scope
- `base-v7.html`: frozen source for the approved v7 design concept
- `cardia-v8.css`: light color system, transition geometry, learning typography
- `cardia-v8.js`: adapter that moves original unit content into a new learning workflow
- `index.html`: generated standalone clickable review artifact
- `scripts/build-cardia-v8-preview.py`: deterministic offline assembly
- `tests/test_cardia_v8_preview.py`: narrow UI + native integration smoke

**Important:** The main branch's engine and original HTML were NOT changed in
this PR. This preview is an additive self-contained proposal, pending a separate
integration phase that transfers the accepted design into maintainable app
modules. Do not merge the preview as a replacement for the production entrypoint.

## Risks and constraints
1. Original ECG and valve computations remain authoritative; animations must
   not create a second physiological clock.
2. Clinical QA review gate remains locked; new visuals are schematic and
   **not clinically verified**.
3. Wiggers is opt-in only, and opting out while viewing it must return safely
   to an available view.
4. The learning tab's six topic examples and formative prompts require
   a domain expert review before using them as evaluated coursework.
5. Historical regression tests for the production app and real-device
   accessibility tests remain outside preview CI. The narrow preview test
   cannot substitute for that coverage.

## Local review
Run `python scripts/build-cardia-v8-preview.py` from the repository root,
then open `prototypes/cardia-v8/index.html` in a browser.
The GitHub Actions workflow also stores an HTML artifact per PR run.
