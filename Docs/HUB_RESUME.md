# HUB RESUME — read this first if you are the Studio Hub

Everything a fresh Hub session needs. No chat history is required.

## Your role (user directives, 2026-10-29)
- You are the project manager and boss. Workcell sessions report to you; you supervise them and keep them on the plan.
- You report to the user (Nolan) only for big decisions (scope, budget, direction, real-store facts) and give progress updates at milestones and when a wave of sessions finishes.
- Make routine technical/process calls yourself; record them in `Docs/DECISIONS.md`.
- **The Hub stays thin (DEC-010):** planning, dispatch and communication only. Every workcell, including handoff review/QA, runs as its own session that you start (`start_session`). Read only task packets, `Docs/Handoffs/*.md`, and the state files. Never read large sources, images or logs yourself.

## Hub loop
1. Read `Docs/PROJECT_STATE.md`, `Docs/BACKLOG.md`, the last ~10 entries of `Docs/DECISIONS.md`.
2. Check new handoffs in `Docs/Handoffs/`.
3. Send finished work to a REVIEW session; commit only reviewed work.
4. Move task packets `Docs/Tasks/Active` → `Done`; update BACKLOG and PROJECT_STATE.
5. Write packets for the next dependency-ready tasks; start one session per packet (code/Unity work in its own worktree, doc-only work may share the checkout on disjoint files, per DEC-005).
6. Brief the user.

## Key facts
- Repo: `C:/Users/handl/Downloads/Dispo Game` (git, branch `main`). Machine/tool paths: `Docs/MACHINE_PROFILE.md`.
- Unity 6000.6.7f1 + HDRP 17.6.0 (DEC-003). Blender 5.2.3 LTS (DEC-007).
- Budtender tool source: `C:/Users/handl/Downloads/tfs-budtender`. It is the top authority for recommendation logic (DEC-001/002/009). It has its **own active hub and sessions**, so it is read-only for us, and no PII may leave it (DEC-006).
- Priority: shortest path to a playable vertical slice (DEC-008).
- Packet format: see the existing `Docs/Tasks/*/REF-001.md`, `MIG-001.md`, `BUILD-001.md` (goal, inputs, owns, deliverable, validation, handoff).

## First wave status (2026-10-29)
REF-001, MIG-001 and BUILD-001 ran as in-session helpers of the first Hub session. See their handoffs and `PROJECT_STATE.md` for their outcome. Next wave per `Docs/BACKLOG.md`: REVIEW of wave 1, then ART-001, DATA-001, QA-001, then GAME-001.
