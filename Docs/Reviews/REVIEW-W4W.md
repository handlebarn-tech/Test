# REVIEW-W4W — GAME-006 cart (multi-line deli sales)

**Verdict: PASS with one fix required (already applied on the review branch).** `claude/compassionate-nobel-de4c9e` @ 19b2866 merged `--no-ff` into `review/wave-4w` off main fe906c7 (clean merge). The merge did **not compile** because of a collision with PERF-001 (B1). I fixed it in a separate commit, and with that fix every gate is green. GO to merge **including that commit**.

## Blocker (fixed in this branch)
- **B1 `PerfCapture.cs` calls `SliceGame.PosSelectWeight`, which GAME-006 removed.** PERF-001 landed on main after GAME-006's base, so the branch could not see it. Raw merge: `csErrors=1` (`PerfCapture.cs(87,41) CS1061`), and compile, EditMode, PlayMode and capture all fail. The review commit changes PerfCapture's bot to the same loop as `SliceBotTests.Step`: ask from `CurrentAsk.Family`, card from `Free(batch) >= CurrentAsk.Grams`, `AddItem()` while `CanAddItem`, else `PosConfirm()`. PERF-001's baseline numbers were not re-run; the 2-item customers change its load slightly, so the Hub may want to re-baseline.

## Gates (single editor through `studio.ps1`, DEC-013; two editors at once not tested)
- `unity-compile` csErrors=0. `unity-test-edit` **174/174** (includes 8 new `CartTests`, the DEC-065 `LeaveRegister_KeepsCart_CancelEmpties`). `unity-test-play` 8 passed, 1 skipped (the GPU capture under `-nographics`). `unity-capture` graybox QA PASS (max deviation 0.22 ft), slice 11 shots.
- **Gate A (DEC-058):** QA-002 is not on main, so I overlaid `TfsParityGateTests` + data from `review/wave-4t` (uncommitted, removed afterwards): compile OK, EditMode **185/185**, the 11 `TfsParityGateTests` pass. No `Code/Domain/` edit in the GAME-006 diff.

## Register on screen (what nobody had seen)
- Slice shot 07 (single line, `Docs/Assets/Specs/SLICE_contact_sheet.png` path) and a temporary extra capture of a 2-line cart, saved as `Docs/Assets/Specs/REVIEW-W4W_Pos_MultiLine.png` (the capture test itself was reverted): Kush Cake 3.5 g $7.00 + Scented Marker 3.5 g $36.00; Subtotal $43.00, Tax $10.80, **Total $53.80** (43.00 × 1.251 = 53.793, rounded once to the nickel, DEC-035); `Scale: 7.00 g`; `+ Add item` greyed (every ask is in the cart, DEC-065 #3); `Customer asked for an eighth + an eighth`; ID badge kept. The MSRP/deal lines are hidden for 2+ lines.

## Checks
- **28 g across lines (DEC-036 M1):** `Confirm` blocks on `CartGrams` summed over all lines before anything else; tests: 14 + 14 sells, 14 + 14 + 3.5 blocked with no stock change. Lines on one batch add up against the jar (`GroupBy(BatchId)`), and `StepLine` skips weights the jar cannot hold.
- **Nickel rounding (DEC-035):** rounded once on the cart total; the last line takes the remainder so the sale events add up to the register total. `house 2 × 3.5 g = $26.25` test.
- **DEC-044:** `PriceFit` against the cart total including the new line, both at Present and at Confirm.
- **DEC-065:** a left-out ask counts fit 0 in the mean; Esc/Back on a multi-line cart keeps the cart; a single line still cancels. All three are implemented and tested.
- **Packet and UX_PS1 §2:** the request strip ticks clauses, the cart chip and R open the register, lines show name · batch · tier with a stepper, pre-tax price and ✕, and removing the last line returns to Results. Second items roll on their own `Random(seed + 4)`, so the slice's draws and jar fills are unchanged (seed 1 keeps its DEC-027 SOLD OUT).

## Minors
- m1 The line steppers do not align between rows (the − g + / price / ✕ columns shift with the width of the name text in the screenshot); UX_PS1 asks for fixed columns. This is a USS fix and USS was outside this packet's Owns.
- m2 The cart chip string hard-codes "/ 3" instead of reading `cartMaxLines`.
- m3 `unitsPerSale` is 1.25, below the real-store ≈ 2 (RES-001 O13); raising `twoItemAskChance` is GAME-010 tuning. The handoff already notes that `SlicePersonaTests` (GAME-010) must call `AddItem` before they merge, and expects small conflicts in `SliceTests.cs`, `SliceBotTests.cs` and `SliceConfig.json`.
- m4 REVIEW-W4L M1 (text scale at 125/150 %) is covered by UX-005 §10 but not built or checked for the cart rows.
- n1 The cart-line weight stepper can set a weight that differs from the ask, and Confirm then blocks with the wrong-weight line; trimming and the over-limit decision are GAME-007.
