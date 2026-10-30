# REVIEW-W3B — ART-002 graybox update + REF-003 scale-stand stills

**Reviewer:** REVIEW specialist · **Date:** 2026-10-29 · **Branch:** `review/wave-3b` = `main` (e1e191b) + `--no-ff` merges of `claude/task-ref-003-e34c4b` (6466f31) and `claude/task-art-002-5e7777` (6788cca). Both merges clean, no conflicts.

## Verdict: **GO with notes**

No blockers. Every gate re-ran green on the merged branch; the stills support the §2.2 spec and the graybox follows it; nothing outside ART-002's ownership was touched. Notes are follow-ups.

## Gates (this machine, merged branch)
| Command | Result |
|---|---|
| `unity-graybox` ×2 | both `Build OK … unchangedScenes=4`, no scene diff (committed scenes match current inputs) |
| `unity-compile` | CompileCheck OK, csErrors=0 |
| `unity-test-edit` | 24/24 passed |
| `unity-test-play` | 3/3 passed (incl. `GrayboxAnchorTests`: §7 anchors present + unique, ≥77 jar slots, scale on a stand by the terminal) |
| `unity-capture` | 24 captures, QA `views=23 maxDeviationFt=0.22 missing=0 tolerance=0.5 PASS` (`Artifacts/Screenshots/bc31871/`) |
| extra: forced rebuild (`-grayboxForce`) | Build OK walls=19 fixtures=52 cameras=23 anchors=124; scenes differ **only in fileIDs** (after normalising IDs every changed line pairs up); reverted |

DEC-013: one other editor (GAME-002) was running; the gate never had to wait.

## Checks
1. **REF-003.** I viewed both source stills and all 5 crops in `References/Index/register/`. No person in any crop (the wide still has customers and staff; the crops avoid them). §2.2 matches the stills: chrome wire stand, black lipped top tray clearly below the counter top, one low wire shelf, clear acrylic box/panel on the counter-side edge, one stand to the staff's right of each POS monitor, black wire bin beside one. Sizes are Low-Med and honestly labelled (keyboard convention). The video-wall promo is flagged as not pricing data. DEC-030 SE exit row is in §1.4; the black door is marked unconfirmed.
2. **ART-002 gates:** all pass (table above).
3. **Evidence.**
   - HUB/HUB 2 swap per DEC-024: CCTV tiles R4C3/R4C4/R5C3/R5C4 → HUB, R5C1/R5C2 → HUB 2 in `graybox_layout.json`; fixtures Low (GAP-110).
   - Scale stands per REF-003 §2.2 / DEC-021/026: follow-up sets 1.6×1.3 ft, 2.5 ft top, 1 shelf, ≈1 ft acrylic panel, west of each monitor (staff's right). R2C4 capture shows top below counter, one low shelf, pale panel. OK.
   - Heights per DEC-037: ceiling 9'-0" (back rooms too: in the 8'–9' range, no per-room value), soffit 7'-6" recorded but not modelled (no ceilings in the graybox), doors 7'-0", entry 6'-0" wide (x 12.5–18.5) × 7'-0". OK.
   - SE exit per DEC-030: `EXT_EMERGENCY_HUB`, 3'-0" opening at x 24.8–27.8 on the HUB south wall, Low, noted as not on the plan.
   - Every height row carries a GAP/DEC id; fixtures carry conf + GAP notes.
4. **DEC-029:** nothing in `Gameplay_Slice.unity` or `Code/Simulation|Presentation/`. The four graybox scenes regenerate from data; see m1.
5. **Hygiene:** largest new binary is 79 KB; `studio.config.json` is gitignored; no PII in the diff.

## Notes (non-blocking)
- **m1 Determinism is skip-if-unchanged, not byte-stable.** An unchanged rebuild leaves no diff (stamp hash), but any real input change (or `-grayboxForce`) rewrites every fileID in all four scenes (≈8.7k lines). Documented in GRAYBOX.md; the DEC-029 commit rule still covers it. Matters once GAME-002 or lighting references graybox objects by fileID: reference by name/anchor only.
- **m2 Station count vs DEC-037.** DEC-037 adopts "12 registers (Dutchie report)"; the graybox has 4 POS + 4 stands on the north leg, and GAP-107 still says the count is open. Hub: decide whether "12 registers" means 12 physical stations (then ART-003 adds stands on the return leg) and update GAP-107.
- **m3 ART-002 handoff** "Delivered" still lists the pre-follow-up stand (1.5×1.5, 3.25 ft top, 2 shelves); the "Gaps / notes" bullet corrects it. Cosmetic.
- **m4 DEC-026** still cites `References/Incoming/…`; the files are now `References/CCTV Register Back Center {East,Wide} 2026-10-29.webp` (REF-003 flagged it; Hub file).
- **m5** The SE exit sits on the HUB south wall although the "furthest SE door" would be in HUB 2 (REF-003 tension). Low and labelled; Nolan can settle which room it opens from.
- **m6** The raw register stills contain identifiable customers and staff, like the existing CCTV walls. Keep them out of any shipped build or public repo.

## Questions for the Hub (only Nolan can settle)
POS/stand count and numbering (GAP-107, m2); a tape measure on one stand (size → High; panel vs 3-sided box); which room the SE exit opens from (m5); GAP-106 compass direction.
