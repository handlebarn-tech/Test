# Handoff — BUILD-004 (hardened DEC-045 hub guard)

**Status:** done; self-test 19/19. Branch `claude/task-build-003-0837ba` (BUILD-003 + main 1b6707f merged + this), not merged. Review together with BUILD-003.

## Changed
- `Tools/Studio/hub_guard.py` (from the main-checkout prototype):
  - Exec regex matches real invocations only: `studio.ps1` via `-File`, `&` or as a statement start; `Unity.exe` followed by a flag; ` -batchmode`; `blender.exe …` or a statement-start `blender` with `-b`/`-P`; `dotnet build|test`.
    Before matching it strips heredoc bodies, PowerShell here-strings (`@'…'@`, `@"…"@`) and `git -m "…"` messages. So doc heredocs, commit messages, `grep studio.ps1` and `rg -i unity -n` pass.
  - cwd under `.claude/worktrees/` → allow everything. A command text naming a worktree path → allow, as before.
  - Edit/Write/NotebookEdit: blocked only when the path resolves under `<CLAUDE_PROJECT_DIR or cwd>/UnityProject/` or `/Tools/` and is not in a worktree. Relative paths are resolved; `notebook_path` is handled.
    The prototype blocked any path containing `/Tools/`, even outside the repo.
  - Malformed or non-object JSON, or any exception → exit 0.
- `.claude/settings.json`: the hook now runs `python -I -c "…runpy.run_path(<CLAUDE_PROJECT_DIR>/Tools/Studio/hub_guard.py)"` only if that file exists.
  Reason: `python missing_file.py` exits **2**, which Claude Code treats as *block*. With the prototype, a session whose project dir lacks the script would have every tool denied.
- `Tools/Studio/hub_guard_test.py`: 19 cases (6 exec blocks, worker build, worktree-path build, hub git `-m`, doc heredoc, here-string, grep/rg, 3 hub edit blocks, hub doc edit, worker edit, bad payload, non-object payload).
- `.gitignore`: `.claude/worktrees/` and `.claude/settings.local.json`, so the main checkout's status stays clean once `.claude/settings.json` is tracked.

## Fail-open behaviour
Only exit 2 blocks in Claude Code; any other non-zero exit is a non-blocking hook error and the tool runs.
- Python missing → shell exits 127 (bash) / 9009 (cmd): non-blocking, the tool runs. Verified: `PATH` without python → 127.
- Guard script missing → the wrapper exits 0. Verified with `CLAUDE_PROJECT_DIR=C:/nowhere`.
- Bad payload → 0 (self-test).

## Validation
- `python -I Tools/Studio/hub_guard_test.py` (run from this worktree) → 19/19 PASS.
- Hook command from `settings.json` run through bash against a fake hub root in the scratchpad: Tools edit 2, Docs edit 0, `blender -b -P` 2 (with message), guard missing 0, python missing 127.

## Notes for the Hub
- After merging, delete the untracked prototype `Tools/Studio/hub_guard.py` and `.claude/settings.json` in the main checkout first, or git refuses to overwrite them.
- Known gaps (by design, a guard against accidents, not an adversary): `Start-Process $Unity`, a variable holding the exe, or `python Tools/Blender/…` are not caught. `-batchmode` inside an unquoted `grep -- -batchmode` would be blocked.
- Every `studio.ps1` invocation is blocked in the main checkout, read-only `status`/`doctor` included, matching the prototype. Allowing those is a Hub call.
