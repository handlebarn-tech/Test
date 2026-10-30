# UX_SLICE — Vertical-slice UI: recommend terminal, POS, HUD, dialogue (UX-001)

**Owner:** UX-001 · **Consumer:** GAME-002 (UI Toolkit build) · **Status:** draft for review · 2026-10-29
**Inputs:** MASTER_PLAN §4.2–4.3, §7.3 · GAMEPLAY_SIMULATION_SPEC §13–14, §17, §19, §24–27, §46, §48–49, §51, §62, §86–88 · `Reconstruction/RECONSTRUCTION_CONTRACT.md` (cited as **C§n**) · `LOGIC_TRIAGE.md` (cited as **T#n**) · tool v7.11.4 recommend screen (layout read only; nothing copied, DEC-006).
**Wireframes:** `Docs/Assets/UX/ux_00_flow.svg` … `ux_09_feedback.svg` (1920×1080 + annotation strip). Regenerate with `python -I Docs/Assets/UX/gen_wireframes.py Docs/Assets/UX`.

Design rules that are DES-001's call are marked **[DES?]** and collected in §9.

---

## 1. Principles

1. **Complex backend, simple floor** (MASTER_PLAN §4.2). The default results view is the tool's Floor Mode (C§13, T#50): 3 cards, no bars, no numbers but price and grams. Chemistry is one deliberate action away (Inspect).
2. **Decision support, not autopilot** (spec §14). The player chooses intents from what they heard; the engine never sees the NPC's hidden intent unless the "Auto-fill intent" assist is on.
3. **Evidence is labelled** (MASTER_PLAN §4.3). Every block in Detail carries OBSERVED / INFERRED / HEURISTIC. No "% correct" anywhere (spec §51).
4. **Diegetic first** (spec §27, §98). HUD is one small cluster; patience is body language, not a bar.
5. **One verb** (spec §62). Interact (E / Ⓐ) opens NPC dialogue, the terminal and the POS. Back (Esc / Ⓑ) always steps back one screen.

## 2. Flow (ux_00)

| # | Step | Screen | Wireframe | Exit |
|---|---|---|---|---|
| 1 | Approach customer | HUD + "Talk" prompt | ux_01 | Interact → 2 |
| 2 | Hear request | Dialogue | ux_02 | Ask question (≤3, [DES?]) · "Look it up" → 3 |
| 3 | Query | Terminal › Query | ux_03 | Search → 4 · Back → 2 |
| 4 | Results | Terminal › Results (rush view) | ux_04 | Inspect → 5 · Compare (2–3 marked) → 6 · Choose → 7 · More options · Edit search → 3 |
| 5 | Inspect | Terminal › Detail | ux_05 | Choose → 7 · Back → 4 |
| 6 | Compare | Terminal › Compare | ux_06 | Choose → 7 · Back → 4 |
| 7 | Present / response | Dialogue (presented state) | ux_07 | ACCEPT → 8 · ASK_* → 4 with refine · REJECT/LEAVE → leaves |
| 8 | POS confirm | POS | ux_08 | Hold-confirm → 9 · Cancel → 7 (reservation released, spec §67) |
| 9 | Feedback | Toast + HUD tick | ux_09 | auto, 4 s |

- Patience (spec §27) keeps running in steps 2–8. If it runs out, the customer leaves from any step; the open screen closes, any reservation is released, and a ⚠ toast shows.
- The physical deli/scale step (spec §20, §66) is outside this spec. The UX assumes the weight is picked on the POS; if DES-001 puts weighing before the POS, the POS weight row becomes read-only **[DES?]**.

## 3. Screens

Terminal presentation: screen-space overlay panel 1600×900 centred, world dimmed 55 %, camera and movement locked while open. (A diegetic render-texture version is a polish task, not slice.) The **request strip** (customer's line(s) verbatim + archetype hint) is pinned at the top of every terminal screen: this is the §46 "persistent intent summary" assist and is on by default.

### 3.1 HUD (ux_01)
Top-right cluster in the safe area: shift clock (game time, 26 px), shift sales $ (22 px), queue count (22 px). Centre dot crosshair. Contextual interact prompt bottom-centre only when a target is in reach. Hidden while terminal or POS is open. Optional assist "Patience hints": a word + icon over queued NPCs (Relaxed / Waiting / Impatient).

### 3.2 Dialogue (ux_02, ux_07)
Subtitle box bottom-centre (1200 px, speaker 18 px, line 28 px, ≤2 lines). Options column right, numbered 1–5. Options: "Look it up" (default focus) + the clarifying questions of spec §49; asked ones grey out. Presented state (ux_07) pins a "Presented: name · weight · price" card top-left and swaps the options to the set for the response state (spec §17).

### 3.3 Terminal › Query (ux_03)
- **Intent tiles** (6, multi-select): Sleep, Pain, Anxiety / calm, Energy, Focus, Social: the slice intent families (spec §9, §87). Each maps to one `INTENTS` key (slice skips the NL parser, MIG-001 handoff item 4). Multi-select merges per C§2 step 9 (crit = max, neg = min, primary = highest threshold) **[DES?] mapping**.
- **Budget** stepper (off, $5 steps) → `opts.maxPrice` (C§2 price intent, C§9 filter).
- **Stay functional** toggle → `neg.sedation = 42` (C§2 step 7 cap value) **[DES?]**.
- Avoid-terpene and First-time are shown disabled with "next wave" (exclusions T#13, new-customer profile T#28 are not in the slice subset). Free-text search is hidden in the slice.

### 3.4 Terminal › Results, rush view (ux_04)
Up to 3 cards (`resultCount 3`), left → right in rank order; card 1 has an accent edge. Card face: rank, strain name, sub-line (brand · tier label · total terps), role tag, fit label, price for 3.5 g tax-incl., grams in jar, one "why" line, anxiety chip, buttons Inspect / Compare / Choose.
- **Fit label** (spec §51): strict pass → "✓ Good fit"; relaxed fallback (C§9 Fallback) → "◐ Possible fit" + banner "No exact match. Closest available." "Strong fit" is not used until DES-001 gives a rule **[DES?]**.
- **None** (fallback also empty): "Nothing matched." with Edit search; no cards.
- **More options** reruns with n = 40 and appends the next 3 unseen (C§9, T#38); cards scroll horizontally, focus stays.
- Out-of-stock is never shown (C§8). Grams come from the simulation's jar stock, not the engine.

### 3.5 Terminal › Detail (ux_05)
Left: domain bars for 5 domains (antimicrobial never shown, C§3), cluster label, anxiety level, `buildScript` line, the tool's caveat sentence rewritten in game voice. Right: batch facts (code, COA date + age, tier, brand, total terps, grams), top 3 terpenes of the averaged in-stock profile, the 4 weight prices. Bars keep the 2–99 display and its saturation at 99 for parity (GAP-208, T#17).

### 3.6 Terminal › Compare (ux_06)
2–3 columns, only: price 3.5 g, type (cluster), anxiety level, the key-difference domain value, batch age. Header sentence = key difference (C§11: largest display gap of the 5 shown domains; "notably" when ≥10). Compare runs the engine compare on the marked groups; it does not re-rank.

### 3.7 POS confirm (ux_08)
Panel 1000×840. Item + batch; weight tiles 3.5 / 7 / 14 / 28 (`STD_WEIGHTS`, disabled when jar grams < weight); lines MSRP, day deal (if any), subtotal, tax 25.1 %, total (36 px). Tax line = total − subtotal so the floor-to-$0.05 rule (C§12) always adds up on screen. Payment Cash / Card (abstract, spec §24–25). **Hold-to-confirm** 0.6 s by default; Cancel releases the reservation.

### 3.8 Feedback (ux_09)
Non-blocking toast top-left, 4 s, never takes focus: "✓ Sale · name · weight", "+$ · jar g before → after", customer line. Reject/leave toasts use ⚠ + warning colour. HUD sales updates once. No satisfaction numbers.

## 4. Input and focus

| Action | Keyboard / mouse | Controller |
|---|---|---|
| Interact / activate focused | E (world), Enter / Space (UI), click | Ⓐ |
| Back / close | Esc | Ⓑ |
| Move focus | arrows, Tab / Shift-Tab, hover | D-pad / left stick |
| Next / prev card | ← → | LB / RB |
| Inspect focused card | I | Ⓨ |
| Toggle compare mark | C | Ⓧ |
| More options | M | RS click |
| Edit search | Backspace | LS click |
| Dialogue option n | 1–5 | D-pad + Ⓐ |

Focus order per screen is the pink numbers in each wireframe. Default focus: Dialogue → "Look it up"; Query → first tile; Results → card 1 Choose; Detail → Choose; Compare → column 1 Choose; POS → weight 3.5 g. Back restores the previous screen's focus. Focus ring: 4 px accent outline + 1.04 scale (scale off under reduced motion). Every element is reachable without a mouse.

## 5. Layout, type and safe area

- Reference 1920×1080; PanelSettings **Scale With Screen Size**, match 0.5. Title-safe 90 %: 96 px left/right, 54 px top/bottom; nothing interactive outside it.
- Type scale at 100 %: Title 36 · H1 28 · Body 22 · Secondary 18 (minimum) · Price/total 36. Min hit target 56 px tall.
- Text scale setting 100 / 125 / 150 %: the root gets `.text-125` / `.text-150`, which override the `--fs-*` variables. At 150 % cards keep their row but grow to the panel height; names ellipsize with the full name in Detail; the "why" line wraps to 2 lines max.

## 6. Colour and status (colour-blind safe)

Okabe-Ito based; status never relies on colour alone (always icon + word).

| Token | Hex | Use |
|---|---|---|
| `--ok` | #56B4E9 | ✓ Good fit, ✓ Low anxiety, in stock, sale toast |
| `--warn` | #E69F00 | ⚠ Moderate anxiety, ◐ Possible fit, fallback banner, leave toast |
| `--bad` | #D55E00 | ✗ High anxiety, errors |
| `--accent` | #009E73 | focus ring, primary button, selected tile |
| `--bg / --panel / --card / --line` | #15181c / #1d2127 / #262b33 / #3a414c | surfaces |
| `--t1 / --t2 / --t3` | #f2f4f7 / #c3c9d2 / #8f98a5 | text (t3 ≥ 4.5:1 on panel) |

High-contrast setting (later): swaps t2/t3 to t1 and lines to #8f98a5.

## 7. Accessibility (spec §46)

| Setting | Default | Effect |
|---|---|---|
| Text scale | 100 % | 100 / 125 / 150 % (§5) |
| Subtitles | on | dialogue box; speaker label |
| Persistent intent summary | on | request strip on all terminal screens |
| Auto-fill intent | off | pre-selects the NPC's emitted `INTENTS` key on Query |
| Recommendation explanations | on | "why" line on cards; off hides it |
| Patience hints | off | word + icon over queued NPCs |
| Slower patience / reduced rush | off | sim multipliers (DES-001 values) |
| Reduced motion | follows OS, else off | no slides/scales; ≤150 ms fades or instant; no money count-up; no shake |
| Hold actions | Hold | Hold ↔ Press for POS confirm (the only hold action in the slice) |
| Interaction highlighting | on | outline on the reachable target |

## 8. UI Toolkit structure and bindings

### 8.1 Documents and files (`Assets/_Project/UI/` suggested, GAME-002 decides)
| UIDocument (sort order) | UXML | Sub-templates | USS |
|---|---|---|---|
| Hud (0) | `Hud.uxml` | `InteractPrompt.uxml` | `Theme.uss`, `Hud.uss` |
| Dialogue (10) | `Dialogue.uxml` | `DialogueOption.uxml`, `PresentedCard.uxml` | `Theme.uss`, `Dialogue.uss` |
| Terminal (20) | `Terminal.uxml` (root `#terminal`, child panels `#query`, `#results`, `#detail`, `#compare`; one visible) | `RequestStrip.uxml`, `IntentTile.uxml`, `StrainCard.uxml`, `DomainBar.uxml`, `CompareColumn.uxml` | `Theme.uss`, `Terminal.uss` |
| Pos (30) | `Pos.uxml` | `WeightTile.uxml`, `PriceLine.uxml` | `Theme.uss`, `Pos.uss` |
| Toast (40) | `Toast.uxml` | — | `Theme.uss`, `Toast.uss` |

`Theme.uss` holds every token in §5–6 as `--*` variables. Root classes: `.text-125`, `.text-150`, `.reduced-motion`, `.hide-why`. Status classes: `.st-ok`, `.st-warn`, `.st-bad`. Card states: `.is-top`, `.is-focused`, `.is-marked`, `.is-fallback`.

### 8.2 Engine-bound fields
Names are the v7.11.4 identifiers in the contract; GAME-002 maps them to GAME-001's C# names.

| Element | Field (source) | Contract |
|---|---|---|
| Intent tile → query | `INTENTS[key]` → `crit`, `neg`, `primary`, `lbl` | C§2 step 9 |
| Budget stepper | `opts.maxPrice` | C§2 price intent, C§9 |
| Stay functional | `neg.sedation` (cap 42) | C§2 step 7 |
| Results list | `findStrains(...)` top N groups, n = 3 (`resultCount`) | C§9, C§1 prefs |
| Fit label / banner | fallback flag from `respond` (strict / relaxed / none) | C§9 Fallback |
| Card name, group id | group `name`, `groupKey` (`normName`) | C§7, C§2 |
| Card sub-line | rep batch `brand`, `tier` (label), averaged `total` | C§1 |
| Role tag | `buildRoleTags` → role per card | C§9 Role tags |
| Why line | first sentence of `buildScript` (cluster text) | C§9 Card copy |
| Anxiety chip / Detail anxiety | `calcAnxietyRisk` → `_anxLevel` (low / moderate / high) | C§6 |
| Price 3.5 g, Detail prices, POS lines | `getEffectivePrices(rep)` per `STD_WEIGHTS`, MSRP, matched deal, `applyTax` | C§12 |
| Domain bars | `scoreDomains(avgProfile)` display_d for sedation, uplift, anxiety_relief, pain_inflammation, focus_cognitive | C§3 |
| Type (cluster) | `classifyCluster(...).primary` → `CL` label | C§5 |
| Top terpenes | `averageProfile` (in-stock, 8-week half-life), top 3 by % | C§7 |
| Batch code, COA date, age | rep `batch`, `date`, `analyzeGroup` `weeksOld` | C§1, C§7 |
| Stock visibility | `batchInStock(rep)` (OOS never listed) | C§8 |
| Compare header | compare key-difference domain, winner, "notably" (gap ≥10) | C§11 |
| More options | `findStrains` n = 40, next 3 unseen | C§9 |
| Drive notice line | drive notice (when the customer mentions driving) | C§2 |

Never bound to UI: `ms`, `scoreRaw`, `CLUSTER_BONUS`, tier nudge, antimicrobial.

### 8.3 Simulation-bound fields (not engine; owned by GAME-002 / DES-001)
`shift.clockGameTime`, `shift.salesTotal`, `queue.count`, `customer.patienceState` (assist only), `customer.archetype`, `customer.visitCount`, `customer.requestLines[]`, `customer.responseState` (spec §17), `dialogue.questionsLeft`, `jar.gramsInStock` (per batch), `transaction.{weight, payment, reservationId}`, `toast.*`.

## 9. Questions for DES-001
1. Intent tile → `INTENTS` key mapping for the 6 tiles; and is "Social" one key or a merge?
2. Does the player pick intents (interpretation skill) with Auto-fill as an assist, as this spec assumes?
3. Fit label rule: is strict = Good / relaxed = Possible enough, or define "Strong fit" (e.g. on `ms` margin)?
4. Clarifying questions: limit (spec assumes 3) and time/patience cost per question.
5. Is "Stay functional" a player toggle (`neg.sedation 42`) or only an NPC-revealed constraint?
6. Weight: chosen on the POS (this spec) or at the scale before the POS? Does the customer state a weight?
7. ASK_CHEAPER / ASK_STRONGER / ASK_LESS_SEDATING / ASK_SIMILAR: the exact refine each applies (budget step, crit/neg deltas; Similar is next wave).
8. Does presenting a card other than #1 have any score effect?
9. Which weekday does the slice shift run on (day deals change every price shown)?
10. HUD money = shift sales total (this spec) or drawer cash?
11. Outcome language on the feedback toast: words only, which set?

## 10. Validation
- Every flow step in §2 has a wireframe: ux_01–ux_09 (+ ux_00 flow). ✔
- Every engine-bound field in §8.2 names a contract section; simulation fields are listed separately in §8.3, not claimed as engine outputs. ✔
- Prices in wireframes are computed from C§12 (Tuesday deals, floor to $0.05): house 3.5 g $14.00 → $10.50 → $13.10; premium 3.5 g $17.50; smalls 3.5 g $8.75; house 7/14/28 g $26.25 / $52.50 / $71.25. Strain names, grams, bar values and text are placeholders, not inventory.
- Each SVG ≤ 500 KB (largest ≈ 12 KB).
