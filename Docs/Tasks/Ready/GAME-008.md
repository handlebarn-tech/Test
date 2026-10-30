# GAME-008 — ID-check events ("cover check-in")

**Role:** GAME · **Priority:** P1 · **Branch:** `task/GAME-008` worktree off `main` (GAME-007 merged. **Runs before GAME-009**, not in parallel: both own Simulation/Slice, Presentation/Slice and SliceConfig/SliceLines keys; AUDIT-001 A3, DEC-064)

## Goal
During a rush the player may cover the check-in door and admit or refuse arrivals by their ID (`Docs/Design/SPEC_COMP002.md` §3). Real flow: staff verify ID before the sales-floor door (RES-001 O2/O3), so the counter never re-checks (DEC-036 M2 stays).

## Read
`Docs/Design/SPEC_COMP002.md` §3, §7, §8 (GAP-COMP-03, GAP-COMP-08); `Docs/Research/AZ_COMPLIANCE.md` B1/B2/B4; `Docs/Specs/UX_PS1.md` ID panel; `Docs/Handoffs/GAME-007.md` (StrikeLedger).

## Owns
Simulation/Slice (ID event, ID case generator), Presentation/Slice (prompt + ID card panel), SliceConfig/SliceLines new keys, EditMode tests. Entry position: an existing ART anchor near the entry door, by name; if none fits, a `TEMP_CheckInDesk` fallback like GAME-002's, reported for ART (GAP-COMP-08). No graybox data edits.

## Deliverable
1. Prompt on rush start at `coverCheckInChance` 0.5; on accept the next `coverCheckInCount` 3 arrivals show an ID; the counter queue's patience keeps draining.
2. ID generator with the SPEC §3 case table and weights; DOB/expiry computed against an in-game date [GDD] so each case is exactly valid or invalid (`minAgeYears` 21, `verticalGraceDays` 30). Out-of-state vertical at 21+ is valid (store policy O3, GAP-COMP-03).
3. Admit/Refuse outcomes per SPEC §3; strikes via `StrikeLedger` with the B4 flavor text.
4. Report rows `idsChecked`, `badIdsCaught`, `validIdsRefused`.

## Validation
Compile/EditMode/PlayMode green. Tests: each case's validity at boundary dates (21st birthday today, vertical day 30 vs 31 after turning 21, expiry today); determinism by seed; refusing a valid ID makes a walkout; admitting an invalid ID adds one strike. DEC-013 gate.

## Handoff
`Docs/Handoffs/GAME-008.md` (≤40 lines). Questions go to the Studio Hub (DEC-033).
