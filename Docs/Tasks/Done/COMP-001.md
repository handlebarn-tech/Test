# COMP-001 — Arizona cannabis compliance review → gameplay adjustments

**Role:** RESEARCH + DESIGN · **Priority:** P0 · **Branch:** `task/COMP-001` worktree off `main`

## Goal
Find every Arizona cannabis law, rule and official guideline that touches what a budtender or dispensary does in our game, then say where the game design must change. Nolan flagged **overselling** (purchase limits) as a likely gap. Follow DEC-032: realistic enough to feel true, never so procedural that it stops being fun.

## Sources (primary first; cite each with URL + date visited)
- Arizona Revised Statutes: Smart and Safe Arizona Act (A.R.S. Title 36, Ch. 28.2, §36-2850 ff.) and the Arizona Medical Marijuana Act (Title 36, Ch. 28.1, §36-2801 ff.).
- Arizona Administrative Code: ADHS rules, Title 9 Ch. 17 (medical) and Ch. 18 (adult use).
- ADHS official guidance, FAQs, bulletins; Arizona Dept. of Agriculture Weights & Measures (scale certification); Arizona Dept. of Revenue (excise/TPT tax on cannabis, ties to GAP-204).
- Secondary sources (law firms, industry guides) only to find primary text; never as sole citation.
- Note anything that changed recently and the effective date; flag where rules are ambiguous.

## Topics (at minimum)
1. **Purchase/possession limits:** adult-use (flower and concentrate amounts, equivalencies for edibles/vapes), medical (per-visit and rolling-period limits), per-transaction vs per-day, how the POS enforces them.
2. ID and age checks, medical card checks, out-of-state cards, visibly intoxicated customers, refusal rules.
3. Who may be in which area (customer vs staff areas), facility agent cards, visitor logs, the vestibule/check-in flow.
4. Deli/bulk flower handling: weighing (certified scales, tare, in view of customer?), packaging (child-resistant, opaque exit packaging), labeling at the counter.
5. Product rules that affect assortment or display: potency caps (e.g. edible per-serving/package mg), display restrictions, samples.
6. Pricing/sales rules: discounts, free product bans, deals; taxes (state excise rate + TPT; how it shows on the receipt).
7. Hours of operation, signage requirements, inventory tracking (seed-to-sale), waste/destruction, recalls, transaction records.
8. Anything else a budtender must do or never do (medical claims/advice, consumption on premises).

## Then map to the game
Read `Docs/Specs/SLICE_DESIGN.md`, `Docs/GAMEPLAY_SIMULATION_SPEC.md` (§12, §20–25, §30, §36–37, §47), `Docs/Specs/UX_SLICE.md`, and DEC-019…021, DEC-027. For each rule, classify:
- **MECHANIC:** becomes a fun decision (e.g. a purchase-limit meter at POS, an ID check with an occasional fake/expired ID, refusing an intoxicated customer).
- **AUTOMATED:** the game enforces it silently or the POS handles it (realistic, no player burden).
- **FLAVOR:** shown in the world (signage, receipts, exit bags), no rule.
- **OMITTED:** cut for fun, with a one-line reason.
Then list concrete changes: to SLICE_DESIGN (slice-now vs later), new SliceConfig constants with sourced values, customer-generator changes (e.g. requests over the limit), and any engine/POS checks. Also check whether any slice behaviour currently **breaks** a rule (e.g. a sale that exceeds a limit, wording that implies medical claims) and mark those **must-fix**.

## Owns
- `Docs/Research/AZ_COMPLIANCE.md` (rule table: rule, citation, plain-language summary, game classification, proposed design change)
- `Docs/Research/AZ_COMPLIANCE_CHANGES.md` (prioritized change list; must-fix first; proposed DEC entries)
- `Docs/Handoffs/COMP-001.md`
Don't edit SLICE_DESIGN or code; the Hub routes the changes.

## Rules
- This is game design research, not legal advice; say so once in the doc header.
- No PII. Don't use Nolan's mail or files (RES-001 handles those).

## Handoff
`Docs/Handoffs/COMP-001.md` (≤40 lines): must-fix list, top mechanics, open legal ambiguities. Report to the Studio Hub.
