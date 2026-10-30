# BUILD-007 — Playtest build 2 (PS1 complete)

**Role:** BUILD · **Dept:** Gameplay · **Priority:** P0 · **Branch:** `claude/task-build-007` worktree off `main` (054e159 or later) · **Owner:** lead subagent · **Reviewer:** none (build only; the lead checks the smoke result)
**Touches:** none · **Interfaces:** `Downloads/Dispo Game Builds/`

## Goal
Build the current `main` (PS1 complete: GAME-009 medical customers) as a Windows playtest build for Nolan, following BUILD-006.

## Read
`Docs/Handoffs/BUILD-006.md` (the procedure and the handoff format); `Docs/TOOLCHAIN_EXECUTION.md` (`studio.ps1 unity-build`, DEC-013 gate); `Docs/Handoffs/GAME-009.md` (what's new, controls).

## Owns
`C:/Users/handl/Downloads/Dispo Game Builds/slice-<shortsha>/` (new folder; never touch earlier builds), `Docs/Handoffs/BUILD-007.md`, and `Docs/BUILD_STATUS.md` (one row).

## Deliverable
1. `studio.ps1 unity-build` from your worktree at main HEAD; the smoke run must pass (`STUDIO_SMOKE_READY`, no crash). Revert any editor side-effect re-serialisation, as BUILD-006 did.
2. Copy the player into `Dispo Game Builds/slice-<shortsha>/` with `BUILD_MANIFEST.json`; launch the copied exe once, check the log for `shift ready`, then kill it.
3. The handoff in BUILD-006's format: exe path and size; smoke results; **new since slice-38b9e5c** (medical customers and the Medical/Adult-use switch T, medical tax, the 14-day allotment, out-of-state cards, the queue strip); a controls table; **known gaps Nolan will notice** (controls, customer flow and recommendation depth from playtest 1 are not in this build: GAME-025/026/017a are next).

## Validation
Smoke passes; the copied exe starts. Gameplay holds 1 Unity slot: if another editor holds the project lock, wait (DEC-013). Never open two editors.

## Handoff
`Docs/Handoffs/BUILD-007.md` (≤40 lines), committed on your branch. Report to the Gameplay lead; never ask Nolan (DEC-033).
