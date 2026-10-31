# HISTORY — how the studio's structure changed, and where the old text lives

Append-only. Purpose: a future Hub or recovery pass can find any earlier version of a rule, state file or role doc without anything having to stay in the live tree. Read an old version with `git show <sha>:<path>`. Checkpoint tag: `pre-recovery-2026-10-30` (= `main` @ 62d1050).

| Date (Phoenix) | Structure / decision | Live text at the time (read with `git show`) | Why it changed |
|---|---|---|---|
| 2026-10-29 21:05 | Bootstrap: thin Hub + workcells + repo memory (STUDIO_OS §50–58 original) | `2075712:Docs/STUDIO_OS.md`, `2075712:CLAUDE.md` | original handoff |
| 10-29 21:12 → 10-30 04:19 | Hub = PM; DEC-010 thin Hub, DEC-045 hard rules + `hub_guard`, DEC-085 standing reviewer pool. HUB_RESUME grows to its richest form. | `de9dc7e:Docs/HUB_RESUME.md` (8.1 KB: standing directives, Hub loop, key facts, session notes), `fcd9b44:Docs/PROJECT_STATE.md` | scale |
| 10-30 07:08 DEC-094 | Departments: Hub → leads → worker subagents; STUDIO_OS §0 (departments version); `Docs/Departments/*.md` | `d000b43:Docs/STUDIO_OS.md` §0, `1ab4e3d:Docs/HUB_RESUME.md`, `49c3970:Docs/PROJECT_STATE.md` (roster) | Hub congestion |
| 10-30 07:48 DEC-112 | Flatten; leads retired | same files | "a disaster, what a waste of money" (two-hop questions, re-reads) |
| 10-30 08:31 DEC-116 | Restartable Hub; HUB_RESUME and PROJECT_STATE cut by half | `6b54008:Docs/HUB_RESUME.md`, `bb511ea:Docs/PROJECT_STATE.md` | cheap Hub resets |
| 10-30 09:17 DEC-117/118/119 | Control plane consolidated (Fable): one rules file, §0 flat, dept files archived, rulings → DEC-118, roadmap | `b29aa29`, `9823517` | fix inconsistency after the lead experiment |
| 10-30 12:08–13:01 DEC-120..133, DOC-005 | Dispatcher-only Hub: reads two files, planner + integrator sessions, spare pool, cards + PO relay | `8ed4129:Docs/HUB_RESUME.md`, `8ed4129:Docs/STUDIO_OS.md` §0, `154be82:Docs/HUB_RESUME.md`, `Docs/Handoffs/DOC-005.md` | cost pressure; Hub was doing intake inline |
| 10-30 evening RECOVERY-001 DEC-138..142 | Hub = project manager again with `PROJECT_BRIEF.md`; planner/integrator/spares retired; background Agents on peer-triggered turns; reviewer fast-fail; model tiers + caps; truth-file guard | current files; forensic report `Docs/Audits/RECOVERY-001.md` | the Hub had lost its brain by rule; usage blow-out (see report §3) |

## Superseded decision chains (newest wins)
- Structure: DEC-010 → DEC-085 → DEC-094 → DEC-112 → DEC-116/117 → DEC-128/132/133 → **DEC-138/139**.
- Session starts on peer-triggered turns: DEC-128 (Agent fallback) → DEC-129 (push request) → DEC-130 (PO session relay) → DEC-133 (spare pool) → **DEC-139** (background Agent in a worktree).
- Hub reading set: HUB_RESUME "Hub loop" (de9dc7e) → §0.6 (DEC-094) → §0.3 (DEC-117) → DOC-005 (two files) → **§0.3 (DEC-138)**.
- Integration: Hub merges `review/*` (DEC-045/085) → leads merge-ready (DEC-094/099) → integrator sessions (DEC-132) → **Hub integrates (DEC-138)**.
- Door hardware: DEC-110 W5/W6 → amended by DEC-115.
- Gloves: DEC-126 → DEC-127. Jar density: earlier thinning → DEC-121.
