# GAME-005 — Real deli canister + stepped bud fill in the slice

**Role:** GAME · **Priority:** P1 · **Branch:** `claude/task-game-005-972696` (off `main` 592086c).

## Goal
The slice's placeholder cylinder jars become the PROC-002 canister with its stepped bud fill (REVIEW-W4E m2, REVIEW-W4F §5, DEC-042/043/046):
- Import `PROC_DeliJar` into Unity through a `unity_dir` in `Tools/Blender/params/deli_jar.json` (regenerated in Blender, so the copy is reproducible). BUILD-005 (LFS for procedural FBX) is not on main: plain binary, as PROC-002 did.
- `SliceGame` spawns jar + fill at the `Anchor_JarSlot_###` anchors, found by name (W3B m1). The jar's +Z label face follows the anchor's forward (into the room).
- Fill step from `InventoryService.Fill` (grams / start): SOLD OUT → F000, else the nearest step (ties up). The steps are read from the fill FBX's object names (`_F<pct>_`), so PROC-003 can change them without code changes. DEC-046: any jar above 0 g shows at least the lowest visible step (data in `SliceConfig.json`).
- Per-brand base band colour (stable hash of the brand into a generic palette, [GDD] placeholder: no brand colours exist) and a generic text label (strain + brand from `batches.json`, no logos). THC % tag stays blank: no THC data in the catalog.
- `SliceBotTests` checks the step mapping instead of the linear `JarFillShown == grams/454`; an EditMode test covers the mapping rule.
- LOW/SOLD OUT labels stay over their jars (GAME-002b), using the new jar height.

## Out of scope
Graybox scenes/builder, ART's lookdev scene (DEC-029), fill mesh changes (PROC-003), HDRP bud materials (ART).

## Validation
Blender regen (deterministic sha), compile, EditMode, PlayMode incl. the slice bot, studio capture run with the SliceCapture shots. DEC-013 two-editor gate (wait/retry 60 s). Handoff `Docs/Handoffs/GAME-005.md`. Never ask Nolan (DEC-033).
