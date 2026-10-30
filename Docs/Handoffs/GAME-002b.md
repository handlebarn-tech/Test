# Handoff: GAME-002b (REVIEW-W3D notes + DEC-044)

**Status:** done. Branch `claude/task-game-002b` (off `main` 0509893), not merged.

## Changes
- **N1 jar labels:** `SliceView` now projects LOW/SOLD OUT labels with `camera.WorldToViewportPoint` × the panel's layout size, not `RuntimePanelUtils.CameraTransformWorldToPanel`, which used `Screen` size and drifted whenever the camera or panel rendered to a texture. The capture test renders the camera into a 1920×1080 RT matching the panel RT. It frames the first sold-out jar from the register side and asserts the SOLD OUT label is visible and within 8 px of its jar's projection (measured 4.5 px). Shot 9 shows Kush Cake SOLD OUT over its empty jar.
- **DEC-044:** `Card.CheckoutPostTax` carries the POS total (nearest $0.05). `PriceFit` uses it, while cards still show the `priceFloor`. Test `PriceFit_UsesPosTotal_NotCardFloor` covers a 14 g Smalls case: card $35.00, POS $35.05, a $35.00 budget gives PriceFit < 1.
- **Nits:** the "More options" button no longer spans the full width (no overlap with Back). Toasts are cleared and suppressed on the report. `MoreOptions()` requires `Pending == null` (test `MoreOptions_BlockedWhilePosOpen`).
- **Capture lighting:** the slice capture's fixed exposure is EV 11 (GrayboxCapture keeps 13). This is a capture-only workaround: real retail lighting is ART-003's.

## Validation
- Compile OK; EditMode **143/143**; PlayMode 4 passed + 1 skipped (the GPU capture test under `-nographics`); bot seed 1 still 12/12, $265.20, Kush Cake sold out.
- SliceCapture with graphics (`-runTests -testCategory SliceCapture`): OK, 10 shots including the new label assertion; contact sheet `Docs/Assets/Specs/SLICE_contact_sheet.png` refreshed.

## Open (for the Hub)
- Not checked by eye in a windowed editor. The projection no longer depends on `Screen`, and the size-matched capture asserts the placement, so a window should behave the same.
- ART-003: the jar wall needs light (dark at EV 13). The ART-002 jar anchors render the jars as wide discs in shot 9; check the anchor scale or jar size.
- N2 is unchanged: `studio.ps1` still has no SliceCapture command (BUILD-002/003).
