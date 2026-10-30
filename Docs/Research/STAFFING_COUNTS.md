# Staffing counts (RES-002, closes GAP-DAY-03 evidence)

**Source:** the Phoenix store's 2026 schedule workbook, found in a retail-team OneDrive "Store Schedules" folder (read-only, DEC-031). It has one worksheet per week, running Fri–Thu, from 2026-01-23 to 2026-12-03 (45 sheets). **As of:** 2026-10-30. **PII:** aggregate counts only (DEC-006). No names, initials, IDs or individual hours are recorded here, and nothing was downloaded.

**Window counted:** 8 consecutive worked weeks, **2026-09-04 → 2026-10-29** (sheets 33–40), 56 days, 8 of each weekday. Sheets 41–45 are future weeks and were not counted. Earlier sheets were not tallied; the January sheet uses an older layout (it has a "Leads" tier).

## Shift pattern (as of Oct 2026)
- Store hours are 08:00–22:00 (O-rows). "CL" means close, counted as 22:00.
- **Budtender open:** 07:30–14:30. Until 2026-09-30 it was 07:30–15:30.
- **Budtender mid:** 10:00–18:00 or 11:00–19:00. Before mid-October there were 0–2 mids a day; since 2026-10-16 there are about 5–6.
- **Budtender close:** 15:00–CL. Before 2026-10-16 it was 14:00–CL.
- **Manager tier** (1 GM plus 2–3 assistant managers): an opener (07:30–15:30), a closer (14:00–CL) and, on weekdays, a third manager-tier person midday.

## Counts: people scheduled on the floor at each sample time (56 days)

| Daypart (sample time) | Budtenders: range | Budtenders: median | Manager tier: range | Manager tier: median |
|---|---|---|---|---|
| Opening (08:30) | 2–7 | 5 | 1–2 | 1 |
| Midday (12:30) | 4–9 | 6 | 1–3 | 2 |
| Shift handover (14:15) | 5–17 | 11 | 2–4 | 3 |
| 5–8 pm rush (18:30) | 4–11 | 6.5 | 1–2 | 1 |
| Late (21:00) | 4–8 | 6 | 1 | 1 |
| Whole day (distinct people) | 9–17 | 12 | 2–4 | 3 |

**Current pattern only** (since the 2026-10-16 change, 14 days): budtenders at Opening 2–6 (median **3**), Midday 5–9 (**6**), Handover 5–9 (**6**), Rush 5–11 (**8**), Late 4–8 (**7**). Before that (wk 33–38) the medians were 5 / 6 / 12 / 6 / 6. Since the change the store opens lighter and the rush is heavier. The handover spike has gone.

## By weekday: budtender median (range) at Opening / Midday / Rush / Late

| Day | Opening | Midday | Rush | Late | Manager tier (median, open/mid/rush/late) |
|---|---|---|---|---|---|
| Mon | 5 (3–5) | 5 (4–5) | 6 (5–8) | 6 (5–7) | 1/2/1/1 |
| Tue | 5 (3–6) | 6.5 (6–7) | 8 (6–11) | 7 (5–8) | 1/2/1/1 |
| Wed | 5 (2–6) | 6 (4–6) | 5.5 (4–6) | 5.5 (4–6) | 1/2/1/1 |
| Thu | 6 (3–7) | 6 (5–7) | 7.5 (5–8) | 7.5 (5–8) | 1/3/2/1 |
| Fri | 5.5 (3–7) | 8.5 (5–9) | 8 (5–11) | 6.5 (4–8) | 1/2/1/1 |
| Sat | 6 (5–7) | 6.5 (5–8) | 7.5 (6–9) | 7 (6–8) | 1/1/1/1 |
| Sun | 4.5 (2–5) | 5 (4–5) | 5 (5–7) | 5 (4–5) | 1/1/1/1 |

Busiest: Tue, Thu, Fri and Sat evenings. Lightest: Sunday all day and Wednesday evening.

## Manager coverage (deli refills, DEC-079)
- Every one of the 56 days has **at least one manager-tier person from open to close**, and none has a gap at 08:30 or 21:00.
- Typically there is **1** at open, **2** midday on weekdays, **2–3 overlapping around 14:00–15:30**, and **1** for the evening and close. On Sat/Sun it is 1 all day apart from the handover overlap.
- So the game can assume **one manager available for refills at every hour**, with a second one at midday on weekdays. The evening rush has only one manager, who also closes.

## Method
1. Each week's sheet has a per-day roster block listing manager tier, then budtenders, each with a shift string. I transcribed these as role + start/end times only, with names dropped at the point of transcription, into a scratch script outside the repo. Then I counted the people whose shift covers each sample time. Where the weekly grid and the per-day block disagreed, I used the per-day block.
2. "Budtenders" means everyone in the budtender section. **This is not the number of registers open.** Some scheduled budtenders work reception/ID check, fulfilment or stocking, or are on break. The sales floor has **11 registers** (F1 counts 12 POS stations, but register 1 moved to BOH, DEC-039/040), so registers open ≤ min(budtenders on the floor, 11).
3. Anomalies: one duplicated manager entry was counted once, and one absence was excluded. One inventory day is noted on the sheet; its counts are normal.

## Confidence
- **High** for scheduled headcount by daypart over these 8 weeks: it is read directly from the sheets.
- **Medium-low** as a proxy for *registers open*: the schedule does not say who is on a register versus at the door, fulfilment or on break.
- Schedules are plans, not punches, so call-outs and swaps are not reflected.
- The pattern changed on 2026-10-16. Use the current-pattern figures for a "today" game day.

## Suggested use (for the Hub, not a decision)
SPEC_SHIFT_DAY §5 placeholders: Opening 0, Rush 1 4, Recovery 2, Steady 3, Rush 2 5, Late 3, Closing 0. Under the current pattern there are about 3 budtenders at open, 6 midday, 8 in the evening rush and 7 late. If roughly 1–2 of those are off-register (door, fulfilment, breaks) and one is the player, ambient coworker registers would be about **Rush 1 1–2, Steady 3–4, Rush 2 5–6, Late 4–5**. The Hub decides the off-register share (see the RES-002 handoff).
