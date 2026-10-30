# GAME-009 — Medical customers

**Role:** GAME · **Priority:** P2 · **Branch:** `task/GAME-009` worktree off `main` (GAME-007 and **GAME-008 merged**: both own Simulation/Slice, Presentation/Slice and SliceConfig/SliceLines keys, so they run one after the other; AUDIT-001 A3, DEC-064)

## Goal
Add medical customers with a rolling 14-day allotment, medical tax, and out-of-state cards that must be sold as adult-use (`Docs/Design/SPEC_COMP002.md` §4).

## Read
`Docs/Design/SPEC_COMP002.md` §4, §7, §8 (GAP-COMP-01/04/05/06); `Docs/Research/AZ_COMPLIANCE.md` A5–A7, F1/F4; `Docs/Specs/UX_PS1.md` medical POS mode; `Docs/Handoffs/GAME-007.md`.

## Owns
Simulation/Slice (customer type, 14-day history, tax path), Presentation/Slice (badge, meter, adult-use switch), SliceConfig/SliceLines new keys, EditMode tests. Tax stays a config value; call the existing `ApplyTax(pre, rate)` with the medical rate (no Domain edits).

## Deliverable
1. `medicalCustomerShare` 0.04 (DEC-048: medical is under 5 %; the exact value is [GDD]; was the 0.10 GAP-COMP-01 placeholder); POS badge "MED card verified".
2. Seeded 14-day history (0–3 prior buys of 3.5–28 g); meter = `medicalLimitGrams14d` 70.87 − history. The 28 g adult-use cap does not apply to a medical sale; the remaining allotment does. Over-allotment asks trim as in GAME-007.
3. `medicalTaxRate` 0.091 (F4); nickel rounding (DEC-035); report rows `medSales`, `medTaxCollected`, `adultUseTaxCollected`.
4. Out-of-state card at `outOfStateMedChance` 0.2: the player must switch the sale to adult-use (25.1 %, 28 g cap); the first wrong attempt is blocked with a hint, later ones add a strike (GAP-COMP-04).

## Validation
Compile/EditMode/PlayMode green. Tests: medical 3.5 g total = pre × 1.091 rounded to $0.05; a 42 g medical sale passes with 70 g remaining and is blocked with 35 g remaining; an out-of-state card cannot confirm as MED; the adult-use path is unchanged (slice price goldens). DEC-013 gate.

## Handoff
`Docs/Handoffs/GAME-009.md` (≤40 lines). Questions go to your department lead (DEC-033, DEC-094).
