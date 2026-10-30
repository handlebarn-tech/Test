# REVIEW-W4X — DOC-001: AUDIT-001 batches A–C (DEC-064) + DEC-066 items

**Verdict: PASS (GO) with minors, fixed in this review commit.** Branch `review/wave-4x` (off `main` c18cf64) merges `claude/task-doc-001` (phase 1 bd399dd, phase 2 dc6bf9f) as b0ef4e3. Reviewer: UX-002 workcell session, 2026-10-30.
**Merge:** no textual conflicts. Main's newer Hub content (DEC-067, QA-002b packet, W4T merge) is intact. BACKLOG was stale for the latest merge, so this commit sets **QA-002 → Done (W4T)** and adds **QA-002b | Active** (DEC-067). GAME-006 Review, UX-005 Done (W4S), REF-009b Done (W4U) and IMP-002 Done (W4V) were already right.

## Method
Every line DOC-001 removed or rewrote (diff c18cf64…b0ef4e3, all 34 files) was read against the approval sheet `Docs/Audits/AUDIT-001_APPROVAL.md` (`claude/audit-001-b559c2` @ 2f5765d) and DEC-064/066. Code-fence counts are even in the edited docs (STUDIO_OS 30, ASSET_PRODUCTION_PLAN 22). Every merge SHA in `Tasks/Done/INDEX.md` resolves.

## Item check
| Item | Approved change | Result |
|---|---|---|
| A1 | GAME-023 Blocked in packet + ROADMAP row | ✔ `State: BLOCKED (DEC-059 m2)` header; ROADMAP row Blocked; row text kept |
| A2 | answered values | ✔ GAME-009 + SPEC_COMP002 0.04 "[GDD], was 0.10" (DEC-048); COMP §1 row 13, §6, GAP-COMP-07 → DEC-049 with the old text kept; §5 caps "partly answered DEC-048" with the full old placeholder kept verbatim; SPEC_GAME004 cooler/fridge rows per DEC-050/062 with "was …" |
| A3 | serialise GAME-008→009, GAME-021→022; note only for running GAME-006/010 | ✔ packet headers keep their old dependency text and append the new one; GAME-010's note is in BACKLOG only (its packet is untouched) |
| B1 | BACKLOG states, duplicates, missing rows; IDs/deps verbatim | ✔ removed rows are only the two duplicate pairs (PERF-001, PROC-003) folded into the first row, plus state-cell rewrites; added rows keep their IDs and dependency text |
| B2 | same-commit rule | ✔ HUB_RESUME step 4 (old sentence kept, rule appended) |
| B3 | GAME-010 Ready → Active | ✔ `git mv`, content unchanged |
| B4 | historical banners README_FIRST, baseline §7 | ✔ banners only |
| B5 | HUB_RESUME owns the Hub reading set | ✔ step 1 + pointers in STUDIO_OS §3 / MASTER §16. PROJECT_STATE left to the Hub (see "For the Hub") |
| B6 | AGENTS ↔ CLAUDE sync, lines only added | ✔ AGENTS gains DEC-033/047 verbatim; CLAUDE gains fidelity + no PII/CRM (verbatim from AGENTS) and the handoff path / durable-decisions wording. **No read-list change** (that is D2) |
| B7 | templates + fences | ✔ § numbers unchanged; fences even |
| C1 | authority banners | ✔ MASTER §3.0 + duplicate-§3.4 note, LIVE ref, chat record, baseline §1, README_FIRST, GSS header |
| C2 | historical-ID banners + "check BACKLOG before a new ID" | ✔ MIGRATION §32, TOOLCHAIN §48, STUDIO_OS §56 |
| C3 | Unity 6.3 → "(superseded by DEC-003 …)" | ✔ the 3 rewritten lines keep "Unity 6.3" and add the note |
| C4 | "as built" notes | ✔ STUDIO_OS §48/§49.5, MASTER §15, INSTALL_MAP, MANIFEST, DOCS_INDEX (the ProjectHistory path line is corrected, not dropped) |
| C5 | DOCS_INDEX router | ✔ |
| C6 | DP "Ratified DEC-057" + precedence in DP and GSS | ✔ §0/§0A verbatim. GSS precedence adds DESIGN_V2 after GSS, consistent with DEC-063 (V2 is an add-on; DP wins) |
| C7 | citation key + DP-WC-00n | ✔ in DP, SLICE_DESIGN, SPEC_GAME004, reconciliation, ROADMAP; DP-0xx keeps its test meaning |
| C8 | SLICE_DESIGN "Amended by" box | ✔ body unchanged |
| C9 | KNOWN_GAPS pointer rows | ✔ COMP/PKG/DAY/PROC-07..12 + GAP-128 (dropped, REF-009b). GAP-127 was already on main |
| C10 | `Tasks/Done/INDEX.md` | ✔ all SHAs verified. **This commit adds REVIEW-W4T (bd6f517)**, merged after DOC-001 |
| C11 | DEC-P crosswalk + "DEC-05x (was DEC-Pn)" | ✔ reconciliation table; GSS, SPEC_GAME004, ROADMAP ×3, GAME-019 ×2 |
| DEC-066 m2/m3 | GAME-022 remap 25/40/25/5/5; GAP-V2-01; DESIGN_V2 rows | ✔ "was e.g. 25/40/20/10/5" kept; KNOWN_GAPS section; DOCS_INDEX + BACKLOG IMP-002 Done |

**Nothing from batches D or E:** no ART renumber (GAME-012/014 only get a "(ROADMAP ID, see DOC-002)" pointer); CLAUDE.md "Read first" unchanged (D2); REFERENCES_INDEX not split (D3); no branch-convention DEC (D4); ROADMAP "Status: proposal" unchanged (E2); no archetype row (E1, deferred per the handoff); GAME-023's scenario path untouched (E7). ✔

## Findings
- **m1 (fixed here):** the handoff says `AUDIT-001_APPROVAL.md` was cherry-picked, but only `AUDIT-001.md` is on the branch. DEC-064 and `Tasks/Done/INDEX.md` cite the approval sheet at `Docs/Audits/`. Added verbatim from 2f5765d in this commit.
- **m2 (fixed here):** BACKLOG QA-002 / QA-002b and the Done-index W4T row (see Merge).
- **n1:** HUB_RESUME step 1 changes "last ~10" to "newest ~15" DECISIONS entries. It matches PROJECT_STATE's existing wording but is a value change not listed under B5. Harmless; Hub to confirm.
- **n2:** the SPEC_GAME004 FOH fridge "Picked how" cell goes from "—" to "pick from fridge". This follows from DEC-050 (the fridge holds drinks), not new design.

## For the Hub (from the DOC-001 handoff, still open)
- PROJECT_STATE "Read with this" → "Hub: HUB_RESUME + newest DECs; workers: your packet only" (B5, Hub-owned).
- `Tasks/Active/REF-009b.md` should move to Done (BACKLOG already says Done, W4U).
- D1 is wider than the sheet says: SPEC_GAME004's header also uses ART-006 for FOH racks. Give it to DOC-002.
