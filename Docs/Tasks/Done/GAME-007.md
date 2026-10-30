# GAME-007 — Purchase-limit meter, over-limit asks, strike ledger

**Role:** GAME · **Priority:** P1 · **Branch:** `task/GAME-007` worktree off `main` (GAME-006 merged)

## Goal
Turn the 1 oz cap from a silent block into a decision: some customers ask for more than the law allows and the player chooses what to trim (`Docs/Design/SPEC_COMP002.md` §2). Add the shift's strike ledger that GAME-008/009 reuse.

## Read
`Docs/Design/SPEC_COMP002.md` §1–2, §7; `Docs/Research/AZ_COMPLIANCE.md` A1/A4/A8; `Docs/Specs/UX_PS1.md` meter + strike sections; `Docs/Handoffs/GAME-006.md`.

## Owns
Same folders as GAME-006 (Simulation/Slice, Presentation/Slice, SliceConfig/SliceLines new keys, EditMode tests). No Domain edits.

## Deliverable
1. POS meter: `cartFlowerGrams / adultUseLimitGrams`, amber at `meterAmberFraction` 0.75, red over; concentrate row hidden (PS3).
2. Over-limit asks at `overLimitAskChance` 0.06 using the SPEC §2 ask shapes; the player removes lines or steps weights down; customer reaction per `primaryTrimFitPenalty`; no legal cart → no-sale.
3. Over-limit Confirm stays **blocked** (real POS, RES-001 O4). There is no over-limit sale path.
4. `StrikeLedger` service (reason, customer index, time) + report rows `strikes`, `overLimitTrims`; "Manager review" flag at `strikeReviewThreshold` 2. Strikes never end the shift (DEC-032).

## Validation
Compile/EditMode/PlayMode green. Tests: each ask shape generates over the cap; every SPEC trim option sells; a 31.5 g cart cannot be confirmed; trimming the primary item lowers fit by the configured penalty; the ledger reaches the report. DEC-013 gate.

## Handoff
`Docs/Handoffs/GAME-007.md` (≤40 lines). Questions go to the Studio Hub (DEC-033).
