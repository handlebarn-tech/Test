# AUDIT-001: read-only Markdown audit

**Base:** main `04f7bc3` (DES-003 merged, DEC-052..059 ratified). Main has since moved to `6000433` (DEC-060/061, PERF-001 packet, REVIEW-W4J, new PROJECT_STATE), so recheck the state-drift items against current main.
**Date:** 2026-10-30 · **Workcell:** AUDIT-001 · **Status:** report only. Every fix below needs Nolan's approval first.

## Scope and method
- **Files:** 167 tracked `.md` files.
  - Root 5, Docs top level 16.
  - Tasks 62: Active 7, Ready 12, Done 43.
  - Handoffs 36, Reviews 25.
  - Design 5, Specs 4, Research 4, Reconstruction 4, Assets 4, References 2.
  - `Tools/**` and `UnityProject/**` have no tracked `.md` files.
- **Reading depth:**
  - Root, state and decision docs: read in full.
  - Large canonical docs: by outline and targeted section.
  - Done tasks, Handoffs and Reviews: header and grep depth.
- **Helpers:** two read-only helper agents covered Tasks, Handoffs and Reviews, and Design, Specs, References and Assets. I spot-checked their key claims against the files.

**Rules every fix must keep:**
- DEC-033 chain of command and DEC-047 raise-uncertainty.
- HUB_RESUME hard rules and the `hub_guard` hook.
- The no-source baseline and DEC-001/002 tool authority.
- The $0 budget, no-PII and no-invented-facts rules.
- Every cited `§n` anchor and task ID.
- Append-only DECISIONS.

No fix deletes guidance. Each one adds a banner, a pointer, a crosswalk table or an "amended by" note.

---

## CRITICAL

**C1. The source-of-truth ranking contradicts DEC-001.**
- **Evidence:**
  - `Docs/MASTER_PLAN.md` §3 "Source-of-truth hierarchy" ranks the live site first (§3.1) and the chat record third (§3.3).
  - `References/LIVE_TFS_BUDTENDER_v7.11.4.md`:7 calls itself the "Highest-available behavioral reference".
  - `NO_SOURCE_RECONSTRUCTION_BASELINE.md` §1 says "strongest available behavioral source is the live deployment".
  - `README_FIRST.md` "Live behavioral reference" says to inspect the live site.
  - The `GAMEPLAY_SIMULATION_SPEC.md` header gives the chat record as its "Primary source basis".
  - DEC-001 makes the local tool source the top authority. Only one line in `CLAUDE.md` and `AGENTS.md` corrects this.
  - MASTER §3.2 and §3.4 are both titled "Explicit current project decisions".
- **Fix:**
  - Add an authority banner to each file: local v7.11.4 source (DEC-001/002/009), then DECISIONS, then live site, then chat record.
  - Insert MASTER "§3.0 Local tool source (DEC-001)" and mark §3.4 as a duplicate of §3.2. Don't renumber.
  - Don't rename the v7.11.4 file; 9 docs cite it.
- **Break risk:** low. These are header additions only.

**C2. Older plans reuse current task IDs for different work.**
- **Evidence:**
  - `UNITY_MIGRATION_PLAN.md` §32: DATA-002 means "Legacy dataset importer", and GAME-004..009 mean scorer, similarity, pricing, inventory, ledger and feedback.
  - `TOOLCHAIN_EXECUTION.md` §48: BUILD-003 means "Unity CI methods" and QA-002 means "Screenshot harness". DEC-059 covers QA-002 only.
  - `ROADMAP_POST_SLICE.md`:80/92 reuses ART-005/006 while ART-005 is the finished lookdev task. REVIEW-W4H m1 is still open.
  - ROADMAP's own DES-003 has already been renamed DES-004.
- **Fix:**
  - Put a banner on MIGRATION §32 and TOOLCHAIN §48: "historical plan IDs; live IDs are in BACKLOG; see DEC-059".
  - Renumber the ROADMAP ART rows to unused IDs with a "(was ART-005)" note.
  - Add a rule to STUDIO_OS: check BACKLOG before allocating a new ID.
- **Break risk:** medium for the ART renumber, because GAME-012/014 depend on those rows. Do it between waves, in the same commit as their dependency updates. The banners carry no risk.

**C3. A blocked task is in `Tasks/Ready/`.**
- **Evidence:** `Docs/Tasks/Ready/GAME-023.md` sits in Ready. BACKLOG says Blocked, and DEC-059 m2 says it "must not be dispatched". ROADMAP shows it as Ready.
- **Fix:** add a `**State:** BLOCKED (DEC-059)` header to the packet, or create `Docs/Tasks/Blocked/`. Fix the ROADMAP row.
- **Break risk:** none. Leaving it risks a wrong dispatch.

**C4. Ready packets copy placeholders Nolan has already answered.**
- **Evidence:**
  - `Docs/Design/SPEC_COMP002.md`:101 and `Docs/Tasks/Ready/GAME-009.md`:15 set `medicalCustomerShare` to 0.10. DEC-048 says under 5 %.
  - SPEC_COMP002 §6 cuts repeat visits "until Nolan answers (GAP-COMP-07)". DEC-049 says there is no daily limit and repeat visits are allowed.
  - SPEC_COMP002 §5 keeps the count toward the caps as a placeholder. DEC-048 answered it.
  - `SPEC_GAME004.md` §2 has two beverage coolers and a placeholder staff fridge, which contradicts DEC-041/050/051.
- **Fix:** mark each GAP "answered by DEC-0xx" inline, correct the values in a COMP/GAME doc task, and add a Hub note to GAME-009 before dispatch.
- **Break risk:** low, because GAME-009 isn't started.

**C5. Packets that can run in parallel own the same files.**
- **Evidence:**
  - GAME-008 and GAME-009 both say they "can run in parallel". Both own `Simulation/Slice`, `Presentation/Slice` and SliceConfig/SliceLines keys.
  - GAME-021 and GAME-022 both touch `Customers.cs`, through generator hooks and `CustomerGenerator`.
  - Running GAME-010 and Active GAME-006 both edit SliceConfig and the Slice tests.
- **Fix:** serialise each pair in BACKLOG and the packets (e.g. "GAME-009 after GAME-008"), or split ownership at file level. For the live GAME-006 and GAME-010, add only a merge-order note.
- **Break risk:** low if running packets are left alone.

**C6. BACKLOG no longer matches the task folders.**
- **Evidence** (`Docs/BACKLOG.md`):
  - **Shown Active but merged or in Done:** ART-003, PROC-002, BUILD-003, DES-002, PROC-004, REF-008, DATA-002 and GAME-002b.
  - **Other stale rows:** BUILD-005 and ART-005 say Ready but are merged. GAME-005's title says "(Done, W4K)" while its state says Ready.
  - **Duplicate rows:** PERF-001 and PROC-003 each appear twice.
  - **Missing rows:** UX-002, GAME-007..010, GAME-011..016 (other packets depend on them), ART-004, BUILD-004, REF-006/007/009 and AUDIT-001.
  - **Stale after the Hub's own move:** GAME-006, QA-002 and UX-005 sit in Active after `04f7bc3` but show Ready.
  - **Packets in the wrong folder:** `Tasks/Active/` still holds the merged ART-005, DATA-002 and UX-002. `Tasks/Ready/GAME-010` is running.
  - **Priorities disagree:** QA-002 is P0 in its packet, P1 in BACKLOG and P0 in ROADMAP. GAME-021/022/023 have similar mismatches.
  - BACKLOG lacks the owner and acceptance-link columns that STUDIO_OS §49.2 requires.
- **Fix:**
  - One Hub pass rebuilds the State column from the folders and merge commits, merges the duplicates and adds the missing rows.
  - Add a rule to HUB_RESUME Hub loop step 4: move the packet and edit its BACKLOG row in the same commit.
  - Use the packets and ROADMAP as the source for priority.
- **Break risk:** low. Keep IDs and dependency text verbatim, and move only idle or merged packets.

## HIGH

**H1. Startup and read-order rules disagree.**
- **Evidence:**
  - `README_FIRST.md` "Start order" preloads 9 docs, and its "First production task" is long done.
  - `CLAUDE.md` and `AGENTS.md` say not to preload.
  - `PROJECT_STATE.md` "Read with this" sends every reader to HUB_RESUME, a Hub-only doc. Workers read PROJECT_STATE first, so that is wasted context for them.
  - On which decisions the Hub reads by default: STUDIO_OS §3 and MASTER §16 say Master + State + Backlog. HUB_RESUME says the last ~10 DECs, and PROJECT_STATE says the last ~15 "through DEC-050".
  - Baseline §7 still says "Begin by indexing" all the plans.
- **Fix:**
  - Banner README_FIRST and baseline §7 as historical: current start is `CLAUDE.md`, and the Hub uses `HUB_RESUME`.
  - Change PROJECT_STATE to "Hub: also HUB_RESUME; workers: your packet".
  - Make HUB_RESUME the single owner of the Hub read set, with STUDIO_OS §3 and MASTER §16 pointing to it.
  - Replace "through DEC-050" with "newest entries".
- **Break risk:** low. Startup comes from CLAUDE.md, which stays unchanged.

**H2. AGENTS.md and CLAUDE.md have drifted apart.**
- **Evidence:**
  - AGENTS.md lacks the DEC-033 and DEC-047 rules.
  - CLAUDE.md lacks AGENTS.md's "Reality fidelity outranks…", the no-PII/CRM rule, "record durable decisions in repo docs" and the explicit handoff path `Docs/Handoffs/<TASK_ID>.md`.
- **Fix:** make one the canonical rules block and the other a mirror that says so. Add each file's missing lines to the other.
- **Break risk:** low; it only adds lines.

**H3. The packet and handoff templates are empty, and code fences are unbalanced.**
- **Evidence:**
  - `Docs/STUDIO_OS.md` §56 (line 500), §57 (506) and §60.1 (573) open a fence with no content. The file has 27 fences, an odd number, so the sections after line 500 render as code.
  - `Docs/ASSET_PRODUCTION_PLAN.md` §44 (line 2614) has the same defect and 21 fences.
  - HUB_RESUME works around it with "see the existing REF-001.md…".
  - Packet structure varies: IMP-001 has no Role/Priority/Branch, handoff limits run from ≤10 to ≤60 lines, and ART-005 lacks the DEC-033 line.
- **Fix:** restore the templates from git history, or write a short standard (Role/Priority/Branch, Read, Owns, Deliverable, Validation, Handoff, plus the DEC-033/047 line), and close the fences. Apply it to new packets only.
- **Break risk:** low. Keep the § numbers.

**H4. The canonical repo layout doesn't match the repo.**
- **Evidence:**
  - DEC-004 says layout follows STUDIO_OS §48.
  - §48, §49.5 and MASTER §15 list files and folders that don't exist: `CHANGELOG.md`, `QA_STATUS.md`, `Assets/ASSET_REGISTRY.csv`, `ATTRIBUTION.md`, `Tasks/Review/` and `README.md`.
  - The license and asset truth actually lives in `LICENSE_LEDGER.md` and `ASSET_CACHE_MANIFEST.json`.
  - `DOCS_INDEX.md` suggests `References/ProjectHistory/`, which doesn't exist.
  - `REPOSITORY_INSTALL_MAP.md` and `MANIFEST.md` describe the original handoff files, with old filenames and SHA-256 hashes.
- **Fix:** add an "as built" note mapping each planned file to its actual one (or "not adopted"), and mark INSTALL_MAP and MANIFEST as historical.
- **Break risk:** none.

**H5. The context routers miss the docs agents now need.**
- **Evidence:**
  - `DOCS_INDEX.md`, MASTER §16 and CLAUDE.md "Read first" don't mention `Docs/Design/*`, `Docs/Specs/*`, `DECISIONS.md`, `HUB_RESUME.md`, `KNOWN_GAPS.md` or `REFERENCES_INDEX.md`.
  - None names `SPEC_DECISION_PRESSURE.md`, though DEC-057 makes it canonical.
- **Fix:** add the missing rows to DOCS_INDEX as the one router, and have MASTER §16 point to it.
- **Break risk:** low. Editing CLAUDE.md changes every session's startup, so it needs Hub and Nolan sign-off.

**H6. The new decision-pressure spec has no precedence rule against GSS.**
- **Evidence:**
  - DEC-057 calls `SPEC_DECISION_PRESSURE.md` a "canonical extension", but its header still says "**Status:** Proposed canonical…".
  - The GSS header says it is canonical "unless later user decisions override it".
  - Neither doc says which wins on conflict.
- **Fix:** add a "Ratified DEC-057" banner and a precedence line to both: DECISIONS, then DP, then GSS, then SLICE_DESIGN and ROADMAP.
- **Break risk:** low. Keep DP §0/§0A verbatim.

**H7. Section and ID citations are ambiguous.**
- **Evidence:**
  - "spec §n" means GSS in ROADMAP §1 ("spec §104"), SLICE_DESIGN and SPEC_GAME004, but DP in the GAME-023 title ("spec §133"). GSS §104 and DP §104 are different topics.
  - DP-0xx means tests in §115 and workcells in §123. The reconciliation maps them inconsistently: DP-002 goes to GAME-017 in one row and to GAME-019 in another.
- **Fix:**
  - Add a citation key: "spec §n = GSS; DP §n = decision-pressure spec".
  - Cite the §123 workcells as DP-WC-00n in the reconciliation. Don't change DP's own headings.
- **Break risk:** medium. GAME-017..024 cite DP-0xx as tests, so that meaning stays.

**H8. SLICE_DESIGN is out of date and has no "amended by" markers.**
- **Evidence:** Active GAME-006 reads it.
  - §3 `priceFit` doesn't say POS total (DEC-044).
  - §4 fills every jar to 454 g (DEC-027 seeds 0.05–1.0).
  - §2.2 builds `IntentQuery` directly (DEC-057 routes it through `QueryParser`).
  - §5 star ratings are replaced by DP §106.
- **Fix:** add an "Amended by" box (DEC-027/035/036/044/057, DP §106) with inline "(see DEC-0xx)" notes. Don't rewrite the body.
- **Break risk:** low. The markers must describe what the shipped tests encode, not change it.

**H9. About 24 GAP IDs aren't in KNOWN_GAPS, and one open question isn't tracked.**
- **Evidence:**
  - GAP-COMP-01..08, GAP-PKG-01..08, GAP-DAY-01/02, GAP-PROC-07..11 and GAP-127 are defined only in specs, ROADMAP and PROC_PIPELINE.
  - DES-003 question N1 (DEC-015/016 versus DP §0A) has no GAP row.
  - `Docs/Specs/ENGINE.md`:50 presents `ParserOptions.Game` with no caveat.
- **Fix:** add pointer rows to KNOWN_GAPS (the specs stay the detail owners), add GAP-DP-03 for N1 ("DEC-015/016 stand, DEC-059"), and add a caveat line in ENGINE.md.
- **Break risk:** none.

**H10. Work went ahead without packets.**
- **Evidence:**
  - GAME-002b, BUILD-005, REF-006/007, DES-003, PROC-003, REF-009 and AUDIT-001 were briefed only by message.
  - Review packets stop after W4E: W4A, W4F–W4Q have reviews but no packets.
  - Five handoffs have no packet anywhere.
- **Fix:** add a `Docs/Tasks/Done/INDEX.md` listing each ID with its brief source and its review. Don't backfill packets.
- **Break risk:** none.

**H11. The engine version conflicts with DEC-003.**
- **Evidence:** MASTER_PLAN's header and §27 step 11, ASSET_PRODUCTION_PLAN §4, and STUDIO_OS:1103 say "Unity 6.3 LTS". DEC-003 chose 6000.6.7f1 + HDRP 17.6.0.
- **Fix:** add an inline "(superseded by DEC-003)" note.
- **Break risk:** none.

## MEDIUM

- **M1. Proposed DEC labels survive after ratification.**
  - **Where:** DEC-P1..P6 in `DES-003_RECONCILIATION.md`, `GAMEPLAY_SIMULATION_SPEC.md`:953 ("proposed DEC", now DEC-053), `SPEC_GAME004.md`:53, `ROADMAP_POST_SLICE.md`:67/95 and `Tasks/Ready/GAME-019.md`:9/15.
  - **Fix:** add a "Ratified as" crosswalk (P1→052 … P6→057) and swap inline to "DEC-05x (was DEC-Pn)".
  - **Break risk:** none, as long as both IDs stay greppable.
- **M2. Branch naming doesn't match practice.**
  - **Where:** DEC-005, STUDIO_OS §54 and the packets say `task/<ID>`; real branches are `claude/task-<id>-<hash>`.
  - **Fix:** record the real convention in a DEC amendment.
  - **Break risk:** don't rename existing branches.
- **M3. Three customer-archetype lists, with no mapping.**
  - **Where:** SLICE_DESIGN §2.1, GSS §11/§28 and DP §11.
  - **Fix:** a mapping row in the reconciliation, kept as a GAP until the Hub rules.
- **M4. ROADMAP's status column duplicates BACKLOG and has drifted.**
  - **Where:** the header still says "Status: proposal".
  - **Fix:** "see BACKLOG", or stamp it "as of <sha>".
- **M5. PROJECT_STATE goes stale fast.**
  - **Where:** it is a hand-kept session table with hard-coded session ids and a build folder.
  - **Fix:** stamp "as of <sha/time>" and add "verify with list_sessions". Keep the ids.
- **M6. LICENSE_LEDGER and ACQUISITION_LIST say "No assets downloaded".**
  - **Where:** both headers; `ASSET_CACHE_MANIFEST.json` has 249 entries.
  - **Fix:** a header stating the manifest is the download truth and the ledger is the license truth.
- **M7. Two documents do several jobs.**
  - **Where:** `REFERENCES_INDEX.md` (60 KB) and `ASSET_PRODUCTION_PLAN.md` (106 KB).
  - **Fix:** split REFERENCES_INDEX with a §-to-file stub, and give DP (80 KB) a section-to-packet index.
  - **Break risk:** medium, because every `§n` must survive.
- **M8. Counts and hashes are copied across docs.**
  - **Where:** md5 228684e9 in DEC-002, RECONSTRUCTION_CONTRACT and GOLDEN_CASES; "1207 batches" in four docs. Packets copy DEC numbers too (25.1 %, 28 g, 70.87 g, 0.25, `customersPerShift` 16).
  - **Fix:** point to DATA_SCHEMA §1 as the pinned block, and have new packets cite the DEC or config key.
- **M9. Older asset and research docs aren't marked as superseded.**
  - **Where:** GRAYBOX.md:23 (4 POS monitors versus DEC-039/040), PROC_PIPELINE:71 (F010 versus DEC-046), OFFICE_FILE_LEADS ("Nothing downloaded"), and GSS §70 (20–45 min versus DEC-056).
  - **Fix:** one-line "Amended by" notes.
- **M10. Packet paths disagree.**
  - **Where:** QA-002 owns `Data/Tests/DpScenarios/` versus GAME-023's `Data/Scenarios/…`; GAME-018 cites `EngineFeatureTests` as a file (it's a class in `ParserGoldenTests.cs`).
  - **Fix:** align GAME-023 to QA-002, which is running.
- **M11. Packets don't follow the CLAUDE.md read order.**
  - **Where:** no packet lists PROJECT_STATE, and only DATA-002 lists CLAUDE.md.
  - **Fix:** a fixed header block on new packets only.
- **M12. DEC-059 n1 has no BACKLOG row.**
  - **Where:** "fast recommendation" in GSS §28.
  - **Fix:** add the row.
- **M13. STUDIO_OS cites vendor guidance URLs and jumps from §3 to §48.**
  - **Fix:** a one-line note that the numbering is inherited.

## LOW

- **L1.** DEC-041/042/043 cite moved `References/Incoming/...` image names. Map them in REFERENCES_INDEX §0 instead, since DECISIONS is append-only.
- **L2.** `Handoffs/RES-001.md`:21 "Questions put to Nolan" predates DEC-033. Add a historical note.
- **L3.** BUILD_STATUS and MACHINE_PROFILE are frozen at 2026-10-29. Stamp them as snapshots and point to `studio.ps1 doctor`.
- **L4.** ART-005.md:3 pins `fa48849` and IMP-001.md:5 says "28 files, ~330 KB". New packets should say "off current main".
- **L5.** DECISIONS has a stray blank line between DEC-051 and DEC-052.
- **L6.** The 63 KB chat record has no "subordinate to DEC-001" banner; covered by C1.
- **L7.** OFFICE_FILE_LEADS names internal M365 folder paths. They aren't PII; the Hub should confirm they're acceptable under DEC-031.
- **L8.** The sibling note `GAME-001-engine-api.md` in the shared notes folder (outside the repo) is stale.
- **L9.** Done packets and handoffs are lean and not loaded by default, so no action is needed.

**Clean:**
- No DEC-033 violations: no packet tells a worker to ask Nolan.
- No invented store or inventory facts, and no PII, in DP or GSS.
- Every cited DEC from 001 to 059 exists.

## Questions for Nolan (through the Hub)
1. **Approval of the batches.** Suggested order:
   - First, dispatch safety: C3/C4/C5.
   - Then state and startup: C6/H1/H2.
   - Then authority and routing: C1/C2/H5–H9.
   - Last, the Medium and Low items.
2. **CLAUDE.md read list (H5).** Should it add `SPEC_DECISION_PRESSURE.md` and DECISIONS? That changes every session's startup.
3. **Archetype mapping (M3).** Does slice "Regular" mean DP "Decisive regular" or "Normal customer"? The Hub may rule.

## Not covered
- I didn't read the body text of the chat record, UX_SLICE, LOGIC_TRIAGE, GOLDEN_CASES or AZ_COMPLIANCE line by line.
- Done tasks, Handoffs and Reviews were read at header and grep depth only.
- I didn't verify the reconciliation's per-row counts.

---
READ-ONLY AUDIT. This report is the only file added (at the Hub's request). No existing project files were modified. Documentation changes require Nolan approval.
