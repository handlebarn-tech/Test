# REVIEW-W5F — IMP-003 drop 1: audit of ChatGPT's `blender_proc_vNext/`

**Verdict: PASS with minors (GO).** Branch `review/wave-5f` (off `main` 6559a51) merges `claude/brave-brattain-30c797` @ 1d13112 cleanly. Doc-only (audit + handoff, +121). Reviewer: independent review session, 2026-10-30. The import folder was only read: no script or `.pyc` was run, imported or copied.

## Summary for Nolan (to approve)
ChatGPT's drop adds a chrome wire-rack generator and small upgrades to our Blender pipeline.
It is safe: it only adds code, it doesn't change any model we already make, and it uses no outside assets.
It isn't ready to use as-is: the racks are a generic 4 ft size, and our store plan already has real sizes for each rack.
Two plumbing bugs need fixing first: a wrong output folder, and collision boxes that would show up in-game as blue boxes.
Recommendation: approve "adapt": take the helper code now, and have a PROC task fix the listed items and build one rack per real placement.
Two small rack questions (shelf count, one long rack or several side by side) go to you through the Hub.

## Spot-checks against the files
- **`proclib.py`**: `diff --strip-trailing-cr` = 0 lines removed, 61 added (3 helpers + a mid-file `mathutils` import). Matches "adopt, fix P1" ✔.
- **`run_generator.py`**: the audit says "additions only. Nothing of ours was removed or changed". **Not quite (m1):** 3 of our lines are rewritten: object naming (`COL_` parts drop the `_LODn` suffix; our comment about LODGroup auto-setup is lost), the per-object `lod_entry` write (now skipped for `COL_`), and the size bbox (now render objects only, inside an `if`). For generators that emit no `COL_` part (none of ours do: `grep COL_ Tools/Blender/generators` is empty) these are equivalent, which fits the audit's sandboxed result that DeliJar FBX/geometry hashes are unchanged. What does change for our generators is R2 (every manifest entry gains `collision` + `validation`, plus 24 new `Validation/*.json`), as the audit says ✔. Also: `COL_` tris are excluded from the budget (audit notes "not counted") ✔.
- **Safety scan** of the three `.py` files: imports are Blender/stdlib only; file writes are the manifest, FBX, validation JSON and contact sheet; no subprocess, network, `eval`/`exec` ✔.
- **Params**: `unity_dir` = `Assets/_Game/Art/Procedural/Fixtures/WireShelving` while all 4 of ours start `UnityProject/` (A1 real bug ✔); no `own_sheet`, and `run_generator` only skips own-sheet/grouped assets from the default sheet (A2 ✔); `require_collision`, `validation_warnings` present (R4/A3 ✔).
- **`GAP-PROC-13`** is unused on main (highest GAP-PROC-12) ✔.
- **Guessed-dimension table** checked against `Docs/Reference/ROOM_FIXTURES.json`: all 7 cited rows match (`[w,d,h]` ft and confidence): Rack_Rolling_1–4 6.0×2.0×6.0 Low/GAP-127; East_Wall 8.7×2.0×6.0 Med; West_Run 8.0×2.0×6.0 Med "2-bay, 4–5 shelves"; South_Wall 5.3×1.8×6.0 Low; Chrome_Cartons 2.5×1.2×6.0 Low; Bags_Tools 3.0×1.5×5.0 Low; Desk_WireRack_Computer 3.4×1.5×6.0 Med black ✔. Height 6 ft = the 72 in guess ✔; width/depth wrong for every placement ✔.
- **m2:** the table omits `Rack_CleaningSupplies_JC` (2.0×1.2×5.0 ft, Low, GAP-127, "small rack of cleaning supplies", DEC-062). Whether it is a wire rack isn't stated; the PROC packet should list it as "wire rack? (GAP-127)" rather than skip it. `Rack_IT_Box` is correctly excluded (a plain black box, DEC-051 Q15).
- Not re-run: the audit's Blender sandbox (tris, determinism, hashes). Its numbers are plausible and internally consistent; the hash claim matches the code reading above.

## For the Hub
- Forward the 6-line summary to Nolan for approval (DEC-069 process).
- Decisions R1 (collision: manifest `collision_boxes` + Unity `BoxCollider`s, recommended, vs `COL_` + `AssetPostprocessor`) and R3 (validation JSON on failure, or drop it). Reviewer agrees with the audit's leans (R1a, drop R3): least code, no churn.
- Register GAP-PROC-13 on integration; Nolan questions 1–2 from the IMP-003 handoff (rolling-rack shelves/casters; BOH runs one unit vs 4-ft bays).
- The PROC integration packet should also restore our `_LODn` naming comment (m1) and include `Rack_CleaningSupplies_JC` (m2).
