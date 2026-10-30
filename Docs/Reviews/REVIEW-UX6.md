# REVIEW-UX6 — UX-006, counter UX addendum (said cards, "Note it as…", query preview, tool outcomes)

**Verdict: PASS with minors (GO).** I reviewed `worktree-agent-ab1c3cb58a8e71856` @ 6e0f00f against main 4dc9915. The branch's own changes are DES-006 (already reviewed in REVIEW-DES6), DES-005 and the UX-006 files. The rest of the `main..6e0f00f` diff is main moving ahead since the branch merged it, not reverts. This file is committed on `review/ux6`, cut from 6e0f00f. Inputs read: the packet, the handoff, `UX_COUNTER_INTEL.md` §2/§9/§13, CF§2–3, RDA§3–5, DEC-103 and the cited tool lines. The lead's rulings on U1–U6 are taken as given.

## Checks
1. **§0–12 unchanged: PASS.** The `UX_COUNTER_INTEL.md` diff is a single hunk that only adds lines from line 187 (§13).
2. **Consistency: PASS.**
   - CF: Esc is pause and Backspace/Ⓑ is Back on every frame (§13.1, §13.8). §13.9 item 1 overrides the old Esc rows.
   - UX-005: Q9 is item 8 and the Q6/Q7 keys are reserved, so §2's numbers never shift. Ⓧ for leave-out mirrors §9's token drop. The new keys Q, P and LB collide with no binding in §9, CF§3.3 or today's keys.
   - RDA§3–5: said cards, Their words plus 2–3 terms, terms listed alphabetically (no position hint), the exact `Parse()` preview, every Responder outcome framed, Q9 revealing the toggle, the reject loop as follow-up lines, tile = chip-only (DEC-057), and misreads never shown (DEC-052). §13.11 maps each frame to RDA§5 items 3–5.
3. **[GDD] labels: PASS.** Every size, timing and copy value is [GDD], cites the tool, or is an existing key.
4. **Tool wording cited by line: PASS** (exception m1). These lines say what §13 says: T:16632 (budget → maxPrice), T:16633-16635 (exclusion note), T:16662-16667 (budget-only ask), T:16677 (Help "Try:"), T:19557 (drive line), T:16595 (PriceOnly), T:16541-16554 (lookup + Near), T:1585-1589 (toggle).
5. **§13.9 deviations justified: PASS.** Each one cites CF§2.4, RDA§3.3/3.5 or DES-006 Q2 (m2 covers completeness).

## Minors
- m1 **Two strings are written by UX although the tool has its own text for those outcomes.**
  - `nearLabel` "Close to it, in stock:": the tool's text is "In stock and close to it[, without {terpene}]:" (`T:16554`).
  - `notFound` "Not on the menu.": the tool's text is "Strain not found." (`T:16544`).
  - Fix: key both to those tool lines, like `helpTry`, so GAME-017a copies the tool's wording (lead ruling U5).
- m2 **§13.9 doesn't list every override, and the handoff's list differs from it.**
  - Two overrides are described only in their own sections: the reject landing on Query instead of Dialogue/`LastReject` (§13.7), and the Q6/Q7 key reservation (§13.5).
  - Item 4 (no free typing) restates a rule rather than overriding one.
  - Fix: add the two overrides to §13.9 so it is the complete override list GAME-017a checks.
- m3 **The tool echoes the price cap only `if hasPricingConfigured()` (`T:16632`).** The `· price cap` route line should follow whether the engine actually sets `maxPrice`, not the raw parse. Note this for GAME-017a.
