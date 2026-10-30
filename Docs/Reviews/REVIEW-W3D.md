# REVIEW-W3D — GAME-002 (playable vertical-slice shift)

**Branch:** `review/wave-3d` = `main` (64ac3ee) + `--no-ff` merge of `claude/task-game-002-7f57d6` (tip 8df0a82). Merge was clean.
**Verdict (GAME-002 alone): GO with notes.** Integration with W3A/W3B (check 7) is pending the Hub's message; one must-fix for that merge is recorded below (I1).

## 1. Studio gates (DEC-013 respected: queued behind two other review editors)
| Gate | Result |
|---|---|
| `unity-compile` | OK, csErrors=0 |
| `unity-test-edit` | **41/41** passed |
| `unity-test-play` | 3 total, 2 passed, 1 skipped (GPU capture), 0 failed |
| SliceCapture (with graphics) | 1/1 passed, 10 PNGs in `Artifacts/Screenshots/901276d/slice/` (local, not committed) |

Shots, viewed one by one:
- POS: the `min-height` fix works; the 28 g tile no longer overlaps MSRP. "✓ 21+ ID verified" is shown. $7.00 + 25.1 % = $8.757, total $8.75 (nearest $0.05).
- Results: tier/cluster labels match the tool. Card price matches the POS total. Fallback/fit lines render.
- Report: every SLICE_DESIGN §1 field is present.
- **Jar wall (shot 9): FAIL on "labels sit over their jars".** All LOW labels sit in one row at y≈112 px, whatever the jar row. No SOLD OUT label is visible, although the toast in the same shot shows Kush Cake 3.5 → 0 g. See N1.

## 2. Play-through (PlayMode bot, seed 1)
`served=12 walkouts=0 noSales=0 revenue=265.20 soldOut=Kush Cake (KAKE081026) stars=3 fallbacks=87`. All 12 customers resolve. Revenue = Σ sale events (true by construction: `Report()` sums `Sales`, so the assert can't fail on its own). The clock stays inside 08–22, every sale is ≤ 28 g, jar fill = grams/454 for every sold batch. Same as the handoff.

## 3. Domain scope (DEC-028)
Only S1 `Catalog.SetInStock`, S2 `Engine/Labels.cs`, S3 `StrainResult.RepBatchId`. No other Domain lines. Engine goldens are unchanged (EditMode suite green). `Labels.cs` was checked line by line against `deploy/2026-10-30-v7114/site/index.html` L15107-15115 (CL name/lbl) and L16463 (`tierLabels2`): exact match.

**Overlap with GAME-003 (`review/wave-3a`)**: both edit `Catalog.cs` and `Recommender.cs`. `git merge-tree` shows no text conflict, but there is a semantic one:
- **I1 (must-fix at integration):** GAME-003 adds a `Dictionary<string, StrainGroup> _byKey` cache to `Catalog` (`Group(key)`), built from `Groups()`. GAME-002's `SetInStock` clears `_groups` but not `_byKey`. After the merge, a sell-out rebuilds `Groups()` with new objects while `Group(key)` keeps returning the stale group: old rep batch, old in-stock order. Fix: one line in `SetInStock`, `_byKey = null;`, plus a test (sell out a rep → `Group(key).Batches[0]` changes). I'll apply it in the integration merge unless the Hub assigns it elsewhere.
- GAME-003 also reworks `FindStrains` (tier chips). `ShiftSim.Fit` calls `Recommender.FindStrains(cat, crit, neg, primary, state)`. Compile at integration will show any signature break.

## 4. Compliance (DEC-035/036)
- M1: `Confirm` rejects grams > `adultUseLimitGrams` 28.0 before any stock change. Tested at 28 g (sells) and 28.5 g (blocked). ✓
- M2: the "✓ 21+ ID verified" line is on the POS. ✓
- M3: `ClockHours = shiftStartHour 14 + t/3600`. Bot and worst case are inside 08–22. ✓
- DEC-035: `CheckoutRound` gives the nearest $0.05 for the POS total, revenue and sale events. Cards and Detail keep `priceFloor`. ✓
  - Note n3: `PriceFit` compares the budget with the **card** price (priceFloor), while the customer pays the POS total, which can be up to $0.05 higher. So a customer can pay a few cents over budget. That's fine for a slice. DES may want PriceFit to use the POS total.

## 5. DEC-029
No graybox scene in the diff. Only `Scenes/Gameplay_Slice.unity` is added (built by `Editor/Slice/SliceSceneBuilder`), plus the `SceneBootstrap.AdditiveScenes` entry and the build-settings entry. ✓ I did not regenerate the scene to diff it against the committed file.

## 6. Rulings on GAME-002 "Decisions taken"
1. **SOLD OUT seeding from rank-1 reps + 3.5 g flooring: ACCEPT.** It meets DEC-027 deterministically. The flooring makes a full jar 451.5 g (fill 0.994), which is harmless. One caution: the effect depends on the seed. Keep the bot assertion `SoldOut not empty` as the guard.
2. **Service start = sim moves the customer to the counter (the walk counts toward speedFit): ACCEPT.** The walk is about 6 s against `fastSeconds` 30.
3. **Metrics definitions (last chip, true families, low stock at shift end): ACCEPT.**
4. **New config keys `impatientFraction`, `minLowStartJars`, `holdConfirmSeconds`, `npcWalkSpeed`: ACCEPT** as [GDD]. `Config_JsonHasEveryField` guards them.
5. **Screen-space jar labels: ACCEPT the approach, but the placement is not shown to work (N1).**

## Notes (none block GAME-002 alone)
- **N1 (fix before the slice is signed off):** jar LOW/SOLD OUT labels don't sit over their jars in the capture (shot 9). `SliceView.JarLabels` projects with `RuntimePanelUtils.CameraTransformWorldToPanel(panel, pos, cam)`, while the capture renders the camera into its own RT and the panel into another. The handoff already says this is unverified in-game. The owner (GAME-002 follow-up) should check it in a windowed run. If it's capture-only, make the capture's camera RT and panel sizes match so shot 9 is real evidence. The SOLD OUT label should also be in shot 9: the Kush Cake jar is likely outside the 9 m / front-of-camera cut.
- **N2:** the slice capture is not in `studio.ps1` (BUILD-002 owns that). I used `-runTests -testCategory SliceCapture` by hand.
- **N3:** see §4 (budget against card price).
- **nits:** on Results, "Back (Esc)" overlaps the right end of the full-width "More options (M)" bar. The fix needs a class on that button (C#), so I didn't make it. A sale toast still shows on top of the report screen. Jar wall lighting is very dark in the capture. `MoreOptions()` doesn't check `Pending == null` (the UI can't reach it during POS, so this is harmless).

## Open for the Hub
- Check 7 is waiting: send the GO for W3A + W3B. I'll then merge both here, apply I1, re-run the gates and confirm `FallbackAnchors.Count == 0`. ART-002's `GrayboxBuilder` emits `Anchor_CustomerSpawn/Exit`, `Anchor_QueueSlot_0..3`, `Anchor_ServiceCustomer/Player`, `Interact_Terminal/Scale` and `Anchor_JarSlot_###`, the same names GAME-002 looks up. The jar slot count is still to be checked.
- Who owns N1 (GAME-002 follow-up or a fix-up during integration)?
