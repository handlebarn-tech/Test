# ART-013 partial handoff (recovered from the dead worker's final report)

**Source:** final message of session `Dispo · spare-6` (`local_9352d1ba`), killed by the usage limit 2026-10-30 ~13:30; captured verbatim by RECOVERY-001 because the "shared notes folder" it mentions does not exist on disk. **Branch/commit:** `claude/art013` @ 14b3eb3. **Packet:** `Docs/Tasks/Ready/ART-013.md`. **Status:** partial, unreviewed. Unity was not run.

## Done (converter `Tools/Studio/room_fixtures_layout.py`, `graybox_layout.json` regenerated)
- **Register 7's stand:** now sits on the operator's left, read from the stand position in the ROOM_FIXTURES register row (the build script used to stop with an error on it).
- **Monitors:** placed on the customer half of the counter top.
- **Station kit:** everything on the staff half except the card terminal, the only item at the customer edge; built-in checks enforce this.
- **Sink and east rack:** the old V5 boxes replaced by the A011 positions.
- **Big trash bins:** only `Trash_Big_SouthReturnEnd` is built (CCTV shows one bin there); `Trash_Big_East_Sink` treated as a duplicate.
- **Clearance check:** 113/114 PASS. The one FAIL comes from ROOM_FIXTURES data, not the build: POS_05's row asks for 5.2 ft behind the stand but only 3.2 ft exists because the back counter runs under the stand.

## Not done
1. **Unity builder:** `GrayboxBuilder` does not read the new stand and monitor positions yet; a Unity build still puts register 7's stand on the wrong side and the monitors at the staff edge.
2. **Matrix tool:** `--matrix` mode not written; no before/after count.
3. **Doors:** importing the PROC door models, placing frames and leaves, cutting each wall opening to the frame's size, adding colliders.
4. **ID stand and guard spot:** planned, not applied. Stand moves 1.1 ft east; guard spot at x 1.8 (1.6 ft to the licences box, 2.4 ft to the wall).
5. **Jar density:** the slice stocks only 77 jars across ~171 jar slots, likely thinner than the stocking shares require (DEC-121). The count comes from game data outside this task's files: **Hub ruling needed** (route to GAME or a data row).
6. Remaining: status fields in the three reference JSONs, the §9.3 table, captures, Unity validation runs, the handoff. The GAME-026 reference copies were not on `main` yet at the time.

## For the Hub
- The POS_05 clearance data conflict (5.2 ft required vs 3.2 ft available) is a REF question (REF-016/ROOM_FIXTURES), not an ART one.
- Next worker: fresh Unity worker from `claude/art013`, merge `main` first (ART-008, PROC-005, PROC-013 doors are now on `main`).
