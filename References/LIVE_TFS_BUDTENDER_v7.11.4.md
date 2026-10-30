# TFS BUDTENDER TOOL — LIVE DEPLOYMENT REFERENCE

> **Authority (DEC-001/002/009; AUDIT-001 C1, DEC-064):** for recommendation logic the order is (1) the local TFS tool source, v7.11.4 build, at `C:/Users/handl/Downloads/tfs-budtender` (read-only, no PII); (2) `Docs/DECISIONS.md`; (3) the live site (identical to the local build, DEC-009); (4) the historical chat record. Text below that ranks the live site or the chat record first predates DEC-001 and is kept for context.
## Public behavioral baseline for the Unity reconstruction

**URL:** https://tfs-phx-budtender.netlify.app/  
**Observed:** 2026-10-29  
**Live version shown:** **v7.11.4**  
**Role in project:** Highest-available behavioral reference for the budtender-tool side of the game, above the older reconstructed v7.3.0 historical record.

---

# 1. Why this matters

The original Three.js/browser source repository is not included in the Claude Code handoff, but the public deployment is still accessible.

Therefore the behavioral source hierarchy is now:

1. **Live deployed application — v7.11.4**
2. Explicit current user/project decisions
3. Historical comprehensive project record
4. New Unity implementation decisions

The live deployment does not expose every source-code constant or private dataset, but it materially reduces ambiguity about current product behavior.

---

# 2. Live app identity

Observed directly in the deployment:

- TFS Budtender Tool
- v7.11.4
- terpene-based cannabis strain recommendation engine
- COA-powered
- terpene-profile matching score
- BA-corrected
- freshness badges/decay language
- 111 terpenes
- 6 effect domains
- 5 lab formats
- offline/local mode supported

The currently public session showed **no inventory loaded** and offered import of a TFS export JSON.

This means the public deployment is useful for behavior/UI reference even when live store inventory is not exposed.

---

# 3. Primary search workflow

The primary search field accepts natural language, with examples including:

- anxiety without couch lock
- something giggly
- back pain
- pain relief but need to drive
- on a budget, help with sleep
- something giggly for a concert

The app explicitly describes search as **natural-language intent parsing**, not keyword-only matching.

It states that the engine understands:

- intent
- modifiers
- negations

The live About content reports **281 search patterns understood**.

Examples of modifiers documented in the live interface:

- “without couch lock” suppresses high-sedation candidates
- “need to drive” boosts focus and penalizes body-heavy profiles
- “budget” biases toward House and FttP tiers
- “light”
- “strong”
- “just a little”

These adjust threshold sensitivity or ranking behavior.

---

# 4. Six live effect domains

The live v7.11.4 interface names the six domains as:

1. **Euphoria / Uplift**
2. **Calm / Sedation**
3. **Energy**
4. **Focus / Cognitive**
5. **Pain / Anti-inflammatory**
6. **Anxiety Relief**

The About page gives representative terpene associations:

- Euphoria / Uplift — limonene, ocimene
- Calm / Sedation — myrcene, linalool
- Energy — terpinolene, pinene
- Focus / Cognitive — pinene, ocimene
- Pain / Anti-inflammatory — caryophyllene, humulene
- Anxiety Relief — linalool, low-myrcene

Treat these as current UI/domain definitions.

---

# 5. Live scoring description

The app describes its recommendation score as a **terpene-profile matching score**.

Current public explanation:

- each strain is scored across six effect domains;
- each terpene contributes effect weights;
- contribution is scaled by concentration tier;
- contributions are summed by domain;
- results rank by fit to the query;
- price/alphabetical order is not the primary ranking;
- the tool explicitly calls this a **matching heuristic, not a pharmacological model**.

This is a better canonical description than the older historical record alone.

Unity should preserve this distinction.

---

# 6. Result-card behavior

The live deployment says result cards can show:

- dominant terpene driving the recommendation
- domain score bars
- cluster tag, such as Anti-Inflammatory or Cognitive
- anxiety-risk flags
- optional full terpene breakdown via Details

Settings allow:

- domain bars on/off
- terpene percentages on/off
- Floor Mode

---

# 7. Floor Mode

Live v7.11.4 definition:

> Simplified result cards for busy registers.

It hides:

- terpene details
- advisory chips
- expand buttons

This confirms that Floor Mode should be treated as a current first-class UX feature, not merely an older design concept.

Unity should preserve the same goal:

**high-speed decision support during rushes.**

---

# 8. Tier filters observed

The current live UI exposes tier filtering including:

- All tiers
- House Smalls
- House Fresh
- TFS Premium
- FttP
- Tier 1
- Tier 2
- Tier 3
- Tier 4
- Unlabeled in inventory filtering

This should be captured as current reference data, but final Unity pricing/tier configuration should remain data-driven.

---

# 9. Customer experience selector

The live search tools expose:

- New
- Experienced

This is a current behavior worth preserving or translating into the game customer model.

Do not equate it with a simplistic single-terpene “beginner-safe” rule.

---

# 10. Search behavior settings

Observed settings include:

- results per query
- pain functional default
- hide out-of-stock in terpene rank
- domain bars
- terpene percentages
- Floor Mode
- inventory default sort
- sidebar startup state

The live explanation of **pain functional default** says pain queries can bias toward non-sedating strains unless the customer specifies otherwise.

The live explanation of out-of-stock handling says OOS strains are already excluded from recommendations, with an additional option to exclude them from terpene-ranking style queries.

This reinforces the hard Unity invariant:

> unavailable products must not appear as ordinary recommendations.

---

# 11. Similar tab

The current live Similar workflow:

- accepts strains a customer previously liked;
- compares terpene profiles;
- uses **cosine similarity**;
- searches current inventory;
- does not require identical profiles, only similar shape;
- can show shared terpenes;
- provides a plain-language reason.

This is a direct preservation target for Unity.

---

# 12. COA parser

The live app describes coordinate-based word extraction from PDFs, specifically to handle multi-column lab reports.

Five live lab-format families shown:

1. Level One Labs
2. Kaycha Labs
3. Full Spectrum Lab
4. SC Labs
5. Apollo / Generic

For the game, this remains editor/tooling-first unless actual COA import becomes part of gameplay.

---

# 13. Current data/storage wording

The live v7.11.4 application says:

### Signed-in/shared-store mode
Inventory, stock, prices, feedback and search log are stored in a shared store database and visible across registers.

### Local mode
Without a database, data stays in the current browser/computer and clearing browser data removes it.

Owners, Admins and Managers can export a backup from Settings.

For the private Unity game, this is useful architectural history but does **not** require recreating the web database/auth layer.

---

# 14. Export/import

The live UI states that a full backup can include:

- strains
- pricing
- brands
- preferences

It exposes:

- Export
- Import all
- Strains only
- Clear all

This strengthens the case for a deterministic Unity data-import/export pipeline, even if the exact web JSON schema is unavailable.

If a real TFS export JSON becomes available later, add a dedicated importer.

---

# 15. Pricing/settings surface

Live settings explicitly cover:

- brands and tier defaults
- tier management
- pricing and deals
- tax rate
- tier prices
- day deals
- strain overrides

This confirms these are current v7.11.4 product concepts.

Unity should preserve the data model where gameplay needs it, not necessarily reproduce the administrative web screens exactly.

---

# 16. Search logging

The live app has a setting to:

- log searches
- show a Sold button
- export log CSV
- clear log

For Unity:

- transaction truth should come from the authoritative game transaction ledger;
- search/recommendation events can still be logged separately for analytics;
- do not recreate the old Sold button as a second stock truth.

---

# 17. Accessibility features observed

Current live settings include:

- dyslexia-friendly typography / OpenDyslexic
- colorblind-safe indicators
- reduced motion
- high contrast mode
- keyboard shortcut rebinding

The Unity game should carry these forward as inspiration for accessibility requirements.

At minimum plan for:

- remappable input
- reduced motion
- readable text scaling
- colorblind-safe signals
- high-contrast UI option where practical
- subtitles

---

# 18. Training content

The current live application includes:

- Customer language
- Cheat sheet
- Terpene guide
- Advanced guide

Customer-language training maps ordinary phrases to intent and suggests follow-up questions.

This is useful for:

- tutorial design
- customer dialogue templates
- player training scenarios
- NPC intent generation

Do not copy every training statement blindly into gameplay logic; some scientific claims may still require calibration.

---

# 19. Examples of customer-language categories visible live

The deployment currently includes training patterns around:

- “best indica” / body-sedation intent
- functional/uplifting “sativa” requests
- highest THC / strongest requests
- balanced/hybrid requests
- symptom-oriented requests
- creative/focus requests
- aroma-based requests

The instructional design repeatedly redirects generic labels toward underlying desired experience.

This is directly useful for the game customer-dialogue generator.

---

# 20. Current live scientific-calibration tension

The About section explicitly says the score is a **matching heuristic, not a pharmacological model**.

However, some training/guide copy still uses strong mechanistic or effect language.

For Unity:

- preserve the heuristic framing;
- use strong scientific claims cautiously;
- separate flavor/training prose from authoritative simulation rules;
- keep configurable evidence/confidence levels.

This aligns with the historical review’s criticism of false precision.

---

# 21. Live-app reference usage by worker type

## MIGRATION / GAMEPLAY
Use this file to confirm:
- current domain names;
- search behaviors;
- Floor Mode;
- Similar behavior;
- OOS exclusion;
- tier concepts;
- settings and workflow.

## UI
Use the live site itself as a UX reference when network access exists.

## QA
Build test cases around:
- negation handling;
- budget;
- functional pain;
- current-stock exclusion;
- Similar/cosine similarity;
- Floor Mode.

## TRAINING / DIALOGUE
Use current customer-language categories as reference for NPC phrasing, but do not reproduce long site copy verbatim in shipped content without review.

---

# 22. Updated source hierarchy

For budtender/recommendation behavior:

```text
1. live v7.11.4 deployment
2. explicit current project decisions
3. historical comprehensive project record
4. Unity implementation decisions
```

For physical store geometry:

```text
1. floor plan
2. CCTV composite
3. other supplied photos/references
4. public imagery
5. temporary conventional assumptions
```

---

# 23. What the live deployment still does NOT give us

Even with this URL, we still do not have guaranteed access to:

- private/current inventory
- exact source repository
- all JavaScript source structure
- exact numeric weight tables
- full 281-pattern rule definitions
- exact BA scalar table
- exact freshness formula
- exact database schema
- exact export JSON schema
- hidden/private account behavior
- all current production data

Therefore these remain configurable reconstruction details unless additional artifacts are supplied.

---

# 24. Unity reconstruction consequences

Because the live app is richer than the historical snapshot, Unity should now explicitly target:

- six live domain names;
- natural-language modifiers/negations;
- current-stock exclusion;
- New/Experienced customer context;
- Floor Mode;
- Similar/cosine workflow;
- tier/budget behavior;
- configurable pain-functional behavior;
- pricing/deal/tax architecture;
- recommendation explanations;
- current v7.11.4 terminology where appropriate.

This should be incorporated into the migration contract before gameplay implementation.

---

# 25. Canonical instruction

> The live application is the closest thing currently available to executable product truth.

Use it to constrain the Unity reconstruction.

Do not treat the older v7.3.0 historical snapshot as the final state when the live v7.11.4 deployment provides newer direct evidence.
