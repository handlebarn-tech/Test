# REVIEW-IMP1 — independent check of the IMP-001 DESIGN_V2 audit

**Branch:** `review/imp-001` = `main` (cab9abf) + `--no-ff` merge of `claude/vigorous-sanderson-28a86a` (b4273b8, 849b6c4). The merge was clean and docs only.
**Pack:** `C:/Users/handl/Downloads/Dispo Game Imports/DISPO_GAME_DESIGN_V2/`. I read it in place with grep/sed only. Nothing was edited, and no `.py` was run.
**Canon checked:** DECISIONS through DEC-061, `GAMEPLAY_SIMULATION_SPEC.md`, `Design/SPEC_DECISION_PRESSURE.md` (DP), `Design/ROADMAP_POST_SLICE.md`, `Specs/UX_PS1.md`.

**Verdict: PASS with required amendments.** The audit is accurate where I checked it, and its verdicts are sound.
It was written against DES-003 *before* the ratification (DEC-052..061), so it misses two tool-parity points (A1, A2) and has two stale items (A3, A4).
- None of this blocks Nolan reading the summary.
- A1 and A2 must go into the integration plan before IMP-002 runs. I left the audit unchanged (owned by IMP-001); the amendments are recorded here for the Hub and IMP-002.

## 1. Spot-checks (18 rows + 2 caveats), all confirmed against the pack
| Row | Claim in the audit | Found in V2 | OK |
|---|---|---|---|
| 1/2 | v7.11.4 pin; "don't snapshot v7.11.5" | README l.9; 15 l.7, l.11, l.29 | ✓ (but see A1) |
| 5 | DecisionRecord + TFS input hash | 01 §4–5; `data_contracts.yaml` | ✓ (but see A2) |
| 12 | "no critical fact unknowable" | 02 l.209 | ✓ |
| 13 | Shares 22/24/14/16/14/10, 35 % cap | 02 l.72–81 | ✓ |
| 14 | Ambiguity 0..3 vs DP tier 4 "contradictory" | 02 l.45; DP l.549 | ✓ |
| 15 | Generator retry cap 12, degrade to SOLVABLE; solve "against store state" | 02 l.125, l.132 | ✓ |
| 16 | Hard budget + price-insensitive is invalid | 02 l.139 | ✓ |
| 20 | Rolling 20 / 50 customer windows | 02 l.237, l.246 | ✓ |
| 21 | Acceptance uses *known* hard constraints + the shown TFS tier | 02 §17 l.272–281 | ✓ (C3 stands) |
| 22 | 2-follow-up loop cap | 02 l.301 | ✓ |
| 23 | Repeat cap 10–20 % | 09 l.149 (the audit cites 02 §19; the source is 09) | ✓ |
| 25 | Standard 32 min, 18–20 arrivals; 26 / 35 min presets | 03 l.4, l.46, l.63 | ✓ |
| 26 | 60 s engagement-relief cap | 03 l.136 | ✓ |
| 30 | PressureBudget points | 04 l.48 | ✓ |
| 32 | `DQ = .40RQ + .30IS + .20QE + .10NSJ` vs DP regret form | 05 l.73; DP l.1159 | ✓ |
| 34 | Median of last 6; an identical seed gives no evidence | 05 l.146–151, l.286; DP l.2501 (0.8 EWMA) | ✓ |
| 35 | V2 "Trusted/Senior" SJ 70 vs DP Trusted SJ 60/55/50/70 | 05 l.8, l.155–160; DP l.2519–2527 | ✓ |
| 40 | `Tab` Floor Mode, `C` Compare | 08 l.25–26 | ✓ |
| 46 | Abstract fixtures `BAT-A` | `QA/qa_scenarios.json` l.10 … | ✓ |
| C11(a) | Nominal ≈ 21 arrivals vs sim 19.3 | 03 phase table: 0.24+2.7+5.76+1.2+6.48+2.7 = 19.08, + 2 specials = 21.1; `shift_queue_results.csv` standard 19.32 | ✓ |
| C11(c) | One z = 1.28 vs 06 service classes | `inventory_policy_stress.py` l.48; 06 l.82–84 | ✓ |

No row was wrong. One citation is off (row 23 → 09 §7, not 02 §19).

## 2. Required amendments (tool parity, DEC-001/002, DEC-052..061)
- **A1 (DEC-060, missed): V2's oracle pin is now stale.** V2 15 makes v7.11.4 the parity oracle and forbids v7.11.5 snapshots. Since DEC-060, Nolan wants the game to **ship the v7.11.5 fixes** (DEC-015 `EmptyTierCountsAsHouse=false`, DEC-016 parser fixes), with the v7.11.4 goldens kept as regression tests.
  - Rows 1 and 2 should be **ADAPT**, not COVERED: the oracle is the *shipped* engine (v7.11.4 + DEC-015/016). V2 15's capture procedure and "parity matrix" apply against that engine, and its "never snapshot v7.11.5" rule is dropped.
  - Headline 2 ("pins v7.11.4 (DEC-002)") should say the pin is superseded by DEC-060.
- **A2 (DEC-057, missed): V2's TFS input is structured, ours is wording.** V2's `TFSInputSnapshot` carries "known fact IDs/values + inventory snapshot + mode" (01 §4, `data_contracts.yaml`). DEC-057: the TFS query reaches the engine **only as known-fact wording through `QueryParser`**, and chip-only queries must equal the DEC-017 golden parses.
  - Row 5 / GAME-018/020 must define the snapshot as the **parser input** (query text + chip + inventory snapshot) and hash that, not a fact-ID list sent to the engine.
  - Otherwise V2 invites a second, structured path into the recommender, which is exactly what DEC-001/057 forbid.
  - This is the most important missed conflict.
- **A3 (DEC-052, note): counterfactual IS in the report.** Row 6 routes V2's counterfactual InformationSufficiency to the GAME-020 report. DEC-052 keeps oracle "evaluation" values out of player UI.
  - The report may say *which question would have mattered*, but must not show TFS scores, ranks or a re-run result list.
  - Add this to the GAME-019/020 acceptance.
- **A4 (stale):**
  - C10 is closed: DEC-061 (Nolan) confirms DEC-055, and an empty jar with backstock is a restock job. Drop the pending N2 question.
  - The audit's DEC-P1..P6 are now DEC-052..057 (P4 → DEC-055/061, P5 → DEC-056 25–40 min, which fits V2's 32 min).
  - The §5 prerequisite "W4Q merged; DEC-P1..P6 ratified" is met.

## 3. Other checks
- **No other parity conflicts found.**
  - V2 keeps hidden truth out of TFS (`invariants: hidden_customer_truth_never_enters_recommendation_service`) and calls acceptance "not recommendation science" (02 §17).
  - C3 and C6 already send judgement to the oracle (DEC-052).
  - DEC-053 (outcomes never touch TFS) matches V2 02 §20. DEC-054 is unaffected.
- **Store facts:** the audit's §4 list is complete. I grepped the pack for registers, security, loyalty, online/pre-order, medical and delivery: no store claims beyond those listed.
  - One modelling note for DES-004 (not a store question): V2's queue model is a **single server**. Canon has 11 numbered registers (DEC-039), with one used by the player in PS1. PS2 must state how many are open.
- **Handoff housekeeping:** the `.git/info/exclude` `Imports/` note is valid (Hub, outside IMP-001's scope).

## 4. Nolan-facing summary: accurate, with one sentence to add
The audit's §6 is accurate. It needs one addition for A1/A2, because V2 assumes the older tool version. Final text:

> Your V2 pack is a detailed, numbers-heavy version of the decision-pressure ideas we already took in from your spec (DES-003). It doesn't change how the budtender tool recommends strains, and it contains no customer data. Most of it fits plans we already have. What it adds: exact starting numbers for shift pacing, difficulty and promotions; rules that keep customers from feeling repetitive; and a list of 70 ways a player could game the system, each with a test.
> **What we'd use:** the customer-generation rules, the anti-cheese list (as a test plan), the queue and shift numbers for the full-shift milestone (PS2), the difficulty "pressure budget", the "did the player miss a question that mattered?" check, and the UX rules about never leaking hidden customer facts.
> **What we'd change:** where V2 and your earlier spec disagree (ambiguity levels, how decision quality is scored, how a customer judges a product), your earlier spec wins. V2 also assumes the older tool version (v7.11.4) and a structured way of feeding the tool. We'd keep your decision to ship the v7.11.5 fixes, and keep the tool fed only through its normal search wording. The one real choice is **how promotions work**: V2 uses "your typical result over the last 6 shifts", and the earlier spec uses "a running average". We recommend V2's way with gentler starting thresholds.
> **What waits:** ordering, suppliers, staff and manager play stay parked until the management milestone (PS4).
> **Nothing changes in the current milestone (PS1).**
> To approve: say "approve as recommended", or edit any line above. We'd also need short answers on storage areas, deliveries, expiry, staffing/breaks and job titles before PS2/PS4, not now.

## 5. For the Hub
- Accept IMP-001 with amendments A1–A4. IMP-002, when approved, applies them: rows 1/2/5/6, headline 2, C10 and the §5 prerequisite.
- D1 (promotion model) and D2 (DP precedence) stand as the audit proposes.
- Q0 (precedence) is still the only Nolan question needed before integration; the store questions wait for PS2/PS4.
