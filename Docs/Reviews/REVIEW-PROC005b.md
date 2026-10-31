# REVIEW-PROC005b: PROC-005 fix round (answers REVIEW-PROC5)

**Reviewer:** fresh one-shot reviewer · **Verdict to:** Hub · **Date:** 2026-10-30
**Reviewed:** `claude/elated-satoshi-3a4844` @ `ddc3112`, merged `--no-ff` onto `review/proc005b` from `main` @ `241b7d7` (merge base `285951d`), no conflicts.
**Sources read:** `Docs/Tasks/Active/PROC-005.md`; `Docs/Reviews/REVIEW-PROC5.md`; `Docs/Handoffs/PROC-005.md` (fix-wave Validation / Not done); the diff; `Docs/Reference/ROOM_FIXTURES.json` (main and branch); `Docs/KNOWN_GAPS.md` (GAP-129/130, GAP-PROC-21..39); STUDIO_OS §0.7; all 9 family contact sheets.

## Verdict: FAIL

Every REVIEW-PROC5 finding is answered on the branch's own base, and the visual bar is now met. The merged result still fails the DEC-047 / "real dimensions only" acceptance rule. Main's REF-013 (`73e0e0c`, not in the worker's history) rewrote the register-run and jar-wall ROOM_FIXTURES rows that this branch's params cite. After the merge those params contradict their own cited rows.

## Checks
| Check | Result |
|---|---|
| `blender.ps1 <gen>` for all 9 families, on the merged tree | All exit 0; manifest has 108 entries, all pass validation. |
| Determinism | No FBX or texture changed on rerun. Validation JSON and manifest differ only by CRLF/LF (`git diff --ignore-cr-at-eol` is empty). |
| `tests/test_validation.py` (headless) | `[SELFTEST] all passed`. |
| Existing jar / fill / packaged-goods exports | Unchanged on rerun (no FBX diff). |
| Unity EditMode (`studio.ps1 unity-test-edit`, on merge commit `5f6906d`) | **Pass:** total 790, passed 788, failed 0, skipped 2 (`Artifacts/TestResults/20261030-123658-269-38176-editmode.xml`). The editor imported every FBX and texture without a failing test. The `.meta` files it generated were not committed and are still owed with the import check, the HDRP material builder and the `to_unity`/BoxCollider test (handoff "Not done"). |
| DEC-122 visual pass (contact sheets) | See "Finding 1" below. |
| REVIEW-PROC5 #2–#8 against the branch's own RF | Resolved: RF ids in `rf`, DeliCounter legs and exports removed, jar-wall depth 2.1 ft, GAP-106/107 and DEC-079 mis-cites gone (grep clean), mop bucket is a GAP-PROC-30 placeholder, GAP-PROC-22..39 all present in KNOWN_GAPS, grab-bar depth carries a `_note`. |

### Finding 1 (DEC-084 visual bar): resolved
These families now read as real, finished fixtures, not graybox:
- register props: keypad terminal, keyboard, monitor, printer, scale stand, scanners;
- restroom: dispensers with brushed stainless, toilet, lavatory, grab bars with flanges;
- the glass-door cooler and fridges, office chair, carts and file cabinets, break-room appliances and lockers, the janitor sink and bucket.

The wire-basket cart and the cooler interior are good. The remaining weaknesses are minors (below), not a fail.

## MAJOR
1. **Register run and jar walls contradict the current ROOM_FIXTURES (REF-013) after the merge.** On the merged tree:
   - `Counter_Register_South` is RF 25.75 × 2.5 ft at (28.16, 21.25); the params use 20.2 × 2.2 ft (`length_m` 6.157). Stations `POS_02..07` all moved about 5.4 ft east (for example POS_07 x 31.0 → 36.4).
   - `Counter_Register_EastReturn` is RF 2.5 × 10.8 ft; the params use 2.2 × 9.8 ft.
   - `Counter_Register_SouthReturn`, which the `SouthReturn` variant cites, no longer exists in RF. REF-013 replaced it with `Counter_Register_SouthWestReturn` (2.5 × 4.5 ft at the **west** end).
   - Params and notes still cite GAP-129 as open. KNOWN_GAPS now says it is **closed by REF-013 (measured)**.
   - `Counter_Register_North` is now 20.49 ft; the params use 20.6.
   - `DeliJarWall_South` is RF 19.23 × 2.0 ft; the params use 21.2 ft / 0.640 m. `DeliJarWall_East` depth is 2.0 ft; the params use 0.637 m.

   Failing item: the packet's "Real dimensions only: from ROOM_FIXTURES …" rule and DEC-047. This is a stale base, not a worker error, but merging as-is would ship values that contradict their cited source.

## minor
1. **Wood finish reads as a wavy zig-zag pattern, not grain.** It is visible on the walnut register cubby doors, the jar-wall North drawers and the break-room cabinets and uppers. The handoff's known limit (grain follows world X) understates it: at contact-sheet distance it reads as a procedural artifact.
2. **Smudge/grime blotches are too strong.** Large white cloud spots show on the restroom mirror and its LOD tile, the stainless dispensers' LODs, the black desk tops and the mop-sink guard. They read as rendering defects, not wear.
3. **Break-room boards (bulletin / cork / fabric / whiteboard) are still plain framed panels.** This is GAP-PROC-34 and acceptable as labelled, but they are the weakest assets in the set.
4. **Lowest-LOD tiles are single boxes for almost every asset.** That is fine for LOD3, but some (for example the cooler's handle-only box) could be read as a missing LOD. No action unless Unity LOD transitions pop.
5. **Handoff counts are inconsistent.** It says "All 92 manifest assets"; the merged manifest holds 108 entries, all passing.

## Required to pass
- Bring the `register_counter_run` and `deli_counter_jar_wall` params and notes in line with REF-013's ROOM_FIXTURES rows: South / EastReturn / North sizes, SouthWestReturn in place of SouthReturn, POS station positions, South/East jar-wall size and depth, and the GAP-129 closed status. Then re-export and re-check determinism.
- EditMode passes (above). The `.meta` files, the import check of the material set-up and the `to_unity`/BoxCollider test are still owed before merge (handoff "Not done").
