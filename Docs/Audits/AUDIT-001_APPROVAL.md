# AUDIT-001 — Approval sheet for Nolan

**Source:** `Docs/Audits/AUDIT-001.md` (run at `04f7bc3`). **Rechecked against main `4fcf7a7`.**
**Rule:** no doc changes until Nolan approves. Every fix only adds a note, a pointer or a table, or corrects a value. None removes a rule or context.
**Tick** a batch to approve all of it, or tick single fixes. An unticked item stays as it is.

Status key:
- **open:** still needed.
- **partly done:** main fixed part of it.
- **already done:** nothing left to do.
- **safe:** docs only, no effect on running sessions.
- **risky:** touches IDs, startup or files that live sessions use.

---

## Batch A — Stop wrong work being started (do first)  [ ] approve batch

- [ ] **A1 (C3). Mark GAME-023 Blocked in its own packet.** *Partly done.*
  - **Files:** `Tasks/Ready/GAME-023.md` header; the GAME-023 row in `Design/ROADMAP_POST_SLICE.md`.
  - **Recheck:** BACKLOG and DEC-059 already say Blocked, but the packet in `Ready/` doesn't. It still reads like work that can start.
  - **Risk:** safe.
- [ ] **A2 (C4). Correct the values Nolan has already answered.** *Open.*
  - **Files:** `Tasks/Ready/GAME-009.md`:15, `Design/SPEC_COMP002.md`:101, §5 and §6, `Design/SPEC_GAME004.md` §2.
  - **Changes:**
    - Medical share 0.10 becomes under 5 % (DEC-048).
    - Repeat visits change from cut to allowed (DEC-049).
    - The count toward the caps follows DEC-048.
    - FOH fridge and cooler follow DEC-050/062.
  - **Risk:** safe. GAME-009 hasn't started.
- [ ] **A3 (C5). Run the tasks that edit the same files one after the other.** *Open.*
  - **Files:** `Tasks/Ready/GAME-008.md`, `GAME-009.md`, `GAME-021.md`, `GAME-022.md`; `BACKLOG.md` dependency column.
  - **Changes:**
    - GAME-009 after GAME-008, and GAME-022 after GAME-021.
    - GAME-006 and GAME-010, both running, only get a merge-order note.
  - **Risk:** safe, as long as the running packets stay untouched.

## Batch B — Fix the task list and startup instructions  [ ] approve batch

- [ ] **B1 (C6). Rebuild BACKLOG's State column from the task folders and merges.** *Open; worse since the audit.*
  - **File:** `Docs/BACKLOG.md`.
  - **Recheck:**
    - Merged tasks still show Ready or Active: UX-002, ART-005, DATA-002, PERF-001 and others.
    - GAME-006, QA-002 and UX-005 show Ready.
    - ART-006 and REF-009b have no rows.
    - PERF-001 and PROC-003 rows are duplicated.
  - **Changes:** merge the duplicate rows and add the missing ones.
  - **Risk:** safe. IDs and dependency text are kept verbatim.
- [ ] **B2 (C6). Add one rule to the Hub loop: move a task packet and update its BACKLOG row in the same commit.**
  - **File:** `HUB_RESUME.md` Hub loop step 4.
  - **Risk:** safe.
- [ ] **B3 (C6). Move GAME-010's packet from `Tasks/Ready/` to `Tasks/Active/`.** It is running.
  - **Recheck:** the merged packets have already left `Active/` (*partly done*).
  - **Risk:** safe. It actually fixes the path in CLAUDE.md for that session.
- [ ] **B4 (H1). Label README_FIRST's 9-doc start list and the baseline's §7 as historical.** Point both to `CLAUDE.md` for workers and `HUB_RESUME` for the Hub.
  - **Files:** `README_FIRST.md`, `NO_SOURCE_RECONSTRUCTION_BASELINE.md`.
  - **Risk:** safe. Only a banner is added; no text is removed.
- [ ] **B5 (H1). Give workers their own read line in PROJECT_STATE.** *Open: it still says "through DEC-050".*
  - **Change:** "Read with this" becomes "Hub: HUB_RESUME + newest DECs; workers: your packet only".
  - **Files:** `PROJECT_STATE.md`; make HUB_RESUME the one owner of the Hub reading list, with `STUDIO_OS.md` §3 and `MASTER_PLAN.md` §16 pointing to it.
  - **Risk:** safe.
- [ ] **B6 (H2). Sync AGENTS.md and CLAUDE.md, adding only the lines each is missing.**
  - **To AGENTS.md:** the DEC-033 and DEC-047 rules.
  - **To CLAUDE.md:** the AGENTS.md lines on reality fidelity, no PII/CRM, recording decisions in repo docs, and the handoff path.
  - **Risk:** low. It adds lines to every session's startup file; nothing is removed.
- [ ] **B7 (H3). Restore the empty packet, handoff and asset-spec templates, and close the broken code fences.**
  - **Files:** `STUDIO_OS.md` §56, §57 and §60.1; `ASSET_PRODUCTION_PLAN.md` §44.
  - **Risk:** safe. The § numbers stay.

## Batch C — Make clear which document wins  [ ] approve batch

- [ ] **C1 (C1). Add an authority banner: local tool, then DECISIONS, then live site, then chat record (DEC-001/002/009).**
  - **Files:** `MASTER_PLAN.md` §3 (add a §3.0 and mark the duplicate §3.4), `References/LIVE_TFS_BUDTENDER_v7.11.4.md`, `NO_SOURCE_RECONSTRUCTION_BASELINE.md` §1, `README_FIRST.md`, `GAMEPLAY_SIMULATION_SPEC.md` header, and the chat record.
  - **Risk:** safe. No files are renamed.
- [ ] **C2 (C2, banners only). Label the old plan task-ID lists as historical, and add a "check BACKLOG before giving out a new ID" rule.**
  - **Files:** `UNITY_MIGRATION_PLAN.md` §32, `TOOLCHAIN_EXECUTION.md` §48 (the QA-002 part follows DEC-059), `STUDIO_OS.md`.
  - **Risk:** safe.
- [ ] **C3 (H11). Add "(superseded by DEC-003: Unity 6000.6.7f1)" next to each "Unity 6.3 LTS".**
  - **Files:** `MASTER_PLAN.md` header and §27, `ASSET_PRODUCTION_PLAN.md` §4, `STUDIO_OS.md`:1103.
  - **Risk:** safe.
- [ ] **C4 (H4). Add an "as built" note to the planned repo layout:** which planned files exist, which don't, and what replaced them (e.g. LICENSE_LEDGER plus ASSET_CACHE_MANIFEST instead of ASSET_REGISTRY.csv). Label INSTALL_MAP and MANIFEST as historical.
  - **Files:** `STUDIO_OS.md` §48 and §49.5, `MASTER_PLAN.md` §15, `REPOSITORY_INSTALL_MAP.md`, `MANIFEST.md`, `DOCS_INDEX.md`.
  - **Risk:** safe.
- [ ] **C5 (H5). Add the missing docs to DOCS_INDEX and make it the one router.** The missing docs: Design, Specs, DECISIONS, HUB_RESUME, KNOWN_GAPS, REFERENCES_INDEX and the decision-pressure spec. MASTER §16 then points to DOCS_INDEX.
  - **Files:** `DOCS_INDEX.md`, `MASTER_PLAN.md` §16.
  - **Risk:** safe. The CLAUDE.md read list is item D2.
- [ ] **C6 (H6). Mark the decision-pressure spec "Ratified DEC-057" and add a precedence line to it and to the gameplay spec:** DECISIONS, then decision-pressure spec, then gameplay spec, then SLICE_DESIGN and ROADMAP.
  - **Files:** `Design/SPEC_DECISION_PRESSURE.md` header, `GAMEPLAY_SIMULATION_SPEC.md` header.
  - **Risk:** safe. §0 and §0A stay verbatim.
- [ ] **C7 (H7). Add a citation key, "spec §n = GAMEPLAY_SIMULATION_SPEC; DP §n = decision-pressure spec", and refer to the workcell list in the decision-pressure spec's §123 as DP-WC-00n.**
  - **Files:** `ROADMAP_POST_SLICE.md`, `Specs/SLICE_DESIGN.md`, `Design/SPEC_GAME004.md`, `Design/DES-003_RECONCILIATION.md`.
  - **Risk:** low. DP-0xx keeps its test meaning, which the GAME-017..024 packets rely on.
- [ ] **C8 (H8). Add an "Amended by" box to SLICE_DESIGN** listing DEC-027/035/036/044/057 and DP §106, with inline "(see DEC-0xx)" notes. The body text isn't rewritten.
  - **File:** `Specs/SLICE_DESIGN.md`.
  - **Risk:** safe. The notes describe what the shipped tests already encode.
- [ ] **C9 (H9). Add pointer rows to KNOWN_GAPS for the unregistered GAP IDs.** These are GAP-COMP, GAP-PKG, GAP-DAY, GAP-PROC-07..12 and GAP-127; the specs keep the detail.
  - **Recheck:** *partly done*. N1 and N2 were answered (DEC-060/061), so the proposed GAP-DP-03 row and the ENGINE caveat are no longer needed.
  - **File:** `KNOWN_GAPS.md`.
  - **Risk:** safe.
- [ ] **C10 (H10). Add `Tasks/Done/INDEX.md` listing tasks that ran without a packet, with each one's brief source and its review.**
  - **Tasks:** GAME-002b, BUILD-005, REF-006/007, DES-003, REF-009, AUDIT-001, and the reviews W4A, W4F–W4S and IMP1.
  - **Risk:** safe.
- [ ] **C11 (M1). Add a crosswalk table mapping DEC-P1..P6 to DEC-052..057, and change inline mentions to "DEC-05x (was DEC-Pn)".**
  - **Files:** `Design/DES-003_RECONCILIATION.md`, `GAMEPLAY_SIMULATION_SPEC.md`:953, `SPEC_GAME004.md`:53, `ROADMAP_POST_SLICE.md`:67/95, `Tasks/Ready/GAME-019.md`.
  - **Risk:** safe.

## Batch D — Risky: do between waves only, never while the affected sessions run  [ ] approve batch

- [ ] **D1 (C2). Renumber the ROADMAP's ART-005 and ART-006 rows to unused IDs, with "(was …)" notes, and update GAME-012/014's dependencies in the same commit.**
  - **Recheck:** worse since the audit. ART-006 is now a real Active task (back rooms + bud materials), while ROADMAP line 92 still uses ART-006 for FOH racks.
  - **Risk:** risky. GAME-012/014 depend on these IDs.
- [ ] **D2 (H5). Add `SPEC_DECISION_PRESSURE.md` and DECISIONS to CLAUDE.md's "Read first" list, as "only the referenced sections".**
  - **Risk:** risky. It changes every session's startup.
- [ ] **D3 (M7). Split the 60 KB REFERENCES_INDEX into `Docs/References/*.md`, keep a stub that maps each old § to its new file, and add a section-to-task index to the decision-pressure spec.**
  - **Risk:** risky. Every cited § must still resolve.
- [ ] **D4 (M2). Record the real branch convention, `claude/task-<id>-<hash>`, in a DEC amendment, and have new packets say "branch per HUB_RESUME".**
  - **Risk:** risky for existing branches, so none are renamed.

## Batch E — Medium and Low cleanup  [ ] approve batch

- [ ] **E1 (M3). Add a row mapping the three customer-type lists to each other, labelled a GAP until ruled.**
  - **Files:** `DES-003_RECONCILIATION.md`; see Q3 below.
  - **Risk:** safe.
- [ ] **E2 (M4). Change ROADMAP's status column to "see BACKLOG", and its "Status: proposal" to "ratified DEC-057".** File: `ROADMAP_POST_SLICE.md`. **Risk:** safe.
- [ ] **E3 (M5). Stamp PROJECT_STATE's session table "as of <sha/time>; verify with list_sessions".** File: `PROJECT_STATE.md`. **Risk:** safe.
- [ ] **E4 (M6). Add a header saying ASSET_CACHE_MANIFEST is the download record and the ledger is the license record, and label both lists as ASSET-001 snapshots.** Files: `Assets/LICENSE_LEDGER.md`, `Assets/ACQUISITION_LIST.md`. **Risk:** safe.
- [ ] **E5 (M8). Make DATA_SCHEMA §1 the one place for the md5 and the "1207 batches" count; have new packets cite DEC or config keys instead of copying numbers.** Files: `Specs/ENGINE.md`, `Reconstruction/RECONSTRUCTION_CONTRACT.md`, `GOLDEN_CASES.md`. **Risk:** safe.
- [ ] **E6 (M9). Add one-line "Amended by DEC-0xx" notes to old asset and research docs.** *Partly done:* PROC_PIPELINE gained a DEC-046 section, but line 71 still says F010 "reads as empty".
  - **Files:** `Assets/Specs/GRAYBOX.md`:23, `PROC_PIPELINE.md`:71, `Research/OFFICE_FILE_LEADS.md`, GSS §70.
  - **Risk:** safe.
- [ ] **E7 (M10). Align GAME-023's scenario path to QA-002's `Data/Tests/DpScenarios/`, and fix the `EngineFeatureTests` reference in GAME-018.** Files: `Tasks/Ready/GAME-023.md`, `GAME-018.md`. **Risk:** safe; neither has started.
- [ ] **E8 (M11, H3). Give new packets a fixed header: "Read CLAUDE.md → PROJECT_STATE → this packet; questions go to the Hub (DEC-033/047)".** It applies to new packets only. **Risk:** safe.
- [ ] **E9 (M12). Add a BACKLOG row for DEC-059 n1, "fast recommendation" in GSS §28.** **Risk:** safe.
- [ ] **E10 (L1–L5). Small stale items:**
  - DEC-041..043 image paths mapped in REFERENCES_INDEX §0.
  - A historical note on RES-001's "Questions put to Nolan".
  - Snapshot stamps on BUILD_STATUS and MACHINE_PROFILE.
  - Drop pinned base SHAs from new packets.
  - Remove the stray blank line in DECISIONS.
  - **Risk:** safe.
- [ ] **E11 (L7). The Hub confirms that the internal M365 folder paths in OFFICE_FILE_LEADS are acceptable under DEC-031.** This is a ruling, not an edit. **Risk:** none.

Already done on main, so dropped from the sheet:
- GAP-DP-01 and N1 closed (DEC-060/061).
- Merged packets moved out of `Tasks/Active/`.
- QA-002 ID ruling (DEC-059).
- GAME-023 recorded as Blocked in BACKLOG and DEC-059 (the packet header is still A1).

---

## Open questions, with recommended answers

1. **Which batches go ahead?**
   - **Recommendation:** approve A now, then B and C together, which are all safe.
   - Approve D only for the next gap between waves.
   - Approve E as one low-priority docs task.
2. **Should CLAUDE.md's "Read first" list add the decision-pressure spec and DECISIONS (D2)?**
   - **Recommendation:** yes, worded as "only the sections your packet cites", and done between waves.
   - This keeps the no-preload rule, and stops workers missing ratified DECs.
3. **Customer types: does the slice's "Regular" mean the new spec's "Decisive regular" or its "Normal customer"?**
   - **Recommendation:** "Normal customer" (0.60). The slice Regular knows roughly what it likes but isn't scripted.
   - The new "Decisive regular" (0.20) is a separate repeat-customer type that arrives with GAME-021.
   - This is a design call the Hub can make; it needs Nolan only if he disagrees.
