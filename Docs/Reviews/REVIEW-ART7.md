# REVIEW-ART7: ART-007 graybox/lookdev rebuild (REF-011/012)

**Reviewer:** Unity pool · **Requested by:** World lead (urgent; playtest build 2) · **Verdict to:** Hub (DEC-112), cc World lead · **Date:** 2026-10-30
**Reviewed:** `worktree-agent-a814e17bba4ec20c5` @ 404daee (includes review/world-1), merged onto `review/art7` from main c3cf568 (merge 21f6d16, no conflicts).
**Sources:** `Docs/Tasks/Active/ART-007.md`, `Docs/Handoffs/ART-007.md`, the diff, DOORS.json, SCENE_ANCHORS.json, GAME-025/026 packets.

## Verdict: PASS with minors

## Checks (on 21f6d16, main merged)
1. **Builds and plays:**
   - `unity-build` succeeds and its smoke run passes: 11 scenes, no crash.
   - EditMode: 782 run, 780 passed, 0 failed, 2 skipped.
   - PlayMode: 9 run, 8 passed, 0 failed, 1 skipped; this includes GrayboxWalk and the anchor tests.
2. **SliceCapture timeout is not a blocker.** `unity-capture` passes: QA 0.22 ft against a 0.5 ft tolerance, 23 views, and the room sheet. Its slice step passes with 27 shots. The worker hit 180 s because the worker branch predates GAME-010, which raised `Capture_EachScreen` to `Timeout(900000)` on main. With main merged in, the longer walk from `Anchor_CustomerSpawn` fits.
3. **Doors:** all 15 rows in DOORS.json were checked against the built scenes. For every row with leaves, `Door_<Id>`, `_L`/`_R`, `_Hinge` pivots and `Anchor_Door_<Id>_A/_B` exist. The arches have A/B anchors only. Grille_101B is skipped (GAP-137), as the packet allows.
4. **Anchors:** all 42 SCENE_ANCHORS rows exist by name. These GAME-025/026 names are present: `Anchor_QueueSlot_0..`, `Anchor_CheckInDesk`, `Anchor_ServiceCustomer`, `Anchor_ServicePlayer`, `Anchor_CustomerSpawn`, `Anchor_Guard_Post`, `Anchor_CheckIn_Wait_*`, `Anchor_Register_NN_Call`, `Door_Entry_L/_R`. `Interact_Terminal` and `Interact_Scale` are unchanged, because station 08 did not move.
5. **Clearance:** I reran `room_fixtures_layout.py --check`: 106 of 114 pass. The 8 failures are the ones the handoff lists, and they come from the reference data, not the build:
   - south operator zones overlap the next stand (GAP-131);
   - the JC door can't be reached past the break-room bench and table;
   - the Vest_FOH door swing hits the trash can.
   REF-013 is expected to fix the south run and the door hinges.
6. **Code:** door, jar-fill and fixture yaw/tag changes are small, deterministic (FNV seed) and editor-only. There is no gameplay code.
7. **Hub citation rule:** placements come from the reference JSONs. The station kit is seeded set dressing labelled as a placeholder until PROC-006b. The review views are camera poses, not store facts.

## Minors (non-blocking for build 2)
1. `GrayboxWalkTests` moves its route to y 31.3, a test change beyond the anchor renames the packet allowed. It is justified by the propped BOH leaf; the World lead should accept it.
2. The three deli-wall review views are framed too close and show only shelves. The room sheet doesn't show the fill pattern.
3. The FOH trash can in the Vest_FOH door swing and the unreachable JC door still need ART/REF decisions (handoff Q2–Q3). Gameplay NPC routing should avoid `Anchor_Door_JC_*` until then.
4. Housekeeping: running Unity on this branch imports main's wire-shelving FBX and writes `.meta` files plus an HDRP global-settings change. I did not commit them; whoever owns the PROC-005 import should commit those `.meta` files.

## Not in scope
The REF-013 corrections (entry move, counters, hinges) are deliberately excluded and go in a follow-up.
