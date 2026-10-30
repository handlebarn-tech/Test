# REVIEW-W3E — REF-004 (TI set + 2026 A011/A012)

**Verdict: PASS with trivial fixes applied.** Branch `review/wave-3e` = `main` + `--no-ff` merge of `claude/task-ref-004-1bebc3` (no conflicts) + this review.

## 1. PII / security (DEC-006, DEC-031, DEC-037) — PASS
- §6, KNOWN_GAPS and the handoff hold no person names, phones, emails, permit/licence numbers or vendor contacts (grep + read). Only the architect firm (RSP, already in the index) and public product/colour names (SW paints, tile and quartz names) appear. Nothing is from the Security sheet, P&P manual or credential files; the handoff says those were not opened, and §6.8 says the A012 folder's security sheet was not read.
- Fix applied: removed the roof-hatch-and-ladder detail from §6.1 (a physical-access detail the game does not need). Door hardware types ("access-controlled", "storeroom lock") are kept: they come from the TI door schedule, not the Security sheet, and are generic.

## 2. Consistency with DEC-037 — PASS
- Retail gyp 9'-0" ✔, soffits 7'-6" ✔, back rooms ACT 8'-0"/9'-0" ✔, interior doors 3'-0"×7'-0" ✔, storefront E101 6'-0"×7'-0" ✔, neon 72" AFF ✔, TL-1 12×24 marble-look / TL-2 8×8 patterned ✔.
- Note for ART: the JC door is 2'-8"×7'-0" (TI schedule), a data-backed exception to the 3'-0" rule.
- A011 (floor) / A012 (lighting) naming is consistent in §0, §6.8, GAP-101 and the handoff. "A013" remains only in REVIEW-W3C, which is history.
- Gap changes are justified by §6: GAP-001 closed (RCP heights); GAP-104 mostly closed (A320/A310); GAP-002, 108, 109, 113 and 114 narrowed, with deli items kept open.

## 3. Confidence labels — fixed
- §5 counter row and GAP-108 said Med, but the §6.4 base-cabinet row said **High** for the same text-derived 34". Changed to Med. The other High labels follow §6's stated rule (a labelled schedule or keynote value).

## 4. Hub ruling recorded: entry width
**Entry storefront = 6'-0" × 7'-0" (TI E101 / DEC-037), not the plan's 9.0 ft.** The plan keeps the centre position. I added flags to §1.4 (ENTRY row) and §5 (Entry opening row) so ART sees it. §5's arch row now gives height 7'-0". The TI arch width (3'-0") differs from the drawn west arch (3.81 ft); the plan width is kept because it is position-bound. ART should keep that open until a site measure.

## Open items for the Hub (unchanged from REF-004)
- The PDFs are not imported (text-only connector). The manual copy into `References/TI/` is queued.
- The 34" counter reaches High only after a render check of A940/A901 once the PDFs land.
- Deli case, deli counter and jar sizes are still open (GAP-108/113). Lead: `COMPILED_Flower Shop_Int Set.pdf`.
