# DISPENSARY GAME — UNITY MIGRATION PLAN
## Existing Budtender/Terpene System → Modular Unity/C# Game Architecture

**Version:** 1.0  
**Date:** 2026-10-29  
**Parent:** `MASTER_PLAN.md`  
**Primary live behavioral reference:** https://tfs-phx-budtender.netlify.app/ (observed v7.11.4)  
**Captured live reference:** `References/LIVE_TFS_BUDTENDER_v7.11.4.md`  
**Historical source record:** `References/Review_Budtender_Tool_Comprehensive_Chat_Record.md`

---

# 1. Purpose

This document is loaded by migration/gameplay/data workers, not by every agent.

It defines how to carry forward the useful behavior of the existing budtender/terpene project into Unity without blindly copying its browser-era implementation or obsolete product decisions.

The supplied historical/current-state record is the **primary reconstruction source** because the original Three.js/browser repository is not available to Claude Code/Codex in this handoff.

It is not a verbatim source-code export, so numeric formulas and undocumented v8 details must not be invented as historical facts. Instead, agents should reconstruct documented behavior faithfully and make any missing implementation choices explicit, configurable, and testable.

---

# 2. What the project record actually proves

The record describes a v7.3.0-era system with three major surfaces:

1. recommendation engine;
2. inventory/pricing/product intelligence;
3. CRM/staff analytics.

It also records a later redesign and references a later build called **Terpene Tool v8 - Claude**.

Therefore:

- v7.3.0 is a well-described historical implementation state;
- later target requirements are documented;
- exact v8/current-code behavior remains to be verified in the actual source.

---


# 2A. Live v7.11.4 corrections to the historical baseline

The public deployment currently identifies as **v7.11.4** and provides newer direct evidence than the v7.3.0 historical snapshot.

Unity reconstruction should treat these as current behavioral targets:

- 281 search patterns understood;
- six named domains:
  - Euphoria / Uplift
  - Calm / Sedation
  - Energy
  - Focus / Cognitive
  - Pain / Anti-inflammatory
  - Anxiety Relief
- natural-language modifiers and negations;
- Floor Mode;
- current-stock/OOS exclusion;
- New vs Experienced customer context;
- Similar using cosine similarity;
- tier/budget behavior;
- pricing/tax/day-deal/strain-override concepts;
- five COA lab formats;
- shared-store mode plus local fallback;
- accessibility controls.

The live app explicitly describes the domain score as a **matching heuristic, not a pharmacological model**. Preserve that framing.

See:
`References/LIVE_TFS_BUDTENDER_v7.11.4.md`

# 3. Mandatory reconstruction preflight

Before writing Unity replacements, MIG-001 must convert the project record into a **behavioral reconstruction contract**.

Produce:

```text
ReconstructionContract/
  FEATURE_MATRIX.csv
  IMPLEMENTED_VS_TARGET.md
  DATA_MODEL.md
  RECOMMENDATION_BEHAVIOR.md
  PRICING_BEHAVIOR.md
  FEEDBACK_MODEL.md
  UI_FLOWS.md
  KNOWN_DEFECTS_TO_FIX.md
  UNRESOLVED_DETAILS.md
  GOLDEN_CASES.json
```

The contract must answer, using only supported documentation:

- What v7.3.0 materially included?
- Which later requirements supersede v7.3.0 behavior?
- Which systems are canonical for Unity?
- Which historical systems are deliberately dropped?
- Which known defects must not be reproduced?
- Which details are genuinely unknown because source code is unavailable?
- What configurable Unity implementation will stand in for those unknowns?

The project record itself documents approximately 1,207 batches, 367 normalized strains, 80 active/in-stock at review time, 111 terpenes, six domains, and five lab formats. It also documents natural-language recommendation, similarity, pricing, Floor Mode, COA ingestion, reporting, accounts and later architecture changes. Use those facts; do not embellish them.

# 4. Porting philosophy

## 4.1 Reconstruct behavior, not browser syntax

Bad approach:

```text
JavaScript class → mechanically translated C# class
DOM screen → copied into Unity UI
Three.js scene → imported as one giant scene
localStorage → random Unity PlayerPrefs
```

Correct approach:

```text
Extract documented domain behavior
→ specify inputs/outputs
→ mark unsupported numeric details as configurable
→ create synthetic/golden tests from documented examples/invariants
→ implement clean C# domain module
→ verify against the reconstruction contract
→ connect to Unity presentation
```

## 4.2 Pure domain assemblies

Recommendation/pricing/catalog code should live in C# assemblies that do not require active Unity scenes.

Suggested boundaries:

```text
Game.Domain.Cannabis
Game.Domain.Recommendation
Game.Domain.Pricing
Game.Domain.Inventory
Game.Domain.Feedback
Game.Simulation
Game.Presentation
Game.Tools
```

The exact assembly names may change, but the dependency direction should remain clean.

---

# 5. Feature migration matrix

| Historical/current feature | Port disposition | Unity direction |
|---|---|---|
| Natural-language intent handling | **PRESERVE / REIMPLEMENT** | Pure C# parser/normalizer with regression cases |
| Inventory-only recommendation | **PRESERVE** | Hard domain invariant |
| Terpene database | **PRESERVE AS DATA** | Deterministic imported dataset |
| Multi-terpene interaction logic | **PRESERVE WITH AUDIT** | Preprocess large source data; test outputs |
| Effect/domain scoring | **PRESERVE WITH CALIBRATION** | Pure C# scoring configuration |
| BA scalars/correction | **PRESERVE WITH AUDIT** | Keep only if current source uses it; test |
| Current-batch preference | **PRESERVE/FIX** | First-class batch candidate model |
| Historical-batch averaging | **FIX / REPLACE** | Never allow stale averages to masquerade as current chemistry |
| Newer-batch weighting | **PRESERVE IF IMPLEMENTED / ADD IF CANONICAL** | Explicit versioned weighting configuration |
| Similar tab / cosine similarity | **PRESERVE** | Pure vector similarity service |
| Comparison | **PRESERVE** | Game UI over same domain data |
| Floor Mode | **PRESERVE UX PRINCIPLE** | Fast player/budtender interaction mode |
| Pricing tiers | **PRESERVE** | Game economy/pricing service |
| Weight pricing | **PRESERVE** | Deterministic pricing rules |
| Deals/day rules | **PRESERVE IF SOURCE GAME USES** | Data-driven modifier system |
| Tax handling | **PRESERVE IF GAME USES** | Data-driven transaction calculation |
| Strain price overrides | **PRESERVE** | Override table |
| COA parser | **EDITOR/TOOL FIRST** | Keep outside runtime unless gameplay requires actual import |
| Five lab parsers | **AUDIT / TOOL** | Port only verified/needed formats |
| Stock status | **PRESERVE/FIX** | Authoritative simulation inventory |
| Manual Sold log | **TRANSLATE** | Game event/telemetry, not separate truth |
| Search logs | **TRANSLATE** | Optional game analytics |
| Stats/reports | **DEFER/PRESERVE SELECTIVELY** | Player/manager screens only if gameplay uses them |
| Customer profiles/PII | **DROP** | NPC state uses game IDs, no real PII |
| Customer visits | **REMODEL** | Game NPC/history only if needed |
| Anonymous feedback | **PRESERVE CONCEPT** | Structured simulation outcome system |
| Batch-aware feedback | **PRESERVE** | Link feedback to recommendation + batch |
| Learned weighting | **DEFER UNTIL BASE PARITY** | Separate from scientific/base score |
| Admin/Manager/Budtender auth | **DROP AS REAL AUTH** | Roles may exist as game concepts, not security layer |
| Owner role / permissions matrix | **DROP OR DEFER** | Only if game simulation explicitly needs management permissions |
| Supabase RLS | **DO NOT PORT BY DEFAULT** | Local private game does not need operational web RLS |
| Account lockout | **DROP** | Historical web security issue, not game mechanic |
| Multi-location shared batch catalog | **DEFER** | Design data model to allow later expansion |
| Location-specific stock | **PRESERVE DATA CONCEPT** | Current location inventory is authoritative |
| Report email distribution | **DROP/DEFER** | Not part of core private game |
| Corporate approval workflow | **ARCHIVE CONTEXT ONLY** | Not runtime game logic |

---

# 6. Recommendation engine migration

## 6.1 Canonical inputs

At minimum:

```text
customer/player-entered intent
active location
available batches
batch terpene vector
domain/effect configuration
pricing/value constraints
explicit modifiers
```

Potential modifiers from the historical UX:

- sleep;
- anxiety/low-anxiety preference;
- pain;
- focus;
- energy;
- social;
- appetite if still canonical;
- no couch lock;
- strong;
- affordable;
- functional;
- flavorful.

Actual vocabulary must be extracted from the current source.

## 6.2 Candidate generation

Hard invariant:

```text
recommendable candidate ⊆ currently available inventory
```

No generic strain knowledge may introduce a product absent from simulation inventory.

## 6.3 Batch model

Recommended:

```csharp
Strain
  id
  normalizedName

Batch
  id
  strainId
  testDate
  terpeneVector
  brand
  tier
  coaMetadata

LocationStock
  locationId
  batchId
  quantity
  availability
  localPriceOverride
```

The current location’s available batch is what the player actually sells.

## 6.4 Scoring decomposition

Keep scoring explainable and separable:

```text
base chemistry/domain score
+ intent fit
+ modifier fit
+ optional value/price factor
+ optional learned signal
= final ranking
```

Do not collapse all sources into one opaque number.

## 6.5 Evidence labels

Recommendation rationale can internally tag reasons as:

```text
Observed
Heuristic
Learned
Inferred
```

This makes later tuning safer.

---

# 7. Large terpene-interaction dataset

The historical project references roughly nine million lines of interaction data.

The project record states that the historical recommendation concept used a dataset of approximately nine million lines and multi-terpene interactions up to roughly five-way combinations. The original raw dataset is not assumed to be present.

Therefore:

1. search the handoff folder for the interaction dataset or derived data files;
2. if present, build a deterministic preprocessing pipeline;
3. if absent, create a **data-provider interface** and a documented placeholder configuration rather than fabricating nine million interactions;
4. preserve the intended principle that effects emerge from terpene combinations rather than simplistic one-terpene stereotypes;
5. keep all scoring coefficients/configuration externalized so real data can replace placeholders later.

Do not claim exact parity with unavailable source data.

---

# 8. Golden regression cases

Because the browser source is unavailable, create a representative **behavioral test corpus from documented examples, invariants and edge cases**.

Each case should include:

```json
{
  "input": {
    "intent": "...",
    "location": "...",
    "inventorySnapshot": "..."
  },
  "expectedBehavior": {
    "mustExcludeOutOfStock": true,
    "mustPreferCurrentBatch": true,
    "expectedCandidateSet": ["..."],
    "notes": "Exact historical numeric score unavailable unless data is supplied."
  },
  "notes": "..."
}
```

Required coverage:

- common intents;
- multiple modifiers;
- no valid candidate;
- one valid candidate;
- near-tie candidates;
- same strain, multiple batches;
- historical versus current batch;
- budget constraint;
- similarity lookup;
- comparison;
- out-of-stock exclusion;
- terpene exclusion;
- unusual terpene vector;
- old batch edge case.

Known bugs get explicit regression tests whose desired Unity behavior intentionally follows the later documented architecture rather than the defective historical behavior.

---

# 9. Scientific-language correction

Historical review identified false-precision risk, especially around:

- anxiety;
- sedation;
- beginner friendliness;
- individual terpene causal claims.

The game may present richer fictionalized simulation feedback, but if it uses the real recommendation logic, UI language should preserve calibration.

Preferred patterns:

- “may lean toward…”
- “higher relative fit for…”
- “profile is more consistent with…”
- “based on this profile…”

Avoid presenting a heuristic score as clinical truth.

---

# 10. Similarity system

The historical system used cosine similarity for “I liked X; what is similar?”

Port as a pure service:

```text
input profile
→ normalized terpene vector
→ eligible current batches
→ cosine similarity
→ ranked alternatives
→ shared-terpene explanation
```

Tests must confirm:

- empty vectors;
- missing terpenes;
- normalization;
- identical profiles;
- near-zero overlap;
- out-of-stock filtering.

---

# 11. Pricing engine

Audit and port:

- tier prices;
- weight-based pricing;
- per-strain overrides;
- day/deal rules;
- tax;
- tax-included behavior if present.

Recommended architecture:

```text
BasePricePolicy
DealPolicy
OverridePolicy
TaxPolicy
TransactionPriceService
```

Pricing should be deterministic and unit-tested independently of UI.

---

# 12. COA parser disposition

The v7.3.0 record describes coordinate-based extraction and five lab-format families.

For the Unity game:

## Phase 1
Keep COA parsing as **offline/editor tooling** if existing data is already normalized.

Reason:
PDF parsing and external lab-format maintenance should not block the playable game.

## Phase 2
Port parsers only if the game has a mechanic where the player imports/processes COAs or if continuing real dataset maintenance requires them.

Parser output should target the same canonical `Batch` schema.

---

# 13. Feedback / learning system

Historical target:

```text
requested goal
→ recommendation
→ exact batch
→ sale/no sale
→ outcome dimensions
```

For the game, this can become a powerful simulation system.

Recommended schema:

```text
FeedbackEvent
  id
  gameCustomerId
  requestedIntent
  batchId
  recommendationScoreSnapshot
  purchaseOutcome
  effectRatings
  wouldChooseAgain
  timestamp/gameDay
```

No real customer identity.

Learned signals should be a **separate feature layer**, not silently alter the base scientific/heuristic rules.

---

# 14. Inventory system

Inventory becomes authoritative game state.

Suggested layers:

```text
Catalog
  definitions

BatchInventory
  physical sellable stock

DisplayInventory
  jar/shelf visual projection

BackstockInventory
  cases/totes

TransactionLedger
  game events
```

A transaction should update one authoritative inventory model. Visuals listen to that state.

No manual “Sold” flag should exist as a separate truth source.

---

# 15. Visual inventory integration

The migration is incomplete until stock state affects scene state.

Example:

```text
Batch B-101:
  backstock = 448 g
  deliJar = 61 g
  salesThisDay = 37 g
```

Scene can derive:

- jar fill;
- number of cases;
- tote/shelf state;
- restock task availability.

The Asset Plan defines how the visuals are generated.

---

# 16. Customer-intent integration

The recommendation engine can become part of the game loop rather than a separate utility.

Potential architecture:

```text
NPC Customer
→ IntentProfile
→ dialogue/player questioning
→ player-selected interpretation/modifiers
→ RecommendationEngine
→ recommended inventory candidates
→ player choice
→ customer acceptance model
→ sale/outcome
```

The source game must be audited before finalizing the exact dialogue/interaction flow.

---

# 17. Floor Mode in Unity

Preserve the historical principle:

**rush interaction should be faster than deep consultation.**

Unity implementation can expose:

### Floor / Rush view
- intent;
- 3 strong options;
- price;
- short reason;
- availability;
- fast select.

### Detailed view
- terpene profile;
- domain reasoning;
- similarity;
- alternatives;
- confidence detail.

Do not rebuild the clutter that the original review rejected.

---

# 18. Browser UI → Unity UI mapping

Do not reproduce browser DOM structure.

Map workflows:

| Browser/tool concept | Unity destination |
|---|---|
| Search/intent entry | player tablet/POS panel/in-world UI |
| Recommendation cards | reusable UI prefab |
| Similar | dedicated panel/action |
| Compare | side-by-side panel |
| Floor Mode | compact UI state |
| Pricing | transaction/POS UI |
| Inventory | manager/backoffice UI if gameplay needs it |
| Stats | optional management screen |
| COA import | editor/tooling unless gameplay requires it |

Use UI Toolkit or uGUI based on implementation preference; choose once during bootstrap and record the decision.

---

# 19. Supabase disposition

The historical application used Supabase direction for shared operational data.

For this private local game, default architecture should **not require Supabase**.

Reasons:

- unnecessary network dependency;
- unnecessary auth/RLS complexity;
- fragile offline behavior;
- operational security concerns irrelevant to single-player simulation.

If cloud sync is later desired, add it behind a repository interface.

Example:

```csharp
IInventoryRepository
IGameSaveRepository
ICatalogRepository
```

Local implementations come first.

---

# 20. Local persistence

Recommended:

- versioned save file;
- explicit schema version;
- migrations between save versions;
- no critical game state in PlayerPrefs;
- atomic save/backup;
- deterministic IDs.

Static content and save data are separate.

---

# 21. Legacy localStorage / JSON migration

The record documents browser-local storage and JSON export/import in earlier phases, but the exact save schema is not provided.

Therefore:
- do not block the Unity build on legacy-save compatibility;
- define a clean versioned Unity save schema;
- if a real legacy export is later supplied, add one-way import tooling then.

---

# 22. Three.js scene reconstruction without source access

The original Three.js scene is not available in this handoff.

The Unity environment therefore uses:

1. the supplied floor plan for geometry;
2. the supplied CCTV composite for placement/density/visual language;
3. public visual references already captured in the Asset Plan;
4. the project-history record for gameplay/product behavior.

Do not invent a claim that Unity preserves exact Three.js object placement.

If the old Three.js source is added later:
- compare measurements/transforms;
- migrate any validated placements that improve fidelity;
- do not replace a more accurate floor-plan reconstruction merely because the old browser scene differed.

# 23. Coordinate/scale contract

Unity:

```text
1 unit = 1 meter
Y up
```

Create a documented transform if legacy Three.js coordinates differ.

Every imported legacy placement should be converted through one deterministic mapping rather than manually eyeballed.

---

# 24. Scene migration order

1. measured shell;
2. validated doors/openings;
3. major fixtures;
4. player controller;
5. interaction anchors;
6. gameplay systems;
7. free/custom asset replacement;
8. lighting;
9. NPCs;
10. audio/polish.

Gameplay should be testable in graybox before final art.

---

# 25. Recommended C# domain model

Illustrative, not final code:

```text
TerpeneDefinition
TerpeneVector
EffectDomain
IntentProfile
StrainDefinition
BatchDefinition
LocationDefinition
StockRecord
PriceTier
DealRule
RecommendationCandidate
RecommendationResult
FeedbackEvent
Transaction
```

Use stable IDs and data importers.

---

# 26. Data validation

Build validators for:

- duplicate strain IDs;
- duplicate batch IDs;
- batch without strain;
- invalid terpene values;
- unknown terpene keys;
- non-finite values;
- missing test dates where required;
- stock pointing to unknown batch;
- price rule missing tier;
- active stock with no chemistry if recommendation requires chemistry.

Fail loudly during import.

---

# 27. Recommended tests

## Unit
- similarity;
- pricing;
- tax;
- intent modifiers;
- batch filtering;
- current-batch preference;
- data validation.

## Golden
- legacy recommendation outputs;
- known-bug corrected outputs.

## Integration
- recommendation + inventory;
- transaction + stock;
- jar fill + stock;
- shelf population + stock.

## Play mode
- customer transaction;
- restock;
- save/load;
- scene transition.

---

# 28. Known legacy defects to turn into tests

- stale historical average influences current recommendation;
- out-of-stock candidate appears;
- unsupported certainty language;
- single-terpene beginner rule;
- manual sold event treated as inventory truth;
- duplicate/normalized strain ambiguity;
- feedback lacking batch/intent link.

---

# 29. Multi-location

The data model should not prevent multiple locations, but initial game scope should not pay the complexity cost unless the source game already uses it.

Design:

```text
BatchDefinition = shared
LocationStock = per location
PriceOverride = optional per location
```

That preserves the historical desired architecture without forcing multiple playable stores into milestone 1.

---

# 30. Operational auth/security history

The historical web product had real security concerns:

- account lockout;
- RLS;
- roles;
- customer PII;
- server-authoritative auth.

For the private game port:

**archive these as historical context. Do not spend migration time recreating them unless they become game mechanics or future online functionality.**

This is intentional scope reduction.

---

# 31. Analytics / reports

Classify after source audit.

Potential game value:

- daily sales;
- customer intents;
- recommendation acceptance;
- stockouts;
- effect-domain demand;
- staff/player performance.

Do not port enterprise-style reporting merely because it existed.

---

# 32. Migration tasks

Recommended work breakdown:

### MIG-001 Current source audit
### MIG-002 Legacy runtime capture / golden cases
### DATA-001 Canonical cannabis data schema
### DATA-002 Legacy dataset importer
### GAME-001 Recommendation domain skeleton
### GAME-002 Intent parser
### GAME-003 Batch/current-stock candidate filter
### GAME-004 Recommendation scorer
### GAME-005 Similarity
### GAME-006 Pricing
### GAME-007 Inventory
### GAME-008 Transaction ledger
### GAME-009 Feedback/outcome model
### UI-001 Floor Mode
### UI-002 Detail/compare/similar
### TOOL-001 COA importer disposition
### QA-001 Recommendation parity suite
### QA-002 Save/inventory integration suite

Each is a separate bounded task/workcell when practical.

---

# 33. Migration milestone acceptance

The domain migration is complete when:

- current source behavior is documented;
- canonical data imports deterministically;
- golden cases exist;
- all intended-preserve systems have C# equivalents;
- known defects have corrected tests;
- inventory is authoritative;
- no customer PII is required;
- source game saves can be imported if needed;
- Unity can run recommendation logic without browser code;
- UI can consume domain results;
- basic transaction changes inventory;
- save/load preserves the resulting state.

---

# 34. What not to do

Do not:

- port HTML/CSS into Unity;
- use a browser view as the permanent core UI;
- copy monolithic JS structure into one massive MonoBehaviour;
- make every domain class inherit MonoBehaviour;
- store all data in scene objects;
- use PlayerPrefs for core saves;
- keep raw nine-million-line data in runtime text assets;
- restore customer PII;
- rebuild real auth before core gameplay;
- call manual game events “POS truth”;
- claim exact parity before tests.

---

# 35. First migration session prompt

```markdown
You are MIG-001.

Objective:
Turn the supplied budtender-tool project record into a precise Unity reconstruction contract. The original Three.js/browser source is NOT available.

Read:
- Docs/MASTER_PLAN.md
- Docs/UNITY_MIGRATION_PLAN.md
- References/LIVE_TFS_BUDTENDER_v7.11.4.md
- References/Review_Budtender_Tool_Comprehensive_Chat_Record.md

If network access is available, inspect:
https://tfs-phx-budtender.netlify.app/

Do not wait for unavailable source code.
Do not invent undocumented v8 features or exact historical scoring coefficients.

Produce:
- v7.3.0 implemented-feature matrix
- later-target architecture matrix
- preserve/fix/reimplement/defer/drop classification
- canonical data model
- documented recommendation behavior
- documented pricing behavior
- known defects that Unity must correct
- unresolved details that need configurable Unity decisions
- synthetic/golden tests derived from documented invariants and examples

Write a concise handoff and stop.
```

---

# 36. Final migration rule

> The Unity port is a controlled reimplementation of the project’s valuable behavior, not a translation of its historical browser architecture.

The correct endpoint is a modular game whose recommendation and inventory systems can be tested independently, whose visuals reflect simulation state, and whose code can be maintained by many fresh agent sessions without reconstructing years of chat history.
