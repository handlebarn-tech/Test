# DISPENSARY GAME — MASTER PLAN
## Canonical Project Direction, Unity Target, Production Roadmap & Context Router

**Version:** 4.0  
**Date:** 2026-10-29  
**Status:** Canonical production plan  
**Third-party asset budget:** $0  
**Required software cost:** $0  
**Target engine:** Unity 6.3 LTS + HDRP *(superseded by DEC-003: the project uses Unity 6000.6.7f1 + HDRP 17.6.0)*  
**Use case:** private, non-commercial, at-home project  
**Execution model:** Hub → department leads → disposable workers (`STUDIO_OS.md` §0, DEC-094)

---

# 1. Purpose of this document

This is the **small, stable strategic document** for the project.

It is deliberately not the asset encyclopedia, migration notebook, or agent-operation manual. Those are separate documents so the Studio Hub does not repeatedly load tens of thousands of words that are irrelevant to its immediate decision.

The project documentation is split as follows:

| Document | Read by default? | Purpose |
|---|---|---|
| `MASTER_PLAN.md` | **Hub: yes** | Vision, constraints, architecture direction, milestones, canonical decisions |
| `UNITY_MIGRATION_PLAN.md` | No | Detailed legacy/current-system audit and Three.js/browser → Unity/C# port strategy |
| `ASSET_PRODUCTION_PLAN.md` | No | Free assets, room-by-room Bill of Assets, custom models, generators, art pipeline |
| `STUDIO_OS.md` | Hub/bootstrap: yes initially | Multi-agent operating model, worktrees, task packets, reviews, context lifecycle |
| `TOOLCHAIN_EXECUTION.md` | No | Exact Unity/Blender automation, build/test/render/evidence contract |
| `GAMEPLAY_SIMULATION_SPEC.md` | No | Core game loop, customers, transactions, shift simulation, progression |
| `AGENTS.md` | Codex: automatically/commonly read | Short repository map and durable rules |
| `CLAUDE.md` | Claude Code: automatically read | Short repository map and durable rules |

**Context rule:** agents start with the smallest document that can answer their task. They follow links/references to deeper documents only when required.

---

# 2. Project definition

The project is a **high-fidelity playable dispensary simulation** reconstructed around the supplied Phoenix dispensary references.

Two major bodies of prior work are being combined:

1. **The physical dispensary reconstruction**
   - supplied floor plan;
   - supplied 25-camera CCTV composite;
   - available public visual references;
   - room-by-room operational understanding.

2. **The existing budtender / terpene tool lineage**
   - natural-language customer-intent translation;
   - inventory-aware recommendation;
   - batch/COA data;
   - terpene/effect-domain scoring;
   - similarity;
   - pricing;
   - Floor Mode;
   - inventory/reporting concepts;
   - later governance redesign.

The Unity project should not feel like a generic cannabis store with a recommendation minigame bolted on. The objective is to make the real operating logic and physical environment reinforce each other.

---

# 3. Source-of-truth hierarchy

When sources disagree, use this order.

## 3.0 Local budtender tool source (DEC-001, added by AUDIT-001 C1)
For recommendation logic and existing implementation, the local TFS tool project at `C:/Users/handl/Downloads/tfs-budtender` is the **highest authority**, above the live site and the chat record (DEC-001); its v7.11.4 build is canonical (DEC-002) and equals the live site (DEC-009). Read-only, no PII (DEC-006). §3.1–3.3 below predate DEC-001 and are kept for context.

## 3.1 Live deployed budtender application
For recommendation/tool behavior, the public **TFS Budtender Tool v7.11.4** deployment is the strongest currently available behavioral reference:

https://tfs-phx-budtender.netlify.app/

Captured observations are stored in:
`References/LIVE_TFS_BUDTENDER_v7.11.4.md`

The live app outranks the older v7.3.0 snapshot when they conflict.

## 3.2 Explicit current project decisions
User-approved decisions in the current project documentation are authoritative.

## 3.3 Current-state project record
Because the original Three.js/browser project is **not available to the agent studio**, `References/Review_Budtender_Tool_Comprehensive_Chat_Record.md` is the canonical behavioral baseline for reconstruction.

It is detailed enough to define the known product goals, features, constraints, architecture history, implemented v7.3.0 capabilities, later requested architecture, and known defects. Where the record distinguishes implemented behavior from future intent, that distinction must be preserved.

If the original source is added later, source inspection becomes a verification pass rather than a prerequisite to beginning the port.

## 3.4 Explicit current project decisions
*(Same rule as §3.2, kept so section numbers stay stable; AUDIT-001 C1.)*
User-approved decisions in the current repository override historical behavior.

## 3.5 Floor plan
The measured/architectural floor-plan reference governs spatial layout where available.

## 3.6 CCTV / visual references
The camera composite governs object presence, density, operational condition and visual language.

## 3.7 Public reference imagery
Use to clarify visible façade/material/retail details, not to override measured geometry without evidence.

## 3.8 Conventional assumptions
Use only as temporary placeholders. Mark them as low confidence and keep them replaceable.

---

# 4. Canonical product heritage from the existing budtender tool

The attached project record establishes that the tool evolved into three overlapping systems by v7.3.0:

- recommendation engine;
- inventory/pricing/product-intelligence system;
- lightweight CRM/staff-analytics system.

The Unity project should **preserve the valuable domain logic, not every historical feature**.

## 4.1 Core value to preserve

The strongest product thesis is:

> Translate ordinary customer language into a small number of inventory-specific recommendations using current batch chemistry while hiding unnecessary complexity.

Conceptually:

```text
customer intent
→ weighted experience/effect domains
→ current batch candidates
→ recommendation scoring
→ small set of options
→ short rationale
→ transaction/gameplay consequence
```

## 4.2 Canonical UX principle

> **Complex backend, simple floor experience.**

A player/budtender should be able to make a decision quickly. Chemistry, batch weighting and scoring detail should be available but not forced into the primary flow.

## 4.3 Canonical evidence principle

The system distinguishes:

- **Observed** — COA chemistry, batch date, inventory record, explicit gameplay/feedback event.
- **Inferred** — predicted experience or similarity.
- **Heuristic** — thresholds and weighting rules.
- **Learned** — aggregated outcome/behavior signals.

An inference must never silently become an observed fact.

---

# 5. Current-state facts that matter to the port

The attached record provides a well-characterized **v7.3.0** snapshot and notes later project evolution.

Known v7.3.0-era capabilities include:

- browser application with local fallback;
- Supabase shared-data direction;
- user accounts and roles;
- inventory batch records;
- stock status;
- COA ingestion;
- five supported lab-format parser families;
- 111-terpene database;
- six effect/domain dimensions;
- BA-corrected contribution logic;
- freshness/age information;
- natural-language search;
- recommendation ranking;
- similar-strain matching via cosine similarity;
- comparison;
- Floor Mode;
- pricing/tax/tier/deal/override logic;
- brands;
- search/sold/activity logs;
- stats/reports;
- team/account controls.

The review dataset contained approximately:

- 1,207 batch records;
- 367 normalized strains;
- 80 active/in-stock at the time;
- 1,127 out-of-stock/historical records.

The record also notes a later current build referred to as **“Terpene Tool v8 - Claude”**, but it does not fully document that build’s exact implementation.

**Therefore the initial Unity port should reconstruct the documented v7.3.0 capabilities plus the explicitly documented later target architecture.**  
The later `Terpene Tool v8 - Claude` reference should be treated as evidence that additional implementation may have existed, but agents must not invent undocumented v8 features.

---

# 6. Historical behavior that should NOT be blindly ported

The later target architecture explicitly moved away from several v7.3.0-era behaviors.

Do not automatically preserve:

- customer profiles or customer PII;
- broad budtender mutation rights;
- historical-batch averaging that distorts current chemistry;
- unsupported beginner/myrcene rules;
- pseudo-clinical certainty in anxiety/effect scoring;
- manual “Sold” clicks as authoritative transaction truth;
- claims of live POS/Dutchie integration that do not exist;
- security/account-lockout behavior from the operational web system;
- monolithic HTML/JavaScript architecture.

For a private single-player game, real organizational authentication, corporate authorization and production RLS are **historical operational concerns**, not required runtime game systems unless intentionally simulated.

---

# 7. Canonical game-system direction

This section defines the architecture direction, not exact implementation details.

## 7.1 Domain layer
Pure C# logic with minimal Unity dependency:

- cannabis catalog;
- strains;
- batches;
- COA chemistry;
- terpene vectors;
- recommendation domains;
- intent parsing/normalization;
- recommendation scoring;
- similarity;
- pricing;
- inventory;
- feedback/outcome model.

This layer must be unit-testable without loading a Unity scene.

## 7.2 Simulation layer

Connect domain logic to the game:

- customer intent;
- customer/budtender interaction;
- recommendation choice;
- sale/decline outcome;
- inventory movement;
- deli jar fill;
- shelf/BOH visual stock;
- pricing;
- store workflow;
- analytics/game progression if present in the source game.

## 7.3 Presentation layer

- first-person / player interaction;
- in-world or tablet-style recommendation UI;
- POS UI;
- menu screens;
- stock visuals;
- NPC animation;
- audio;
- environment;
- CCTV;
- lighting.

## 7.4 Tooling layer

Editor/offline tools for:

- importing legacy data;
- generating product assets;
- validating batch/terpene data;
- COA parsing if retained;
- asset validation;
- reference comparison;
- build validation.

---

# 8. Unity architecture principles

1. **Do not dump the Three.js scene into Unity and call it a port.**
2. Preserve domain behavior with tests.
3. Rebuild rendering, scenes, interaction, navigation, animation, audio and lighting natively.
4. Use data-driven definitions rather than scene-object hardcoding.
5. Keep static reference/catalog data separate from mutable save state.
6. Keep game-specific customer state anonymous/non-PII.
7. Treat batch as a first-class entity.
8. Current/in-stock batch chemistry outranks stale historical averages.
9. Make every assumption replaceable.
10. Tie visual inventory to simulation inventory.

Recommended additive scene structure:

```text
Bootstrap
Retail
BackRooms
Hub
Exterior
GameplaySystems
NPCs
Audio
Lighting_Day
Lighting_Night
```

This also reduces merge conflicts between parallel agents.

---

# 9. Data strategy

## 9.1 Static/reference data

Examples:

- terpene definitions;
- effect-domain configuration;
- strain catalog;
- batch/COA records;
- price tiers;
- product/package definitions.

Import through deterministic conversion tools into a compact Unity-friendly form.

## 9.2 Large interaction dataset

The historical project used an interaction dataset described as roughly nine million lines.

Do **not** load raw multi-million-line source text at runtime.

Migration task:

1. identify exactly what the current engine actually consumes;
2. reproduce that transformation outside Unity;
3. precompute/normalize the minimum runtime representation;
4. regression-test recommendation outputs against the source system;
5. version the derived dataset and generator.

## 9.3 Save state

Use a versioned local save model for:

- current stock;
- day/time;
- transactions;
- gameplay progression;
- NPC/customer outcome history if retained;
- settings.

No real customer identity is needed.

---

# 10. Recommendation-engine rules

The port must preserve these constraints:

- inventory-only recommendations;
- no invented strains;
- current-batch-first behavior;
- deterministic enumeration;
- explicit fallback when data is insufficient;
- THC/lineage must not become the primary ranking engine;
- synergy/domain logic should remain distinguishable from learned outcomes;
- similarity remains explainable;
- scientific language remains calibrated;
- recommendation UI must remain fast.

The Unity port should build **golden regression cases** before rewriting the engine. The expected output does not have to be byte-for-byte identical where known bugs are intentionally fixed, but every intentional behavior change must be recorded.

---

# 11. Visual-inventory contract

The physical simulation should expose the same inventory truth as gameplay.

Examples:

```text
inventory decreases
→ deli jar visibly empties

BOH case transferred to FOH
→ BOH stack decreases
→ FOH stock increases

shelf stock sells
→ visible facing count changes

delivery received
→ cases/totes appear in receiving/backstock
```

Visual inventory is not decorative. It is a projection of simulation state.

---

# 12. Reality-reconstruction rules

The physical-store target is governed by the separate Asset Production Plan.

High-level rules:

- exact architecture before decorative polish;
- exact major fixtures before generic props;
- ordinary commercial detail is more important than cannabis clichés;
- BOH/HUB density matters;
- exterior/service infrastructure matters;
- lighting should look like a real retail building, not a cinematic dispensary concept;
- CCTV degradation belongs on CCTV feeds, not the player camera.

Unknown geometry must be tracked, not confidently invented.

---

# 13. Zero-dollar production rule

Hard constraints:

- third-party assets: free only;
- production software: free only;
- custom modeling is preferred over weak free substitutions;
- free assets require license/provenance records;
- CC0 preferred;
- CC BY allowed with attribution;
- unclear/ripped assets rejected.

Detailed sourcing belongs only in `ASSET_PRODUCTION_PLAN.md`.

---

# 14. Multi-agent studio model

The studio runs as Nolan → Hub → workers → fresh short-lived reviewers → Hub merges (DEC-116/117; the DEC-094 department leads were retired by DEC-112). The operating model is defined only in `STUDIO_OS.md` §0; it replaced the Hub-and-Workcell text that was here.

---

# 15. Repository memory model

> **As built (AUDIT-001 C4, DEC-064):** the repo follows this layout with these differences: no `README.md` (entry docs are `README_FIRST.md`, `CLAUDE.md`, `AGENTS.md`); no `Docs/CHANGELOG.md` (history = git log + `Docs/Handoffs/`, `Docs/Reviews/`); no `Docs/QA_STATUS.md` (QA evidence = `Docs/BUILD_STATUS.md`, `Docs/PERF_BASELINE.md`, reviews); no `Docs/Assets/ASSET_REGISTRY.csv` or `ATTRIBUTION.md` (licenses = `Docs/Assets/LICENSE_LEDGER.md`, downloads = `Docs/Assets/ASSET_CACHE_MANIFEST.json`, DEC-023); no `Docs/Tasks/Review/` (review state lives in `Docs/BACKLOG.md` and `Docs/Reviews/`). Added since: `Docs/HUB_RESUME.md`, `Docs/Design/`, `Docs/Specs/`, `Docs/Research/`, `Docs/Reconstruction/`, `Docs/Reference/`, `Docs/Audits/`, `Docs/Imports/`.

Conversation history is not project memory.

The repository should contain:

```text
Docs/
  MASTER_PLAN.md
  UNITY_MIGRATION_PLAN.md
  ASSET_PRODUCTION_PLAN.md
  STUDIO_OS.md
  PROJECT_STATE.md
  BACKLOG.md
  DECISIONS.md
  KNOWN_GAPS.md
  REFERENCES_INDEX.md
  BUILD_STATUS.md
  QA_STATUS.md
  Assets/
    ASSET_REGISTRY.csv
    ATTRIBUTION.md
    Specs/
  Tasks/
    Ready/
    Active/
    Review/
    Done/
  Handoffs/
```

`PROJECT_STATE.md` is the small file the Hub rereads frequently.

This master document should change rarely.

---

# 16. Context-routing rule

> **Current routing:** the Hub's reading set is owned by `Docs/HUB_RESUME.md` ("Hub loop" step 1); `Docs/DOCS_INDEX.md` is the doc router. They win over the table below, which is the original plan kept for context (AUDIT-001 B5/C5, DEC-064).

Default context by role:

| Role/task | Mandatory docs | Load only if needed |
|---|---|---|
| Hub | Master + Project State + Backlog | Migration / Assets / Studio OS / Toolchain / Gameplay sections |
| Gameplay port | Task + Migration relevant section | Gameplay Spec + Master architecture principles |
| Gameplay simulation | Task + Gameplay Spec relevant section | Migration domain rules |
| Environment art | Task + Asset relevant section + references | Gameplay only for interaction anchors |
| Build / CI / automation | Task + Toolchain relevant section | Studio OS ownership rules |
| Procedural asset worker | Task + Asset custom/generator sections | Master |
| QA | Task + acceptance criteria + affected docs | Other docs only to verify intent |
| Reviewer | Task + handoff + changed files | exact referenced source section |
| Build/integration | Project State + task + build docs | deep art/migration only if build issue requires |

**Never preload all four large documents into every session.**

---

# 16A. Gameplay simulation authority

`GAMEPLAY_SIMULATION_SPEC.md` defines the default minute-to-minute game.

Its new mechanics are explicitly labeled as game-design decisions so they are not confused with historical budtender-tool behavior.

Initial player fantasy:

> Work a dispensary shift as a budtender: understand customers, recommend real available batches, physically complete deli/product transactions, manage visible stock, survive rushes, and improve shift performance.

Management systems are later progression, not vertical-slice prerequisites.

---

# 16B. Toolchain execution authority

`TOOLCHAIN_EXECUTION.md` defines how agents actually operate Unity and Blender.

Core execution rule:

> Prefer deterministic shell/script execution, machine-readable results, builds, tests, renders and screenshots over manual GUI clicking.

The first BUILD workcell must discover the actual machine, software paths and performance target rather than assuming hardware.

---

# 17. Milestone roadmap

> **Current plan (DEC-119):** `Docs/Design/ROADMAP_POST_SLICE.md` is the one live roadmap (milestones PS1 → M-B → PS1b → PS2 → PS3 → M-F → M-G → PS4, task IDs, dependencies, critical path) and wins over this section. M0–M10 below are the original production milestones, kept for context; the roadmap cites them as "M-n".

## M0 — Documentation baseline and reconstruction freeze
Goal: turn the supplied project-history record into a precise reconstruction contract before implementing Unity systems.

Outputs:

- canonical feature matrix from the project record;
- implemented-v7.3.0 vs later-target distinction;
- canonical data-schema specification;
- recommendation-engine behavioral specification;
- pricing specification;
- feedback/privacy/governance target specification;
- known defects and intentional corrections;
- explicit unknowns that the record does not resolve;
- synthetic/golden test cases derived from documented rules and examples.

Because the original Three.js/browser source is unavailable, Unity implementation may begin from this documented contract. If source is supplied later, it becomes a verification/correction input.

## M1 — Repository and Unity foundation
Outputs:

- Unity 6.3 HDRP project; *(superseded by DEC-003: the project uses Unity 6000.6.7f1 + HDRP 17.6.0)*
- repository/doc structure;
- AGENTS.md / CLAUDE.md;
- build scripts;
- validation framework;
- coding/art conventions;
- empty additive scene structure.

## M2 — Measured dispensary graybox
Outputs:

- floor-plan-accurate room shell;
- major doors/openings;
- retail/back-room/HUB zones;
- exterior envelope;
- player scale;
- reference comparison cameras.

Acceptance:
player can traverse correct geometry before expensive art work begins.

## M3 — Domain-engine reconstruction
Outputs:

- catalog/batch data model;
- recommendation engine;
- intent processing;
- similarity;
- pricing;
- inventory;
- tests against source/golden cases.

Do not combine this milestone with final graphics.

## M4 — Core playable vertical slice
Preserve the actual source game where known.

Minimum proposed integration:

```text
customer need/intention
→ player/budtender interaction
→ recommendation UI
→ choose product
→ transaction outcome
→ inventory state changes
→ visible store state updates
```

If the existing Three.js game has a different canonical loop, the source audit overrides this proposal.

## M5 — Hero retail environment
- register run;
- deli counter;
- jar walls;
- living wall;
- POS;
- material baseline;
- core lighting.

## M6 — Procedural stock and BOH
- product package generator;
- shelf population;
- deli fill;
- case stacks;
- FOH/BOH/HUB state visualization.

## M7 — NPC behavior
- navigation;
- queue;
- customer intent;
- transaction handoffs;
- restock/delivery behavior;
- animation.

## M8 — Complete environment / exterior
- office;
- break room;
- hall;
- restroom;
- HUB/HUB2;
- exterior;
- parking;
- utilities;
- CCTV.

## M9 — Audio / lookdev / final interaction polish
- ambience;
- foley;
- glass;
- reflections;
- day/night;
- UI polish;
- visual comparison.

## M10 — Optimization / regression / final build
- profiler pass;
- memory;
- draw calls;
- NPC budget;
- CCTV budget;
- build validation;
- full walkthrough;
- known-gap review.

---

# 18. Migration gates

Before a legacy feature is ported, classify it:

- **PRESERVE** — valuable and still canonical.
- **PRESERVE WITH FIX** — valuable, but known defect must be corrected.
- **REIMPLEMENT** — behavior matters; implementation should be replaced.
- **EDITOR/TOOL ONLY** — useful for content creation but not player runtime.
- **DEFER** — valid future system but not needed for initial vertical slice.
- **DROP** — obsolete, privacy-heavy, operational-only or contrary to current direction.

The detailed classification is in the Unity Migration Plan.

---

# 19. Quality gates

## Code
- compiles;
- tests pass;
- no unrelated refactor;
- configuration is data-driven;
- save compatibility considered;
- runtime errors checked;
- repeated systems profiled.

## Art
- real-world scale;
- correct pivot;
- clean normals/UV/material;
- LOD/collider where required;
- license recorded;
- reference comparison performed.

## Scene
- physical scale credible;
- plan geometry correct;
- no major intersections;
- lighting tied to fixtures;
- audio zones valid;
- density matches reference;
- performance measured.

## Migration
- source behavior documented;
- parity/golden tests exist;
- intended differences recorded;
- obsolete behavior not accidentally restored.

---

# 20. Known reference gaps

These are source limitations, not planning omissions:

- exact ceiling height/grid;
- exact register numbering;
- precise FOH/BOH area assignment where ambiguous;
- exact janitor-closet position;
- HUB2 visual details;
- restroom finishes;
- some office details hidden from cameras;
- full roof layout;
- some exterior elevations;
- exact fixture dimensions not present in references.

Every gap should have:

- confidence level;
- temporary placeholder if needed;
- replacement path;
- no downstream irreversible dependency.

---

# 21. Known software/product gaps requiring source audit

The attached project record is detailed but not the actual current repository.

Before porting, verify:

The following details are **not fully supported by the supplied record** and must not be invented as historical facts:

- exact source code of `Terpene Tool v8 - Claude`;
- exact final numeric coefficients/weights for all recommendation formulas;
- exact final terpene-exclusion implementation;
- exact final newer-batch weighting formula;
- exact final Supabase schema after later changes;
- exact Three.js game systems that were not documented in the project record;
- exact browser save format beyond the documented localStorage/JSON direction;
- exact current UI implementation beyond the documented workflows.

Agents should implement a clean, configurable version consistent with documented behavior and record every invented engineering choice as a **new Unity implementation decision**, not as a claim about the old project.

---

# 22. Success criteria

Do not judge success by:

- number of features;
- code size;
- number of terpene rules;
- number of downloaded assets.

Judge the project by:

- fidelity to the physical reference;
- speed/clarity of customer-service decisions;
- correct inventory behavior;
- recommendation consistency;
- stable gameplay loop;
- believable visual inventory;
- smooth NPC/store flow;
- maintainability;
- performance;
- ability for fresh agents to continue work without giant context dumps.

---

# 23. Scope discipline

New features must answer:

1. Does it improve the game or a real store workflow being simulated?
2. Is it supported by the source game/project?
3. Does it create an observable player experience?
4. Is its data authoritative?
5. Can the same value be achieved more simply?
6. Does it belong in the current milestone?

If not, backlog it rather than expanding the active task.

---

# 24. Canonical art direction

Avoid:

- generic weed-shop caricature;
- excessive neon;
- head-shop clutter unsupported by reference;
- stylized low-poly hero assets;
- perfect empty luxury showroom;
- abandoned-warehouse grime;
- random cannabis leaves everywhere.

Target:

> A real, busy, modern dispensary whose front-of-house looks intentionally designed and whose back-of-house looks operationally dense.

---

# 25. Canonical technical rule

> Preserve behavior, not obsolete implementation.

Three.js/browser code, monolithic HTML, Supabase-era auth and old CRM architecture are historical implementations.

The Unity project should preserve valuable domain outcomes while becoming a modular, testable game architecture.

---

# 26. Canonical studio rule

> The repository is memory.  
> The Hub is coordination.  
> Workcells are labor.  
> Review is independent.  
> Context is disposable.

If a session becomes large because it contains history rather than active task information, its knowledge has not been externalized correctly.

---

# 27. First boot sequence

The first Hub session using this document should:

1. create/confirm repository structure;
2. install the short `AGENTS.md` / `CLAUDE.md`;
3. create `PROJECT_STATE.md`;
4. create `BACKLOG.md`;
5. create `DECISIONS.md`;
6. create `KNOWN_GAPS.md`;
7. create `REFERENCES_INDEX.md`;
8. archive supplied references without alteration;
9. read and index the supplied project-history record;
10. generate the documented-behavior reconstruction contract;
11. initialize Unity 6.3 HDRP; *(superseded by DEC-003: the project uses Unity 6000.6.7f1 + HDRP 17.6.0)*
12. create the first dependency graph;
13. dispatch only dependency-ready workcells.

Do not begin by downloading hundreds of assets or rebuilding the final store.

---

# 28. Initial workcell sequence

Recommended initial parallelism:

### REF-001 — Canonical reference index
Owns:
- floor plan;
- CCTV mapping;
- project record;
- confidence levels.

### BUILD-001 — Repo / machine / Unity bootstrap
Owns:
- STUDIO-DOCTOR machine profile;
- Unity/Blender executable discovery;
- Unity project;
- folder structure;
- initial command wrappers;
- validation/build scaffolding.

### MIG-001 — Documented-system reconstruction contract
Owns:
- project-history record analysis;
- feature inventory;
- documented data schemas;
- implemented-vs-target matrix;
- known-defect corrections;
- synthetic/golden cases;
- explicit unresolved implementation details.

After those stabilize:

### ART-001 — Measured graybox
### GAME-001 — Domain engine skeleton
### QA-001 — Baseline acceptance harness

---

# 29. Document maintenance

This master plan should remain compact and stable.

Update it only for:

- project-goal changes;
- major architecture decisions;
- milestone changes;
- durable constraints.

Do **not** paste:

- asset catalogs;
- debug logs;
- individual task progress;
- long research findings;
- worker transcripts;
- build output.

Those belong in the specialized documents or task/handoff files.

---

# 30. Final project thesis

> Build a high-fidelity dispensary simulation whose physical store, product inventory and customer-recommendation systems operate as one coherent game.

> Reconstruct what is unique.  
> Source free what is generic.  
> Proceduralize what repeats.  
> Port domain behavior with tests.  
> Drop obsolete privacy/operational baggage.  
> Keep the floor experience simple.  
> Keep project truth in files.  
> Give every worker one bounded deliverable.  
> Finish milestones before expanding scope.
