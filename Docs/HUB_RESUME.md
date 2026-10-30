# HUB RESUME — read this first if you are the Studio Hub

Everything a fresh Hub session needs. No chat history is required.

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
1. Read `Docs/PROJECT_STATE.md`, `Docs/BACKLOG.md`, the last ~10 entries of `Docs/DECISIONS.md`.
2. Check new handoffs in `Docs/Handoffs/`.
3. Send finished work to a REVIEW session; commit only reviewed work.
4. Move task packets `Docs/Tasks/Active` → `Done`; update BACKLOG and PROJECT_STATE.
5. Write packets for the next dependency-ready tasks; start sessions for them, grouped sensibly (code/Unity work in its own worktree, doc-only work may share the checkout on disjoint files, per DEC-005).
6. Brief the user.

## Key facts
- Repo: `C:/Users/handl/Downloads/Dispo Game` (git, branch `main`). Machine/tool paths: `Docs/MACHINE_PROFILE.md`.
- Unity 6000.6.7f1 + HDRP 17.6.0 (DEC-003). Blender 5.2.3 LTS (DEC-007).
- Budtender tool source: `C:/Users/handl/Downloads/tfs-budtender`. It is the top authority for recommendation logic (DEC-001/002/009). It has its **own active hub and sessions**, so it is read-only for us, and no PII may leave it (DEC-006).
- Priority: shortest path to a playable vertical slice (DEC-008).
- Packet format: see the existing `Docs/Tasks/*/REF-001.md`, `MIG-001.md`, `BUILD-001.md` (goal, inputs, owns, deliverable, validation, handoff).

## Where things stand
See `Docs/PROJECT_STATE.md` → "NEXT ACTIONS". Wave 1 is complete and sits on branch `review/wave-1` awaiting REVIEW-W1. Packets for the next sessions are in `Docs/Tasks/Ready/`.

## Session notes
- Starting a session: `start_session` user_asked, fresh, `use_worktree: true`, `source_branch: main`; brief = packet path + "read CLAUDE.md, then the packet; never ask Nolan; end with a ≤15-line summary for the Studio Hub" + commit identity `git -c user.name=Nolan_Bradford -c user.email=handlebarn@gmail.com commit` (no global git identity is set). Reviews merge task branches onto `review/wave-*`; the Hub merges reviewed branches into main with the same identity.
- Unity: max 2 editors (DEC-013); studio.ps1 has a wait gate. Fresh worktrees copy `Tools/Studio/studio.config.example.json` → `studio.config.json`.
- Message a running session with SendMessage `to` = its `local_…` id (listed in PROJECT_STATE). `list_sessions {"linked": true}` shows the family.
- The TFS tool's own hub is the peer session "TFS tool: project hub (phases 1-7)". Relay tool defects there; never edit its files.
