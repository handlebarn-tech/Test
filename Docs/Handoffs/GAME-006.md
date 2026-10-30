# Handoff: GAME-006 (cart: multi-line deli sales)

**Status:** done, pending review. Branch `claude/compassionate-nobel-de4c9e` (off `main` 04f7bc3). No `Code/Domain/` edits, no graybox edits.

## Changes
- **Customer asks** (`Customers.cs`): `Customer.Asks` (1–2 `Ask {Family, Grams, Clause, Chip}`); `TrueFamily`/`Grams` stay as properties on ask 0, so existing callers compile. `twoItemAskChance` 0.25 [GDD] adds "…and an eighth of something for energy" from the family cores (cores with a "." skipped). Second asks never push the cart over 28 g (over-limit asks are GAME-007). Budget = floor(Σ grams × perGram).
- Second items roll on their own `Random(seed + 4)`: the slice's draws and jar fills are unchanged. Offset 1 lost seed 1's DEC-027 SOLD OUT (customer 6's 7 g of Kush Cake blocks customer 7's ounce); 20 of offsets 1–30 keep it, so I picked 4.
- **Cart** (`ShiftSim.cs`): `Cart` = `CartLine {Ask, Card, Grams, Fit, Price; BatchId, PreTax}`, plus `RegisterOpen`, `CurrentAsk`, `AddItem`, `OpenRegister`, `RemoveLine`, `SetLineGrams`, `StepLine` (skips weights the jar can't hold), `Free(batch)` (jar minus cart) and `CartPrice()`.
- `Confirm()` blocks in this order: M1 on summed grams, then wrong weight per line, then jar per batch (lines on one batch add up). Then one `Sell` per line. The total is rounded once on the cart (DEC-035), and the last line takes the rounding, so Σ events = total. `Confirm(grams)` remains the single-line path.
- `Cancel()` empties the cart with no stock change. `Pending` is now a read-only alias for the last line.
- **Scoring**: `Present` scores the current ask. `PriceFit` is taken against the cart total with the new line (DEC-044). At sale, satisfaction = §3.4 with the **mean item fit**; an ask left out of the cart counts 0 [GDD].
- **Report**: `UnitsPerSale`. Interpretation accuracy and top intents count every ask.
- **View** (`SliceGame`/`SliceView`): `Choose` becomes `Add to cart` once the cart has lines. The request strip ticks each clause. A cart chip (click / **R**) opens the register. Register lines show name · batch · tier, − g +, pre-tax and ✕, then `+ Add item` / `Cart full (3)` and Subtotal / Tax / Total. A "Units per sale" row is added to the report. New `SliceLines` keys: `andClause, secondClause, addToCart, cartChip, goToRegister, addItem, cartFull, removeLine`. New config keys: `twoItemAskChance`, `cartMaxLines`.
- **Bots** (EditMode `RunBot`, PlayMode `Step`): Add item while an ask is open, then confirm.

## Validation (studio.ps1)
- `unity-compile` OK.
- `unity-test-edit` **173/173**. New `CartTests` covers:
  - 2-line rounding: house 2×3.5 g = $26.25, not $26.30.
  - 14 + 14 g sells.
  - 14 + 14 + 3.5 g is blocked with no stock change.
  - Cancel leaves stock unchanged.
  - Step/remove; same-batch jar check.
  - Seed determinism of the asks; two-item line keyword safety.
  - The bot sells a 2-item cart.
- `unity-test-play` 8 passed + 1 skipped (the GPU capture, as before). The PlayMode bot now also asserts that a 2-item cart is sold and M1 holds on each cart.
- Seed 1: 12/12 served, 15 lines, **unitsPerSale 1.25**, $364.00, Kush Cake sold out.
- Not run: SliceCapture with graphics. Nobody has looked at the register on screen yet.

## Overlap / follow-ups
- **GAME-010** (`claude/task-game-010-2ab042`) also edits `SliceTests.cs` (other hunks), `SliceBotTests.cs` (lines 65–68) and `SliceConfig.json` (`customersPerShift`). Expect small merge conflicts.
- Its `SlicePersonaTests` call `sim.Confirm(c.Grams)` as soon as `Pending != null`, so on a 2-item customer they sell line 1 only. They need the AddItem loop, and the 16-customer run must re-check the SOLD OUT.
- unitsPerSale 1.25 is well below the real-store ≈ 2 (RES-001 O13). Raising `twoItemAskChance` is GAME-010 tuning.
- The 3rd line exists for tests and for GAME-007; the generator makes at most 2 asks.
- REVIEW-W4L **M1** (text scale at 125/150 % for the cart rows and the register) has not landed in UX_PS1. I reused the existing USS classes (USS is not in my Owns), so the cart rows are not yet checked at 150 %.

## Questions for the Hub
1. An ask left out of the cart counts fit 0 in the mean. Is that OK, or should only the sold lines be averaged?
2. Back/Esc on the register still means Cancel, which empties the whole cart (unchanged US§4). Should Esc on a multi-line cart instead go back to the cards and keep the cart?
3. `+ Add item` is disabled once every ask is in the cart: a customer is never sold an item they didn't ask for. Is that what UX intends?
