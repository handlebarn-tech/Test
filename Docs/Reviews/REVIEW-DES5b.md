# REVIEW-DES5b — DES-005b: DEC-103/109/110 folded into the flow spec, W5U minors, DES-007 roadmap + tone

**Verdict: PASS with minors (GO).** I reviewed `worktree-agent-a3b6d4b4d43f54152` @ cf5d614 against main bbb80bb: 9 files, docs only. This file is committed on `review/des5b`, cut from cf5d614. Inputs read: the packet, the handoff, the diff, DEC-079/101/103/106/109/110, REVIEW-W5U, and main's `DOORS.json` and `SCENE_ANCHORS.json`. The lead's ruling (AZ vertical ID stays at the register) is taken as given.

## Checks
1. **Each change cites its DEC: PASS.**
   - The CF header, §3.2, §4.2–4.4, §5.0, §5.2, §6, §7 and §8 each cite DEC-103 (by item number), DEC-109, DEC-110 or DEC-079.
   - The packet edits, the SPEC_COMP002 §3 and UX_PS1 §4/§8 notes, the GAP rows and the roadmap rows each carry their DEC.
2. **No store facts beyond DEC-103/106/109/110: PASS.**
   - The call lines, the scan of the back of the ID plus green light, the ID re-shown at the register, check-in in seconds, the four propped doors, no inner door, the GM floor map (DEC-079), restroom staff only and push bars only on exits/delivery (DEC-110), and spawn on the parking side (DEC-110 W4) all match their sources.
   - The new register ID cases are DEC-109 lead-ruled game cases labelled [GDD].
   - TONE's "$2,000 per violation" is the existing [SRC] string (SPEC_COMP002 §3, AZ_COMPLIANCE B4).
   - New values (3 s, 0.6 s, 0.02, 2 s, station 08) are all [GDD].
3. **Door and anchor names match main: PASS.**
   - All 27 names in CF and the packets resolve against main's `DOORS.json` (ids, objects, `leafObjects`) and `SCENE_ANCHORS.json` (names plus aliases).
   - The propped set `Vest_FOH`, `Vest_BOH`, `Hall_Office` and `HUB2_HUB` equals main's `defaultState: proppedOpen` rows.
   - The leaves rule (spawn only for 1/2) and the zero-padded `<NN>` anchors match REVIEW-REF12 m1 and REVIEW-REF11 m2.
4. **KNOWN_GAPS touches only Gameplay rows: PASS.** The only edits are GAP-DAY-04 (now citing DEC-096, W5U m3) and a new GAP-CF-01..08 block. GAP-CF-04 stays open and is not re-asked (DEC-105).
5. **Roadmap append-only: PASS.** It adds a new §7 with 11 LT rows, and the diff deletes no lines. The phasing matches DEC-101 (1)–(8).
6. **W5U m1–m3: PASS.** GAME-026 Owns says never concurrent with GAME-025; both headers carry Dept, Owner, Reviewer, Touches and Interfaces; GAP-DAY-04 cites DEC-096.

## Minors
- m1 **The AZ-vertical row in the CF§4.4 table still says "[GDD, flagged to the lead]".** Replace that with "lead ruling (DES-005b)" now that the lead has ruled it stays at the register.
- m2 **GAME-026 Dependencies still writes `Anchor_Register_<n>_Call/_Operator`.** Elsewhere it is `<NN>`, zero-padded. Align it.
- m3 **CF§3.2 "Emergency exits: `npcUse = none`" doesn't match the field.** In DOORS.json and §7.1 the field is an empty list meaning nobody (`[]`). Reword to "`npcUse` empty".
- m4 **For World (already in the handoff):** main's DOORS.json has `JC` = pushBar and `Ext_Delivery` = lever, which contradicts DEC-110 W6 (push bars only on emergency exits and delivery). CF correctly reads the field as given and leaves the data fix to World.
