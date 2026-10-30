# Handoff: GAME-007 (limit meter, over-limit asks, strike ledger + W4W m1/m2/m4)

**Status:** done, pending review. Branch `claude/task-game-007` (off `main` 0fca821). No `Code/Domain/` edits.

## Changes
- **Over-limit asks** (`Customers.cs`): with `overLimitAskChance` 0.06, a customer asks one of the SPEC_COMP002 §2 shapes. The roll uses its own `Random(seed + 7)`, so seed 1 is unchanged. Shapes: 0 = 28 X + 3.5 Y (31.5 g); 1 = "two ounces" of X, modelled as two 28 g asks where the second can only be dropped (56 g); 2 = 14 X + 14 Y + 7 Z (35 g). Sets `Customer.OverLimit`. `CustomerGenerator.OverLimitAsks/Say/ShapeGrams` are public for tests.
- **Trims** (`ShiftSim`): Confirm still blocks anything over 28 g; there is no over-limit sale path (RES-001 O4). An over-limit customer accepts a line ≤ its ask, never above it.
- `CartFit`: a trimmed-out item doesn't count. Trimming the primary (ask 0, removed or stepped down) costs `primaryTrimFitPenalty` (0.5) × its fit. An ask never put in the cart still counts 0 (DEC-065).
- **Over-limit Cancel:** Cancel while still over the cap = the customer refuses and leaves as a no-sale (`Cancel()` returns true; line `overLimitLeave`).
- **Meter:** `MeterFraction`, `Meter` (Neutral / Amber ≥ 0.75 / Red > 1). The view shows `Flower {g} / 28 g`, a 75 % tick, state words and the trim hint. Confirm is disabled on red, and entering red fires the `overLimit` toast once. The concentrate row is not built (PS3).
- **`StrikeLedger`** (`Strike {Reason, CustomerIndex, Time}`, `Added` event) via `sim.Strike(reason)`. The strike toast has a --bad border and lasts 6 s (`strikeToastSeconds`).
- **Report:** `Strikes`, `OverLimitTrims`, `ManagerReview` (≥ `strikeReviewThreshold` 2), shown in the report's Compliance block. GAME-007 has no strike source (an over-limit sale is impossible); GAME-008/009 add sources. Strikes never end the shift.
- **W4W m1/m2:** cart lines ellipsize name and batch·tier (name tooltip); − / g / + / price / ✕ are fixed-width columns. `cartChip` and `cartFull` read `cartMaxLines`.
- **W4W m4:** `SliceGame.TextScale` (100/125/150) and `SetTextScale` set the root `.text-125/.text-150` classes.
  - At 125/150 % the register is two columns in the 1728×972 safe area and never scrolls (UX_COUNTER_INTEL §10). Payment and Confirm share a row, so a red 3-line cart fits at 100 % (was 982 px). Register toasts never cover the register.
- **Bots:** the EditMode `RunBot`, PlayMode `Step` and `PerfCapture` bots all trim red carts (drop the last line) and add the next ask only if it fits. **`PerfCapture.cs` is outside my Owns:** without this change it would hang on a blocked over-limit cart.

## Validation (studio.ps1, DEC-013 waits honoured)
- **Compile and tests:** compile OK. EditMode **194/194**, including Gate A (DEC-067): 11 `TfsParityGateTests` plus the Engine/Parser goldens, all passing. PlayMode 8 passed + 1 skipped (GPU).
- **New `OverLimitTests` (9):** each shape is over the cap (all 3 appear at chance 1); line keyword safety; meter states; 31.5 g cannot be confirmed (no stock change; Cancel = no-sale); every SPEC trim option sells; stepping above an ask is blocked; the primary-trim penalty; the ledger reaches the report (Manager review at 2); the bot trims at chance 0.5.
- **`unity-capture` PASS, 14 shots.** The last customer is forced into a 35 g ask, and its red 3-line register is shot at 100/125/150 %. Asserted at each scale:
  columns aligned (< 1 px), panel and Confirm inside the safe area, meter value and line cells one line, no toast over the title. Shots: `Docs/Assets/Specs/GAME-007_Pos_Red_{100,125,150}.png`.
- Seed 1 is unchanged: 12/12, $364.00, Kush Cake sold out; no natural over-limit customer this seed.

## Overlap
GAME-010 also touches `SliceConfig.json`, `SliceTests.cs` (I changed `RunBot`), `SliceBotTests.cs` and `Customers.cs`. Its persona bots need the trim rule.

## Questions for the Hub
1. Is "Cancel while the cart is still over the cap = the customer refuses (no-sale)" the intended reading of SPEC §2 "cannot make it legal (or refuses)"? Cancel on a legal cart still only empties it.
2. Is there a settings screen for text scale? None exists; it is a `SliceGame` field for now. Only the register and meter honour 125/150 %; the other panels in UX §10 belong to GAME-008/017.
