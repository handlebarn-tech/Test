# REVIEW-REF13 — REF-013: GAP-129/130/132/134 from the drawings, DEC-110, DOORS.json field audit

**Verdict: FAIL (1 major; quick fix-check).** The DOORS.json field audit, the measurements and the round-trip all pass. The major is HUB sizes left with no source and no GAP once GAP-132 closed (Hub rule 2026-10-30: an uncited store value is MAJOR).

I reviewed `worktree-agent-a2b65d251ee0f6ac2` @ 73e0e0c (parent 67b5cbf, `review/world-1` lineage): 7 files, docs and data. This file is committed on `review/ref13`, cut from 73e0e0c. Inputs read: the packet, the handoff, the diff, DEC-048/050/103/110, the A901 and A011 text layers (PyMuPDF, read only) and REFERENCES_INDEX §6.4/§8.5. I checked everything with a scratch script.

## Checks
1. **DOORS.json, field by field (required): PASS.** I printed all 15 rows × 13 audited fields.
   - Every value has a source (an A310 schedule line, an A011 vector, CCTV, a DEC or a label) or is a Low placeholder with GAP-137/138. No "typical" value is left.
   - Fixes from earlier: JC → lever and Ext_Delivery → pushBar (DEC-110 W6). Grille height 7'-6" per A310 101B. `clearOpening` is now Low/GAP-137 everywhere, as a derived value. Hall_Office `selfClosing` is downgraded to unknown because it has no schedule.
   - The rule for disagreeing A310 sets is stated in `_about`, and only values that agree across every candidate set are kept.
   - The handoff's change table matches the data.
2. **Measurements: PASS.**
   - The A901 sheet's text layer (page 13, detail 17 "POS ENLARGED PLAN") prints **9'-0"**, **2'-6"**, **27'-9"** and **19'-2¾"**. A011 prints **30'-6"** and **47'-2¼"**. These are the figures §8.5 uses.
   - South-run arithmetic: face y 20.0, staff edge 22.5, stand to 23.8, back counter at 27.0. That gives 3.2 ft behind the stand and 4.5 ft from counter to back counter.
   - The counter height of 2.833 ft is the A940 34" maximum (RI §6.4, High).
   - I did not re-extract the vector coordinates (A011 lines 3017/3019/2744) or the G000 parking scale. Those are the worker's readings, and A011 and A012 agree to within 0.01 ft.
3. **Entry pair at y 8.9–14.9: PASS (Med frame).**
   - `IDCheck_Stand` at y 7.15–8.65 sits just north of the north jamb. That is "directly left inside the entrance" for someone walking east (DEC-048).
   - The guard post (y 6.7), check-in (7.9) and wait 0 (9.9) shift with it. Spawn and Exit are on the parking side (DEC-110 W4 plus G000).
4. **Round-trip: PASS.** All three JSONs are LF-only in the commit and byte-identical with `json.dumps(indent=1, ensure_ascii=False)`.
5. **Scope: PASS.** No Office row changed. 28 rows changed, 1 was replaced (south return → SouthWestReturn), and the count stays 127.

## Major
- **M1 Closing GAP-132 removed the GAP from three HUB rows whose sizes have no store source, and raised them from Low to Med.** DEC-110 W3 confirms only *where* the desk and counter are, not their size.
  - `HUB/Desk_Computer` 5.0 × 2.5 × 2.5 ft: no size source.
  - `HUB/Counter_Long_EastWall`: depth 2.29 ft and height 2.833 ft have no source. The A940 34" applies to the retail millwork, not this existing HUB bench. The length of about 20 ft is ±3 ft from CCTV perspective, which §8.5 itself calls "Low (length)".
  - `HUB2/Cabinets_Storage_OfficeWall` 6.0 × 1.5 × 7.0 ft is cited only as "graybox FX_HUB2_Cabinets matches". That is our own placeholder, not store evidence.
  - Fix: keep each position at Med (DEC-110 W3, plus A011 for the room), but set the size fields Low with a gap. Either reopen a narrowed GAP-132 ("HUB furniture sizes"), or put them under GAP-110 if the Hub prefers. Do not raise a question (DEC-105/110): these are working placeholders.

## Judgement asked for: hinge rule (HUB2_HUB, Ext_Delivery)
- **Assessment: the TI drawing is reliable evidence for hinges.** On the three doors where CCTV shows the hinge, A011 agrees every time:
  - Hall_Office: E (R3C4);
  - Office_HUB2: W (chat_office_L);
  - Vest_FOH: N, which is right-handed, against the left default (FOH still).
  So A011's right-handed HUB2_HUB (S) and Ext_Delivery (N) are more likely correct than the left default, which Nolan called "my best recollection" and qualified with "most doors".
- **But** DEC-110 W5 says overrides come only from CCTV, and that is Nolan's rule, so the worker correctly applied the left default (Low, GAP-137, with the disagreement recorded). It is not a reviewer's place to override it.
- **FOR NOLAN (via the Hub):** propose amending DEC-110 W5 to "per-door overrides from CCTV **or the A011/TI vector drawing**". That would flip these two to S and N at Med. It needs no new question, just the Hub's proposal of the rule change.

## Minors
- m1 **Entry hardware storefrontPull → lever** applies DEC-110 W6 literally ("lever elsewhere"). It now contradicts CONTROLS_FLOW_PS1 §7.1 (DES-005b), which keeps `storefrontPull` for the entry, and my REVIEW-IMP3B m1, which pointed IMP-003 at DOORS.json. The data is cited, so this is not a major. **The Hub should rule once** whether the aluminium storefront pair is a W6 exception, then align DOORS.json, CF§7.1 and IMP-003 R6.1.
- m2 **`defaultState: closed` is Med on 8 rows on the strength of "not listed in DEC-103 (6)".** DEC-103 lists the doors that are *almost always propped*; being absent from that list doesn't prove a door is closed. Make these Low with GAP-138, or reword the source as "inferred from DEC-103 (6)". The working value can stay.
- m3 **Frame: A011 prints the retail interior 30'-6", but the V5 frame is 29.0** (the printed 1,373 SF ÷ 47.19 ft = 29.1 also supports 29.0). The two-anchor approach (south features from the south wall, west-wall features from the north wall) puts the whole 1.5 ft discrepancy into the customer floor between the north and south runs. That is documented and acceptable for now, but the Hub should queue a frame decision (GAP-125 family) before ART-007's final pass.
