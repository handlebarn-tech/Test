# REVIEW-W4B — BUILD-003 (studio runner fixes + SliceCapture) + BUILD-004 (DEC-045 hub guard)

**Branch:** `review/wave-4b` = `main` (2e401e3) + `--no-ff` merge of `claude/task-build-003-0837ba` (8738078). The merge was clean (06a5739).
**Final verdict: GO.** I made one fix in review: the hub guard can no longer block a worker whose shell cwd has left its worktree (§2). The notes below don't block.

## 1. Gates (all through `studio.ps1` on 06a5739; the DEC-013 slot wait is in the script)
| Gate | Result |
|---|---|
| `doctor` | pass, all checks passed |
| `status` | pass. The result file `20261029-233513-964-37412-status.json` uses the new `-fff-PID` stamp, and grouping still lists the older results |
| `unity-compile` | pass, csErrors=0 |
| `unity-test-edit` | **143/143** |
| `unity-capture` | pass: graybox 24 shots, QA PASS (max deviation 0.22 ft); **slice: passed=1 failed=0 skipped=0 shots=10** |

## 2. BUILD-004 / DEC-045 hub guard
- Self-test `python -I Tools/Studio/hub_guard_test.py`: 19/19 on the branch, **20/20** after my fix.
- I ran my own probe against the real paths of this machine (main checkout = `C:\Users\handl\Downloads\Dispo Game`):
  - Denied in the hub (exit 2): `powershell -File .\Tools\Studio\studio.ps1 doctor`; edits under `UnityProject/` or `Tools/`, with forward slashes, a lower-case `tools`, or a `Docs\..\Tools` escape.
  - Allowed in the hub (exit 0): `git log --grep studio.ps1`, `cat Tools/Studio/studio.ps1`, `git commit -m "…studio.ps1…"`, a doc heredoc, a here-string, edits to `C:/Other/Tools/` (outside the repo), and edits to a `ToolsExtra/` sibling.
- Hook command from `.claude/settings.json`, run through bash:
  - Main checkout as the project → exit 2, with a message.
  - Worktree as the project → 0.
  - Script missing (`CLAUDE_PROJECT_DIR=C:/nowhere`) → 0.
  - Python missing (`PATH=/usr/bin`) → 127, which Claude Code treats as non-blocking.
  - Garbage payload → 0.
  - It fails open in every case the packet lists.
- **Fixed in review (worker safety):** `check()` allowed a call only when the payload's `cwd` was in a worktree. A worker whose shell cwd had moved outside its worktree (for example a `cd` into the scratchpad) was denied `-batchmode` or `& ..\studio.ps1`. I reproduced both denials.
  - Fix: also allow when `CLAUDE_PROJECT_DIR` is a worktree. The Hub's project dir is the main checkout, so the Hub's own rules are unchanged.
  - New self-test case "worker cwd outside worktree allowed".
  - With this, the guard can't block a worker session as long as its project dir is its worktree, and every workcell is started that way.

## 3. BUILD-003 (REVIEW-W3A n2/n3/n5 + SliceCapture)
- **n2:** `$Stamp` = `yyyyMMdd-HHmmss-fff-<PID>`, used for every log, result and XML. The `status` grouping regex handles both stamp forms. OK.
- **n3:** `Assert-UnityReady` re-checks `Test-ProjectLocked` after `Wait-UnitySlot` and reports `blocked` (exit 2). I checked the code; the handoff's held-lock repro shows `blocked`, and I did not repeat it.
- **n5:** `dirtyPathCount` replaces `dirtyPaths`. I fixed the spacing (`=@(` → `= @(`).
- **SliceCapture:**
  - It runs after graybox capture and QA, takes the slot again through `Assert-UnityReady`, and passes `-sliceCaptureDir`, which `SliceCaptureTests` reads.
  - A pass needs passed > 0 and failed = 0, and the summary carries the shot count. 10 shots here.
  - The skip path (no `Category("SliceCapture")`) returns before Unity runs. I checked it by reading the code; BUILD-003 ran it on a6e230c, and I did not re-run it, because the category is on main now.

## Notes (none block)
- **n1:** guard false positive: a quoted mention like `echo 'use -batchmode' >> Docs/x.md` is denied in the hub (`(^|\s)-batchmode`). The guard fails closed only in the hub, so this is safe. Reword, or use the Write tool.
- **n2:** known gaps are by design (BUILD-004 handoff): `Start-Process $Unity …` and a variable holding the exe pass. A command that names any `/.claude/worktrees/` path is allowed whatever it runs.
- **n3:** the hub can't run even read-only `studio.ps1 status` or `doctor`. Allowing those is a Hub call; I left it as it is.
- **n4:** if the project-lock re-check fires before the slice step, the graybox shots are already written but the run reports `blocked` (BUILD-003 note). Re-running is safe.
- **Merge step for the Hub:** delete the untracked prototype `Tools/Studio/hub_guard.py` and `.claude/settings.json` in the main checkout first, or git refuses the merge (BUILD-004 handoff).
