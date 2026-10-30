# REVIEW-IMP3B — IMP-003: rebuilt round 3 + rounds 4, 5, 6 (ChatGPT toolkit audit)

**Verdict: PASS with minors (GO).** This supersedes REVIEW-W5T. I reviewed `worktree-agent-aa0d2341e0f4619cc` at commits 4a615d6, 289019d, 02573db, a976d0d and ecb8132: 3 files, +994 lines, docs only. This file is committed on `review/imp3b`, cut from ecb8132. Inputs read: the packet, the handoff, the new audit and checklist sections, DEC-097/105/110, main's `packaged_catalog.json` and `DOORS.json`, and the four drops (read only; I ran no Blender). The lead's rulings Q6–Q8 are taken as given.

## Checks
1. **Every finding cites a drop file and an authority: PASS.** I sampled R3b, R5.1 and R6.1–6.2. Each item names a drop file or generator plus an RF, RI, TI or DEC source. The research gaps say where the missing evidence might be found.
2. **Measured claims spot-checked against the drops: PASS (8/8).**
   - Round 6 generators return `(w,d,h)` (`desert_landscaping.py:48`, `exterior_site.py:44`, `lighting_fixtures.py:62`), while `manifest_box` writes Unity `(w,h,d)` (`round6_common.py:119`). This confirms the 37/37 size failures.
   - Collision sits under `'collision': {'boxes': …}` in rounds 5 and 6 (`deli_supplies.py:104` and the round-6 generators), not `collision_boxes`.
   - `ribbon_obj` (`round4_quality.py:110`) and `bmesh.ops.create_torus` (`:93`) exist as the round-4 crash sites.
   - Drop 6 ships `cash_drawer_tray.py`.
   - `canonical_reuse_map.json` claims `PROC_Register_CashDrawer/BarcodeScanner/POSMonitor/ScaleStand` and the round 4/5 families.
   - Round 5 creates `UVMap_Lightmap` after the base and label UVs (`round5_common.py:18,32`).
   - The tri counts and determinism come from the worker's Blender run; I did not re-run them.
3. **Brand rule (W5T m1): PASS.** R5.1 keeps High Variety on 510 carts and ToK on ready-to-use vapes. main's catalog confirms both: HIGH VARIETY VAPE has 14 rows under 510 THREAD and 11 under READY TO USE, and ToK VAPE has 9 under READY TO USE. So the "add a High Variety 2 g AIO" item is backed by data. The round-3 preroll tin and beverage can that misused brands are moved to BRAND-001 fictional names. R5.1's hard check against `packaged_catalog.json` is added.
4. **Door hardware (DEC-110): PASS with m1.** Push bars go only on the 3 exit and delivery openings, levers everywhere else, and there is no lock or access-control detail.
5. **No repeat Nolan questions (DEC-105): PASS.** The new rounds raise no Nolan questions. Q6 is settled by the DEC-051 Q9 precedent, and Q8 goes to a World REF look. The handoff lists what was searched. Minor m2.
6. **R3b.0.4 matches DEC-097: PASS.** Channel 0 = `UVMap_Main`, 1 = a lightmap UV exported from Blender, 2 = `UVMap_Label`, Unity's "Generate Lightmap UVs" off. It also flags that every drop uses the reversed order (`[Main, Label, Lightmap]`) and says not to port the per-triangle lightmap cells.

## Minors
- m1 **The entry door's hardware conflicts with World's door contract.**
  - R6.1 says to replace `EntryDoor`'s pull with a lever "unless the Hub rules a storefront exception".
  - World's contract on main has `DOORS.json` Entry `hardware: storefrontPull`, and CONTROLS_FLOW_PS1 §7.1 (DES-005b) reads DEC-110 the same way: levers on every leaf door except the storefront pull on the entry.
  - Fix: follow DOORS.json, or settle it with the World lead. It doesn't need a Hub ruling.
  - Also name the push-bar doors by their DOORS.json ids (`Emergency_RetailE`, `Ext_Emergency_SE`, `Ext_Delivery`) rather than the graybox opening names.
  - FYI: main's DOORS.json still has `JC` = pushBar and `Ext_Delivery` = lever. That is a known World fix; follow DEC-110 rather than that data.
- m2 **RG3-2 says "…or ask Nolan".** Per DEC-105/110, the RG items should say "through the lead/Hub after the listed search" rather than suggest asking Nolan directly.
