# REVIEW-W5K — RES-002: anonymised staffing counts (PII-critical)

**Final verdict: PASS (GO), after the addendum below.** `review/wave-5k` was rebuilt from `main` 4a635ec as **one squash commit** (e3e19c2) of `claude/xenodochial-bell-85575c` @ adb0243, so the first commit's person-identifying lines never enter main's history. Docs only: `Docs/Research/STAFFING_COUNTS.md` + `Docs/Handoffs/RES-002.md`. Reviewer: standing Docs reviewer (DEC-085), 2026-10-30.

## First pass (c133df3): FAIL
- **Clean:** no names, initials, IDs, phones or emails; no capitalised word in the added lines other than weekdays, months, headings and role words; the commit message had no names; the personal OneDrive path wasn't recorded. Counts are medians/ranges over 56 days at fixed sample times, the method is stated (roles + times only, names dropped at transcription, scratch outside the repo) and nothing was copied verbatim.
- **M1 (must-fix):** three lines described one identifiable person or one person's day: a uniquely held role's working hours, one manager's individual shift entries, and a health-related absence. (Deliberately not quoted here, so this review doesn't carry them into main.)
- **m1:** "12 registers" cited from F1. The sales floor has 11 (DEC-039/040).

## Addendum: re-review of adb0243 (squashed)
- **M1 closed.** The squashed diff now reads "a third manager-tier person midday" (no named role + hours), "one duplicated manager entry was counted once" and "one absence was excluded". A grep of the squashed diff for the removed phrasings and shift times finds nothing. The remaining role detail is a headcount ("1 GM plus 2–3 assistant managers") and opener/closer patterns that rotate across several people: acceptable ✔.
- **m1 closed:** "11 registers (F1 counts 12 POS stations, but register 1 moved to BOH, DEC-039/040)" ✔.
- The squash commit message carries no PII ✔. Nothing else changed.

## Placeholder rule for the off-register question (DES-004 input, for the Hub)
Recommended [GDD] rule, replacing SPEC_SHIFT_DAY §5's `openRegistersByPhase` until Nolan answers:
`ambientRegisters(phase) = clamp(budtenders(phase) − offRegister(phase) − 1, 0, 10)`, with `offRegister = max(1, round(0.2 × budtenders))` (door/ID, fulfilment, stocking, breaks). The −1 is the player, and 10 = 11 floor registers minus the player. Doors-closed phases (Opening, Closing) stay 0.
With current-pattern medians (open 3, midday 6, rush 8, late 7; Recovery uses the opening count, Steady the midday count) this gives **Rush 1 1, Recovery 1, Steady 4, Rush 2 5, Late 5**, inside RES-002's suggested ranges. Ambient registers have no sim effect (DEC-077 B), so the rule drives only presentation and PERF-002 NPC counts.
Question for Nolan: "About how many scheduled budtenders are off-register (door/ID, fulfilment, stocking, breaks) at open, midday, the evening rush and late?" Placeholder 20 %, min 1.

## For the Hub
Merge `review/wave-5k` as is (fast-forward or merge commit). **Do not merge `claude/xenodochial-bell-85575c` itself:** c133df3 still holds the removed lines. Consider deleting that branch once merged.
