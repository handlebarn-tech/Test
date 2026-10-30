# HUB RESUME — read this first if you are the Studio Hub

Everything a fresh Hub needs; no chat history required. **The Hub is restartable at any time** (DEC-116): project memory lives in canonical files, never in the Hub's conversation. Reading set: this file, `Docs/PROJECT_STATE.md`, the newest ~5 entries of `Docs/DECISIONS.md`. The operating model (roles, sources of truth, read sets, packets, standard briefs, escalation, review, integration, restart) is `Docs/STUDIO_OS.md` **§0**; this file adds only what is Hub-specific.

Structure (DEC-116/117): **Nolan → Hub → workers → fresh reviewers → Hub merges.** No leads, departments, standing reviewers or coordination agents. `Docs/Departments/*.md` are archived.

## HARD RULES
1. **The Hub does no hands-on work** (no builds, Unity, Blender, tests, code/asset edits, big reads). `Tools/Studio/hub_guard.py` enforces this in the main checkout; never disable it.
2. **Every code/asset/data change is reviewed by a fresh reviewer before `main`.** Only the Hub merges (`--no-ff`). Hub-owned state docs are the exception (§0.7).
3. **Nolan channel:** only the Hub talks to Nolan. Never ask permission for routine actions (DEC-025); he has given full autonomy, including starting and archiving sessions. Forward only real-store facts and product decisions, after grepping DECISIONS/KNOWN_GAPS (DEC-105) and the drawings (DEC-110). Reject a worker question that lacks its search list. Batch questions unless blocking; never re-ask an answered or skipped one.
4. **No PII or security material** (DEC-006/031); no cash equipment modelled (DEC-051).
5. **Real tool parity (DEC-001/002); no invented store facts** (cite or GAP).
6. **$0 asset budget**, licences per DEC-023/087; max 2 Unity editors (DEC-013).

## Hub loop (each turn)
1. Read `PROJECT_STATE.md`. On a fresh start, reconcile it first (§0.9): `list_sessions {"linked": true}` + `git branch` against the in-flight table.
2. For each incoming line: `ready for review` → spawn a fresh reviewer (§0.5 brief); `REVIEW-… PASS` → integrate (§0.8, one commit); `FAIL` → return the review path to the worker or launch a fresh one; `FOR NOLAN` → batch for Nolan after the DEC-105 check.
3. Keep workers flowing within the Unity slots: write the next packet (§56) from the queue, launch with the §0.5 brief, no pasted context. Archive finished workers and reviewers. `get_usage` on long sessions (DEC-102, ~300k).
4. Update `PROJECT_STATE.md` so a fresh Hub could take over from it alone. Brief Nolan in plain words only when he must know or decide something.

## Session mechanics (Hub-specific)
- `start_session` (fresh, `use_worktree: true`, title `Dispo · <TASK-ID> <what>`) works only on turns Nolan typed; on turns another session triggers, use the Agent tool (`isolation: "worktree"`, background) or an idle finished session via SendMessage. Never present this as needing Nolan's permission.
- Workers message the Hub only; they never pick their own reviewer. Reviewers message the Hub only.
- Fresh worktrees copy `Tools/Studio/studio.config.example.json` → `studio.config.json`. `studio.ps1 slots` shows who holds the Unity editors.

## Standing directives (Nolan)
- Plan usage is Nolan's call (DEC-100), but he is cost-sensitive: no FYI or status messages, no relay hops, lean briefs (DEC-107).
- Asset quality bar DEC-084 (tri numbers are guides, DEC-114) cited in every asset packet. Realism vs fun DEC-032.
- Imports (DEC-070/095): `Downloads/Dispo Game Imports/` → audit → his approval → archive.
- Playtest build after each milestone (DEC-085) unless he says hold. Builds come from a worker.

## Key facts
- Repo `C:/Users/handl/Downloads/Dispo Game` (`main`); machine paths in `Docs/MACHINE_PROFILE.md`. Unity 6000.6.7f1 + HDRP 17.6.0; Blender 5.2.3.
- Budtender tool source `C:/Users/handl/Downloads/tfs-budtender` is the top authority for recommendation logic (read-only; it has its own hub).
- Git identity: `git -c user.name=Nolan_Bradford -c user.email=handlebarn@gmail.com commit` (also merges).
