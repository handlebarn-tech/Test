# GAME-006 — Cart: multi-line deli sales

**Role:** GAME · **Priority:** P1 · **Branch:** `task/GAME-006` worktree off `main` (GAME-002b merged; UX-002 for the view layer)

## Goal
Customers can ask for up to 3 deli items (two strains, or two weights) in one transaction, and the POS becomes a cart. This is the base for every PS1 decision (`Docs/Design/ROADMAP_POST_SLICE.md` §2).

## Read
`Docs/Design/SPEC_COMP002.md` §2, `Docs/Specs/SLICE_DESIGN.md` §2–4 and §8, `Docs/Handoffs/GAME-002.md`, `Docs/Handoffs/GAME-002b.md`, `Docs/Specs/UX_PS1.md` (UX-002, once merged), DEC-035/036/044.

## Owns
- `Assets/_Game/Code/Simulation/Slice/` (cart model, `ShiftSim` sale path, `CustomerGenerator` two-item asks)
- `Assets/_Game/Code/Presentation/Slice/` POS view (cart lines)
- `SliceConfig.json`, `SliceLines.json` (new keys only)
- `Assets/_Game/Code/Tests/EditMode/Slice/` new tests
Don't touch `Code/Domain/` (engine parity, DEC-001). No graybox edits.

## Deliverable
1. `Cart` with lines `{batchId, grams, preTax}`; one `Sell` event per line on a single Confirm; Cancel changes nothing (no reservation, unchanged rule).
2. POS total = Σ line pre-tax → tax 25.1 % → nickel rounding **once on the cart total** (DEC-035); `PriceFit` against that total (DEC-044).
3. The M1 cap applies to the cart's summed flower grams (DEC-036).
4. Generator: `twoItemAskChance` [GDD, start 0.25] → a second clause ("…and an eighth of something for energy") built from the existing family cores; each item scored with the slice fit formula; satisfaction uses the mean item fit in the existing §3.4 weights.
5. Report: `unitsPerSale` (real-store target ≈ 2, RES-001 O13).

## Validation
`studio.ps1 unity-compile`, `unity-test-edit`, `unity-test-play` green. Tests: a 2-line cart rounds once; 14 + 14 g sells; 14 + 14 + 3.5 g is blocked with no stock change; cancel leaves stock unchanged; seed determinism; the bot plays a 2-item customer. DEC-013 Unity gate (≤ 2 editors).

## Handoff
`Docs/Handoffs/GAME-006.md` (≤40 lines). Questions go to the Studio Hub (DEC-033).
