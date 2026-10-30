# REVIEW-W4A — REF-005 (TI PDFs imported, counter/entry render-check)

**Verdict: GO with one correction applied.** Branch `review/wave-4a` = `main` + `--no-ff` merge of `claude/task-ref-004-1bebc3` (commits 6f9863e, 4754fbe) + this review. Conflicts in KNOWN_GAPS and REFERENCES_INDEX resolved: main's GAP-106/107 (DEC-039) and CCTV register rows kept; REF-005's TI rows, GAP-108, entry rows and §6.4 kept.

## 1. PDFs in `References/TI/` — PASS
I paged all three (text per page + a 37-page contact sheet + full renders of A011/A012).
- **Interior TI Approved Set (37 pp):** cover/G-sheets, general notes, A-series plans, RCP, door/finish schedules, partitions, elevations, millwork, I101, S-, M-, P-, E-sheets. No security plan, camera/alarm layout, P&P manual or credentials sheet. "Security/alarm/CCTV" hits are fire-alarm notes, the retail security grille (door schedule) and an electrical note that low-voltage CCTV/security is "by others" — boilerplate only.
- **A011 / A012 (1 p each):** floor plan with room areas, POS runs, door notes; lighting plan with legend. Nothing sensitive.
- The PDFs carry title blocks with firm phone/web and a few vendor contacts on the finish sheet (p. 11); DEC-037 allows this.
- Docs: no person names, phones, emails or permit/licence numbers in REFERENCES_INDEX §6, KNOWN_GAPS or the handoff (grep). Only the public business name/address of the Ahwatukee set (10827 S 51st St) appears in §6.9 and the handoff; a business address, not personal data. Optional: drop the street number.

## 2. Render-check claims
- **Entry 6'-0": holds.** A011 shows a two-leaf out-swinging storefront pair, each leaf about 3'-0" at 1/4"=1'. Matches E101 and the Hub ruling.
- **Counter 34": holds.** A940 detail 11 (3DE two-drawer POS cabinet) reads 2'-10" MAX, 4" base, 2'-6" top.
- **1½" quartz top: WRONG, corrected.** Detail 11 shows a **2" quartz edge**. The 1½" dimension sits on detail 12 (4D four-drawer cabinet, "countertop with backsplash") and detail 9. REF-005 "corrected" REF-004's 2" to 1½" by mis-attributing it. Fixed in §6.4 (both rows), §5 and GAP-108; added a correction note to the handoff. §6.4's "2'-0" box" depth for detail 11 was also unsupported (top is 2'-6", 4D overall 2'-1"); reworded. 34" is now High (rendered).

## 3. Consistency with DEC-037 / DEC-039 — PASS
- DEC-037: values used are heights/materials/types; positions not taken from the TI. Entry 6'-0" × 7'-0" consistent in §1.4, §5, §6.2, GAP-104. A011/A012 naming consistent.
- DEC-039/GAP-107: main's "mostly closed" row preserved untouched.
- §6.9: Ahwatukee set correctly excluded (not Phoenix), no values taken.

## 4. File sizes — PASS
9.15 MB, 252 KB, 251 KB; all under 10 MB, plain git.

## For the Hub
- Deli case, deli counter and jar sizes remain open (GAP-108/113); no file source.
- ART: use quartz 2" edge on POS top, 2'-6" deep; 1½" only on other cabinet tops.
- Not done: I did not re-check A901 elevations 5/8 renders or the other REF-005 §6 value changes beyond the counter and entry.
