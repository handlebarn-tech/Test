# REVIEW-REF12 — REF-012, office walkability and door geometry audit

**Verdict: PASS with minors (GO).** I reviewed `worktree-agent-a2f71eef653a08c1c` @ 7428391, cut from 2a8a95a. It changes 5 files, docs and data only. This file is committed on `review/ref12`, cut from 7428391. Inputs read: the packet, the handoff, the diff, DEC-051/076/088/090/103, the existing GAP-122/127 entries, SPEC_SHIFT_DAY §2 and the CONTROLS_FLOW_PS1 §7.1 contract (5c8031b). I checked everything with a scratch script.

## Checks
1. **No invented store facts: PASS.**
   - Every Low confidence field in all 15 rows carries a gap id. The new gaps are only GAP-135..139; the existing GAP-122 is reused for the A011/graybox position mismatch, which is legitimate.
   - Every hinge without a source is marked "placeholder" (GAP-137).
   - Entry `leaves: 2` comes from A310 E101 PAIR and the A011 3'-0" leaves.
   - DEC-103 (6) is applied correctly: the north-wall office door `Hall_Office` and the connector `HUB2_HUB` are `proppedOpen`, and so are FOH and BOH. No inner buzzed door is modelled, and the exit alarm stays unknown (GAP-138).
   - Entry swing geometry checked: L hinge at the south jamb, yaw −90 + (−90) → west; R mirrors it. Both swing out.
2. **Office rows: PASS.**
   - Only the 15 Office rows changed (13 moved or resized, 2 door rows with notes only). `_about`, `version`, `graybox_contradictions` and the other 71 rows are unchanged against the base.
   - Stated facts are kept: the cabinets stay on the south wall beside the HUB 2 door (DEC-051 Q9), the deli cart stays under the canister shelf, and the standing desk stays on the east wall (Q13). These moved only 0.2–0.45 ft along or onto their stated walls.
   - The large moves are the drum kit, plant, wire cart and chair, all guesses now tagged GAP-135.
3. **DOORS.json matches §7.1: PASS.**
   - Single-leaf rows use `Door_<Id>` as the child of `Door_<Id>_Hinge`. The pair uses `Door_<Id>_L/_R`, each with `<object>_Hinge`.
   - The anchors are `Anchor_Door_<Id>_A/_B`. Every row has `closedRotation` and a signed `openAngle`.
   - All enums match §7.1: `leaves`, `selfClosing` (true/false/unknown), `lock`, `npcUse`, `hardware` and `defaultState`.
   - `staffOnly` is never set together with customer `npcUse`. Every field convention is explained in `_about`.
4. **Round-trip: PASS.** `json.dumps(d, indent=1, ensure_ascii=False)` reproduces both files byte for byte. They have no trailing newline, and the encoding needs `ensure_ascii=False` because of the em dashes and ×; same convention as before.

## Minors
- m1 **Gameplay must handle rows that are not doors.** The arches have `type: opening` and `leaves: 0`, with a null pivot, rotation and `defaultState`; the grille has `type: foldingGrille` and `leaves: null`. §7.1 doesn't mention either case. GAME-025's door runtime should spawn leaves only for `leaves` ∈ {1, 2}. Tell the Gameplay lead (contract note, no data change).
- m2 **Rows with unknown positions are listed but not placed.** `Emergency_RetailE` has its existence at Low, and `Grille_101B` is listed but not placed. Gameplay and ART should skip any row whose `confidence` has `existence` or `all` = Low until GAP-137 closes. Say this in `_about`.
- m3 **The handoff is 51 lines.** Studio handoffs normally run to 40 or fewer. Trim it next time; no action now.
- m4 **FYI, not in REF-012's scope.** DEC-103 (4) says the guest shows the ID again at the register, which corrects DEC-086. CONTROLS_FLOW_PS1 §4.2 ("the counter never re-checks"), which I passed in REVIEW-W5U before DEC-103 existed, is now out of date. That is Gameplay's to fix.
