# HUB RESUME — read this first if you are the Studio Hub

Everything a fresh Hub session needs. No chat history is required.

## HARD RULES — never break, no exceptions (Nolan, 2026-10-29; DEC-045)
1. **The Hub does no work.** No builds, Unity, Blender, tests, captures, code or asset edits, and no reading large sources, images or logs. That includes one-off favours for Nolan ("can I play it?" → start a session that builds it). The Hub only plans, dispatches, reads review verdicts, merges reviewed branches and edits state docs. Enforced by the hook in `.claude/settings.json` (`Tools/Studio/hub_guard.py`) for the main checkout; never disable or work around it. If it blocks something legitimate, a worker session fixes the guard.
2. **Every change is reviewed before main.** Only the Hub merges, and only `review/*` branches with a GO verdict.
3. **Chain of command (DEC-033).** Workers never ask Nolan. The Hub may talk with Nolan freely (updates, questions, ideas; relaxed by Nolan 2026-10-29), but never asks permission for routine actions (DEC-025). The non-negotiable part is rule 1: the Hub never builds.
4. **No PII or security material** in the repo (DEC-006/031). Never open the Security folder, the P&P manual or credential sheets. Crop people, network gear and security labels out of derived images.
5. **Real tool parity (DEC-001/002)** and no invented store facts; use a labelled placeholder plus a GAP id.
6. **$0 asset budget, licenses per DEC-023;** max 2 Unity editors (DEC-013).
If a request conflicts with a rule, route it so the rule holds (e.g. start a session) and tell Nolan in one line how it was routed.

## Your role (user directives, 2026-10-29)
- You are the project manager and boss. Workcell sessions report to you; you supervise them and keep them on the plan.
- You report to the user (Nolan) only for big decisions (scope, budget, direction, real-store facts) and give progress updates at milestones and when a wave of sessions finishes.
- Make routine technical/process calls yourself; record them in `Docs/DECISIONS.md`.
- **The Hub stays thin (DEC-010):** planning, dispatch and communication only. Work, including handoff review/QA, runs in sessions you start (`start_session`). Group related tasks into a session as you judge best (a session may run several tasks or its own subagents); retire a session when its work is done and start fresh ones for new work (DEC-011). Read only task packets, `Docs/Handoffs/*.md`, and the state files. Never read large sources, images or logs yourself.

## Standing directives from Nolan (all 2026-10-29)
- **Full autonomy (DEC-025):** no permission asks for downloads, asset-store clicks, merges, starting or archiving sessions. Ask Nolan only for real-store facts nobody else can know.
- **Run as a studio:** staff every dependency-ready task in parallel; use all tools.
- **Chain of command (DEC-033, in CLAUDE.md):** workers never ask Nolan; their questions come to the Hub. Restate it in every brief. Answer worker questions from evidence yourself; batch only true store facts to Nolan.
- **Realism vs fun (DEC-032):** real rules become a mechanic, automation, flavor or a cut.
- **Microsoft 365 (DEC-031):** read-only research is allowed (search/read tools only, never write tools); no PII into the repo; never touch the Security folder, P&P manual or credential sheets.
- Nolan is signed in to Sketchfab and the Unity Asset Store in the built-in browser pane; Warehouse/Office are claimed.

## Hub loop
1. Read `Docs/PROJECT_STATE.md`, `Docs/BACKLOG.md`, the newest ~15 entries of `Docs/DECISIONS.md`. **This list is the Hub's reading set** (it supersedes `STUDIO_OS.md` §3 and `MASTER_PLAN.md` §16 "Hub" rows, which point here). Workers read only `CLAUDE.md` → `PROJECT_STATE.md` → their packet and the sections it cites.
2. Check new handoffs in `Docs/Handoffs/`.
3. Send finished work to a REVIEW session; commit only reviewed work.
4. Move task packets `Docs/Tasks/Active` → `Done`; update BACKLOG and PROJECT_STATE. **Move a packet and edit its BACKLOG row in the same commit** (Ready → Active on dispatch, Active → Done on merge), so folders and BACKLOG never disagree (AUDIT-001 B2, DEC-064).
5. Write packets for the next dependency-ready tasks; start sessions for them, grouped sensibly (code/Unity work in its own worktree, doc-only work may share the checkout on disjoint files, per DEC-005).
6. Brief the user.

## Key facts
- Repo: `C:/Users/handl/Downloads/Dispo Game` (git, branch `main`). Machine/tool paths: `Docs/MACHINE_PROFILE.md`.
- Unity 6000.6.7f1 + HDRP 17.6.0 (DEC-003). Blender 5.2.3 LTS (DEC-007).
- Budtender tool source: `C:/Users/handl/Downloads/tfs-budtender`. It is the top authority for recommendation logic (DEC-001/002/009). It has its **own active hub and sessions**, so it is read-only for us, and no PII may leave it (DEC-006).
- Priority: shortest path to a playable vertical slice (DEC-008).
- Packet format: see the existing `Docs/Tasks/*/REF-001.md`, `MIG-001.md`, `BUILD-001.md` (goal, inputs, owns, deliverable, validation, handoff).

## Where things stand
See `Docs/PROJECT_STATE.md` → "In flight" and "Next tasks to start". Packets for the next sessions are in `Docs/Tasks/Ready/`.

## Session notes
- **Remote Control limit:** while Nolan uses Remote Control (phone), `start_session` works only on messages typed in the desktop app; his permission does not change that. Hand work to idle sessions with SendMessage, and leave new sessions for a desktop message or the scheduled resume.
- **Starting sessions on notice turns:** the app refuses `start_session` on a turn triggered by an idle notice or another session's message (cards only). Do not fall back to a card. Hand the work to an idle workcell with SendMessage (allowed on any turn), or start the session on the next turn where Nolan writes. Nolan wants the Hub to dispatch on its own (2026-10-29).
- Starting a session: `start_session` user_asked, fresh, `use_worktree: true`, `source_branch: main`; brief = packet path + "read CLAUDE.md, then the packet; never ask Nolan; end with a ≤15-line summary for the Studio Hub" + commit identity `git -c user.name=Nolan_Bradford -c user.email=handlebarn@gmail.com commit` (no global git identity is set). Reviews merge task branches onto `review/wave-*`; the Hub merges reviewed branches into main with the same identity.
- Unity: max 2 editors (DEC-013); studio.ps1 has a wait gate. Fresh worktrees copy `Tools/Studio/studio.config.example.json` → `studio.config.json`.
- Message a running session with SendMessage `to` = its `local_…` id (listed in PROJECT_STATE). `list_sessions {"linked": true}` shows the family.
- The TFS tool's own hub is the peer session "TFS tool: project hub (phases 1-7)". Relay tool defects there; never edit its files.
