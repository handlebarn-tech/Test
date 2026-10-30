# REVIEW-REF11 — REF-011, sales-floor layout audit (+ SCENE_ANCHORS)

**Verdict: PASS with minors (GO).** m1 must be fixed before the handoff's questions go up to the Hub (DEC-105). I reviewed `worktree-agent-a3e83b7d768da38d0` @ 9b111fa: 6 files, docs and data only. This file is committed on `review/ref11`, cut from 9b111fa.

Inputs read: the packet, the handoff, the diff, REFERENCES_INDEX §1.5/§2/§8, DEC-039/048/079/103/104/105, CF§7.2–7.3 (5c8031b), and BAND 10 and BAND 11 viewed at full frame. I checked everything with a scratch script.

## Checks
1. **No invented facts: PASS** (m1 is a process point, not an invented fact).
   - All 41 new rows cite sources. Only rows were added: none of the 86 existing rows changed, and `version` moved to rev7.
   - Every Low row and Low anchor carries a gap id. New gaps are only GAP-129..134; the existing GAP-110 is reused.
   - No raw CCTV or photos are committed.
2. **South counter move (+2.6 ft) and east return move (−1.4 ft): PASS.**
   - The south move is argued from evidence. BAND 10, rotated, shows the south staff aisle: register stands on the left, and the jar wall's back counter with bins and shelves on the right. Counting about 3–4 ft of 8" grout lines between them is credible. Using the low end, 3.0 ft, is conservative, and the row is Low (GAP-129).
   - The east move is inferred by symmetry, since BAND 11 shows only the arched counter wall. It is honestly marked Low (GAP-130) and asked.
   - The knock-on queue-field clash is flagged (R5).
3. **Three deli walls: PASS (Med).**
   - North: R2C3/R2C4 and the wide still.
   - East: BAND 11 shows arched backlit teal shelves with deli jars over a counter.
   - South: BAND 10 shows a back counter, 2 tiers and bins.
   - Re-posing R2C3–R2C5 as looking north from behind the south run is consistent across the audit's R2 and §2.
4. **SCENE_ANCHORS: PASS** (m2).
   - It has 42 unique names: `Anchor_CustomerSpawn/Exit`, `Anchor_CheckIn`, `Anchor_Guard_Post`, `Anchor_CheckIn_Wait_0..3`, `Anchor_Queue_0..11`, and `_Call`/`_Operator` for all 11 stations. These match CF§7.2–7.3.
   - Aliases: `Anchor_CheckInDesk`, `Anchor_QueueSlot_0..3` and `Anchor_ServiceCustomer/ServicePlayer` (on station 08, the player station).
   - `_about` covers how aliases are built.
5. **Round-trip: PASS.** `json.dumps(indent=1, ensure_ascii=False)` reproduces both files byte for byte.
6. **Merge with REF-012: PASS.** I ran `git merge-tree review/world-1 9b111fa`. The merge is clean. The merged `ROOM_FIXTURES` is rev7 with 127 rows, keeps all 27 REF-012 Office rows exactly, keeps all REF-011 rows and its contradictions, and still round-trips.

## Minors
- m1 **DEC-105 (no repeat questions): handoff Q4 and Q6 should not go to Nolan.**
  - Q4 (player's register): DEC-103 (7) says this was already answered in DEC-079, where the GM assigns registers on a floor map, and calls asking again a miss. Which station the player defaults to is a game choice: keep 08 as a [GDD] placeholder in `player_station` and drop the question.
  - Q6 (where a busy check-in line forms): DEC-103 (5) says check-in is quick and doesn't back up. Drop Q6, or keep only the spawn-side part (Q5).
- m2 **Station numbers in the anchor names are zero-padded** (`Anchor_Register_02_Call`). CF§7.3 writes `<StationNo>`. State the two-digit format in `_about`, and tell the Gameplay lead so GAME-026 builds names the same way.
- m3 **Every SCENE_ANCHORS entry still carries GAP-134 or GAP-131**, including `Anchor_CheckIn` at Med, apart from stations 09/10, which have none. That is correct, but it means Gameplay's fallback warning will list almost every anchor until ART-007 lands. This is a note, not a fix.
