# Dispensary Game — Claude Code Instructions

Studio structure (DEC-116/117): **Nolan → Studio Hub → sessions (workers, fresh short-lived reviewers, integrators, planners) → Hub fast-forwards `main`.** No leads, departments or standing reviewers. The Hub only dispatches sessions, relays messages and questions, fast-forwards `main` and archives sessions; it never does task work or runs in-Hub agents (DEC-128..132). The operating model (roles, sources of truth, read sets, packets, briefs, escalation, review, integration, Hub restart) is `Docs/STUDIO_OS.md` **§0 only**; everything below §0 there is history.

## Start here (by role)
- **Studio Hub:** `Docs/HUB_RESUME.md` (hard rules and per-message actions) and `Docs/PROJECT_STATE.md`. Nothing else.
- **Worker:** your packet `Docs/Tasks/Active/<TASK_ID>.md`, then only the docs and sections it cites. Do not load `PROJECT_STATE.md`, `BACKLOG.md`, `Docs/Departments/` or the documentation tree.
- **Reviewer:** the packet, the diff, the handoff's Validation and Not-done sections, the acceptance sources the packet cites (STUDIO_OS §0.3/§0.7). Nothing else.

## Rules (canonical; `AGENTS.md` only points here)
- The original Three.js/browser *game* source is unavailable; use `NO_SOURCE_RECONSTRUCTION_BASELINE.md`. The budtender *tool* source IS available locally and is the top authority for recommendation logic (DEC-001/002/006 in `Docs/DECISIONS.md`): read-only, no PII.
- $0 third-party asset budget. Free software pipeline.
- Do not invent missing store/reference facts. Do not hallucinate inventory or product data. Every store value cites a source or is a labelled GAP (DEC-047).
- Reality/reference fidelity outranks generic dispensary aesthetics.
- Customer PII/CRM behavior is not part of the target game.
- Preserve canonical behavior, not obsolete browser architecture.
- Stay within your packet's `Owns` paths. Avoid unrelated refactors. Run the packet's validation.
- Record durable decisions in repository docs, never in chat: propose DEC/GAP entries in your handoff's `## For the Hub`.
- Write a concise handoff at `Docs/Handoffs/<TASK_ID>.md` (STUDIO_OS §57), commit it on your branch, then ONE line to the Hub. When the deliverable is complete, stop; a new task uses a fresh context.
- **Resolve routine uncertainty yourself (DEC-105/110, STUDIO_OS §0.6):** search the docs your packet cites, then `Docs/DECISIONS.md`, `Docs/KNOWN_GAPS.md`, the floor plan / TI drawings and `Docs/Reference/*.json` for anything about layout or size, then `Docs/Research/` and `Docs/Handoffs/REF-008.md`. If they answer it, apply and cite. If not, use a labelled GAP placeholder, keep working, and list the question in the handoff with what you searched. A question Nolan already answered or skipped is never asked again.
- **Stop and message the Hub at once only for:** scope change, an edit needed outside your `Owns`, contradicting authoritative sources, risk of lost work, a blocked dependency.
- **Chain of command (DEC-033/098): nobody below the Hub contacts Nolan.** No AskUserQuestion, no questions or "want me to…?" in your messages. Anything he must know or decide goes in the handoff marked `FOR NOLAN`; the Hub forwards it. If Nolan writes to you directly, answer him fully and record what he said in your handoff.
