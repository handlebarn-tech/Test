# REVIEW-W4L — UX-002 (PS1 UX spec: cart, limit meter, ID stand, medical POS, strikes)

**Verdict: PASS with one condition.** There are no blockers. M1 (text-scale rules for the new panels) is a short UX amendment that must land before GAME-006/008 build those views. The minors go to the Hub or the GAME packets.
**Branch:** `review/wave-4l` = main (79fdfc9) + merge of `claude/task-ux-002-c4fbb2` at 430b82e. The merge was clean. It is docs only: `Docs/Specs/UX_PS1.md`, 8 SVGs + `gen_ps1.py` under `Docs/Assets/UX/PS1/`, the handoff, and the packet move. Reviewer: REVIEW-W4L, 2026-10-30.

## 1. Decisions — OK
- **DEC-036:** M1 Confirm stays blocked over 28 g, and the red state disables Confirm (§3). M2: the `✓ 21+ ID verified` badge is kept, and the counter never re-checks.
- **DEC-048:** the limits are 28 g flower and 5 g concentrate. The concentrate row is built but hidden until PS3, and the PS3 `counts as {0} g` line covers packaged equivalents (edible ≈ 0.1 g). Medical is "rare (< 5 %)", with the same pre-tax prices, a lower tax and a higher allotment (§5). The ID stand sits left inside the entrance and is staffed by a guard (§4), and Q1/Q2 put the guard-vs-player conflict to the Hub instead of guessing.
- **DEC-049:** per transaction only. The adult-use meter resets for every cart, and a returning customer is allowed, gets no strike and no special UI (§3).
- **DEC-050:** packaged goods are out of PS1 scope. The fetch step (FOH / Fridge / Cooler source tag, patience keeps draining) is noted for GAME-004/PS3 and not wireframed. That is correct for the deli-only scope.
- **DEC-035/044:** the cart total is rounded once (§2), and price fit is left to GAME-006.
- **DEC-001 (TFS meaning): OK.** Results cards, fit labels, ranking and the engine query are unchanged. "Choose" only gets the label "Add to cart" once the cart has a line, `+ Add item` reruns the same Query, and the cart never re-ranks. The mean item fit is game satisfaction, not engine output. No engine field gains a new meaning.
- **H1 copy rule:** none of the 45 new strings claims an effect. The ID-card wireframe uses generated names and no real people (no PII).

## 2. GAME-006..010 packets — consistent, with the gaps below
- GAME-006: 1–3 lines, one Confirm, Cancel with no inventory change (SLICE_DESIGN §4), cart rounding and per-item presentation all match. The POS weight tiles become a per-line stepper, so the default focus moves from "3.5 g" to line 1 (documented).
- GAME-007: meter fraction / amber 0.75 / red blocks Confirm, trim by removing a line or stepping a weight down, no over-limit sale path, ledger and report rows all match.
- GAME-008: the case table, Admit/Refuse outcomes, strikes, the `verticalGraceDays` reason and the report rows match. The UX adds a **world marker + walk to the stand + E** (UX decision 3), which is not in the packet (m2).
- GAME-009: badge, 14-day meter, 9.1 % line, Sale type switch, and the out-of-state "blocked + hint, then blocked + strike" all match. The packet still says `medicalCustomerShare` 0.10 against DEC-048 < 5 % (m3).
- GAME-010: no UI dependency and no conflict.

## 3. UX-001 conventions — OK
The spec reuses the tokens, the Okabe-Ito status colours and the icon + word rule: the meter states are `⚠` / `✗` + text, never colour only. It also reuses the toast placement and rule (never takes focus) and the Hold-to-confirm. The 6 s strike toast is a documented deviation from the 4 s toast. The panels fit the 90 % title-safe area at 100 % text (900 ≤ 972 px tall).

## 4. Accessibility
- Keyboard: every new control has a direct key (§7), and nothing new needs a mouse. Opening the ID panel with focus on the card, so a stray Enter cannot admit, is good. The Counter line strip is forced on while covering, independent of the Patience-hints assist, so queue state never depends on an off-by-default option.
- **M1 (condition) — text scale 125/150 % undefined for every new panel.** US§5 only defines how cards behave at larger text. These have fixed sizes: the 80 px cart rows (name, batch·tier, stepper, price, ✕), the 1000×900 register (only 72 px under the safe-area limit at 100 %), the ID card at ID-1 ratio (770×486 / 540×856), the 440×420 Counter line strip and the 440 px meter row. Fix: state what wraps, ellipsizes or grows at 150 %. DOB, EXP, TYPE and FORMAT on the ID card must **never** ellipsize, because they are the decision. Say whether the register scrolls past the safe area or moves Payment to the right, as ps1_06 already does for medical.
- **m1 — `Ⓨ hold` for "Go to register" collides with US§4 `Ⓨ` = Inspect** on the Results screen, where the cart chip lives. It also adds a second hold action, which must obey the "Hold actions: Hold ↔ Press" assist (US§7: today the POS confirm is "the only hold action"). Pick a free button, or state the assist rule for it.

## Findings
**Blockers:** none.
**Major:** M1 (above): a UX amendment before GAME-006/008 view work.
**Minor (Hub to route):**
- m1 the controller Ⓨ conflict and the hold assist (above).
- m2 GAME-008's packet should add the stand world marker, the `◆ ID stand {n}/3` HUD line, the E-interact and the "arrivals wait at the stand" rule. It should also rename "check-in door" to the DEC-048 **ID stand** left inside the entrance (anchor or `TEMP_CheckInDesk`, GAP-COMP-08).
- m3 GAME-009's `medicalCustomerShare` 0.10 conflicts with DEC-048 (< 5 %). Set it to something like 0.04 [GDD] in the packet before GAME-009 starts.
- m4 The ps1_06 amber caption `⚠ 7.4 g left after this sale` is not in §5 or the §8 string table: the medical amber state has no string key. Add one (e.g. `medNearLimit`), or use §3's wording.
- m5 (PS3) The `counts as {0} g` line does not say **which row** a packaged line fills (flower vs concentrate: prerolls → flower, vapes/extracts/edibles → concentrate per DES/COMP). Say so when GAP-COMP-02 is mapped. The 3-line cart cap will likely be too low for packaged baskets in PS3.
- m6 The ID-card art says "ARIZONA · DRIVER LICENSE". The card must stay a generic layout, not a replica of the real AZ licence design or its security features. Note this for GAME-008/ART.
**Nits:** "Near the 1 oz limit" sits next to "{g} / 28 g". That is fine (DEC-036 uses 28.0 g), but keep the two consistent if the label is ever tuned. §5 does not say whether the badge changes when a MED customer is rung as Adult-use.

## For the Hub
- Answer or route the UX-002 Q1–Q4 (ID stand ownership, scanner verdict, out-of-state auto-switch, 14-day history on the POS). Until Q1/Q2 are answered, GAME-008 builds the placeholders: (a) the player covers the stand, and no verdict is shown.
- Ratify the 7 UX decisions in `Docs/Handoffs/UX-002.md`. I see no conflict in any of them except m1.
- Move `Docs/Tasks/Active/UX-002.md` to Done on merge. GAP-COMP-07 can close (DEC-049).
