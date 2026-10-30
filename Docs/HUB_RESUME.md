# HUB RESUME — read this first if you are the Studio Hub

Everything a fresh Hub session needs. No chat history is required.

## Your role (user directives, 2026-10-29)
- You are the project manager and boss. Workcell sessions report to you; you supervise them and keep them on the plan.
- You report to the user (Nolan) only for big decisions (scope, budget, direction, real-store facts) and give progress updates at milestones and when a wave of sessions finishes.
- Make routine technical/process calls yourself; record them in `Docs/DECISIONS.md`.
- **The Hub stays thin (DEC-010):** planning, dispatch and communication only. Work, including handoff review/QA, runs in sessions you start (`start_session`). Group related tasks into a session as you judge best (a session may run several tasks or its own subagents); retire a session when its work is done and start fresh ones for new work (DEC-011). Read only task packets, `Docs/Handoffs/*.md`, and the state files. Never read large sources, images or logs yourself.

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
- Starting a session: give it its packet path and "read CLAUDE.md, then the packet; report to the Studio Hub when done". Use a worktree for code/Unity work.
- The TFS tool's own hub is the peer session "TFS tool: project hub (phases 1-7)". Relay tool defects there; never edit its files.
