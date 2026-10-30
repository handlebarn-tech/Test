# REVIEW-W2B — DES-001 + UX-001 + ASSET-001

**Reviewer:** REVIEW (docs) · 2026-10-29 · **Branch:** `review/wave-2b`
**Merged (`--no-ff`, no conflicts):** `claude/task-des-001-635c15` (incl. reconcile 64f5fbb), `claude/task-ux-001-1115a2`, `claude/task-asset-001-9856c0`. `git merge-tree` against current `main` (dcd3b88, GAME-001 already merged) is clean.

## Verdict: **GO with notes**
GAME-002 can be written with no open design questions. Two engine gaps (S1 live stock, S2 labels) are already GAME-002 sub-tasks and need the Hub's routing before the build starts. The three real-store facts are now answered (DEC-019..021) and cited. With 454 g jars the sold-out state is effectively unreachable in the slice (n7), which needs a DES/Hub call.

## 1. DES-001 ↔ UX-001 ↔ GAME-001
- **UX_SLICE §9 questions:** all 11 answered in SLICE_DESIGN §10, plus the other conflicts (patience, budget stepper, Compare, Detail, More options, role tags, reservation, payment, request strip). §10 states it rules where the docs differ. ✔
- **Engine names:** every name in SLICE_DESIGN §6 and the GAME-002 draft checked against `Catalog.cs`, `Recommender.cs`, `Scoring.cs`, `Pricing.cs` (GAME-001, identical on `main`): `Catalog.Load`, `Groups()`, `StrainGroup.Key/Batches`, `Batch.Id/Brand/BatchCode/TestDate/Total/InStock`, `cat.Intents`, `IntentQuery{Crit,Neg,Primary,Label}`, `ShopState{ResultCount,ActiveTiers,NewCustomer,EmptyTierCountsAsHouse}`, `Recommender.Recommend/FindStrains`, `RecommendResult.Outcome/Strains`, `Outcome.Ok/Fallback/None`, `StrainResult.Name/Tier/Ms/Cluster/AnxietyRisk/Domains/Profile`, `EngineConstants.FallbackCritFactor/FallbackCapAdd/DisplayMax`, `Pricing.GetEffectivePrices(...).Prices[g]`, `Pricing.ApplyTax`, `PriceTables.TaxRate`. All exist. ✔ `ResultCount = int.MaxValue` is safe (`Take`). The relaxed transform in §6 matches `Recommend` line for line.
- **S1 claim confirmed:** `Groups()` caches its in-stock-first order and `FindStrains` skips a group whose `Batches[0]` is OOS, so selling out the rep hides a strain that still has stock. `AverageProfile` filters `InStock` live, so only the order is stale. Still open on `main` (no `SetInStock`/`InvalidateGroups`).
- **Bound fields:** UX §8.2 uses v7.11.4 names; SLICE_DESIGN §6 maps each kept one. Fields UX binds that the slice cuts (budget stepper, Stay functional, role tag, why line, Compare, drive notice, `visitCount`, `questionsLeft`, `reservationId`) are cut in §9/§10.
- **Gap found (fixed in doc):** the card's "tier label" has no engine source: `StrainResult.Tier` is an id (`smalls`, `t3`) and labels live in `tierLabels2` L16463. Folded into sub-task S2 (SLICE_DESIGN §6 gap 2, GAME-002 S2).

## 2. Source discipline (8+ [SRC] spot-checks, tool v7.11.4 `index.html`, read-only)
| Cite | Claim | Result |
|---|---|---|
| L15620 | `sleep` sedation 38, pri sedation | ✔ |
| L16107 | insomnia PHRASE_MAP 55/40 (INTENTS key = 45/35) | ✔ both |
| L15464 | in-stock-first batch sort | ✔ |
| L16377 | `_anxLevel` <38 low, <55 mod, else high | ✔ |
| L16638-16645 | relaxed retry ×0.60 floor, caps +12 ≤99; "No exact match… Closest available" | ✔ |
| L19442-19452 | More options: n=40, next 3 unseen | ✔ |
| L21010 / L21018 / L21036 | `STD_WEIGHTS`, `TIER_DEFAULTS`, `DEFAULT_DAY_DEALS` | ✔ |
| L21062 / L21123 / L21134 | tax 25.1, floor to $0.05, `applyTax` | ✔ |
| L17517 | `_prefs.resultCount` | ✗ off by 2: the default is L17519 (L17517 is `_invSort`). Fixed in SLICE_DESIGN §8. GAME-001's `ShopState` comment has the same drift (not ours to edit) |

- **Goldens:** the six §2.2 rows equal `golden_cases.json` → `parsed` for RC-01/03/04/09/10/11 exactly. ✔
- **Prices:** Tue deals = smalls/house/premium/t1/fttp ✔. Smalls 3.5 g list $13.10, deal $8.75; house deal $13.10; premium $17.50; house 7/14/28 g $26.25/$52.50/$71.25 post-tax: all recomputed ✔. 35 in-stock smalls, 77 in-stock batches ✔ (snapshot).
- **No invented store facts:** draw weights, archetypes and budgets are tagged [GDD] and disclaimed. The 3 open store facts were flagged in the DES-001 handoff; Nolan has since answered them (DEC-019 454 g jars, DEC-020 deli only, DEC-021 scale at the register) and SLICE_DESIGN/GAME-002 now cite them. ✔
- **Line-safety rule:** rendered every opener × core × weight × budget against the 287 INTENTS keys: no key other than the family's own. ✔

## 3. Constants
SliceConfig §8 covers every number used in §1-§5 and §10. Sanity rows recomputed: 0.60+0.25+0.15 = 1.00 → 100 ✔; 0.25+0.15 = 0.40 → 40 < 50 REJECT ✔; 0.12+0.40 = 0.52 → 52 ≥ 50 ACCEPT ✔.

## 4. ASSET-001 (8 rows re-verified 2026-10-29, nothing downloaded)
| Row | Checked via | Result |
|---|---|---|
| PH-CashRegister_01 | Poly Haven API | Joe Seabuhr, 9,927 tris, CC0 ✔ |
| PH-hand_truck | Poly Haven API | Mutanzom3D, 13,220 tris ✔ |
| PH-kloofendal_overcast_puresky | Poly Haven API | Greg Zaal, HDRI ✔ |
| SK-c9f6e2 | Sketchfab API | CC Attribution, Meowdeler, 1,992 tris, downloadable ✔ |
| SK-938a9b | Sketchfab API | CC Attribution, anfang, 1,074 tris, downloadable ✔ |
| LIB-KEN-IF | kenney.nl page | CC0, 100 files ✔ |
| AUD-BSB | bigsoundbank page | "Subway Door Bell #1", Joseph SARDIN, CC0/WTFPL/PD ✔ |
| FNT-BAR | google/fonts OFL.txt | OFL 1.1, © 2017 The Barlow Project Authors, no RFN ✔ |

Poly Haven license page states CC0. No asset binaries in the merged diff (only `.md`, `.svg`, `.py`). Redistribution flags are consistent: CC0 committable; Sonniss, Quaternius and Unity Asset Store kept out of the repo (`ThirdParty/`, gitignored); Sketchfab CC-BY needs attribution and the import-time provenance check.

## 5. Hygiene
No PII (email/phone/customer-name scan clean). No tfs-budtender content copied: only line numbers and short identifiers. SVGs 2-12 KB (≤ 500 KB limit); no PNGs.

## Notes (non-blocking)
- **n1 Stale UX artefacts.** UX_SLICE §2-§3 and wireframes ux_02/03/04/06 still show Focus/Social tiles, multi-select, questions, Compare, budget stepper, role tag/why line. SLICE_DESIGN §10 rules, so GAME-002 is unblocked; a short UX-001 touch-up (or a banner on UX_SLICE) would stop builders misreading them.
- **n2 Accessibility rows not covered.** UX §7 "Slower patience / reduced rush (DES-001 values)" has no SliceConfig keys, and "Recommendation explanations" toggles a cut line. Recommend: hide both in the slice.
- **n3 Patience words differ:** DES Calm/Impatient/Leaving vs UX hint Relaxed/Waiting/Impatient. Pick one in GAME-002 (DES states, UX words is fine).
- **n4 Core-line wording.** §2.6 says cores use the tool's "regression wording", but RC-03/04/09/10/11 queries are bare (`stress relief`, `pain`…). The cores contain them, and no parser runs in the slice, so this is harmless.
- **n5 Hub routing.** S1 (live stock) and S2 (cluster + tier labels) touch `Code/Domain/`; GAME-003 is also editing Domain. Route them before GAME-002 starts.
- **n6 DES-001 handoff** "Needs from GAME-001" still lists pre-ENGINE.md proposals; its follow-up section supersedes them.

- **n7 Sold-out state is effectively unreachable (DEC-019).** With 454 g jars, the worst case is 12 customers × 28 g = 336 g, all on one jar, which still leaves 118 g (26 %, above `lowStockFraction` 0.25). Neither LOW nor SOLD OUT can occur in the slice, and the "batch at 0 g" and S1 rep-sell-out paths are reachable only in EditMode tests. If the slice must *show* these states, it needs a design tweak, e.g. some jars start partly full via a [GDD] `startFillFraction` (per batch or a seeded few). That is a DES-001 / Hub decision; I did not redesign it. GAME-002 tests should still drive 0 g directly through `InventoryService`.

## Fixes made on this branch
- SLICE_DESIGN §8: `resultCount` cite L17517 → L17519.
- SLICE_DESIGN §6 gap 2 + GAME-002 S2: add tier display names (`tierLabels2` L16463).
- Hub update: SLICE_DESIGN §2.5, §4, §7, §8 and GAME-002 "Open inputs" now cite DEC-019 (454 g jars), DEC-020 (deli only) and DEC-021 (scale stand at the register, GAP-107) instead of placeholders. The DES-001 handoff's "Decisions for Nolan" list is left as a historical record.
