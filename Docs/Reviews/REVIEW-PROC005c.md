# REVIEW-PROC005c: PROC-005 round 3 (answers REVIEW-PROC005b)

**Reviewer:** fresh one-shot reviewer · **Verdict to:** Hub · **Date:** 2026-10-30
**Reviewed:** `claude/elated-satoshi-3a4844` @ `6a99d40`, merged `--no-ff` onto `review/proc005c` from `main` @ `154be82` (worker base `75b05e6`), no conflicts.
**Sources read:** `Docs/Tasks/Active/PROC-005.md`; `Docs/Reviews/REVIEW-PROC005b.md` (`review/proc005b` @ `35c47b2`); `Docs/Handoffs/PROC-005.md` (round 3, Validation, Not done); the diff; `Docs/Reference/ROOM_FIXTURES.json` at `4854069` (REF-013) and at current `main` (REF-016, `14332c3` + `fb78346`); `Docs/KNOWN_GAPS.md` (GAP-129/130/131); contact sheets.

## Verdict: FAIL

The REVIEW-PROC005b MAJOR is fixed against REF-013: every counter and jar-wall size matches. But main moved again while round 3 was running. REF-016 (merged to main after the worker's base) re-placed the south-run registers. The branch's `South` stations now contradict their cited `POS_xx` rows. Same failure class as round b (stale base, not a worker error): packet rule "Real dimensions only: from ROOM_FIXTURES" / DEC-047.

## Checks
| Check | Result |
|---|---|
| Counter sizes vs current RF | **Match.** North 20.49 × 2.2 ft (6.245 × 0.671 m), EastReturn 2.5 × 10.8 (0.762 × 3.292), South 25.75 × 2.5 (7.849 × 0.762), SouthWestReturn 2.5 × 4.5 (0.762 × 1.372), height 2.833 ft. Confirmed in params, manifest collision boxes and validation. REF-016 left these rows' size/pos unchanged. |
| SouthReturn → SouthWestReturn | Done: SouthReturn exports, Unity copy, validation and manifest entry removed; SWR added, faces E, axis +y. |
| North / EastReturn stations | Match RF POS_10/09/08 (x 36/30/24) and POS_12/11 (y 12/16). Display-case slot x 38.7 agrees with the new REF-016 row `DisplayCase_Lit_NorthRun`. |
| Jar walls vs current RF | **Match.** North 25.9 × 2.1 ft, South 19.23 × 2.0, East 14.0 × 2.0 (counter 0.5896 + back panel 0.02 m). REF-016 changed only `matrix` on these rows. |
| GAP-129 | Round-3 params cite it only as "closed by REF-013". |
| Determinism | `blender.ps1 register_counter_run`, `deli_counter_jar_wall` and `textures` on the merged tree: all exit 0. No FBX or PNG changed. Validation JSON, manifest and `finishes.json` differ only by CRLF/LF (`git diff --ignore-cr-at-eol` is empty). The manifest holds 108 entries. |
| Unity EditMode | **Not rerun this round.** The verdict fails on data and the South/SWR exports must change again, so the next round must run it. Round b passed 788/790 on the previous exports. |
| DEC-122 visual (register run, jar walls, restroom, break room) | See minors below. |

## MAJOR
1. **South-run register stations contradict main's REF-016 ROOM_FIXTURES.** Current RF (GAP-131 narrowed: DEC-039 read west → east):
   - The straight South run carries **5** stations: POS_02..06 at x **21.2 / 25.0 / 28.8 / 32.6 / 36.4** (registers 2,3,4,5,6 west → east). The branch has **6** stations, 7,2,3,4,5,6 east → west at x 36.4 … 20.4 (the REF-013 values).
     Expected `local_x_m` (x − 28.16 ft, axis +x): R2 −2.1214, R3 −0.9632, R4 0.1951, R5 1.3533, R6 2.5116.
   - **Register 7** is now `POS_07` at (17.56, 23.2), rot 90, faces **W**, on the west-end block (the run end plus `Counter_Register_SouthWestReturn`). The branch's SWR variant says "No register" and has `stations: []`. On the SWR axis (+y, centre y 24.75) the monitor sits at local x ≈ −0.4724 m.
   - **Orientation needs a call:** the RF SWR row says `faces: E`, but POS_07 faces W and its matrix says "its west face is R7's customer face". The worker must model the card terminal and customer side on the block's west face. If that cannot be done without contradicting the SWR row, it is a source conflict for the Hub.
   - The South contact sheet shows 6 walnut drawer cabinets laid out on the old stations. They must follow the 5 new ones.

## minor
1. **Wood finish (b-m1): resolved.** The zig-zag is gone. Grain reads as straight stripes on the register cubby doors, the jar-wall North drawers and the break-room cabinets. It still runs across the doors (handoff known limit: grain follows world X), which is acceptable until the PROC-007 UVs.
2. **Smudges (b-m2): resolved.** The restroom mirror and stainless dispensers show faint, plausible wipe marks, with no white clouds.
3. **Boards (b-m3): unchanged.** They are still plain panels under GAP-PROC-34, acceptable as labelled.
4. **LOD3 single boxes (b-m4): unchanged.** No action unless Unity LOD transitions pop.
5. **Handoff counts (b-m5): resolved** (108 entries stated). The older fix-wave table (finding 2 row) still says `_South (… GAP-129)` and `_SouthReturn`; mark it as superseded by round 3.
6. **New (REF-016 `POS_StationKit`):** the RF row puts the monitor on the **customer half** of the top, facing the operator. `components.pos_monitor` puts it 0.3 m in from the staff edge of a 0.76 m top, which is the staff half. The offsets are GAP-RK-LAYOUT, so this is only a minor: cite the row and move the monitor toward the customer half when you re-fit the stations.
7. The Unity `.meta` files, the HDRP material builder and the `to_unity`/BoxCollider test are still owed (handoff "Not done").

## Required to pass
- Re-fit `register_counter_run` to main's current ROOM_FIXTURES (REF-016):
  - South: 5 stations, R2..R6 at the x values above;
  - register 7 on the SouthWestReturn block per POS_07, with the orientation conflict resolved or escalated;
  - monitor placement per `POS_StationKit`.

  Then re-export, re-check determinism and regenerate the contact sheet.
- Run Unity EditMode (`studio.ps1`, DEC-013) on the merged result.
- Before submitting, diff `Docs/Reference/ROOM_FIXTURES.json` between your base and `main`, so a later REF does not leave the base stale again.
