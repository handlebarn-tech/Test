# REVIEW-PS1 — GAME-009 (medical customers) + W5N m2, W5S m1/m2

**Verdict: PASS with minors (GO).**
- I merged `claude/task-game-009` (26081fa) `--no-ff` into `review/ps1` (b5ce9f2), cut from main 97ee06f. The merge was clean.
- No `Code/Domain/` edits. Tax goes through the existing `Pricing.ApplyTax(pre, rate)` and `CheckoutRound`.
- Two edits are outside the packet: `PerfCapture.cs` and `SlicePersonaTests.cs`. The lead accepts both. Both are bot-only changes so the bots don't stall on medical carts, and they look correct.

## Gates (studio.ps1, Gameplay's slot, 0/2 in use at start; DEC-013)
- `unity-compile`: csErrors=0.
- `unity-test-edit`: 217 total, 215 passed, 0 failed, 2 skipped. Both skipped tests are `[Explicit]` (DEC-072).
- **Gate A (DEC-067):** `TfsParityGateTests` 11/11, `EngineGoldenTests` 23/23, `ParserGoldenTests` 95/95.
- New `MedicalTests`: 7/7.
- `unity-test-play`: 8 passed, 1 skipped (GPU capture).
- `unity-capture`: graybox QA PASS (23 views, max deviation 0.22 ft). Slice capture PASS, 27 shots.

## Packet validation
- **3.5 g medical total = CheckoutRound(pre × 1.091): PASS.**
  - Tested in `MedicalTests`.
  - In shot 21, $7.00 + 9.1 % = $7.637, which the register shows as **$7.65**. That is correct nickel rounding (DEC-035).
  - Cards use `ApplyTax(pre, 9.1)`.
- **42 g with 70 g left passes; 42 g with 35 g left is blocked: PASS.**
  - The blocked case returns `overMedLimit` and leaves stock unchanged.
  - Removing a line (28 g) then sells.
  - The 28 g adult-use cap is not applied to a medical sale (`CartCap` = allotment left).
- **An out-of-state card can't confirm as MED: PASS.**
  - The 1st try is blocked with a hint; the 2nd adds the strike `strikeOutOfStateMed` (GAP-COMP-04 [GDD]).
  - Switching to adult-use sells at 25.1 % under the 28 g cap again.
  - The bot test confirms no out-of-state medical sale ever happens.
- **Adult-use path unchanged: PASS.**
  - The house 3.5 g Tuesday golden still gives $13.15 at the register and $13.10 on the card.
  - The switch throws for non-MED customers.
  - Customer generation uses its own `Random(seed + 13)`, so the slice draws are unchanged.
- **Config and report: PASS.**
  - Config: `medicalCustomerShare` 0.04 (DEC-048), `medicalLimitGrams14d` 70.87 (A5), `medicalTaxRate` 0.091 (F4, provisional OPEN-4). Each is tagged with its source in `SliceConfig.json`.
  - Report rows `MedCustomers`, `MedSales`, `MedTaxCollected`, `AdultUseTaxCollected` are present. The two tax rows add up to the total tax (test).
- **Prices follow the sale type: PASS.** Cart totals, per-line display prices and the tax line all read `TaxRate` live, so toggling medical/adult-use reprices the whole cart.
- **W5N m2: PASS.** At 150 % the ID panel header shows one uncut line between the title and the date: "Counter line (0) ◆ Stand: 1 waiting" (shot 15).
- **W5S m1: PASS.** The TUNING line now says careless 61.6, slow 59.9.
- **W5S m2: PASS.** `SimBot_WorksTheStand_Lawfully_NoStrike` forces the cover prompt, so the `workStand` path runs in the default suite.
- **Shot 21 (out-of-state MED at 100 %): PASS.**
  - Both badges show.
  - Meter: "14-day remaining 3.5 g / 21.87 g". Caption: "Allotment 70.87 g · 49 g bought".
  - Tax line: "Tax 9.1% (medical)".
  - The sale-type switch is in the payment row.

## Minors
- m1 The worker reports Gate A as 131. The three named suites total 129 (11 + 23 + 95), and all of them pass. The extra 2 are probably other Domain tests; the count is cosmetic.
- m2 The out-of-state warning is only a badge. Confirm stays enabled (green) on a medical out-of-state cart, so the first hint costs the player one click. This is by design (1st try free), and UX may want the switch to pulse.
- m3 Every repeated wrong Confirm after the first adds another strike, with no cap per customer. This matches "later ones add a strike", but a double-click could take two strikes. Gameplay should decide whether to cap at one strike per customer.
- m4 The worker's questions go to the lead:
  - At an amber medical meter no state word is shown, because UX_PS1 §8 has no medical amber string.
  - A MED patient can arrive with history ≥ 70.87 g (3 × 28 g), so their medical cap is 0 and they can only buy adult-use. FOR NOLAN if the lead can't settle it: does the real store see patients who have used up their allotment?
