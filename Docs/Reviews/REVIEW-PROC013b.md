# REVIEW-PROC013b: door sheet follow-ups (closed elevation tile; Hall_Break closer side)

- **Reviewed:** `claude/intelligent-lumiere-b0fd09` @ 511e9a2 · **merge base:** `main` @ 29da42f (Check 0 passed: `git merge-base --is-ancestor 29da42f claude/intelligent-lumiere-b0fd09` is true; the worker merged `main` 29da42f at 511e9a2, DEC-148)
- **Reviewer:** fresh session (STUDIO_OS §0.3/§0.7), strong visual review (DEC-122). Review branch `claude/review-proc013b-ebabc2` = `review/proc013b` @ 5784aed.
- **Sources read:** packet `Docs/Tasks/Active/PROC-013b.md`; `git diff 29da42f...claude/intelligent-lumiere-b0fd09 --stat` (18 files) and the full `doors.py` hunk; `Docs/Handoffs/PROC-013b.md` (Validation, Not done, For the Hub); `Docs/Reviews/REVIEW-PROC013.md` m2/m4/m5; `Docs/KNOWN_GAPS.md` GAP-DOOR-1; `Docs/REFERENCES_INDEX.md` §6.2 (rows 105, set 2.0 text); `Docs/Reference/DOORS.json` Hall_Break row and its `audit.selfClosing` line; `References/Index/cctv/wall2_R3C4.jpg`; all 15 `Docs/Assets/Specs/PROC_doors_*.png` sheets (a composite of the 15 closed tiles, plus Entry and Hall_Break in full and an Entry meeting-stile crop at 3×).

## Verdict: PASS with minors

## Checks
| Check | Result |
|---|---|
| 0. Branch contains `main` 29da42f | Pass. |
| Sheets run | Pass. `blender -b --factory-startup --python-exit-code 10 -P Tools/Blender/generators/doors.py -- sheets` (Blender 5.2) printed `EXIT=0` after 1 m 52 s. It rewrote all 15 per-door sheets plus the contact and LOD sheets. `git status` was clean afterwards, so my rerun is byte-identical to what the worker committed (deterministic; the contact and LOD sheets are unchanged). |
| No geometry / export / params change | Pass. `git diff --stat 29da42f HEAD -- Art/ Tools/Blender/params/ Docs/Assets/Specs/*manifest*` is empty. The `doors.py` diff is inside the `# --- review sheets` section (it starts at line 555): the `assemble` and `door_lines` signatures (new `frac` parameter, default `OPEN_FRAC`, so the other views are unchanged), `render_door` (new `closed` view, `frac = 0`), the `sheets()` view list and tile row, and docstrings. No geometry builder is touched. `KNOWN_GAPS.md`, `DECISIONS.md`, `CLAUDE.md` and the other truth files are untouched (GAP text is proposed in the handoff, as the packet requires). |
| Deliverable 1: closed tile on every per-door sheet | Pass. All 15 sheets are 2800 × 560 with five tiles: push 3/4, swing 3/4, 40 % elevation, closed elevation, evidence. The closed tile is labelled "drawn CLOSED". |
| Visual: leaves shut in frames | Pass. 11 swing leaves each sit inside their jambs under the head, with the undercut at the floor and the closer, lever, push bar or kick plate where the record says. The two arches and the grille have no leaf, so their closed tile matches the elevation. |
| Visual: Entry | Pass. Both leaves are shut and the two meeting stiles sit side by side with the thin seam between them and the back-to-back pulls at the meeting edge. At 1× the stiles read as dark on dark and the seam is faint; at 3× it is clear (see minor 2). |
| Deliverable 2: Hall_Break closer side | Pass. See Check 1. Sources are read and cited, the GAP is kept, and the geometry is not moved. That is the packet's allowed outcome and the right call while ART-013 consumes the Hall_Break FBXs. |
| Deliverable 3: m2 | Pass. No change, as the packet says. |
| Hall_Break closed tile vs evidence | Pass. The closed tile shows the parallel-arm closer at the head on the hall face; the evidence crop beside it shows the same face with none. The mismatch the handoff describes is visible by eye. The R3C4 still itself shows the whole head of the door and no closer on its hall face. |

### Check 1 (DEC-047)
- The closer-side reasoning cites both sources it names. A310 set 2.0 for door 105 is in REFERENCES_INDEX §6.2 line 344 ("storeroom lever + closer") and in `DOORS.json` Hall_Break `audit.selfClosing` ("A310 105 set 2.0: surface closer/stop", line 1215). It has no mount side. CCTV wall2 R3C4 exists at the path given and I read it myself: hall face, black "EMPLOYEES ONLY" door, fire label, lever on the right (latch) side, nothing at the head.
- The geometry facts it relies on match `DOORS.json`: hinge N, swing east into the break room, anchor A (Hall) at x 12.4 and B (Break) at x 17.4, so the hall face is the push face. The hinge side as seen from the hall also matches the still.
- The proposal is labelled Med confidence and is in the handoff's `## For the Hub`, not written into truth files. Every value either cites a source or is a labelled GAP. Pass. One wording minor (minor 1).

## MAJOR
None.

## minor
1. **Proposed GAP-DOOR-1 text is firmer than the handoff body.** The `## Done` section hedges ("*if* the scheduled closer is installed … Med"), but the proposed KNOWN_GAPS wording says flatly "so the 105 closer is on the break-room (pull) face". The schedule is the 2022 TI set and the store changed in 2023 (A011, DEC-120), so the R3C4 absence is equally consistent with the closer having been removed. When the Hub registers the amendment, keep the "if still installed" qualifier so the GAP doesn't assert an unseen closer. The pull face is never seen, so the claim is an inference from absence.
2. **Entry astragal/meeting stiles are legible only when zoomed.** The packet's validation wants the meeting stile pair and astragal to be visible. They are at sheet zoom 3× (the worker admits this and lists "no separate zoomed meeting-stile detail tile" under Not done), but at 1× the seam is dark aluminium on dark aluminium. Accepted, since the elevation orthographic view cannot do better without changing materials or adding a tile. If a later sheet pass touches the Entry, a zoom crop of the centre would make it reviewable at a glance.
3. **Office_HUB2 closed tile has low contrast.** The white leaf sits on the grey wall stub and the closer (grey on white) is barely visible. The leaf is distinguishable but its fit against the frame is hard to judge by eye. The worker noted the leaf is white; no action needed on geometry, but a darker stub for light leaves would help a future pass.
4. **Housekeeping.** The packet says it was "written by me … as briefed" (worker-authored packet); fine for the process, noted only for the record. `PROC_PIPELINE.md` and other docs do not describe the per-door sheet tile count, so nothing is stale.
