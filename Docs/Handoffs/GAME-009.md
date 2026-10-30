# Handoff: GAME-009 (medical customers) + W5N m2, W5S m1/m2

**Status:** done, pending review. Branch `claude/task-game-009` (main merged at ffdf61f). No `Code/Domain/` edits.

## Changes
- **Customers** (own `Random(seed + 13)`, so the slice draws are unchanged): `medicalCustomerShare` 0.04 (DEC-048) are MED patients. `outOfStateMedChance` 0.2 of them hold an out-of-state card. 14-day history = 0–`medicalHistoryMaxBuys` 3 prior buys of a `weightOdds` weight [GDD].
- **Sale type** (`ShiftSim.MedicalSale`, `ToggleSaleType`, T key / button; MED customers only): it defaults to Medical.
  - `TaxRate` is `medicalTaxRate` 9.1 % (F4) or pricing's 25.1 %. Cards use `Pricing.ApplyTax(pre, TaxRate)`; the POS rounds to the nickel once on the cart total (DEC-035).
  - `CartCap` is the allotment left (`medicalLimitGrams14d` 70.87 − history, A5) or 28 g. A medical sale ignores the 28 g cap.
- **Over-allotment:** MED patients may trim like over-limit customers (`Customer.CanTrim`). Cancel on a red cart = refusal / no-sale (DEC-073).
- **Out-of-state card rung as medical:** the 1st Confirm is blocked with a hint toast; later ones add a strike (GAP-COMP-04 [GDD]). Adult-use then sells under the 28 g cap.
- **Report:** `MedCustomers`, `MedSales`, `MedTaxCollected`, `AdultUseTaxCollected` (`SaleEvent.Medical`). The medical rows hide when the shift had no MED customer (UX_PS1 §6).
- **View** (UX_PS1 §5):
  - `✓ MED card verified` replaces the 21+ badge; `⚠ Card: out-of-state` badge.
  - Meter "14-day remaining {g} / {left} g" with the allotment caption and `✗ Over the 14-day allotment`; tax line `Tax 9.1% (medical)`.
  - The sale-type switch sits in the payment row.
- **W5N m2:** at 125/150 % the ID panel header carries a one-line Counter line (queue size, ● / ◐ / ▲ counts, stand count), because the full-safe-area panel hides the HUD strip.
- **W5S m1:** `TUNING_PS1.md` line 46 seed-1 numbers updated: careless 61.6, slow 59.9 (re-measured; perfect 83.7).
- **W5S m2:** `IdCheckTests.SimBot_WorksTheStand_Lawfully_NoStrike` forces the prompt in the default suite, so RunBot's `workStand` path and the no-strike assert run.
- **Bots** (EditMode `RunBot`, PlayMode `Step`, `SlicePersonaTests`, `PerfCapture`): add an item only while it fits under `CartCap`; switch an out-of-state card to adult-use; a lone red medical line switches to adult-use. **`PerfCapture.cs` and `SlicePersonaTests.cs` are outside my packet;** without these changes the bots stall on medical customers.
- **Capture:** `[Timeout(900000)]` (the retuned 16-customer shift runs past 180 s). The sale-toast shot now fires on the first sale, since the first cart may be 2 lines.

## Validation (studio.ps1, Gameplay's Unity slot)
- **Compile and tests:** compile OK. EditMode **215 passed + 2 skipped** of 217; the 2 skips are GAME-010's `[Explicit]` Balance/Explore sweeps (DEC-072), not failures. Gate A (DEC-067): all 131 parity + golden tests pass. PlayMode 8 passed + 1 skipped (the GPU capture).
- **New `MedicalTests` (7):**
  - 3.5 g medical total = CheckoutRound(pre × 1.091);
  - 42 g passes with 70 g left and is blocked with 35 g left (no stock change; a trim then sells);
  - out-of-state: blocked, then strike, then adult-use sells at 25.1 %; adult-use keeps 28 g;
  - the adult path is unchanged ($13.15 / $13.10 golden; switch is MED-only);
  - generator share / history / out-of-state;
  - the bot serves a 50 % medical shift (taxes add up, never an out-of-state medical sale).
- **`unity-capture` PASS, 27 shots:** the out-of-state MED register at 100/125/150 % (badges, meter, tax line and switch on screen); the ID panel header strip at 125/150 % (one line, uncut, clear of title and date). Shots: `Docs/Assets/Specs/GAME-009_*.png`.
- **Seed 1** (16 customers): 16/16 served, 25 lines, $602.90, Rainbow Drip sold out, 0 strikes.

## Notes / questions (through the Hub)
- At an amber medical meter no state word is shown, because "Near the 1 oz limit" is adult-use copy and UX_PS1 §8 has no medical amber string. UX may add one.
- Is the history mix right? A patient can arrive with history ≥ 70.87 g (3 × 28 g), i.e. no allotment left, who can only buy adult-use. Does the real store see such patients? (GAP-COMP-01/04 area.)
