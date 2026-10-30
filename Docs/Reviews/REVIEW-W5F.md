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

## Addendum 2026-10-30 — drops 2–4, delta check, PROC fix checklist (9d5be47)
**New verdict: PASS with minors (GO), covering drops 1–4.** `review/wave-5f` merged `main` (4a635ec) and then `claude/brave-brattain-30c797` @ 9d5be47 (aa465fc), cleanly. Docs only: audit +392, new `IMP-003_PROC_FIX_CHECKLIST.md` (318 lines), handoff. Reviewer: standing Docs reviewer (DEC-085). Import folders were read only. The drop 2 zips were extracted to my scratchpad for grep and nothing was executed. The audit's Blender sandbox runs were not repeated.

### Summary for Nolan (to approve, replaces the drop 1 summary)
ChatGPT has now sent four batches: about 60 store fixtures and props, extra Blender helper code, a texture loader and label maker.
The code is clean and repeatable, uses no outside assets, and doesn't change any model we already have.
The fixes ChatGPT said it made in round 1 are not in the files we received, so those findings still stand.
Most sizes are generic guesses where our store plans already have the real answer (lockers, cabinets, register counter, doors, sink), and everything is below your new high-quality bar.
Recommendation: approve "adapt": per DEC-083 our PROC worker takes the code and fixes everything on the checklist; reject the cash drawer and the made-up entry vestibule.
Five store questions (rack shelves, rack runs, locker doors, where IDs are checked, deli counter front) go to you through the Hub.

### Spot-checks against the files (all confirmed)
- Drop 2: `proclib_add_beveled_box.patch` is 0 bytes; `fixed_ladder.json` LOD1 `tube_segments` 5 (B1); cooler `moving_parts` lists only `DoorFrame_nn` (S6); `break_room.json` lockers `columns` 4 × `rows` 2 (8 doors vs one 2 × 6 ft unit); `register_station.json` has a `CashDrawer` variant (C1).
- Drop 4: `cc0_pbr.build_material(download_sources=True)` default, calling `api.polyhaven.com` and the ambientCG API at build time with an unchecked `extractall` (B3 fail is right); `label_decals.APPROVED_BRANDS` lacks The Flower Mine (DEC-081); `building_shell_exterior.json` has an `EntryVestibule` variant.
- Store facts cited by the audit/checklist match their sources: ROOM_FIXTURES `Lockers_Staff` 2.0 × 1.5 × 6.0 High, `Cart_Deli_Prep` 2.5 × 1.6 × 2.9 "FOR DELI USE ONLY", `Cooler_GlassDoor_2Door` 4.0 × 2.5 × 6.5, `Fan_Portable` white 1.0 × 0.8 × 1.0, `ToolChest_Black` 2.75 ft, `Ladder_FireEscape` 9.0 ft, `Cabinet_Tall_Black_A` plain closed; RI E101 6'-0" × 7'-0" storefront pair; RI POS cabinet 34" max / 2'-6" top / 4" base; DEC-062 "old silver manual paper-towel dispenser"; RI "Excluded by rule … cash-handling equipment" (DEC-051).
- Checklist: every audit finding has an item with a source; DEC-083 (studio PROC worker fixes all, ChatGPT not asked) and DEC-084 (P4 budgets as LOD0 guides, LOD0–LOD3, 2K/4K PBR, §Q per family) are applied; W6 now includes `Rack_CleaningSupplies_JC` (first-pass m2 closed) ✔.

### Minors
- **m3 ID check isn't unknown.** Audit B2/B5, checklist §20 and handoff Q4 say where IDs are checked is "a store fact we don't have", with best guess (b) at the register. The repo already has a check-in ID desk: DEC-036 M2 ("ID-verified at check-in"), AZ_COMPLIANCE C3 ("a check-in vestibule is store practice"), O15 (training covers check-in), and RES-002 lists a reception/ID-check role. Re-frame Q4 as "where is the check-in desk and what is on it?", with best guess (a) plus the occasional counter re-check (AZ_COMPLIANCE_CHANGES L2).
- **m4** The handoff's drop 2 bullet "S3: prop budgets above DEC-069's ~1k" and audit S3 ("set prop budgets to ≤ 1000") are superseded by DEC-084. The checklist P4 says so; add the same pointer in the audit/handoff so nobody applies S3.
- **m5** Checklist §1 still says drop 1's copies "are ours plus additions only". Three lines of `run_generator.py` are rewritten (first-pass m1); equivalent for our generators, but the PROC worker should diff, not assume.
- **m6** The handoff Q3 locker best guess "2 × 3 small doors" isn't supported by a source (R3C5 shows only the top); fine as a labelled guess, keep GAP-126.

### For the Hub
- Forward the 6-line summary for Nolan's approval (DEC-069/083), plus handoff Q1–Q5 with Q4 re-framed per m3.
- Decisions still pending: collision route (R1/S4/C1; reviewer agrees with R1a manifest boxes), validation JSON (R3/C3), `mesh_stats` extras (T2/C4), and the card terminal as a generic prop or not.
- Ask ChatGPT for the round-1 files it claims to have fixed only if the Hub still wants them. Under DEC-083 the PROC worker fixes them anyway, so they are optional.
