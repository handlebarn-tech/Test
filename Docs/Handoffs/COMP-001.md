# COMP-001 handoff — Arizona compliance review

**Status:** done · **Branch:** `claude/task-comp-001-c5bcd5` · Docs only (no `UnityProject/`, no SLICE_DESIGN). Game design research, not legal advice.

## Delivered
- `Docs/Research/AZ_COMPLIANCE.md`: 42 rules in 8 groups, each with citation, summary, DEC-032 class, slice/later, change.
- `Docs/Research/AZ_COMPLIANCE_CHANGES.md`: must-fix first, SliceConfig constants, later mechanics, omissions, proposed DECs, Nolan questions.

## Overselling verdict
The slice cannot oversell today (one sale, max 28 g < 1 oz per transaction, A.R.S. 36-2858(A)(1)(c)), but nothing enforces it.

## Must-fix (GAME-002, small)
1. **M1** POS blocks Confirm over `adultUseLimitGrams` = 28.0 g per transaction (+ EditMode test).
2. **M2** SLICE_DESIGN/UX: all queued customers are 21+ adult-use, ID-verified at check-in; POS shows "21+ ID verified".
3. **M3** Shift clock inside the legal 07:00–22:00 sales window (R9-18-308(A)(1)(a)).
Tax 25.1% is correct as additive 16% excise + 9.1% Phoenix TPT (42-5452(D)); no change.

## Top later mechanics
Limit meter + over-limit asks (violation strike, not game over); counter ID-check event with expired/under-21/30-day-rule IDs; medical customers (2.5 oz/14 days, card verify, 9.1% tax, out-of-state cards buy adult-use); edible 10/100 mg validator when packaged goods arrive.

## Open legal ambiguities
- ADHS rules read on Cornell LII mirror (official azsos PDFs returned 403); re-verify.
- Per-day limit: statute is per transaction only; store policy unknown (Nolan).
- Ounce = 28 g vs 28.35 g undefined; 28 g used.
- Phoenix city TPT 2.8% (July 2025 release) vs stale-looking 8.6% chart titles.
- No primary source found for: edible→flower equivalency, giveaways, scale class/NTEP, visitor logs, Metrc mandate, intoxicated-customer duty.

## Validation
Each table row cites a section; statutes/tax read on azleg.gov, azdor.gov, phoenix.gov on 2026-10-29. No downloads, no PII.
