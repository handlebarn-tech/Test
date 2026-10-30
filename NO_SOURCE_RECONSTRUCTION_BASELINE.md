# DISPENSARY GAME — NO-SOURCE RECONSTRUCTION BASELINE
## What Claude Code Should Assume When the Original Three.js/Browser Project Is Unavailable

**Status:** Canonical handoff note  
**Date:** 2026-10-29

---

# 1. Situation

Claude Code will receive this folder but **will not receive the original Three.js/browser source project**.

Therefore the studio must not block on a source-code audit.

The strongest available behavioral source is the live deployment:

https://tfs-phx-budtender.netlify.app/

Captured observations:
`References/LIVE_TFS_BUDTENDER_v7.11.4.md`

The historical reconstruction remains the second major source:

`References/Review_Budtender_Tool_Comprehensive_Chat_Record.md`

The live deployment currently identifies as v7.11.4 and supplies current UI/behavior evidence. The historical record remains a high-detail reconstruction of the substantive project history, decisions, requirements, critiques and earlier v7.3.0 state.

It is not a verbatim source export.

---

# 2. What is known well enough to reconstruct

The project record supports rebuilding these systems:

- natural-language customer-intent workflow;
- inventory-only recommendation behavior;
- terpene-driven effect/domain scoring concept;
- multi-terpene synergy principle;
- batch/COA model;
- current-batch preference requirement;
- similar-strain matching using cosine similarity;
- comparison workflow;
- Floor Mode / rush-mode UX;
- pricing tiers;
- weight pricing;
- deals/tax/overrides;
- stock/availability model;
- COA ingestion concept;
- 111-terpene database concept;
- six-domain scoring concept;
- five lab-format parser concept;
- feedback/outcome redesign;
- anonymous/batch-aware feedback target;
- manager/admin/budtender historical role model;
- later Owner/admin/permissions direction;
- multi-location shared-batch / location-stock architecture concept;
- reporting/analytics direction.

---

# 3. What is NOT known exactly

Do not claim historical exactness for:

- final v8 source code;
- final numeric scoring coefficients;
- exact six domain names if not otherwise present in project files;
- exact BA scalar values;
- exact newer-batch weighting formula;
- exact terpene-exclusion implementation;
- exact current Supabase schema;
- exact browser save schema;
- exact current UI layout beyond documented behavior;
- any Three.js geometry/scene placement not represented in the supplied floor plan/CCTV.

For these:
- create clean configurable Unity implementations;
- label them as **new Unity implementation decisions**;
- keep them easy to revise if old files are later recovered.

---

# 4. Historical behavior to preserve

Preserve the project’s core product thesis:

> A budtender should be able to describe what the customer wants in normal language and receive a small set of defensible recommendations from actual available inventory using batch-aware terpene information.

Preserve:
- complex backend / simple floor UX;
- inventory-only recommendations;
- deterministic enumeration;
- no hallucinated strains;
- batch as a first-class entity;
- current/newer chemistry over stale historical averages;
- similarity/comparison;
- calibrated uncertainty;
- price as secondary to fit;
- optional deeper chemistry detail;
- fast rush workflow.

---

# 5. Historical behavior to intentionally leave behind

Do not rebuild:
- customer PII/CRM as a core feature;
- broad budtender admin rights;
- web authentication complexity unless needed for game mechanics;
- Supabase RLS as a hard runtime dependency;
- account lockout logic;
- corporate approval workflows;
- manual “Sold” logging as a separate source of truth;
- historical averaging that creates a chemistry profile no current batch actually has;
- unsupported single-terpene beginner rules;
- pseudo-clinical precision.

---

# 6. Unity reconstruction standard

When exact historical code is unavailable:

1. follow documented invariants;
2. make the implementation modular;
3. externalize coefficients/configuration;
4. write tests from documented examples and failure cases;
5. record every new engineering decision;
6. never rewrite an unknown into a fake historical fact.

---

# 7. First instruction to Claude Code

Do not ask where the browser source is.

Assume it is unavailable.

Begin by indexing:
- Master Plan;
- Unity Migration Plan;
- Asset Production Plan;
- Studio OS;
- this baseline;
- historical project record;
- floor plan;
- CCTV composite.

Then create the reconstruction contract and proceed.
