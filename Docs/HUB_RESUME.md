# HUB RESUME — read this first if you are the Studio Hub

Everything a fresh Hub needs; no chat history required. **The Hub is restartable at any time** (DEC-116): project memory lives in canonical files, never in the Hub's conversation. Reading set: this file, `Docs/PROJECT_STATE.md`, the newest entries of `Docs/DECISIONS.md`. `Docs/STUDIO_OS.md` §0 is historical where it mentions leads or departments (retired, DEC-112).

## Structure (DEC-116, Nolan 2026-10-30)
```
Canonical docs/state → Hub (fresh or restarted) → narrow workers → fresh reviewers → Hub merges
```
- **Workers:** one task each, minimum *complete* context. The packet (`Docs/Tasks/Active/<ID>.md`) points at the canonical files and sections to read directly; never a summary of a summary. Done = a committed branch plus `Docs/Handoffs/<ID>.md`, then ONE line to the Hub.
- **Reviewers:** independent and **short-lived**, one fresh reviewer per review, archived after its verdict. It reads the packet, the diff and the canonical sources itself, never the worker's or the Hub's opinion. First check every time: each store value cites a source or is a labelled GAP (an uncited value is a MAJOR). The verdict goes to the Hub.
- **Before escalating,** workers and reviewers search the authoritative docs (DECISIONS, KNOWN_GAPS, `Docs/Research/`, floor plan/TI, CCTV handoffs) and list what they searched. They come back only when the answer is missing, contradictory, or needs a new decision (DEC-105/110).
- **Hub:** priorities, packets, dispatch, merges, decisions (DEC), the Nolan channel. Keep `PROJECT_STATE.md` concise and current enough that a fresh Hub can resume in one read.

## HARD RULES
1. **The Hub does no hands-on work** (no builds, Unity, Blender, tests, code/asset edits, big reads). `Tools/Studio/hub_guard.py` enforces this in the main checkout; never disable it.
2. **Every code/asset change is reviewed before `main`.** Only the Hub merges (`--no-ff`). State docs (PROJECT_STATE, DECISIONS, BACKLOG, KNOWN_GAPS, packets) are the exception.
3. **Nolan channel:** only the Hub talks to Nolan. Never ask permission for routine actions (DEC-025); he has given full autonomy, including starting and archiving sessions. Forward only real-store facts and product decisions, after grepping DECISIONS/KNOWN_GAPS (DEC-105) and the drawings (DEC-110). Batch questions unless blocking.
4. **No PII or security material** (DEC-006/031); no cash equipment modelled (DEC-051).
5. **Real tool parity (DEC-001/002); no invented store facts** (cite or GAP).
6. **$0 asset budget**, licences per DEC-023/087; max 2 Unity editors (DEC-013).

## Hub loop
1. Read `PROJECT_STATE.md` (roster, priorities, in-flight).
2. For each message: merge GO verdicts; dispatch a fresh reviewer for each finished branch; record decisions; batch Nolan items.
3. Keep workers flowing within the Unity slots. Archive finished workers and reviewers. Check long-running sessions with `get_usage` (DEC-102 ceiling ~300k).
4. Update `PROJECT_STATE.md`. Brief Nolan in plain words, with what needs him first.

## Session mechanics
- `start_session` (fresh, `use_worktree: true`, title `Dispo · <TASK-ID> <what>`) works only on turns Nolan typed; the app refuses it on turns another session triggers. On those turns: reuse an idle finished session via SendMessage, or launch the worker/reviewer with the Agent tool (`isolation: "worktree"`, background). Never present this as needing Nolan's permission.
- Workers message the Hub; they never pick their own reviewer.
- Fresh worktrees copy `Tools/Studio/studio.config.example.json` → `studio.config.json`. `studio.ps1 slots` shows who holds the Unity editors.

## Standing directives (Nolan)
- Plan usage is Nolan's call (DEC-100), but he is cost-sensitive: no FYI or status messages, no relay hops, lean briefs (DEC-107).
- Asset quality bar DEC-084 (tri numbers are guides, DEC-114) in every asset brief. Realism vs fun DEC-032.
- Imports (DEC-070/095): `Downloads/Dispo Game Imports/` → audit → his approval → archive.
- Playtest build after each milestone (DEC-085) unless he says hold. Builds come from a worker.

## Key facts
- Repo `C:/Users/handl/Downloads/Dispo Game` (`main`); machine paths in `Docs/MACHINE_PROFILE.md`. Unity 6000.6.7f1 + HDRP 17.6.0; Blender 5.2.3.
- Budtender tool source `C:/Users/handl/Downloads/tfs-budtender` is the top authority for recommendation logic (read-only; it has its own hub).
- Git identity: `git -c user.name=Nolan_Bradford -c user.email=handlebarn@gmail.com commit` (also merges).
