# REVIEW-W5N — GAME-008: cover the ID stand, ID checks, strikes, report rows, text scale (+ W5G m1/m2)

**Verdict: PASS (GO) with minors.** Branch `review/wave-5n` (off `main` 1abafc1) merges `claude/task-game-008` (a73f8b7 + 7b5b056) cleanly as 9478ceb. Reviewer: UX-002 workcell session, 2026-10-30.

## Validation (studio.ps1, DEC-013 slot gate respected)
| Gate | Result |
|---|---|
| `unity-compile` | `csErrors=0; CompileCheck OK` |
| `unity-test-edit` | **204/204**: EngineGolden 26, ParserGolden 99, EngineFeature 5, **TfsParityGate 15**, DomainAssembly 2, IdCheck 11 (new), Slice 22, Cart 11, OverLimit 10, ProcArt 24 |
| `unity-test-play` | 9 total, 8 passed, 1 skipped (GPU capture under `-nographics`), 0 failed |
| `unity-capture` | PASS, graybox QA 23 views (max dev 0.22 ft); slice 24 shots incl. the cover prompt and the horizontal/vertical ID panel at 100/125/150 % (`Artifacts/Screenshots/9478ceb/slice/SLICE_09…18`) |

**Gate A (DEC-067):** TfsParityGate + engine and parser goldens all green. **No `Code/Domain/` edits** (diff: Simulation/Presentation/Tests/Data/USS only). The ID stand never touches `Search`/`Recommend`.

## Packet `Docs/Tasks/Active/GAME-008.md` and SPEC_COMP002 §3
| Item | Result |
|---|---|
| 1 Prompt at rush start, `coverCheckInChance` 0.5; next `coverCheckInCount` 3 arrivals show an ID; queue patience keeps draining | ✔ rolled once at the first rush spawn on its own RNG stream (`seed + 11`, so slice draws are unchanged); covered arrivals wait in `Stand` (`AtStand`); queue and stand both drain, so an ignored stand still ends the shift (tested) |
| Decline → small satisfaction hit | ✔ `declineCheckInDelaySec` 20 s [GDD] added to the wait penalty for those arrivals |
| 2 Generator: §3 cases and weights; DOB/expiry against the in-game date | ✔ `IdCardGenerator.Make` against `shiftDate` 2026-10-27 (a Tuesday = `shiftDayOfWeek`); weights from config match §3 (40/15/10/10/5/5/10/5). Out-of-state vertical at 21+ is valid (O3, GAP-COMP-03) |
| Validity rules (`minAgeYears` 21, `verticalGraceDays` 30) | ✔ `IdRules.IsValid`: expiry day counts (B2 "unexpired"); 21st birthday today = valid; AZ vertical valid through day 30, invalid at 31. Boundary tests for each, plus 300 IDs per case landing on their side |
| 3 Outcomes + strikes | ✔ admit valid → queue; admit invalid → queue + `StrikeLedger` strike with the B4 "$2,000 per violation" flavour; refuse valid → Walkout (own toast); refuse invalid → new `Refused` outcome, excluded from satisfaction and queue-wait averages |
| 4 Report rows | ✔ `IdsChecked`, `BadIdsCaught`, `ValidIdsRefused` in the Compliance block |
| Entry anchor | ✔ `Anchor_CheckInDesk` by name, `TEMP_` fallback beside the entry (DEC-048 "left inside the entrance"); GAP-COMP-08 for ART |

**DEC-036 M2:** the counter never re-checks ID. The POS still shows only the passive `✓ 21+ ID verified` badge (`SliceView.cs:319`); the decision lives at the stand. ✔
**UX_PS1 §4/§7:** prompt Y/N (Esc = decline), waits for an open screen to close, auto-declines after 8 s; stand marker + E; panel with header, in-game date, ID-1 card (portrait for vertical), A/R/Esc; HUD becomes the Counter-line strip while covering. No Enter binding, so a stray Enter can't admit. ✔

## W5G m1 / m2
- **m1:** `.meter-red .meter-fill` uses `var(--bad)` (#D55E00, the UX vermilion); the orange-red look is that token. No change was needed. ✔
- **m2:** the cover prompt and ID panel honour 125/150 %. Fresh shots checked: the prompt at 150 % fits with both buttons; the vertical ID at 150 % fills the safe area and repeats DOB / EXP / TYPE / FORMAT full size in a readout column, so the portrait card's ellipsized TYPE is still readable. ✔

## GAME-010 overlap (if it merges first)
- A merge with `claude/task-game-010-2ab042` applies **cleanly** (`git merge-tree`, no conflicts). Shared files: `SliceConfig.json`, `SliceTests.cs`, `SliceBotTests.cs`.
- **m1 (tuning):** GAME-010's persona bots (`SlicePersonaTests`) and `RunBot` (default `acceptCover=false`) never answer the prompt, so `Cover` stays Offered with no effect. Real players, though, get the 20 s decline delay on 3 arrivals in about half of shifts (or the stand's patience cost if they cover). GAME-010's `TUNING_PS1` numbers therefore don't include ID events. After both merge, re-run the persona grid with a "declines" and a "covers + perfect judge" persona, or note it in TUNING_PS1.
- n1: any GAME-010 code that counts outcomes (served + walkouts + noSales) must add `Refused` (the handoff flags this too).

## Minor / nits
- **m2:** at 125/150 % the full-safe-area ID panel hides the Counter-line strip, so the queue isn't visible during the check (UX_PS1 §4 wants it visible; §10 scale wins today). UX to decide, e.g. a compact strip inside the panel.
- n2: `TurnedAgo` steps *upward* past a Feb-29 DOB, so with an in-game date where today−30 days is Feb 29, an `AzVerticalRecent` at day 30 could land on day 31 (invalid). It can't happen with 2026-10-27; if `shiftDate` becomes configurable per shift, step toward the valid side instead.
- n3: the `ID age helper` assist (UX_PS1 §4, off by default) is not built; that's acceptable for PS1.

## For the Hub
Merge on GO. Route m1 to GAME-010 (persona/tuning note) and m2 to UX.
