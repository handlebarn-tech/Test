# UX_COUNTER_INTEL — PS1b "Customer Intelligence" UI: questions, KNOWN facts, query preview, TFS workflows, no-sale, debug, report v2 (UX-005)

**Owner:** UX-005 · **Consumers:** GAME-017 (questions, KNOWN strip, info tag, preview), GAME-018 (Similar / Compare / Details), GAME-019 (no-sale, ASK_* lines), GAME-020 (debug panel, report v2) · **Status:** draft for review · 2026-10-30
**Inputs:** `Design/SPEC_DECISION_PRESSURE.md` (cited **DP§n**), `GAMEPLAY_SIMULATION_SPEC.md` (**GSS§n**) §13, §27, §49, §51, §80, §98, `Specs/UX_SLICE.md` (**US§n**), `Specs/UX_PS1.md` (**P1§n**), `Design/ROADMAP_POST_SLICE.md` §2b, DEC-052/057, REVIEW-W4L M1.
**Wireframes:** `Docs/Assets/UX/PS1b/cx_01…cx_08.svg` (1920×1080 + note strip). Regenerate: `python -I Docs/Assets/UX/PS1b/gen_ps1b.py Docs/Assets/UX/PS1b` (reuses the PS1 kit, so tokens match).

This extends US and P1; everything not restated is unchanged: tokens and colour (US§6), type and safe area (US§5), toasts (US§3.8), focus ring and Back (US§4), accessibility table (US§7). Values marked [GDD] are UX tuning, not law. Copy rule H1: no effect claims in any string.

## 0. Two boundaries that every screen keeps
1. **TFS cards mean only what the tool means** (DP§0A, §17). A result card shows rank order, fit label, price, grams, why line, anxiety chip, as today. No gameplay value is ever drawn on or inside a card: no completeness, risk, "best", DecisionQuality, satisfaction or evaluation rank.
2. **Evaluation-oracle values never reach player UI** (DEC-052, W4Q n2). `BestAvailableResolution`, utilities, regret, the true-intent TFS rank and per-customer `DecisionQuality` numbers live only in the dev debug panel (§6). The player report shows shift-level bands as words (§7).

## 1. Flow changes (from US§2)

| Step | Slice / PS1 | PS1b |
|---|---|---|
| Hear request | options: Look it up · Edit search | options: **1 Look it up · 2 Ask… · 3 Nothing fits right now** (3 only after the first search for this customer). KNOWN strip pinned top-left (cx_01) |
| Ask | — | 2 opens the question list (Q1–Q4, Q6–Q8); answer plays as subtitle; KNOWN updates; back to options |
| Query | intent tiles | tiles + **query preview** + Similar entry when a liked strain is known (cx_02) |
| Results | Inspect · Choose | **Details** (renamed Inspect) · Compare marks + **Compare n** · Similar · Choose · **Nothing fits right now** (cx_03) |
| Present / response | ACCEPT / ASK_* / REJECT | ASK_* customer lines reveal a KNOWN field (source ↩ or ✋); player is back on Results with the strip updated |
| No-sale | Cancel on POS | **Nothing fits right now** → confirm card (cx_04) → customer leaves, no sale |
| Report | slice rows + Compliance | **report v2** (cx_06, cx_07) |

## 2. Question menu (cx_01) — GAME-017
- **Opens** from dialogue option **2 Ask…** (key 2 / click / Ⓐ). The list replaces the options column at the same place (380×540). Backspace / Ⓑ returns to the options; Esc closes dialogue as today.
- **Items** (DP§9 wording, shortened to fit one line at 100 %; full wording is what the player character says aloud):

| # | Menu text | Spoken line (subtitle) | DP |
|---|---|---|---|
| 1 | What are you looking for? | What kind of experience are you looking for? | Q1 |
| 2 | Anything you don't want? | Anything you definitely don't want? | Q2 |
| 3 | Need to stay functional? | Do you need to stay functional? | Q3 |
| 4 | Trying to stay under anything? | Trying to stay under anything? | Q4 |
| 5 | Had anything you liked? | Anything you've had before that you liked? | Q6 |
| 6 | Anything you didn't like? | Anything you've had before that you didn't like? | Q7 |
| 7 | When will you use it? | When are you planning on using it? | Q8 |

  Q5 (product type) is not listed until PS3 (DP§9). Order is fixed so muscle memory works.
- **Already-answered questions** look exactly like unanswered ones: no grey-out, tick, counter or "asked" badge, and the order never changes (DP§10). This replaces US§3.2 "asked ones grey out" and retires `dialogue.questionsLeft` (US data list): there is no hard question cap, only DP§12 friction.
- **Answer:** player line (subtitle, speaker "You") → customer line → a new fact drops into the KNOWN strip (fade ≤150 ms; instant under reduced motion). If the field was already known the customer restates it (`restate` line) and nothing in the strip changes. If the question reveals nothing new for this customer (e.g. no budget), the customer's "no constraint" line plays and no chip is added (`noConstraint`).
- **Friction** (DP§12): after the tolerance threshold the customer answers with a deflection line instead (`deflect1..3`), chosen in order, never repeated twice in a row. No anger icon, no bar; the queue's body language (GSS§27, §98) and the clock carry the cost.
- **Time cost:** a question costs its DP§9 seconds on the sim clock (GAME-017). The UI shows no number or bar for it (DP§39).
- **ASK_\* follow-ups** (GAME-019, DP§27): after a presented card, the customer's ASK_* line reveals a field; the chip gets source ↩ (follow-up) or ✋ (rejection). The player then lands on Results with Edit search one key away, as today.

## 3. KNOWN strip and CUSTOMER INFO tag (cx_01–cx_03) — GAME-017
- **One component, two placements:** dialogue → top-left panel over the world (1290 wide); terminal → second row of the request strip on every terminal screen (1520 wide), under the opener line, which stays verbatim.
- **Content:** label `KNOWN`, then one chip per **known** field in fixed order: Effect, Also, Avoid, Stay functional, Budget, Time, Liked, Didn't like, Amount. Chip = `{Field}: {value} {source glyph}`. Unknown fields are **not** shown (listing "Budget ?" would tell the player which fields matter for this customer).
- **Source glyphs** (DP§4 `RevealSource`): 💬 said it (opener) · ❓ you asked · ↩ follow-up · ✋ after a rejection · ↺ remembered (repeat memory, GAME-021) · 🧾 purchase history (GAME-021). The glyph is never the only carrier: the chip's tooltip / screen-reader name is `{Field} {value}, {source word}`.
- **Low confidence:** value prefixed `≈` when `confidence < knownVagueBelow` [GDD 0.7] (e.g. "maybe around twenty" → `Budget: ≈ $20`).
- **Overflow:** chips wrap to a 2nd row, then a `+{n}` chip that opens the full list (focusable).
- **CUSTOMER INFO tag** (DP§17, GSS§51): at the right end of the KNOWN row, never on a card, never in the results grid. Words: `● CUSTOMER INFO COMPLETE` / `◐ CUSTOMER INFO PARTIAL` / `○ NEED MORE CUSTOMER INFO`, from `InformationCompleteness` ≥ `infoCompleteAt` [GDD 0.8] / ≥ `infoPartialAt` [GDD 0.4] / below. Style is deliberately unlike a fit label: square corners (fit chips are pills), `--t2` text and border, never `--ok/--warn/--bad`. It updates on reveal events only.
- **Assist:** the tag is the accessibility/assist row `Customer info hint` (default on). GAME-022 may set it per difficulty (question Q1 in the handoff).

## 4. Query preview (cx_02) — GAME-017
- Panel `You'll search for` between the tiles and Search: the **exact** string the composer passes to `QueryParser` (DEC-057), in quotes, never ellipsized (wraps to 3 lines max at 150 %). The debug panel shows the same string.
- Under it, one **token** per known fact that the composer turns into wording (effect, avoid, stay functional, budget, time). Tokens start on; ✕ / Del on a focused token drops it from this search only (the fact stays KNOWN). Liked / didn't-like strains are not wording: they drive Similar.
- **Chips stay the quick path:** a tile sets the effect token (replacing a KNOWN effect token for this search). Chip-only = the tile's canonical wording, which must equal the DEC-017 golden parse.
- No free typing in PS1b (keeps the floor simple and the composer canonical).
- Empty preview (nothing known, no tile): Search disabled with `Pick what they're after first.`

## 5. Similar, Compare, Details (cx_02, cx_03) — GAME-018
| Workflow | Entry | Shows | Cost tag [GDD band] |
|---|---|---|---|
| Details | card button **Details** (I) — was Inspect | ux_05 Detail screen unchanged | `quick` |
| Compare | mark 2–3 cards (C toggles; mark box on each card) → footer **Compare {n}** (Shift+C) | ux_06 compare screen with the engine's compare output, no re-sort | `takes a moment` |
| Similar | **Similar to {strain}** on Query and Results footer, only while KNOWN has a liked strain | Results screen titled `Similar to {strain}`, cards in the engine's Similar order, same card face | `takes a moment` |

- **Cost shown diegetically, not as a timer** (DP§39): the button carries a cost word (`quick` < 4 s, `takes a moment` 4–10 s, `takes a while` > 10 s on the sim clock [GDD bands]), the result appears at once (≤0.6 s "Pulling it up…" beat, instant under reduced motion), and the time passes on the sim clock: the HUD clock moves and queued customers' body language reacts. No seconds, bars or rings.
- Compare with fewer than 2 marks: button disabled `Mark 2–3 to compare`. A 4th mark replaces the oldest.
- Similar on a sold-out liked strain still runs (the engine excludes stock, DP-024); the header reads `Similar to {strain} (sold out)`.

## 6. "Nothing fits right now" (cx_03, cx_04) — GAME-019
- **Placement:** dialogue option 3 and the Results footer, bottom-left, far from Choose. Neutral button style (it can be the right call, DP§30). Shown only after the first search for this customer.
- **Confirm card** (800×340, centred): title `Tell them nothing fits right now?`, the DP§30 line quoted, `They'll leave without buying.`, buttons **Keep helping** (default focus) and **Tell them**. Enter acts on the focused button only, so a stray Enter or a repeated N never ends the service.
- After: customer reply line, neutral toast `↩ No sale · {reason}` 4 s. Informed vs avoidable is never hinted; it appears only in the report counts and the debug panel.

## 7. Report v2 (cx_06, cx_07) — GAME-020
- **Header:** stars from the DP§106 gate + one reason line: `All three categories acceptable` / `Overall acceptable · one category weak: {CAT}` / `Major breakdown: {CAT}` / `Capped: {severe flag}` (DP§107). Stars never come from an average.
- **Category row:** SERVICE · FLOW · OPERATIONS tiles, each a band word + shape: `▲ Strong` / `● Acceptable` / `▼ Weak`.
- **Revenue** in its own dashed box to the right: `Revenue (not part of the stars)`.
- **Summary rows** (DP§108): Customers served, Average wait, Average service time, Average decision quality (**band word** from the DP§23 bands: Excellent / Good / Acceptable / Poor / Major mistakes; no number), Customer satisfaction (band word), Walkouts, Stockouts, Waste (`—` until a waste mechanic exists).
- **Detail tabs** (← → / LB RB): Service (§109), Consultation (§110), Inventory (§111), Flow (§112), Compliance (P1§6 unchanged). Counts are plain counts; `Average customer info` uses the CUSTOMER INFO words; `Relevant question rate` is a %. Rows for systems not built yet are hidden, not 0 (restock rows wait for GAME-012); built rows with no events show 0.
- Not shown anywhere in the report: utilities, regret, true-intent ranks, per-customer DQ.

## 8. Dev debug panel (cx_05) — GAME-020
- F3 (exists), debug builds and editor only (`Debug.isDebugBuild || Application.isEditor`, as today, GSS§80). Non-modal, never takes focus, fixed 100 % text (not scaled), mouse-wheel scroll. Shows the serving customer, else the last served. Header: customer #, archetype, seed.
- **Two fixed columns** with their own header colour and rule (DP§113): **TFS VALUES · engine output** (left: query sent, parse, outcome, candidates in TFS order with fit labels, Similar/Compare outputs, workflows used, player-selected candidate + its TFS rank) and **GAMEPLAY VALUES · simulation + evaluation** (right: TRUE profile, KNOWN profile with sources, InformationCompleteness, InformationRisk, QuestionTolerance, desired/actual depth, QueueCost, satisfaction, then a sub-block `EVALUATION (uses true intent, DEC-052)`: BestAvailableResolution, utilities, DecisionRegret, `DecisionQuality {n} (gameplay, not a fit)`). A value never moves between columns.
- **Rejection explanation** (DP§114) full width below: every line prefixed `[TFS]` or `[GAME]`: query used, card chosen (TFS rank), facts not yet learned, outcome, gameplay cause. Never phrased as the game knowing the card was wrong.

## 9. Input mapping (new controls)
New keys avoid I, M, F3 and the PS1 keys (R, A, Del, Y/N in the cover prompt, T, E). Number keys are scoped to the open list.

| Control | Keyboard / mouse | Controller |
|---|---|---|
| Open question list | 2 (dialogue) / click | Ⓐ on "Ask…" |
| Ask question n | 1–7 while the list is open / click | D-pad + Ⓐ |
| Back from question list | Backspace / click | Ⓑ |
| Expand KNOWN overflow | focus `+n`, Enter / click | Ⓐ |
| Drop preview token | Del on focused token / click ✕ | Ⓧ |
| Search | Enter / click | Ⓐ |
| Details | I / click | Ⓨ |
| Compare mark | C / click box | Ⓧ |
| Compare n | Shift+C / click | Ⓧ hold |
| Similar to {strain} | S / click | RS click |
| Nothing fits right now | 3 (dialogue) · N (Results) / click | LS click |
| No-sale confirm | Tab / → to "Tell them", Enter; Esc = Keep helping | Ⓐ on focus · Ⓑ |
| Report tabs | ← → / click | LB / RB |
| Debug panel | F3 (exists) | — |

Focus order is the pink numbers in each frame. Default focus: question list → item 1; Query → preview (then Search); Results → card 1 Choose; no-sale confirm → Keep helping; report → first detail button. N on Results is safe: it only opens the confirm. Keyboard focus nav is still the GAME-002 open item; direct bindings work meanwhile.

## 10. Text scaling 125 / 150 % (REVIEW-W4L M1, PS1 + PS1b panels)
Root classes `.text-125` / `.text-150` as US§5. Rules per panel:

| Panel | 125 / 150 % behaviour | Never truncates |
|---|---|---|
| Cart line (P1§2, 80 px) | grows to 96 / 112 px; name and batch·tier ellipsize (full name in focus tooltip and Details) | stepper, grams, line price, ✕ (fixed columns) |
| Register (P1§2, 1000×900) | at ≥125 % switches to **two columns in the full safe area** (1728×972): lines + Add item left, meter / totals / payment / Confirm right (cx_08), as medical does. **Never scrolls**; Confirm always on screen | totals, Confirm |
| Limit meter row (P1§3, 440 px) | bar widens with its column; label and `{g} / {cap}` stay one line, state text and trim hint wrap to 2 lines | value, state words |
| ID card (P1§4) | card scales up to fit the panel (panel grows to the safe area); if a decision field cannot reach the chosen scale on the card (vertical IDs at 150 %), DOB / EXP / TYPE / FORMAT are also listed in a readout column beside the card at full scale | **DOB, EXP, TYPE, FORMAT**; NAME may ellipsize |
| Counter line strip (P1§4, 440×420) | width 550 / 660, height grows per row; at most 5 rows, then `+{n} more` | patience words, `◆ Stand: n waiting` |
| Cover prompt (P1§4, 800×300) | height grows; body wraps | both buttons |
| KNOWN strip | chips wrap to 2 rows, then `+{n}` | CUSTOMER INFO tag (never wraps) |
| Question list | panel widens to 520 / 620; each item wraps to 2 lines | — |
| Query preview | wraps to 3 lines | the preview text (never ellipsized) |
| Results cards | as US§5 | fit label, price |
| Report v2 | rows grow; each tab scrolls vertically inside the panel (no timed action there) | star reason line, band words |
| Debug panel | not scaled (dev only) | — |

## 11. New strings (for `SliceLines.json`)

| Key | Text | Used by |
|---|---|---|
| `optAsk` | Ask… | GAME-017 |
| `askBack` | Back | GAME-017 |
| `q1Menu` / `q1Say` | What are you looking for? / What kind of experience are you looking for? | GAME-017 |
| `q2Menu` / `q2Say` | Anything you don't want? / Anything you definitely don't want? | GAME-017 |
| `q3Menu` / `q3Say` | Need to stay functional? / Do you need to stay functional? | GAME-017 |
| `q4Menu` / `q4Say` | Trying to stay under anything? / Trying to stay under anything? | GAME-017 |
| `q6Menu` / `q6Say` | Had anything you liked? / Anything you've had before that you liked? | GAME-017 |
| `q7Menu` / `q7Say` | Anything you didn't like? / Anything you've had before that you didn't like? | GAME-017 |
| `q8Menu` / `q8Say` | When will you use it? / When are you planning on using it? | GAME-017 |
| `speakerYou` | You | GAME-017 |
| `restate` | Like I said, {0}. | GAME-017 |
| `noConstraint` | Not really, whatever works. | GAME-017 |
| `deflect1` / `deflect2` / `deflect3` | I don't really know, man. / I just want something. / Can you just show me something? | GAME-017 (DP§12) |
| `knownLabel` | KNOWN | GAME-017 |
| `knownFields` | Effect / Also / Avoid / Stay functional / Budget / Time / Liked / Didn't like / Amount | GAME-017 |
| `knownChip` | {0}: {1} | GAME-017 |
| `knownVague` | ≈ {0} | GAME-017 |
| `knownMore` | +{0} | GAME-017 |
| `srcOpener` / `srcAsked` / `srcFollowup` / `srcRejection` / `srcMemory` / `srcHistory` | said it / you asked / follow-up / after a rejection / remembered / purchase history | GAME-017, GAME-021 |
| `infoComplete` / `infoPartial` / `infoNeedMore` | ● CUSTOMER INFO COMPLETE / ◐ CUSTOMER INFO PARTIAL / ○ NEED MORE CUSTOMER INFO | GAME-017 |
| `previewLabel` | You'll search for | GAME-017 |
| `previewEmpty` | Pick what they're after first. | GAME-017 |
| `details` | Details | GAME-018 |
| `compareMark` | Compare mark | GAME-018 (screen reader) |
| `compareN` | Compare {0} | GAME-018 |
| `compareNeed` | Mark 2–3 to compare | GAME-018 |
| `similarTo` | Similar to {0} | GAME-018 |
| `similarSoldOut` | Similar to {0} (sold out) | GAME-018 |
| `costQuick` / `costMoment` / `costWhile` | quick / takes a moment / takes a while | GAME-018 |
| `pullingUp` | Pulling it up… | GAME-018 |
| `noFit` | Nothing fits right now | GAME-019 |
| `noFitTitle` | Tell them nothing fits right now? | GAME-019 |
| `noFitSay` | I don't really have anything that fits what you're asking for right now. | GAME-019 (DP§30) |
| `noFitCost` | They'll leave without buying. | GAME-019 |
| `noFitKeep` / `noFitTell` | Keep helping / Tell them | GAME-019 |
| `noFitReply` | Alright, thanks for being straight with me. | GAME-019 |
| `noFitToast` | ↩ No sale · {0} | GAME-019 |
| `starsReason` | All three categories acceptable / Overall acceptable · one category weak: {0} / Major breakdown: {0} / Capped: {0} | GAME-020 |
| `catService` / `catFlow` / `catOps` | SERVICE / FLOW / OPERATIONS | GAME-020 |
| `bandStrong` / `bandOk` / `bandWeak` | ▲ Strong / ● Acceptable / ▼ Weak | GAME-020 |
| `revenueApart` | Revenue (not part of the stars) | GAME-020 |
| `dqBands` | Excellent / Good / Acceptable / Poor / Major mistakes | GAME-020 (DP§23) |
| `reportSummary` | Customers served / Average wait / Average service time / Average decision quality / Customer satisfaction / Walkouts / Stockouts / Waste | GAME-020 |
| `tabs` | Service / Consultation / Inventory / Flow / Compliance | GAME-020 |
| `svcRows` | Ideal sales / Good compromises / Acceptable compromises / Informed no-sales / Avoidable mismatches / Avoidable no-sales | GAME-020 |
| `conRows` | Questions per customer / Relevant question rate / Average customer info / Over-consulted customers / Under-consulted customers | GAME-020 |
| `invRows` | Proactive restocks / Reactive restocks / Emergency restocks / Stockouts / Lost sales from stock | GAME-020 (restock rows after GAME-012) |
| `flowRows` | Peak queue / Walkouts / Average queue / Rush throughput / Recovery | GAME-020 |

Debug-panel labels are dev-only and stay in code (not localised). All strings are procedural or conversational; none claims an effect (H1). Customer answer lines for each question/archetype are GAME-017 content data (`SliceQuestions.json`), held to H1 too.

## 12. Validation
- GAME-017: question list, answer flow, friction lines → cx_01; KNOWN strip + info tag → cx_01–03; preview + tokens + chips → cx_02. GAME-018: Details, Compare marks/button, Similar → cx_02/03 (Detail and Compare screens reuse ux_05/ux_06). GAME-019: no-sale button + confirm → cx_03/04; ASK_* follow-ups → §2 (dialogue frame ux_07 unchanged). GAME-020: debug panel + explanation → cx_05; report v2 + details → cx_06/07. M1 → §10 + cx_08. ✔
- No gameplay value inside a TFS card (cx_03 note; §0). Oracle values only in cx_05. ✔
- Every new string is in §11. ✔ Each SVG < 10 KB. ✔

---

## 13. PS1b-a addendum — said cards, "Note it as…", query preview, tool outcomes (UX-006, for GAME-017a)

**Owner:** UX-006 · **Consumer:** GAME-017a (first playable depth) · **Status:** draft for review · 2026-10-30
**Inputs:** `Design/RECOMMENDATION_DEPTH_AUDIT.md` (**RDA§n**) §3–5; `Specs/CONTROLS_FLOW_PS1.md` (**CF§n**) §2.4, §3.3; DEC-103; §0–§11 above; today's screens in `Presentation/Slice/SliceView.cs` (Dialogue, Query, Results, Detail, Pos).

§0–§12 stand. This section adds the GAME-017a frames and overrides only the lines named in §13.9. Every size, timing and copy value here is **[GDD]** unless it cites the tool (`T:<line>`, RDA) or an existing key. Copy rule H1 holds: no string claims an effect. No product or strain name appears in any string; `{strain}` is filled at runtime from the catalog (RDA§3.2).

### 13.1 Flow (GAME-017a)
```
World ─E Talk─► Dialogue ──1 Look it up──► Query ──Enter Search──► Results ──Choose──► Pos ─► customer reacts
                  │  ▲                       ▲  │                     │                              │
                  │  └──Backspace────────────┘  └── Q Ask… ───┐       └─Backspace─► Query            │
                  └──2 Ask… ──► Questions ◄────────────────────┘                                     │
                                  (answer → new said card)          REJECT + follow-up line ◄────────┘
                                                                    → new said card ✋ → Query (re-read, re-search)
```
- The counter ID re-show (DEC-103) belongs to the counter/POS flow (GAME-026); these frames start once the dialogue opens and are unchanged by it.
- Esc opens the pause menu everywhere (CF§2.1); **Backspace / Back / Ⓑ** is Back on every frame below (CF§2.4).

### 13.2 Said cards (all frames) — GAME-017a deliverable 3
A **said card** is one customer statement: an opener clause, a question answer, or a follow-up line after a rejection (RDA§3.3). It replaces the field chips of §3 for GAME-017a (`CustomerKnowledge` minimal; GAME-017 adds field chips later, §13.9).

```
┌──────────────────────────────────────────────┐   ┌───────────────────────────────┐
│ 💬 "Something chill."                       │   │ ❓ "Under forty, if I can."    │
│ → Note it as…   (not noted yet ●)            │   │ → under $40          (term)    │
└──────────────────────────────────────────────┘   └───────────────────────────────┘
┌──────────────────────────────────────────────┐   ┌───────────────────────────────┐
│ ✋ "That one's gonna knock me out."          │   │ 💬 "Something for sleep."      │
│ → their words                                │   │ → as said            (locked)  │
└──────────────────────────────────────────────┘   └───────────────────────────────┘
   example lines are [GDD] placeholders from RDA§3.2 style, not data
```
- **Face:** line 1 = source glyph (§3: 💬 opener, ❓ asked, ✋ after a rejection, ↩ follow-up) + the verbatim words in quotes, wrapping to 2 lines, never ellipsized. Line 2 = the reading: `→ Note it as…` + an unread dot, `→ their words`, `→ {term}`, or `→ as said` for a direct phrase (already tool wording, RDA§3.3; no picker, card shows a lock glyph 🔒 and tooltip `Already how the tool says it`).
- **No component name** (effect, budget…) on the card: naming the component would do the interpretation for the player (RDA§3.3 point 4).
- **Size:** 300 × 64 px at 100 % [GDD]; 8 px gap; cards in the order said, oldest first, 2 rows then `+{n}` (as §3 overflow). Text scale: card grows to 2 lines of quote at 125/150 %; reading line never truncates.
- **Placement:** dialogue = the KNOWN panel top-left (§3, 1290 wide); Query/Results = second row of the request strip (§3, 1520 wide). Same component, same order.
- **New card:** fades in ≤150 ms [GDD] (instant under reduced motion), plus a one-time `New` tag until the card is first focused. Screen reader name: `{source word}: "{words}", noted as {reading}`.
- **Excluded from this search** (Del, §13.4): card dims to `--t3`, reading line `→ left out of this search`.

### 13.3 "Note it as…" picker (Query) — GAME-017a deliverable 3
Opens on a focused, non-locked card (Enter / click / Ⓐ). A popover anchored under the card, 360 wide [GDD], focus trapped inside.

```
            ┌──────────────────────────────────────┐
            │ "Something chill."                   │
            │ Note it as…                          │
            │  1 ◉ Their words   "something chill" │  ← always first, default focus
            │  2 ○ {term A}                        │
            │  3 ○ {term B}                        │
            │  4 ○ {term C}            (if a 3rd)  │
            │  ──────────────────────────────────  │
            │  Leave it out of this search   Del   │
            └──────────────────────────────────────┘
```
- **Options:** `Their words` (the verbatim phrase goes to the parser) then the component's 2–3 terms from `SliceNeeds.json` (RDA§3.1), shown exactly as the composer will write them. Terms are listed **alphabetically** so position never tells which term reproduces the need. No term carries a hint, colour or score.
- **Choose:** number key 1–4 or ↑↓ + Enter / click / D-pad + Ⓐ → sets the reading, closes the popover, preview updates at once, focus moves to the next unread card (else back to the card).
- **Re-reading** is always allowed: reopen and pick another. It costs no sim time in GAME-017a [GDD] (searching does, §13.4).
- **Close without change:** Backspace / Ⓑ / click outside.

### 13.4 Query frame: preview, "the tool will", New-customer toggle — GAME-017a deliverable 3
```
┌─ request strip ────────────────────────────────────────────────────────────────────────────┐
│ Customer · {archetype}   "{opener line verbatim}"                                         │
│ [said card][said card][said card]  +1                                                      │
├────────────────────────────────────────────────────────────────────────────────────────────┤
│ What are they looking for?                                                                 │
│ [tile][tile][tile][tile][tile][tile]          ← quick path, unchanged                      │
│                                                                                            │
│ You'll search for                                                                          │
│ "something chill, under $40"                  ← exact Parse() input, never ellipsized      │
│ The tool will: recommend strains · price cap $40   ← route line (§ below)                  │
│                                                                                            │
│ Customer: ( Experienced | New customer )   P       ← only after Q9 has an answer          │
│                                                                                            │
│ [Ask… Q]                                   [Search  Enter]                                 │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```
- **Preview** (`previewLabel`, §4): the exact string passed to `QueryParser.Parse(ParserOptions.Game)` = the readings of the included cards, in card order, joined by the GAME-017a composer (separator and casing are the composer's, golden-captured, RDA§5 item 7). Wraps to 3 lines at 150 %. The debug panel shows the same string.
- **Unread cards:** Search is not blocked, but pressing Search while any card is unread opens the picker on the first unread card instead (default focus `Their words`, so Enter, Enter is the fast path). Every searched word is therefore a reading the player chose (RDA§3.3 point 2).
- **Tiles:** a tile still means a chip-only search (= the DEC-017 golden, DEC-057). While a tile is active the preview shows the tile's canonical wording only, the cards dim with `Tile search: cards not used`, and pressing the tile again (or Del on it) returns to the composed query.
- **Empty** (no included card, no tile): Search disabled, `previewEmpty`.
- **"The tool will"** (`toolWill`): one line from the parsed query, naming only the route and the values the tool itself echoes in its result: `recommend strains` / `look up {strain}` / `find strains like {strain}` / `show lowest prices` / `compare` ; plus `· price cap ${n}` when a max price parsed (`T:16632`), `· leaving out {terpene}` per exclusion (`T:16633-16635`), `· new-customer filter on` when the toggle is on. When the parse has no intent and no price, the line reads `not sure what to search; it will suggest wording` (the Help route, `T:16677`). It **never** shows intent keys or domains: that would reveal how their words parse, which is the player's call.
- **New / Experienced toggle** (tool `T:1585-1589`; sets `ShopState.NewCustomer`, default off as the engine): a two-state segmented control, shown only once Q9 has been answered (RDA§3.4 loop 1). P / click / LB toggles. Label `Customer:` then `Experienced` / `New customer`. It is a tool input, not wording, so it never appears in the quoted preview, only in the route line.
- **Ask…** button (Q / click / Ⓨ): opens the question list (§13.5) straight from Query, so the follow-up loop never needs a trip back to the dialogue. Backspace from the list returns to the frame it came from.
- **Search** (Enter / click / Ⓐ on Search): runs `QueryParser.Parse(Game)` → `Responder.Respond`, costs a flat search time [GDD] (GAME-017a config key; none is shown), opens Results.

### 13.5 Question list (GAME-017a cut) — GAME-017a deliverable 4
Same panel, rules and friction-free behaviour as §2, with **Q9** added as item 8. GAME-017a lists only Q1–Q4, Q8, Q9; items 5–6 (Q6/Q7) are hidden until GAME-017 and their keys do nothing, so numbers never change when they arrive.

```
┌ Ask… ─────────────────────────────┐
│ 1  What are you looking for?      │
│ 2  Anything you don't want?       │
│ 3  Need to stay functional?       │
│ 4  Trying to stay under anything? │
│ 7  When will you use it?          │
│ 8  Ever gotten anxious from it?   │  ← Q9, new
│                       Back ⌫ / Ⓑ │
└───────────────────────────────────┘
```
- Asking plays `You` line → customer answer line (subtitle) → a new **❓ said card** (§13.2). A restated or `noConstraint` answer adds no card (§2).
- Time cost: one flat [GDD] value per question in GAME-017a (no tolerance/deflection, RDA§5 item 4). Shown nowhere as a number (DP§39).
- Q9's answer card is a normal said card; answering also reveals the New/Experienced toggle (§13.4).

### 13.6 Results by tool outcome — GAME-017a deliverable 3
Header: `Search: "{query}"` (the preview string; replaces `Search: {chip}`), `Edit search` (Backspace). Card face is today's (§0); role tags and the why line stay GAME-018 (slot reserved under the fit label, hidden in GAME-017a). Every Responder outcome has a frame; texts the tool already has come **from the tool** (key cites the line, GAME-017a copies the wording; UX does not write it):

| Outcome (`ResponseKind` / `ResponseOutcome`) | Frame | Text source |
|---|---|---|
| Recommend · Ok | cards as today | — |
| Recommend · Fallback | `◐` banner + cards (exists) | `fallbackBanner` (exists) |
| Recommend · None | heading, no cards, `Edit search` focused | `noneMatched` (exists) |
| Recommend · ExcludedAll | as None + the exclusion note | tool's ExclusionNote text (`T:16633-16635`) |
| Recommend + `AskEffectForBudget` | prompt line above cards: the tool's "what effect" ask (`T:16662-16667`); focus on `Ask… Q` | tool line, key `askEffectForBudget` |
| PriceOnly | list rows `{strain} · {g} g · ${post}` in the tool's order, no fit label | tool order `T:16595-16612` |
| Strain lookup · found | one card (same face) + `Choose` / `Details` | — |
| Strain lookup · out of stock / excluded | the card dimmed `Out of stock` / exclusion note, then `Close to it, in stock:` + Near cards | tool `T:16541-16554`; key `nearLabel` [GDD copy] |
| NotFound | heading `Not on the menu.` + `Edit search` | [GDD] copy, key `notFound` |
| Help | heading + the tool's `Try: …` suggestions as plain text (not buttons: the player must re-read, not click a fix) | tool line `T:16677`, key `helpTry` |
| Drive notice (any outcome) | neutral line under the header | tool line `T:19557`, key `driveNotice` |
| Compare (if parsed) | GAME-018 frame; in GAME-017a shows as Help-style heading `Compare comes later.` [GDD] | — |

```
 Ok / Fallback                         Help                                   Lookup, out of stock
┌──────────────────────────────┐      ┌──────────────────────────────┐       ┌──────────────────────────────┐
│ Search: "something chill"    │      │ Search: "your heaviest one"  │       │ Search: "do you have {strain}"│
│ ◐ {fallbackBanner}           │      │ {tool help heading}          │       │ [card dimmed · Out of stock] │
│ [card][card][card]           │      │ Try: {tool suggestions}      │       │ Close to it, in stock:       │
│ More options (M)             │      │                              │       │ [card][card][card]           │
│ Edit search ⌫   Choose Enter │      │ Edit search ⌫   Ask… Q       │       │ Edit search ⌫   Choose Enter │
└──────────────────────────────┘      └──────────────────────────────┘       └──────────────────────────────┘
```
Default focus: Ok/Fallback/lookup → card 1 Choose (§9); None/ExcludedAll/NotFound/Help → `Edit search`.

### 13.7 Reject → follow-up → re-search — GAME-017a deliverable 5
```
Results ─Choose─► Pos ─present─► customer REJECTS
   → subtitle: follow-up line naming the unmet component (ASK_LESS_SEDATING / ASK_CHEAPER / ASK_STRONGER as lines only)
   → new ✋ said card, unread, `New` tag
   → screen: Query (not Dialogue), focus on the new card, picker closed
   → player: Enter → Note it as… → (optionally Q Ask…, Del to drop a card, re-read older cards) → Search
   → Results with the new query
```
- Landing on Query with the new card focused replaces today's "back to dialogue with `LastReject`" (`SliceView` dialogue line); the line still plays as a subtitle (2 s min, [GDD]) and stays readable as the card.
- Older cards keep their readings; nothing resets.
- No icon, score or colour marks the misread (DEC-052: misread regret is evaluation-only).

### 13.8 Input map (adds to §9; Esc = pause, Backspace = back per CF§2.4)
| Control | Keyboard / mouse | Controller |
|---|---|---|
| Move between said cards | ← → / Tab (Query, Results strip) / hover | D-pad ← → |
| Open Note it as… | Enter on a card / click | Ⓐ |
| Pick reading | 1–4 / ↑↓ + Enter / click | D-pad ↑↓ + Ⓐ |
| Leave card out / back in | Del on card or in picker / click `Leave it out…` | Ⓧ |
| Close picker | Backspace / click outside | Ⓑ |
| Ask… from Query or Results | Q / click | Ⓨ (Query) · Ⓨ stays Details on Results, so Ask… is the footer button there |
| Ask question n | 1–4, 7, 8 while the list is open | D-pad + Ⓐ |
| New / Experienced toggle | P / click | LB |
| Search | Enter on Search / click | Ⓐ on Search |
| Edit search (Results → Query) | Backspace / click | Ⓑ |
| Pause | Esc | Start |
New keys Q and P avoid every bound key (§9, CF§3.3, today's E/Y/N/A/R/M/F3). Number keys are scoped to the open list or picker. Focus order on Query: first unread card (else first card) → tiles → toggle → Ask… → Search.

### 13.9 Overrides of earlier text (for review)
1. §2 "Esc closes dialogue as today" and §9 "No-sale confirm … Esc = Keep helping" → Backspace / Ⓑ (CF§2.4); Esc is pause.
2. §3 field chips → said cards in GAME-017a; GAME-017 may add field chips later beside them (RDA§3.5 `"{said}" → {term}`).
3. §4 tokens per known fact → per-card include/exclude (Del); the composer joins the player's readings, not fields (RDA§3.3). Tile = chip-only search, not "replace the effect token".
4. §4 "No free typing in PS1b" stands (DES-006 Q2).
5. §2 list numbering: Q9 is item 8.

### 13.10 New strings (add to §11; all [GDD] unless a tool line is cited)
| Key | Text | Used by |
|---|---|---|
| `noteAs` | Note it as… | GAME-017a |
| `readTheirWords` | Their words | GAME-017a |
| `readAsSaid` / `readAsSaidTip` | as said / Already how the tool says it | GAME-017a |
| `readUnread` | not noted yet | GAME-017a (screen reader + tooltip) |
| `readLeaveOut` / `readLeftOut` | Leave it out of this search / left out of this search | GAME-017a |
| `cardNew` | New | GAME-017a |
| `tileOnly` | Tile search: cards not used | GAME-017a |
| `toolWill` | The tool will: {0} | GAME-017a |
| `toolRoutes` | recommend strains / look up {0} / find strains like {0} / show lowest prices / compare / not sure what to search; it will suggest wording | GAME-017a |
| `toolMods` | price cap ${0} / leaving out {0} / new-customer filter on | GAME-017a |
| `profileLabel` / `profileExp` / `profileNew` | Customer: / Experienced / New customer | GAME-017a |
| `q9Menu` / `q9Say` | Ever gotten anxious from it? / Have you ever gotten anxious from it? | GAME-017a (RDA§3.4) |
| `searchHeader` | Search: "{0}" | GAME-017a |
| `askEffectForBudget` | (tool line `T:16662-16667`) | GAME-017a |
| `helpTry` | (tool line `T:16677`) | GAME-017a |
| `driveNotice` | (tool line `T:19557`) | GAME-017a |
| `nearLabel` | Close to it, in stock: | GAME-017a |
| `outOfStock` | Out of stock | GAME-017a |
| `notFound` | Not on the menu. | GAME-017a |
| `compareLater` | Compare comes later. | GAME-017a |

### 13.11 Validation
- Each frame maps to RDA§5 "In": said cards + picker + preview + Search route + outcome texts → item 3 (§13.2–13.4, §13.6); Q1–Q4/Q8/Q9 + flat cost → item 4 (§13.5); reject loop → item 5 (§13.7); toggle → RDA§3.4 / row 13. ✔
- Consistent with §0 (no gameplay value on a card; misread never shown) and CF§2 (Esc pause, Backspace back). DEC-103 only touches the counter ID/call flow, outside these frames. ✔
- No product data: example lines are labelled placeholders; `{strain}` is runtime; tool texts are cited, not written here. ✔
