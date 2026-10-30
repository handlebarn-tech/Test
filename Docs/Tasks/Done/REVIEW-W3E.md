# REVIEW-W3E — Review REF-004 (TI drawing set + 2026 A011/A012)

**Role:** REVIEW (docs) · **Priority:** P1 · **Branch:** worktree off `main`; local branch `review/wave-3e`.

## Setup
`git merge --no-ff claude/task-ref-004-1bebc3` onto `review/wave-3e` (it contains a RES-001 merge already on main; expect no conflicts). Read `Docs/Handoffs/REF-004.md` and `Docs/Tasks/Active/REF-004.md`.

## Checks
1. PII/security (DEC-006/031): REFERENCES_INDEX §6 and KNOWN_GAPS hold no names, phone/email, permit or license numbers, vendor contacts, or anything from the Security sheet, P&P manual or credential files.
2. Consistency: §6 values agree with DEC-037 (retail 9'-0" gypsum, soffits 7'-6", back rooms 8'–9' ACT, doors 3'-0"×7'-0", storefront 6'-0"×7'-0", neon 72" AFF); A011/A012 naming is consistent across §0, §1 and GAP-101; closed/narrowed gaps are justified.
3. Confidence labels: text-derived values (e.g. 34" counter) are marked Med, not High.
4. Hub ruling to record in the review: entry storefront width = 6'-0" (TI E101/DEC-037) over the plan's 9.0 ft; flag §1.4 for ART.

## Owns
`Docs/Reviews/REVIEW-W3E.md`; trivial doc fixes.

## Done when
`review/wave-3e` holds the merge and the review with a verdict. Report the verdict and a ≤10-line summary to the Studio Hub (never ask Nolan; DEC-033).
