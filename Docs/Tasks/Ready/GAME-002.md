# GAME-002 — Vertical-slice shift loop (DRAFT by DES-001; Hub finalizes)

**Role:** GAME (Unity gameplay) · **Priority:** P0 · **Depends on:** GAME-001 (engine + catalog), ART-001 (graybox + anchors), UX-001 (UI spec) merged to `main` · **Branch:** `task/GAME-002` worktree off `main`

## Goal
Make one playable shift (DEC-008) in the Retail graybox exactly as `Docs/Specs/SLICE_DESIGN.md` specifies: 12 customers, chip-based intent → real engine top 3 → pick → accept/reject → POS confirm → grams decrement → jar fill change → shift report.

## Read
- `Docs/Specs/SLICE_DESIGN.md` (all of it; it is the design authority for this task).
- `Docs/Specs/ENGINE.md` (GAME-001) and `Docs/Handoffs/GAME-001.md`.
- `Docs/Specs/UX_SLICE.md` (UX-001) for screens and bindings.
- `Docs/Assets/Specs/GRAYBOX.md` (ART-001) for anchor names.
- `Docs/Reconstruction/golden_cases.json` → `parsed` for RC-01/03/04/09/10/11.

## Owns (existing BUILD-001 asmdefs)
- `Assets/_Game/Code/Simulation/` (`Dispo.Simulation`): shift, customers, queue, inventory service, scoring, POS logic. Keep it Unity-free where practical so EditMode tests can cover it.
- `Assets/_Game/Code/Presentation/` (`Dispo.Presentation`): slice screens per UX_SLICE, NPC movement, jar visuals
- `Assets/_Game/Data/Slice/` (`SliceConfig` asset, `SliceIntents.json`, line templates)
- Slice-only edits in the Retail scene: anchors already placed by ART-001, jar spawner, NPC capsule
- Tests in `Assets/_Game/Code/Tests/EditMode/Slice/` and `.../PlayMode/Slice/`
Do not touch `Code/Domain/` (GAME-001) unless the Hub grants the sub-tasks below as a scoped Domain edit.

## Engine API (real names, `Dispo.Domain.Engine`; mapping in SLICE_DESIGN §6)
`Catalog.Load` · `IntentQuery` built from `SliceIntents.json` (not `Intents.Resolve`) · `Recommender.Recommend(cat, crit, neg, primary, ShopState)` → `RecommendResult{Outcome, Strains}` · `Recommender.FindStrains(...)` with `ResultCount = int.MaxValue` plus the relaxed transform via `EngineConstants.FallbackCritFactor/FallbackCapAdd/DisplayMax` (fit, §3.2) · `cat.Groups()` → `Batches[0]` for rep batch/brand · `Pricing.GetEffectivePrices(cat.Pricing, tier, dow).Prices[g]` → `Pricing.ApplyTax` · `cat.Intents.Keys` (line-safety test).

## Sub-tasks: API gaps (Hub routes them to GAME-001 or grants a scoped Domain edit)
- **S1 Live stock (blocking):** `Catalog.Groups()` caches its in-stock-first order, so flipping `Batch.InStock` at 0 g leaves a stale rep. Add `Catalog.SetInStock(batchId, bool)` that invalidates the cache. Test: sell out the rep of a multi-batch strain → the strain stays listed with the next batch as rep, and its profile is re-averaged. Re-run all slice goldens after.
- **S2 Cluster + tier labels (blocking for cards):** expose the `CL` label strings (L15107-15115) and the tier display names (`tierLabels2`, L16463), copied from source, as engine data or `Scoring.ClusterLabel(int)` / a tier-label lookup.
- **S3 (optional):** `StrainResult.RepBatchId`.

## Deliverable
1. `SliceConfig` with every key in SLICE_DESIGN §8; no gameplay literals in code.
2. `SliceIntents.json` (6 families, §2.2) plus line templates (§2.6).
3. Seeded customer generator (§2), queue + patience (§5), shift timeline and rush (§1).
4. Terminal flow (§3.1, with the UX resolutions in §10: single-select tiles, Inspect, More options, no Compare/ASK_*/questions/budget stepper) on `Recommender.Recommend` against live stock; fit/price/speed/satisfaction/response (§3.2–3.5).
5. `InventoryService` (single stock authority) + `Sell` event; jar fill/LOW/SOLD OUT visuals; POS confirm/cancel (§4).
6. End-of-shift report with every field in §1.
7. A debug overlay (dev builds only) showing each customer's true family, budget and computed fit, so QA can verify the scoring.

## Validation
- `studio.ps1 unity-compile`, `unity-test-edit`, `unity-test-play` all pass.
- EditMode tests:
  - each `SliceIntents.json` row equals the golden `parsed` for its RC id;
  - every rendered line passes the INTENTS-key safety rule (§2.6);
  - generator determinism (seed 1 twice → identical customer list);
  - scoring formula unit cases, including the three sanity rows in §8;
  - a sale decrements grams exactly once; cancel changes nothing; a batch at 0 g is never returned by `FindStrains`;
  - POS blocks a sale when grams < request;
  - post-tax prices match the golden `pricing` table for the shift day.
- PlayMode test: auto-play seed 1 with a bot that always picks card 1 for the true family. All 12 customers resolve, the report has no null fields, revenue = Σ sale events, and jar fill = grams/start for every sold batch.
- Capture: one screenshot per screen in the flow plus the report (`unity-capture`).

## Open inputs (from DES-001; Hub resolves before start)
- `startGramsPerBatch` = 28 g is a placeholder: no source has quantities.
- Every in-stock batch is treated as deli flower.
- The register-run service station is a layout choice (GAP-107).

## Handoff
`Docs/Handoffs/GAME-002.md` (≤40 lines). Report to the Studio Hub.
