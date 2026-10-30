# BUILD-004 — Harden the DEC-045 hub guard

**Role:** BUILD · **Priority:** P1 · **Branch:** `claude/task-build-003-0837ba` (on top of BUILD-003, main 1b6707f merged in)

## Goal
Turn the prototype PreToolUse hook (`Tools/Studio/hub_guard.py` + `.claude/settings.json`, uncommitted in the main checkout) into a reviewed, tested guard that blocks Hub execution work without blocking legitimate Hub git/doc commands.

## Read
`Docs/HUB_RESUME.md` HARD RULES; DEC-045, DEC-033, DEC-013.

## Owns
`Tools/Studio/hub_guard.py`, `Tools/Studio/hub_guard_test.py`, `.claude/settings.json`, the `.claude/` lines in `.gitignore`, `Docs/Handoffs/BUILD-004.md`.

## Deliverable
1. Exec detection matches real invocations only: studio runner via `-File`, `&` or as a statement; `Unity.exe` with flags; `-batchmode`; Blender exe with `-b`/`-P`; `dotnet build|test`. Heredoc bodies, PowerShell here-strings and `git -m` messages are ignored.
2. Everything is allowed when cwd or the target path is under `.claude/worktrees/`. In the main checkout, edits under `UnityProject/` and `Tools/` are blocked; Docs stay allowed.
3. Fail open on a malformed payload, on a missing python, and on a missing guard script.
4. Self-test `python -I Tools/Studio/hub_guard_test.py` covers: hub build blocked, worker build allowed, hub git/doc heredoc allowed, hub code edit blocked, worker code edit allowed, bad payload allowed.

## Validation
Self-test from the worktree; the hook command run through bash against a fake hub root (block, allow, guard missing, python missing).

## Handoff
`Docs/Handoffs/BUILD-004.md` (≤40 lines). Reviewed together with BUILD-003.
