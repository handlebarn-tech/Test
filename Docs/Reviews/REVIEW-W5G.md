# REVIEW-W5G — GAME-007 (limit meter, over-limit asks and trims, strike ledger) + W4W m1/m2/m4

**Verdict: PASS with minors (GO to merge).** `claude/task-game-007` (a6ab1dc + 5cc916a) merged `--no-ff` into `review/wave-5g` off main dee39f4; clean merge (W5A not yet on main; the two touch different files). No `Code/Domain/` edit (the diff is Simulation/Slice, Presentation/Slice, one USS file, data, tests, and `PerfCapture.cs`, see m3).

## Gates (single editor via `studio.ps1`, DEC-013; two editors at once not tested)
- `unity-compile` csErrors=0. `unity-test-edit` **194/194**, including **Gate A (DEC-067)**: the 11 `TfsParityGateTests` plus the Engine/Parser goldens, all passing, and 9 new `OverLimitTests`.
- `unity-test-play` 8 passed, 1 skipped (GPU capture). `unity-capture` graybox QA PASS (max deviation 0.22 ft), slice **14 shots**, including the red 3-line register at 100/125/150 %.

## Checks
- **SPEC_COMP002 §2 / DEC-036 — PASS.** Over-limit Confirm stays blocked, and there is no path to sell above 28 g (an over-limit customer accepts a line at most equal to its ask, never above). The three ask shapes (31.5, 56 and 35 g) come from the spec, with weights from `STD_WEIGHTS`. They roll on their own `Random(seed + 7)`, so seed 1 is unchanged (12/12, $364.00). The meter is `cartFlowerGrams / 28`, Neutral < 0.75, Amber to 1.0, Red above 1.0, with a 75 % tick, state words and the "Remove a line or step a weight down" hint, which does not say which line to drop (that is the decision). The concentrate row is not built (PS3, DEC-048).
- **Trim scoring — PASS.** A trimmed-out item does not count against fit. Removing or stepping down the primary ask costs `primaryTrimFitPenalty` (0.5) × its fit (test). An ask never added still counts 0 (DEC-065).
- **DEC-073 — PASS.** Cancel while the cart is still over the cap = the customer refuses and leaves (no-sale, `overLimitLeave`); Cancel on a legal cart only empties it. Text scale is a `SliceGame` field (no settings screen), honoured by the register and meter only.
- **StrikeLedger — PASS.** `Strike {Reason, CustomerIndex, Time}`, an `Added` event, a strike toast (6 s) and report rows `Strikes`, `OverLimitTrims`, `ManagerReview` at 2. It has no strike source until GAME-008/009, so those rows cannot be seen in play yet; strikes never end the shift.
- **Text scale (W4W m4) — PASS for the register and meter.** I viewed the fresh 100 % and 125 % shots and the branch's 150 % shot. At 125/150 % the register is two columns inside the safe area and does not scroll (names and batch·tier ellipsize with a tooltip; the − g + / price / ✕ columns are aligned across all three lines); the red meter, hint, totals and Confirm (dimmed, disabled) are all visible, and the toast does not cover the register. At 100 % the red 3-line cart fits inside the panel. The capture test also asserts the alignment, safe-area fit and one-line meter cells at each scale. W4W m1 (column alignment) and m2 (cart chip reads `cartMaxLines`) are fixed.

## Minors
- m1 The red meter bar renders orange-red; the ✗ icon and the words carry the state (not colour only), but confirm the fill uses the UX `--bad` token.
- m2 125/150 % covers only the register and meter; the cover prompt, ID card and strip belong to GAME-008/017 (DEC-073). There is no settings screen yet (later UX task).
- m3 `PerfCapture.cs` is outside GAME-007's Owns; the change (bot trims a red cart) is necessary, since the bot would otherwise hang on a blocked over-limit cart, and it is small. Fine, but note it for PERF-001's owner.
- m4 `overLimitAskChance` 0.06 gives no natural over-limit customer in seed 1, so a normal 12-customer shift rarely shows the feature; GAME-010 tuning. The Cancel-as-refusal rule has no pre-warning in the register that I could see; I did not test the on-screen text.
- m5 GAME-010's persona bots need the trim rule (the handoff notes this). Overlap with `SliceConfig.json`, `SliceTests.cs`, `SliceBotTests.cs` and `Customers.cs` expected.
