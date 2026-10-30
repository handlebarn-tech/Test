# GAME-003 — Full natural-language parser port + exclusions, compare, Similar

**Role:** GAME / engine · **Priority:** P1 · **Branch:** `task/GAME-003` worktree off `main` (GAME-001 merged)

## Goal
Port the v7.11.4 query parser and the remaining recommend features MIG-001 triaged as KEEP, so free-text customer requests (post-slice) and the full tool behaviour run in `Dispo.Domain`, passing every recommend golden.

## Read
`Docs/Handoffs/GAME-001.md`, `Docs/Specs/ENGINE.md`, `Docs/Reconstruction/RECONSTRUCTION_CONTRACT.md` (parser, PHRASE_MAP, exclusions, like-X, maxAnx/refine, maxPrice, role tags, compare, Similar sections), `Docs/Reconstruction/LOGIC_TRIAGE.md`, `GOLDEN_CASES.md` + `golden_cases.json`, DEC-014…017.

## Owns
- `Assets/_Game/Code/Domain/` new files under `Engine/Parser/` and `Engine/Features/`; additive changes to existing engine files only where the port requires (keep GAME-001's public API stable).
- `Assets/_Game/Code/Tests/EditMode/` new test files.
- `Docs/Specs/ENGINE.md` (extend).
- Don't touch `Simulation/`, `Presentation/`, UI or scenes (GAME-002 will own those).

## Deliverable
1. Parser: `parse(query)` → crit/neg/primary/exclusions/flags, with PHRASE_MAP and the pain-functional default, citing source lines.
2. Features: exclusions (`EXCL_MAX_PCT`), like-X, maxAnx/refine, maxPrice filter, role tags, compare, Similar, terpene rank, strain overrides / brand pricing classes as triaged KEEP.
3. Goldens: every recommend golden in `golden_cases.json` replayed from the raw query through the parser (not the recorded parse). DEC-016: MC-7 and GAP-206 get a v7.11.4 golden plus a game-expected golden; propose the DEC text in your handoff.
4. If a golden can't pass, list it with the reason; don't edit `golden_cases.json` (DEC-014).

## Validation
`studio.ps1 unity-compile`, `unity-test-edit` all green; count of goldens passing from raw queries. DEC-013 Unity gate.

## Handoff
`Docs/Handoffs/GAME-003.md` (≤40 lines). Report to the Studio Hub.
