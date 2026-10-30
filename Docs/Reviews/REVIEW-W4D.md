# REVIEW-W4D — GAME-002b (slice polish: REVIEW-W3D notes + DEC-044)

**Branch:** `review/wave-4d` = `main` (aa926f9) + `--no-ff` merge of `claude/task-game-002b` (154f235). The merge was clean.
**Final verdict: GO.** N1, DEC-044 and the W3D nits are fixed and the gates are green. Only non-blocking notes remain, for ART and BUILD.

## 1. Gates (DEC-013: `studio.ps1` slot wait; the capture used the same editor-count check)
| Gate | Result |
|---|---|
| `unity-compile` | OK, csErrors=0 |
| `unity-test-edit` | **143/143** passed |
| `unity-test-play` | 5 total, 4 passed, 1 skipped (GPU capture under `-nographics`), 0 failed |
| SliceCapture with graphics (`-runTests -testPlatform PlayMode -testCategory SliceCapture`, by hand, N2) | 1/1 passed, including the new SOLD OUT placement assertion. 10 PNGs in `Artifacts/Screenshots/slice/` (local, not committed) |

Shots I viewed myself:
- **Shot 9 (jar wall): PASS.** Each LOW label sits just above its own jar, and the labels follow the rows and the perspective, so they are no longer stuck in one row at y≈112. **SOLD OUT** (orange) sits over the empty Kush Cake jar, and the toast in the same shot shows Kush Cake 3.5 → 0 g.
- Shot 5 (Results): "More options (M)" is now a left-aligned button and doesn't overlap "Back (Esc)".
- Shot 10 (Report): no toast on top of the report. 12 served, $265.20, Kush Cake sold out, 26 low jars (the same as the W3D bot numbers).

## 2. N1: windowed check. I argued from the code; I did not open a windowed editor.
I did not do a windowed PlayMode check, because other sessions held editor slots and a screenshot from an interactive editor can't be automated here. The argument from the code:
- `JarLabelPanelPos` = `cam.WorldToViewportPoint(world)` × `_root.layout` size. The viewport is a 0..1 fraction of the camera rect. The camera rect is never changed (no `.rect`/`pixelRect` in `_Game/Code`), so it is the full screen in a window and the full RT in the capture.
- `_root.layout` is in panel units after `ScaleWithScreenSize` (reference 1920×1080, match 0.5). The labels live in `.jar-layer`, which is absolutely positioned to fill `_root`, so `left`/`top` use the same units. The fraction × panel size mapping holds at any window size or scale. `Screen` is not used anymore, and that was the W3D defect.
- Limit: the test's 8 px assertion recomputes the same formula with W×H. That is true because the panel RT is 1920×1080 at scale 1, so the assertion checks consistency, not an independent position. The independent evidence is shot 9, which matches.
- Residual risk (low): a window aspect far from 16:9 still maps correctly, since both axes scale on their own. The −30/−12 px label offsets are in panel units, so a label keeps its size relative to the UI.

## 3. DEC-044: PASS
- `Card.CheckoutPostTax = price.PostTax` (the POS total, DEC-035 nickel rounding). `Score()` uses it for `PriceFit`. Cards still show `PricePostTax` (`CardPostTax`, the priceFloor). `Confirm()` already sold at `price.PostTax`, so the budget check now matches what the customer pays.
- `PriceFit_UsesPosTotal_NotCardFloor`: every card's `CheckoutPostTax` equals `Price(...).PostTax`. A budget equal to the card price gives PriceFit < 1 when the POS total rounds up. The `Assume` skips the test instead of failing it if no such card exists; it passed here, so the case was found.
- The only other budget use is `Responder` in Domain (the parser's price intent), which is not touched.

## 4. Nits: all fixed
- Back/More options overlap: a `more` class with `align-self: flex-start` (shot 5).
- Toast over the report: `Toast()` returns early on the Report screen, and `Render()` clears toasts when it enters Report (shot 10).
- `MoreOptions()` guard: `Require(Results != null && Pending == null)`. `MoreOptions_BlockedWhilePosOpen` covers it (it throws while the POS is open and works after Cancel).

## 5. Scope
- No scene or graybox changes (DEC-029). No Domain changes. The changes are in Presentation, Simulation, Tests and USS, plus the contact sheet and the handoff.
- The capture exposure goes from EV 13 to 11 in the slice capture only, and GrayboxCapture is unchanged. Fine as a test-only workaround until ART-003 lights the jar wall.

## Notes (none block)
- **n1 (ART):** the jars still render as wide flat discs on the wall (ART-002 anchor scale or jar size), as the handoff says. Far labels overlap each other at the end of the wall ("LOW LOW", "LCLOW"). That is cosmetic, and the 9 m cut limits it. Spreading the labels is a later UX pass, not this task.
- **n2 (BUILD):** the SliceCapture run is still not in `studio.ps1` (W3D N2; BUILD-002/003).
- **n3 (process):** N1 was not checked in a windowed editor, by the handoff or by this review (§2). The first windowed or standalone play session (BUILD-PLAY) should check that the labels sit over their jars at a non-16:9 window size.

No fixes were made in this review.
