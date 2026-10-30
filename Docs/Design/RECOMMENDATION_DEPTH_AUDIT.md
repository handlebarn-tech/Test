# RECOMMENDATION_DEPTH_AUDIT — PS1b vs the TFS budtender tool (DES-006)

**Owner:** DES-006 · **Consumers:** GAME-017..020 (amended in place), Gameplay lead · **Status:** for review · 2026-10-30
**Problem (DEC-096 #4):** a sale today is "choose one effect, choose one strain, done". This audit checks PS1b against the tool's real workflow and says what to change.

**Sources.** Tool = `C:/Users/handl/Downloads/tfs-budtender/dev/v7114/tool.html` (v7.11.4 source, DEC-002), cited `T:<line>`. Game code under `UnityProject/Assets/_Game/Code/`, cited by file:line. Spec = `Docs/Design/SPEC_DECISION_PRESSURE.md` (DP§n), `Docs/Specs/UX_COUNTER_INTEL.md` (UX§n). No PII, no product names, no inventory values are copied here; strain references are runtime slots (`{strain}`) filled from the game catalog.

## 1. Root cause in one paragraph
The ported engine already holds most of the tool's depth (parser with ~284 intent keys `T:15619-15974`, phrase synonyms `T:16095-16161`, negation patterns `T:16063-16094`, conflict resolution `T:16195-16210`, fuzzy fallback `T:16223-16235`, exclusions, price intent, like-X, compare, similar, refine). The game uses almost none of it. `ShiftSim.Search` calls `Recommender.Recommend` with one of 6 fixed intent families (`Simulation/Slice/ShiftSim.cs:136-146`, `:505-506`); no file in `Simulation/` or `Presentation/` calls `QueryParser`, `Responder`, `Refine` or `Similarity`. Customers are generated from the same 6 families and their line contains exactly one parser keyword (`Data/Slice/SliceIntents.json` `_doc`; `Customers.cs:68`). So the player maps one keyword to one tile. PS1b as written adds questions and workflows, but its query composer still turns structured KNOWN fields into wording by itself (GAME-017 Deliverable 5, UX§4). That means the game does the interpreting, not the player. The tool's own follow-up step (Refine chips) is in no packet.

## 2. Audit table

Ported = in `Code/Domain/Engine/`. Exposed = reachable by the player in today's slice. Gap severity: **H** = keeps "one effect, one strain", **M** = loses a real tool step, **L** = polish / later.

| # | TFS tool capability (file:line) | Ported? | Exposed today? | PS1b coverage (before DES-006) | Gap |
|---|---|---|---|---|---|
| 1 | Free-text search box: "Type what the customer needs: effect, condition, or budget" `T:1552-1559`, `handleSend` `T:19520`, `submit` `T:19542-19548` | yes: `QueryParser.Parse`, `Responder.Ask` (`Features/Responder.cs:64`) | **no**: 6 tiles straight into `Recommender.Recommend` (`ShiftSim.cs:505`) | GAME-017 D5 composer: KNOWN fields → wording → parser; no free typing (UX§4) | **H**: the composer writes the wording, so the player never interprets anything |
| 2 | Intent vocabulary: ~284 keys incl. vague/colloquial ("chill", "wound up", "in a funk", "first timer") `T:15619-15974`; phrase map `T:16095-16161` | yes (`Parser/ParserTables.cs`, `QueryParser.cs`) | no | GAME-017 KNOWN fields: Effect/Also/Avoid/Stay functional/Budget/Time (UX§3) | **H**: needs are still drawn from 6 families; the vocabulary that makes phrasing matter is unused |
| 3 | Negation/modifiers: "without couch lock", "stay functional", "gotta work", "not too heavy", "won't make me paranoid" `T:16063-16094`; "sleep but gotta work" stays sleep `T:16085-16086`; conflict resolution `T:16195-16210` | yes | no | GAME-017 tokens "avoid", "stay functional" | M: covered only as structured tokens, not as the customer's own phrasing |
| 4 | Wrong-term handling: indica/sativa/hybrid → relaxing/energizing/balanced in the fuzzy fallback `T:16227-16229`; "good" → mood boost `T:16234`; anything unparsed → Help "Try: …" `T:16677` | yes (`ResponseOutcome.Help`) | no | none | **H**: "wrong term" customers cannot exist |
| 5 | Customer-language training ("what they say vs what they mean, and what to say back"): 7 decode cards, each with example phrasings, meaning, a script and **follow-up questions** `T:2196-2319` (body `T:2200-2216`, functional `T:2218-2233`, potency redirect `T:2235-2250`, balanced `T:2252-2267`, symptom `T:2269-2284`, creative `T:2286-2302`, aroma `T:2304-2319`) | n/a (training content) | no | DP§6 openers, DP§9 Q1–Q8 | **H**: the tool itself defines the interpretation step and its follow-ups; PS1b has no utterance styles and lacks the "anxious before / how experienced" follow-up (`T:2263-2264`, `T:2297-2298`) |
| 6 | Price intent: `detectPriceIntent` `T:21744-21758`, `PRICE_INTENTS` `T:21696`; budget → `maxPrice` `T:16632`; budget-only → "What effect are they looking for?" `T:16662-16667`; price-only lowest prices `T:16595-16612` | yes (`QueryParser.DetectPriceIntent` `:424`, `Responder.PriceOnly`, `AskEffectForBudget` `Responder.cs:40`) | no (budget only feeds `PriceFit`, `ShiftSim.cs:420`) | GAME-017 budget token | M: the tool's budget prompts are not shown anywhere |
| 7 | Terpene exclusions "no/without/avoid/…-free X" `T:15975-15999`; hard filter + note `T:16633-16635` | yes (`Features/Exclusions.cs`, `QueryParser.ExtractExclusions`) | no | GAME-017 "Avoid" chip (domain or terpene undefined) | M: undefined whether Avoid becomes a negation phrase or a terpene exclusion |
| 8 | Strain lookup "do you have X?" incl. out-of-stock nearest list `T:16541-16554` | yes (`Responder.StrainLookup`, `Near`) | no | none | M: the "product reference" utterance has no route |
| 9 | "Like X (but more Y / but no Z)" → `likeKey` + exclude X `T:16018`, `T:16047-16050`, `findStrains` `T:15357` | yes (`FindOptions.LikeKey`) | no | none | M |
| 10 | Compare: text "compare A vs B" (≤3) `T:16043`, `T:16046`, Compare panel `T:19470-19518`, output `T:16556-16563` | yes (`Responder.CompareStrains`) | no | GAME-018 Compare | covered |
| 11 | Similar tab: liked strains (≤4) → blended cosine, top 6 in stock `T:1970-1983`, `T:20778-20788`, `T:20824-20866` | yes (`Features/Similarity.cs:32`) | no | GAME-018 Similar | covered |
| 12 | **Refine follow-up chips** after every recommend result: 11 structured edits `T:19583-19595`, `refineSearch` `T:19596-19610`, chip choice by result `buildFollowUpChips` `T:19612-19641` | `Refine.Apply` yes (`Features/Refine.cs:21`); **chip selection not ported** | no | none (GAME-018 only lists `Refine` under Read) | **H**: this is the tool's own follow-up loop ("something lighter", "keep it functional", "lower anxiety risk") |
| 13 | New / Experienced customer toggle `T:1585-1589`, `setCustomerProfile` `T:14810`; New = anxiety-risk filter + onset sort `T:14827-14845` | yes (`ShopState.NewCustomer`, `Recommender.cs:151`, `:159`) | no | GAME-017 TRUE `Experience`, no route to the engine | M: an input the real budtender sets after asking |
| 14 | Tier chips + "{tier} only" refine `T:1572-1582`, `toggleTier` `T:18614`, `setTierAndRerun` `T:19643-19648` | yes (`ShopState.ActiveTiers`, `PassesTierChips` `Recommender.cs:101`) | no | none | L: defer (pricing tiers come with PS2 price work) |
| 15 | Show more options: n=40 rerun, tf re-sort, next 3 `T:19442-19460` | yes (`Responder.MoreOptions` `:166`) | yes, but the game reimplements it via `Recommend(n)` (`ShiftSim.cs:149-157`) | none | L: switch to `Responder.MoreOptions` once the parser route is live (parity) |
| 16 | Result card: role tag ("Most functional", "Lowest anxiety"…) and why line `T:16253-16264`, `T:16382-16469` | yes (`Features/RoleTags.cs`, `Responder.RoleTags` shown only when Ok, `Responder.cs:39`) | no (`SliceView.cs:12` "no … role tag or why line") | UX§0 lists "why line … as today" | M: the tool's reasons for choosing *between* cards are hidden, so card 1 is the only sensible pick |
| 17 | Fallback "no exact match, closest" `T:16638-16645`; nothing-matched guidance `T:16647-16656` | yes | partly (banner, `SliceView.cs:238-239`) | — | L |
| 18 | Details modal `T:16513-16521` | card data yes | yes (Inspect) | GAME-018 Details | covered |
| 19 | Drive notice `T:19545`, `T:19557` | yes (`ParsedQuery.Drive`) | no | none | L: show the tool's line when a story says "driving after" |
| 20 | Terpene rank quick tools `T:19433-19440`, `T:16565-16592` | yes | no | none | L (expert customers, later) |
| 21 | Recent searches `T:20961-20995`, pinned panel `T:14900-14930` | no (UI only) | no | none | L |

**Summary.** The 6 rows marked **H** (1, 2, 4, 5, 12, plus the composer half of 3) are why a sale stays shallow even after GAME-020. Similar, Compare and Details are covered well.

## 3. How customers express needs

### 3.1 TRUE need = canonical tool wording, not a family
Each customer gets a **need** from a new data file `Data/Slice/SliceNeeds.json`: `trueQuery` (wording in the tool's own vocabulary, e.g. an effect plus a modifier plus an optional budget). Its parse is captured as a golden from v7.11.4 with `ParserOptions.Game` by extending `Tools/Data/golden_game003.js` (DEC-014/016 pattern). We never hand-write a parse. `TrueFamily` stays as the need's base family so existing code and goldens keep working. The DEC-052 evaluation oracle then grades against the parse of `trueQuery`, so a richer truth needs no new formula. Each need has 1–4 **components** (effect, modifier, avoid, budget, time, experience, reference). Each component has spoken variants per style and 2–3 **terms** (tool wording). One term reproduces the component; the others are plausible readings with a different, legitimate parse.

### 3.2 Utterance styles
Customer lines are customer speech and pass copy rule H1 (no effect claims). The examples below are [GDD] placeholders written for this doc, not tool copy.

| Style | What the customer does | Example (component) | Parser reality (why it matters) | Typical tier (DP§7) |
|---|---|---|---|---|
| Direct | says tool vocabulary | "Something for sleep, nothing that makes me anxious, under forty." | parses as said; the "said" phrase is the term | 0–1 |
| Vague | a colloquial word | "Something chill." / "What's good?" | "chill" is an INTENTS key (relaxing); "good" should fall to mood boost in the fuzzy fallback `T:16234` (the golden decides). Searching their words is legal and returns a real but maybe wrong answer | 2–3 |
| Wrong term | strain-type or potency talk | "Your heaviest indica." / "Highest THC you've got." | indica → relaxing `T:16227`; potency has no effect parse, so the tool redirects to the effect goal (`T:2235-2250`) → the player should ask Q1 | 2–3 |
| Story | a situation, no keyword | "Double shift tomorrow, I need to crash tonight but can't be dragging at six." | mixes sleep with a work cap; the tool keeps it a sleep ask `T:16085-16086`; the player picks terms | 1–2 |
| Product reference | names a strain | "Got anything like {strain}?" / "Do you have {strain}?" | like-X route `T:16047-16050` or Similar `T:20824`; lookup with nearest-in-stock if out `T:16541-16554` | 1–2 |
| "What I had last time" | names nothing | "Whatever I got last time, it was good." | no tool route without a name: Q6 reveals `{strain}` (or GAME-021 memory/history later) → Similar / like-X | 2–3 |
| Contradictory | conflicting wants | "Really relaxing, but I can't get sleepy." | the tool's conflict resolution `T:16195-16210` decides; the player chooses which term leads | 4 |

`{strain}` is always drawn at runtime from the game's catalog (in or out of stock as the scenario needs). Never from text in the data file.

### 3.3 From words to a query: recommendation
**Composed phrase cards, not free typing (PS1b).** Every customer statement (opener clause, question answer, ASK_* line) becomes a **said card** in the KNOWN strip. It holds the verbatim words plus a source glyph (UX§3). Before searching, the player gives each card a reading with **"Note it as…"**: `Their words` (the verbatim phrase goes to the parser) or one of the component's 2–3 terms. Direct phrases are already terms and skip the picker. The query preview (UX§4) shows the joined text exactly as `QueryParser.Parse` receives it. The engine route is `QueryParser.Parse(ParserOptions.Game)` → `Responder.Respond`, and the UI shows every tool outcome (Ok, Fallback, None, Help, AskEffectForBudget, PriceOnly, Strain + Near, ExclusionNote, Drive).

Why this and not free text:
1. **It keeps the tool's essence.** The tool is natural-language first (`T:1559`). Picking between their words and a budtender translation is exactly what the decode cards teach (`T:2196-2319`).
2. **It is gateable.** Every word in the query traces to something the customer said or to a translation of it. QA-002's input gate stays meaningful. With free typing the player could type a full query ("sleep, functional, no anxiety, under 40") every time and skip questions, which is the DP§18 autopilot again.
3. **It is deterministic and testable.** Every term's parse is golden-captured, so there is no typo or spelling variance, and it works on controller.
4. **Mistakes come from the player.** A wrong reading gives a legitimately different TFS result (DP§0A allowed list: "what natural-language query … reaches the TFS recommendation logic"). Nothing is reranked.

Free typing stays a later PC/expert option (question Q2 in the handoff). Chip tiles stay as the quick path, and chip-only queries must equal the DEC-017 goldens (DEC-057).

### 3.4 Follow-ups: three loops, all from the tool
1. **Player questions** (DP§9, UX§2) plus one new question **Q9 "Ever gotten anxious from it?"**. It covers the tool's repeated follow-up on anxiety history and experience (`T:2263-2264`, `T:2297-2298`). It reveals Experience/anxiety-prone and enables the **New customer** toggle (row 13), so the engine gets `ShopState.NewCustomer` exactly as the tool's button sets it.
2. **Customer ASK_* lines** after a presented card (GAME-019, DP§27), spoken in a style too ("Is that gonna knock me out?"). They become new said cards.
3. **Refine** (row 12): after an Ok/Fallback recommend result, the tool's own refine options run `Refine.Apply` → `Responder.Respond`. Until the chip selection is ported (blocker B1 in the handoff), refine is done by re-composing with the new card. That is still a legitimate parser input.

### 3.5 Tie to the KNOWN profile (GAME-017)
`KnownField` adds `said` (verbatim, list) and `term` (the player's chosen reading, null until set). `isKnown` = said exists. The KNOWN chip shows `"{said}" → {term}`. Completeness (DP§15) counts known fields. A new gameplay-only `InterpretationMatch` (term parse vs component parse) is evaluation-only (DEC-052), never shown on a card, and feeds regret (GAME-019) as "misread" separately from "didn't ask".

## 4. Packet amendments (applied)
All four packets now carry a `## DES-006 amendments` block. Short version:
- **GAME-017:** need catalog + golden capture; utterance styles; said/term KNOWN fields; Note-it-as picker; composer joins the player's chosen terms; parser + Responder route with every tool outcome shown; Q9 + New-customer toggle; Avoid split into negation phrase vs terpene exclusion; new tests (wrong reading, verbatim search, Help redirect); Phase A = first-playable cut (§5).
- **GAME-018:** Refine loop (B1 placeholder); like-X search and strain lookup + Near; role tags + why line on cards; `Responder.MoreOptions`; counters for refine/lookup.
- **GAME-019:** oracle = parse of `trueQuery`; ASK_* lines mapped to the tool step they invite; "misread" regret term; resolutions include re-reading, refine and lookup.
- **GAME-020:** record said/term pairs, verbatim vs translated, refine keys, profile toggle; explanation names the misread; `ShallowSaleRate` (DEC-096 KPI) in log, debug panel and persona targets.
None edits `Code/Domain/` (DEC-001). Gate A (DEC-067) stays on every PR; the new goldens are additive.

## 5. First playable depth (playtest 2 cut)
**Goal:** the smallest change after which a sale needs *hear → interpret → (ask) → search the tool's way → read the cards → react to a follow-up*. No scoring, report or V2 machinery.

**In:**
1. `SliceNeeds.json`: 12 needs = the 6 DEC-017 families × 2 modifiers drawn from parser vocabulary (e.g. functional/daytime, avoid anxiety/first-timer, budget). Each need has the direct, vague, wrong-term and story styles, plus product reference for 2 needs. 2–3 terms per component. Goldens for every `trueQuery` and every term composition.
2. Generator: pick need + style on its **own RNG stream** (existing draws and seeded jar fills unchanged). Tier-0 direct customers say today's line.
3. KNOWN strip (said cards), Note-it-as picker, query preview, Search via `QueryParser.Parse(Game)` → `Responder.Respond`, tool outcome texts. Tiles kept as the quick path.
4. Questions Q1, Q2, Q3, Q4, Q8, Q9 with a flat [GDD] time cost and one answer line each. No tolerance/friction, completeness or risk (GAME-017 proper).
5. One follow-up loop: on reject, the customer's line names the unmet component (ASK_LESS_SEDATING / ASK_CHEAPER / ASK_STRONGER as lines only) and adds a said card. The player re-reads and re-searches.
6. `ShiftSim.Fit` gains an overload on the parsed `trueQuery` (same Ms/Ms_top formula, `ShiftSim.cs:436-449`); the satisfaction formula is unchanged.
7. Tests: composed query result == `Responder.Ask` on the same text; chip-only == DEC-017 golden; correct-term composition parse == `trueQuery` golden; a seeded wrong-reading scenario scores a lower Fit; seed determinism; persona bots (the perfect bot asks and reads, a tiles-only bot loses satisfaction on tier ≥ 2).

**Out (stay in GAME-017..020):** tolerance/deflection, completeness/risk, CUSTOMER INFO tag, Similar/Compare/Details timing, Refine menu, no-sale, ServiceEvaluator, report v2, debug panel, V2 additions.

**Owns (proposed packet GAME-017a, cut from GAME-017):** `Simulation/Slice/Customers.cs`, `Simulation/Slice/ShiftSim.cs` (Search/MoreOptions route, Fit overload), `Simulation/Slice/SliceData.cs` (load needs), new `Simulation/Slice/CustomerKnowledge.cs` (minimal said/term KNOWN; GAME-017 extends it), `Presentation/Slice/SliceGame.cs`, `Presentation/Slice/SliceView.cs`, new `Data/Slice/SliceNeeds.json`, `SliceLines.json` / `SliceConfig.json` (new keys only), `Tests/EditMode/Slice/` (new tests + `SlicePersonaTests.cs` bots), `Tools/Data/golden_game003.js` (add the needs cases) → new `Docs/Reconstruction/golden_cases_needs.json`, `Docs/Handoffs/GAME-017a.md`. No `Code/Domain/` edits. Depends on QA-002b's Gate A pass with `ParserOptions.Game` (DEC-067) before merge, and on the same merges GAME-017 waits for. UX: a one-frame addendum for the picker and said cards (UX-005 owner).
