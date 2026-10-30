# REVIEW-ART008: graybox final pass on REF-013 (ROOM_FIXTURES rev8, DOORS DEC-115)

- **Reviewed:** `claude/festive-hamilton-c0ced4` @ `1440ff6`. Merge base: `main` @ `a8f4bd4`. Merged `--no-ff` into `review/art008`, which was cut from `main` @ `241b7d7`.
- **Reviewer:** a fresh, one-shot reviewer (STUDIO_OS §0.3).
- **Sources read:**
  - Packet: `Docs/Tasks/Active/ART-008.md`.
  - The diff.
  - `Docs/Handoffs/ART-008.md`: changes, Checks, and the Remaining clearance and DEC-115 (5) sections.
  - `Docs/DECISIONS.md`: DEC-047, DEC-110, DEC-115, DEC-120 (4).
  - `Docs/Reference/DOORS.json` and `ROOM_FIXTURES.json`, via the converter.
  - A011 PDF vectors, for the frame ruling.

## Verdict: PASS with minors

## Checks
Every check below was run by me, on `review/art008` @ the merge commit.

**DEC-047: no uncited store values.**
- The new store values are the entry opening (y 8.9–14.9) and the east exit (y 21.65–24.65). Both are read from the DOORS `target_opening`, and each `graybox_layout.json` wall opening carries that A011 source note.
- The hinges come from DOORS rev3:
  - HUB2_HUB `hinge_jamb` S, hinge at y 51.1.
  - Ext_Delivery `hinge_jamb` N, hinge at y 49.5.
- The swing directions in the layout match the DOORS `swing` text for:
  - HUB2_HUB (into HUB, east).
  - Ext_Delivery (west, to the exterior).
  - Emergency_RetailE (east).
  - Entry pair (west).
- The grid origin and seat-snap constants are check-tool parameters, not store values.
- No uncited values were found.

**Packet Do items:**
1. The SW return is used in the builder: `COUNTERS` → `Counter_Register_SouthWestReturn`. ✓
2. The swing check skips `propsDoor` fixtures. This is limited to an open door whose id matches the fixture row's `propsDoor`, so it is not a blanket exclusion. ✓
3. Hinges per DEC-115 (1) ✓. The break room is rebuilt from rev8 (table group at y 37.0).
4. Openings applied ✓, and every step was re-run (see below).
5. Remaining clearance items are settled or GAP'd:
   - Vest_FOH trash can: settled as the prop.
   - JC anchors: now reachable.
   - The POS zone and behind-stand FAILs are traced to REF data (GAP-131), with specific REF follow-ups. No values were invented.

**`room_fixtures_layout.py` regeneration:** the converter re-run reproduces the committed `graybox_layout.json` byte for byte, apart from line endings.

**`room_fixtures_layout.py --check`: 108/114 PASS.** This matches the handoff. The 6 FAILs are the 5 south POS operator-zone overlaps (3.4 ft zone on a 3.2 ft pitch) and the POS_02 behind-stand clearance (3.2 < 5.2). All are GAP-131 REF data, as the handoff says.

**Unity validation** (`Tools/Studio/studio.ps1`, after `git lfs pull`; see m1):
- `unity-graybox`: PASS, csErrors 0. All 4 scenes and lookdev unchanged, so the committed scenes are deterministic.
- `unity-test-edit`: PASS, 790 run, 788 passed, 0 failed, 2 skipped.
- `unity-test-play`: PASS, 11 run, 10 passed, 0 failed, 1 skipped. This includes the re-routed `GrayboxWalkTests`.
- `unity-build`: PASS. Smoke test loaded 11 scenes with no crash.
- `unity-capture`: PASS.
  - QA: 23 views, maxDeviation 0.22 ft against a 0.5 tolerance, rooms sheet plus top-down.
  - Slice: 1/1, 28 shots.
  - Output is in `Artifacts/Screenshots/1a394a8-20261030-131014-266-31336`.

**Assembled scene (DEC-120 (4)):**
- *Top-down.* It shows the rev8 south run at x ≈15.2–40.9, closed at the west by the SW return down to the back counter. The north L with its east return, the stanchion field at x 6–15 / y 11–17, and the break-room table group are all in place.
- *Slice world view.* The registers, deli wall jars and HUD render in the built slice, and the player starts on the customer floor.
- *Built player.* It runs all 11 scenes without exceptions.

**A011 frame ruling (DEC-115 (5)).** I re-measured it independently with PyMuPDF:
- Drawing 4735 is the vertical dimension line at x 1150.56. Wall-face lines exist at pt y 175.0 (north) and 723.5 (south).
- (723.48 − 174.96) / 17.987 = **30.495 ft**. The ruling (30.5 ft, the dimension beats the area label) is confirmed.
- Not re-basing is correct: a re-base would need edits to REF-owned JSON and to GAME-026 anchors, both outside `Owns`.

## MAJOR
None.

## minor
- **m1 (tooling, not ART-008).** Fresh worktrees check out the 96 Git LFS files as pointers. Unity then imports `PROC_DeliJar.fbx` and the JarFill and packaged-goods FBX with no meshes. My first run, before `git lfs pull`, failed:
  - EditMode: 20 failures (`JarFillImportTests` and `PackagedGoodsImportTests`: no LODGroup).
  - PlayMode: 4 Slice failures (`SliceGame.SpawnJars`: "Sequence contains no elements").
  - Build smoke: crash.
  - Capture: slice capture failed.

  All of these went green after `git lfs pull`, with ART-008 unchanged. Suggested OPS row: `studio.ps1 doctor` (or every unity-* command) should block on LFS pointer files in Assets, and the fresh-worktree setup note should add `git lfs pull`.
- **m2 (FYI for GAME-026 / ART-013 / REF-016).** With rev8, the south run plus the SW return closes the customer floor off from the arch, so the player and staff reach BOH only round the north run's west end and along the staff aisles. That is what the REF data says; ART-008 implements it faithfully. Any NPC or player route that assumed a direct floor-to-arch path needs the new route, and the REF-016 evidence reviewer should confirm this closure against CCTV.
- **m3 (Hub queue).** The handoff's REF follow-ups still need registering:
  - Narrow the POS operator zones to the 3.2 ft pitch, or re-measure the pitch.
  - Set POS_02 `behind_stand` to 3.2.
  - A REF re-base task for the 30.5 ft retail depth (y +1.5 south of the retail mid-floor).
  - Lifting REVIEW-ART7 m3 (NPCs avoiding the JC anchors) in GAME-026.
  - The untracked PROC wire-shelving and register-kit `.meta` files from the import are still uncommitted (REVIEW-ART7 m4), for their owner.
