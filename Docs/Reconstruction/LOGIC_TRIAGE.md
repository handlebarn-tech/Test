# Logic triage: TFS Budtender v7.11.4 → Dispo Game (MIG-001)

Classes: **PRESERVE** (port exactly; golden cases are the oracle) · **PRESERVE WITH FIX** (port, but fix a known defect, and record the deviation in the golden test) · **TRANSFORM** (becomes a game mechanic) · **EDITOR-TOOL** (offline/import tooling, not runtime) · **DEFER** · **DROP**. `L#####` = line in the v7.11.4 page. Defect IDs come from `tfs-budtender/TRACKER.md` / `HUB.md`, except **NEW** (found here).

## Recommendation core

| # | Feature | Class | Rationale / game mechanic |
|---|---|---|---|
| 1 | Query normalization + framing/product-word strip (L16030) | PRESERVE | Customer lines feed the same parser |
| 2 | INTENTS table, 287 keys (L15619) | PRESERVE | Port as data. Intent families seed the customer-line generator (spec §9-10) |
| 3 | PHRASE_MAP, 54 regexes, span blanking (L16098, L16165) | PRESERVE | Regex parity is checked by the golden cases |
| 4 | Negation patterns + `_sleepAsk` (L16066-16093) | PRESERVE WITH FIX | **NEW GAP-206**: "trouble sleeping but gotta work" loses the sleep ask (X-15). The game matches `sleep\w*` |
| 5 | Conflict resolution crit vs neg (L16195) | PRESERVE | |
| 6 | Pain-functional default cap 55 (L16211) | PRESERVE | A store setting, default on |
| 7 | Fuzzy fallback, 8 broad regexes (L16226) | PRESERVE | |
| 8 | "for the day" not understood (RC-16) | PRESERVE WITH FIX | **MC-7**: adopt the v7.11.5 fix (copy the `daytime` numbers). Golden RC-16 expects the v7.11.4 "unknown" until the fix is applied |
| 9 | Strain-name mention + Levenshtein fuzzy (L15916-15954) | PRESERVE | Players and NPCs name strains by sight |
| 10 | Compare intent + key-difference note (L16043, L16555) | PRESERVE | UI becomes the compare panel (spec §19) |
| 11 | Like-X-but-Y (L16048) | PRESERVE | |
| 12 | Terpene rank "most X" (L16058, L16573) | PRESERVE | |
| 13 | Hard terpene exclusions, unknown = excluded (L15975-16012) | PRESERVE | Becomes an allergy/avoid constraint on NPCs |
| 14 | Price intent detection (L21696-21759) | PRESERVE | Budget constraint on NPCs (spec §12) |
| 15 | Drive notice (L19545) | PRESERVE | A compliance line the player can say |
| 16 | Domain scoring: tiers, dominant bonus, BA, NF, clamp 2-99 (L15040-15201) | PRESERVE | Exact constants. Port `scoreRaw` for ranking |
| 17 | Display saturation at 99 (anxiety/pain often 99) | PRESERVE | Parity first. A UI change (raw-relative bars) is a later design call (GAP-208) |
| 18 | BA scalars incl. terpinolene 0.55 floor (L15127) | PRESERVE | Data, labelled "business choice" (SCI-7d) |
| 19 | Six domains incl. hidden antimicrobial (L15042) | PRESERVE WITH FIX | Use the code ids. The About-page "Energy" domain does not exist in code (GAP-201) |
| 20 | Clusters + tiebreakers + BCP solo (L15202) | PRESERVE | Cluster tag on cards; NPC "type" hints |
| 21 | CLUSTER_BONUS (L15327) | PRESERVE | The only multi-terpene "synergy" in ranking |
| 22 | Pairwise synergy / interaction dataset | DROP | Not in code (contract §5). Do not invent coefficients |
| 23 | Anxiety risk model (L15288) | PRESERVE | Drives the new-customer guardrail and advisory chips |
| 24 | In-stock-only profile + 8-week half-life averaging (L15475, L15483) | PRESERVE | Already the "current batch" rule. Satisfies the migration plan's averaging fix |
| 25 | Freshness decay `getFreshnessScalar` (L15162) | DROP | DEAD code. Not in scoring since v4.3.2 |
| 26 | Age badge (`weeksOld`, L15529) | TRANSFORM | Visible jar age/date label. Older stock ties to sell-through pressure (spec §22) |
| 27 | Tier nudge, house priority (L15408) | PRESERVE | Real store behaviour. Exposed as a store-policy config |
| 28 | New-customer profile: anx ≤60 filter + myrcene penalty (L14827, L15417) | TRANSFORM | Novice NPC archetype sets it, or the player toggles it after asking "first time?". Logic unchanged |
| 29 | `applyProfileSort` (L14834) | DROP | DEAD |
| 30 | Tier chip filter, empty tier = house (L15364) | PRESERVE WITH FIX | **V73-NT5**: treat empty as "no tier" (the v7.11.5 fix) |
| 31 | Max-price filter (L15374) | PRESERVE | |
| 32 | Neg-headroom penalty, primary 1.5×, primary-only for sed/pain (L15382-15394) | PRESERVE | |
| 33 | Like-X cosine bonus (L15413) | PRESERVE | |
| 34 | One-shot relaxed fallback ×0.60 / +12 (L16639) | PRESERVE | "Closest available" dialogue state |
| 35 | Role tags (L16264) | PRESERVE | Short "why" chip in rush view |
| 36 | Card scripts `buildScript` (L15561) | PRESERVE | Text as data. Language audit per UNITY_MIGRATION_PLAN §9 is DEFER |
| 37 | Refine chips (L19583) | TRANSFORM | Follow-up dialogue options ("lighter", "more body") during the conversation |
| 38 | Show more options (L19442) | PRESERVE | "Anything else?" |
| 39 | `tf` terpene re-sort (L16637) | PRESERVE | |
| 40 | Similar / cosine (L20813-20893) | TRANSFORM | Regular says "I liked X" → Similar workflow (spec §18). Algorithm preserved |
| 41 | Strain lookup + "close to it" for OOS (L16551) | PRESERVE | Out-of-stock substitution moment |

## Pricing

| # | Feature | Class | Rationale / game mechanic |
|---|---|---|---|
| 42 | Tier price tables (L21018) + day deals (L21036) | PRESERVE | Economy data. Weekday deals change demand |
| 43 | Resolution order: override > brand class > tier; first deal wins (L21172) | PRESERVE | |
| 44 | Tax 25.1% + floor to $0.05 (L21123-21138) | PRESERVE | Floor vs round is open with Nolan (GAP-204). Port the floor |
| 45 | pct_msrp / use_tier / custom deals / strain overrides | PRESERVE | Data model kept. Editing them is #46 |
| 46 | Pricing page / tier manager UI | EDITOR-TOOL | Manager mode later (DEFER as a game screen) |
| 47 | Unreleased v7.11.5 Tier 2 14 g $77 | DEFER | Adopt only after the tool ships it (DEC-002) |
| 48 | `isFirstWeekdayOfMonth` (L21165) | DROP | DEAD |
| 49 | Price-save race fix v7.11.4 (C-4) | DROP | Cloud concurrency; no game equivalent |

## UX, feedback, data, ops

| # | Feature | Class | Rationale / game mechanic |
|---|---|---|---|
| 50 | Floor Mode (L17575, CSS L169-175) | TRANSFORM | Rush view: 3 picks + price + stock + role tag (spec §13). Ranking is identical in both views |
| 51 | Anonymous fit feedback (L22615-22677) | TRANSFORM | The NPC's reaction after a sale is the "matched/poor" event, aggregated per batch. Never feeds ranking (kept) |
| 52 | Sold toggle + search log (L22066, L22082) | TRANSFORM | Sale event from the POS sim. Optional analytics |
| 53 | Learned / outcome-weighted ranking (v7.1.0 history) | DEFER | Removed in the tool. Revisit only after base parity |
| 54 | Stats / reports (Phase 6b) | DEFER | End-of-shift summary later |
| 55 | COA PDF parser + 7 lab readers, coaValidate, Data check | EDITOR-TOOL | DATA-001 imports JSON. MC-3/MC-4 range checks become importer validation |
| 56 | Inventory edit / stock toggle / bulk bar | TRANSFORM | Stock comes from the simulation (restock, sell-through), not from manual toggles |
| 57 | Export/import JSON, `_sanitizeImport` rules | EDITOR-TOOL | The importer reuses the sanitize rules (finite, ≥0, <50, keep zeros) |
| 58 | Pinned panel, keyboard shortcuts | DEFER | |
| 59 | Accessibility prefs (dyslexia, colorblind, motion, targets, contrast) | DEFER | Re-do as Unity UI settings later |
| 60 | Learn/Training tab | DEFER | The science audit found wrong claims; off-limits in the tool |
| 61 | Supabase, multi-store, accounts, roles, lockout, idle sign-out, demo mode | DROP | Web-ops security. Roles could return as game concepts only |
| 62 | Memory growth `_parsedReg` (MC-9), latency at 5k batches (MC-10), non-Latin `normName` (U8) | DROP | Browser-architecture issues. Game inventory is small and fixed-alphabet |
| 63 | `deriveTerpChem`, `analyzeStrain` | DROP | DEAD |

## Counts

PRESERVE 34 · PRESERVE WITH FIX 4 · TRANSFORM 8 · EDITOR-TOOL 3 · DEFER 6 · DROP 8 (63 rows; the ticket-level defects are listed below).

## Known defects and game disposition

| Defect | Where | Game |
|---|---|---|
| MC-7 "for the day" → unknown | INTENTS | Fix (#8) |
| V73-NT5 empty tier counted as House Fresh in chips | L15364 | Fix (#30) |
| NEW: "sleeping" not caught by `_sleepAsk` | L16086 | Fix (#4). Report to the tool hub via the Studio Hub, since we are read-only there |
| SCI-7d terpinolene floor disclosure | DB note | Label it as a business choice in data |
| Price rounding floor vs round | L21123 | Keep the floor; GAP-204 |
| SCI-8 accuracy never measured | n/a | Keep the "heuristic, not pharmacology" framing; satisfaction is a game model |
| S6 501 batches lacked a COA date (now 48 after backfill) | data | Importer flags undated batches; they take the oldest weight (L15498) |
| DATA-PARSER / L1 (no-COA batches, image-only Kaycha) | parser | Out of scope (EDITOR-TOOL) |
| MC-3 / MC-4 data range checks | import | Importer validation |
| MC-9, MC-10, U8, C-4, F3/F5/F7, B6 | web/cloud | DROP |
