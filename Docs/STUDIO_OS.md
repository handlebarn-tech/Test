# DISPENSARY GAME — STUDIO OPERATING SYSTEM
## Multi-Agent Hub, Workcells, Context Lifecycle, Reviews & Repository Memory

**Version:** 4.0 (§0 rewritten by RECOVERY-001, DEC-138..142: Hub = project manager, workers, fresh reviewers; §1+ historical)  
**Date:** 2026-10-30  
**Parent:** `MASTER_PLAN.md`  
**Target environments:** Claude Code, Codex-style coding agents, or comparable repository-capable agent systems

---

# 0. OPERATING MODEL: Nolan → Hub (project manager) → workers → fresh reviewers → Hub integrates (DEC-116/117, DEC-138..142, current)

> **This section is the only live rules text in this file.** §1 down is history from earlier structures (workcell pool, department leads, dispatcher-only Hub) and is superseded wherever it differs. Still-live *reference* sections: §48 repository layout, §56–57 templates, §63–65 acceptance gates, §67 task IDs, §68 priorities, §73–76 asset acquisition, licences and reference confidence. Do not restate these rules elsewhere; point here. Universal rules every agent gets automatically are in the root `CLAUDE.md`; the Hub's loop and hard rules are in `Docs/HUB_RESUME.md`; the stable project picture is `Docs/PROJECT_BRIEF.md`. The reasoning behind this model: `Docs/Audits/RECOVERY-001.md` and `Docs/Research/AGENT_OPERATIONS_RESEARCH_2026-10-30.md`.

## 0.1 Roles
- **Nolan:** owner. Decides product, real-store facts, scope, irreversible moves. Reaches the studio through the Hub chat; until he designates a new PO session, the Hub batches questions for him in a `FOR NOLAN` block at the end of its replies (DEC-144).
- **Hub** (`Dispo Game studio hub`, main checkout, restartable): project manager with ultimate operational authority under Nolan (DEC-139). Prioritises, writes packets, dispatches, answers worker questions from the registries, starts reviewers, integrates accepted work, keeps `PROJECT_STATE.md`/`BACKLOG.md`/`DECISIONS.md`/`KNOWN_GAPS.md` routing/roadmap scope current, escalates. Does no production work (`hub_guard.py`, DEC-045). Its conversation is never project memory.
- **Worker:** fresh session (or background Agent in a worktree on peer-triggered turns), one packet, one branch, one deliverable. Full authority over implementation inside its `Owns`. Reports to the Hub only.
- **Reviewer:** fresh per review, archived after the verdict. Verifies against the packet and the cited sources; never manages, never edits the worker's branch. Model by the character of the review (DEC-143).
- **Specialist:** a worker whose packet is research, audit, intake mapping or a spec (REF, RES, AUDIT, IMP, DES, DOC). Same lifecycle as a worker.
- There are no leads, departments, standing reviewers, planner sessions, integrator sessions or spare sessions (DEC-112/116/138).

## 0.2 Sources of truth
| Need | Authority |
|---|---|
| Stable project picture (what, constraints, Nolan's directives, systems map, glossary) | `Docs/PROJECT_BRIEF.md` (Hub-owned; changes only when a durable fact changes) |
| Live studio state: in flight, queue, recovery, open Nolan items, builds | `Docs/PROJECT_STATE.md` (Hub writes it; running sessions in `list_sessions` and `git branch --no-merged main` win over its tables) |
| The plan: milestones, task IDs, dependencies, critical path | `Docs/Design/ROADMAP_POST_SLICE.md` (no task state; Hub edits scope, DEC-119) |
| Task registry and lifecycle | `Docs/BACKLOG.md` (ID, title, deps, state incl. Later/Blocked/Dropped); packet location `Tasks/Ready` → `Active` → `Done` is the executable state, mirrored in the same commit |
| Ratified decisions | `Docs/DECISIONS.md` (append-only; newest wins; superseded chains listed in `Docs/HISTORY.md`) |
| Unknowns / placeholders | `Docs/KNOWN_GAPS.md` |
| Real-store facts and dimensions | `Docs/REFERENCES_INDEX.md`, `Docs/Reference/*.json`, `References/`, `Docs/Research/`, `Docs/Handoffs/REF-008.md`, DECs |
| Recommendation logic | the TFS tool source (DEC-001/002), then `Docs/Reconstruction/` |
| Gameplay / UX / asset specs | `Docs/Specs/`, `Docs/Design/`, `Docs/Assets/Specs/` as the packet cites |
| History (never updated after the fact) | `Docs/Handoffs/`, `Docs/Reviews/`, `Docs/Audits/`, `Docs/HISTORY.md`, git log and the tag `pre-recovery-2026-10-30` |
Rules live in `CLAUDE.md`, `HUB_RESUME.md` and this section; the picture lives in `PROJECT_BRIEF.md`; state lives in `PROJECT_STATE.md`; facts live in the registries. Nothing is copied between them: packets and briefs cite path + §. If a fact appears in two places, the registry wins and the other copy is deleted, not updated.

## 0.3 Read sets
| Role | Reads at start | On demand | Never |
|---|---|---|---|
| Hub | `CLAUDE.md` (automatic), `PROJECT_BRIEF.md`, `HUB_RESUME.md`, `PROJECT_STATE.md`, newest ~5 DECs, Ready/Active BACKLOG rows, `git log`/branches/sessions | a packet it writes or fixes; the Validation / Not-done / For-the-Hub sections of a handoff and the Verdict/MAJOR/minor sections of a review it integrates; the exact spec § a ruling needs; DECISIONS/KNOWN_GAPS by grep | code, assets, images, logs, transcripts, whole specs, worker reasoning |
| Worker | `CLAUDE.md` (automatic), its packet, the exact docs/§ the packet cites | repo files the task needs; registries in §0.2 when resolving uncertainty (§0.6) | `PROJECT_STATE.md`, `BACKLOG.md`, other packets, `Docs/Departments/`, this file below §0 |
| Reviewer | `CLAUDE.md`, the packet, the diff, the handoff's Validation and Not-done sections, the acceptance sources the packet cites | the registries to check a cited fact | the worker's reasoning, the Hub's opinion, `PROJECT_STATE.md` |

## 0.4 Packets (one per task; template §56)
A packet is the worker's whole brief: goal, `Owns`, deliverable, validation, the exact citations to read, the base (`main` @ sha or a named branch). Facts, rules and decisions are cited by path + §/ID, never pasted. **The Hub writes it** in `Docs/Tasks/Ready/` (30–80 lines; a specialist packet may be longer). The worker's first commit moves it to `Active/`; the Hub moves it to `Done/` with the BACKLOG row in the integration commit. A packet is not edited while its worker runs, except to prevent lost work; follow-ups get a new packet or ride the FAIL review. Allocate IDs only after checking `BACKLOG.md` (§56 note).

## 0.5 Session mechanics
- On Nolan's own turns the Hub uses `start_session` (`context: "fresh"`, `use_worktree: true`, title `Dispo · <ID> <what>`; model by the character of the work: cheaper for bounded, deterministic work, strongest for ambiguous, architectural, cross-system, high-risk or judgment-heavy work, DEC-143). On turns another session or an event triggered, the app refuses `start_session`; the Hub then runs the same brief as a background `Agent` with `isolation: "worktree"` (DEC-139). No spare sessions, no proposal cards unless Nolan asks.
- Standard briefs (whole text, fill the brackets):
  - **Worker:** *"Read `Docs/Tasks/Ready/<ID>.md` and follow it; your first commit moves it to `Docs/Tasks/Active/`. Base: `<main @ sha | branch>`. Commit with `git -c user.name=Nolan_Bradford -c user.email=handlebarn@gmail.com commit`. Resolve uncertainty per `Docs/STUDIO_OS.md` §0.6; never contact Nolan. When done: write `Docs/Handoffs/<ID>.md` (§57), `git merge main` into your branch and fix conflicts, re-run the packet's validation, stop background monitors and processes, commit, then send the Hub ONE line: `<ID> ready for review: <branch> @ <sha>`."*
  - **Fix round (same or fresh worker):** *"FAIL: fix per `Docs/Reviews/REVIEW-<ID>.md` on `<branch>`; merge `main` first; append the fix to the handoff; report `ready for review` again."*
  - **Reviewer:** *"Review `<branch>` @ `<sha>` against `Docs/Tasks/Active/<ID>.md`. First check: `git merge-base --is-ancestor main <branch>`; if false, write a one-line FAIL `rebase on main` and stop. Then read the packet, the diff, the Validation and Not-done sections of `Docs/Handoffs/<ID>.md`, and the acceptance sources the packet cites; run the packet's validation yourself. Write `Docs/Reviews/REVIEW-<ID>.md` (§0.7) on `review/<id>` cut from `main` with the worker branch merged `--no-ff`; one line to the Hub: `REVIEW-<ID>: PASS|PASS with minors|FAIL, <n> MAJOR, <n> minor`. Do not change the worker's branch or message the worker. Stop background monitors before reporting."*
- Unity: max 2 editors (DEC-013), `studio.ps1 slots`; fresh worktrees copy `Tools/Studio/studio.config.example.json` → `studio.config.json` and run `git lfs pull` before any Unity validation (REVIEW-ART008 m1).
- Context ceiling ~300k tokens per session (DEC-102; an upper bound, hand over earlier on context pressure, DEC-143): a worker that passes it writes a partial handoff, commits, and reports `blocked: context`; the Hub starts a fresh worker from the branch.
- Archive a session only after its final report, one attempt (DEC-133 item 2). Workers nest under the Hub.
- Caps (DEC-140/143): 4 concurrent worker/reviewer sessions plus the Hub, 2 Unity editors, no overlapping `Owns`. Nolan can change the numbers.

## 0.6 Uncertainty and escalation (worker)
1. **Resolve it yourself first.** Search, in order: the docs the packet cites → `Docs/DECISIONS.md` (grep the topic; newest wins) → `Docs/KNOWN_GAPS.md` → for layout, size, distance or hardware: the floor plan / TI drawings, `ROOM_FIXTURES.json`, `DOORS.json`, CCTV (DEC-110) → `Docs/Research/`, `Docs/Handoffs/REF-008.md`. If any answers it, apply and cite. A question Nolan answered, skipped or left unanswered is never asked again (DEC-105).
2. **Not found:** use a labelled GAP placeholder, keep working, and list it in the handoff under `## Questions for Nolan (through the Hub)` with the sources searched. A question without the search list is sent back.
3. **Message the Hub at once only for:** scope change; an edit needed outside your `Owns`; two authoritative sources that contradict each other; risk of lost or corrupted work; a blocked dependency; context above ~300k. Everything else waits for the handoff.
4. **Nobody below the Hub talks to Nolan** (DEC-033/098). Mark anything he must know or decide `FOR NOLAN` in the handoff; the Hub forwards it, batched (DEC-144). If Nolan writes to you directly, answer fully and record it in the handoff.
5. **Truth files are Hub-only** (DEC-141): `CLAUDE.md`, `AGENTS.md`, `Docs/HUB_RESUME.md`, `Docs/PROJECT_BRIEF.md`, `Docs/PROJECT_STATE.md`, `Docs/STUDIO_OS.md`, `Docs/DECISIONS.md`, `Docs/Design/ROADMAP_POST_SLICE.md`. Propose changes in `## For the Hub` or as a file under `Docs/Proposals/<ID>_<topic>.md`; the Hub applies them. `KNOWN_GAPS.md` rows and `BACKLOG.md` rows named in your packet's `Owns` you may edit.

## 0.7 Review
- Every code/asset/data change is reviewed by a fresh reviewer before `main`. Hub-written tracking and rule files are the exception.
- Check 0: the branch contains current `main` (else instant FAIL "rebase on main", no further reading). Check 1: each store value cites a source or is a labelled GAP; an uncited value is a MAJOR (DEC-047). Then the packet's acceptance items and validation, run by the reviewer.
- Verdict file `Docs/Reviews/REVIEW-<ID>.md`: header (branch @ sha, merge base, sources read), `## Verdict: PASS | PASS with minors | FAIL`, `## Checks`, `## MAJOR` (blocks merge), `## minor` (the Hub routes each to a row or a fix before merge). A FAIL names the failing acceptance item; it never prescribes the implementation.
- The reviewer reports to the Hub only. PASS → the Hub integrates. FAIL → the Hub forwards the review path to the worker (or a fresh worker). A second FAIL on the same MAJOR goes to the Hub for a decision, not a third blind round.

## 0.8 Integration and state update (Hub, one commit per accepted task, DEC-138)
In the main checkout, on `main`:
1. `git merge --no-ff review/<id>` (or the reviewed branch) with the project git identity. If it conflicts, SendMessage the worker `merge main and report again`; do not resolve production files in the Hub.
2. Move the packet `Active/` → `Done/`; set the BACKLOG row to Done.
3. Append the DEC/GAP entries proposed in the handoff's `## For the Hub` and the review after checking them against the registries (grep; newest wins). List verified `FOR NOLAN` items under PROJECT_STATE "Open with Nolan" and raise them in the Hub's next reply `FOR NOLAN` block, batched (DEC-144).
4. **Track:** route review minors to rows; new legitimate work gets a BACKLOG row (ID, deps, Later or Ready); obsolete rows become `Dropped (reason)`; rows whose dependencies are all Done move to Ready (write the packet) and into the PROJECT_STATE queue. If a milestone's P0/P1 rows are all Done, mark it closed in the roadmap, queue its build (§91) and open the next milestone.
5. Update `PROJECT_STATE.md`: remove the in-flight row, order the queue, note a due build. Update `PROJECT_BRIEF.md` only if a durable fact changed.
6. Commit; archive the worker and reviewer after their final reports; dispatch the next queue items within the caps.
Handoffs and reviews are never edited afterwards; corrections are new entries in the registries.

## 0.9 Hub restart and recovery
A new Hub reads `PROJECT_BRIEF.md`, `HUB_RESUME.md`, `PROJECT_STATE.md`, then reconciles with `list_sessions` (linked and unlinked), `git branch --no-merged main` and `git status` of dirty worktrees; it corrects `PROJECT_STATE.md` itself and continues the loop. No chat history is ever needed; if it seems to be, `PROJECT_STATE.md` was left stale and the Hub fixes it. Sessions briefed under older rules are replaced, not resumed. Any older text or file can be read from git (`Docs/HISTORY.md` lists where); nothing is deleted to make room.

---


# 1. Purpose

This document defines **how agents work**, not what the dispensary looks like or how recommendation math works.

The core design is:

> **Thin persistent Hub + short-lived specialist workcells + repository-backed memory + independent review.**

The repository is the source of durable project knowledge.

A conversation is a temporary work surface.

---

# 2. Current agent-platform design principles

The studio structure intentionally follows modern agentic-coding practices:

- keep root instruction files concise;
- use them as maps to deeper documentation;
- store project knowledge in structured repository docs;
- use separate worktrees/contexts for independent work;
- break complex work into phase/task files;
- capture material decisions/context in files;
- use independent review;
- reset/replace contexts when they become stale.

Official references for future maintainers:

- OpenAI, “Harness engineering: leveraging Codex in an agent-first world”  
  https://openai.com/index/harness-engineering/
- OpenAI, “Iterating Development Workflows with Codex”  
  https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex
- OpenAI Help, Codex plan/CLI features including multi-agent tools and worktrees  
  https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
- Anthropic, “Claude Code: Best practices for agentic coding”  
  https://www.anthropic.com/research/claude-code-best-practices
- Anthropic advanced patterns guidance: keep `CLAUDE.md` small and use scoped rule files when needed.

---

# 3. Document-loading policy

> **Current reading sets: §0.6 (DEC-094).** The list below is the original policy, kept for context.

Hub default:
- Master Plan
- Project State
- Backlog

Hub loads Migration Plan only when:
- planning/reviewing port work.

Hub loads Asset Plan only when:
- planning/reviewing art/asset work.

Workers:
- read task packet;
- read only referenced document sections;
- inspect needed repository files.

Reviewers:
- read task + handoff + changed files + exact acceptance sources.

No worker is rewarded for reading everything.

---

# 48. MASTER REPOSITORY STRUCTURE

> **As built (AUDIT-001 C4, DEC-064):** the repo follows this layout with these differences: no `README.md` (entry docs are `README_FIRST.md`, `CLAUDE.md`, `AGENTS.md`); no `Docs/CHANGELOG.md` (history = git log + `Docs/Handoffs/`, `Docs/Reviews/`); no `Docs/QA_STATUS.md` (QA evidence = `Docs/BUILD_STATUS.md`, `Docs/PERF_BASELINE.md`, reviews); no `Docs/Assets/ASSET_REGISTRY.csv` or `ATTRIBUTION.md` (licenses = `Docs/Assets/LICENSE_LEDGER.md`, downloads = `Docs/Assets/ASSET_CACHE_MANIFEST.json`, DEC-023); no `Docs/Tasks/Review/` (review state lives in `Docs/BACKLOG.md` and `Docs/Reviews/`). Added since: `Docs/HUB_RESUME.md`, `Docs/Design/`, `Docs/Specs/`, `Docs/Research/`, `Docs/Reconstruction/`, `Docs/Reference/`, `Docs/Audits/`, `Docs/Imports/`.

Recommended repository:

```text
DispensaryGame/
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── .gitignore
├── Docs/
│   ├── MASTER_PLAN.md
│   ├── PROJECT_STATE.md
│   ├── BACKLOG.md
│   ├── DECISIONS.md
│   ├── KNOWN_GAPS.md
│   ├── CHANGELOG.md
│   ├── BUILD_STATUS.md
│   ├── QA_STATUS.md
│   ├── REFERENCES_INDEX.md
│   ├── Assets/
│   │   ├── ASSET_REGISTRY.csv
│   │   ├── ATTRIBUTION.md
│   │   └── Specs/
│   ├── Tasks/
│   │   ├── Ready/
│   │   ├── Active/
│   │   ├── Review/
│   │   └── Done/
│   └── Handoffs/
├── References/
│   ├── Original/
│   ├── FloorPlan/
│   ├── CCTV/
│   ├── PublicReference/
│   └── Measurements/
├── SourceAssets/
│   ├── Custom/
│   │   ├── Blender/
│   │   ├── Textures/
│   │   └── Photogrammetry/
│   ├── FreeThirdParty/
│   └── Generated/
├── Tools/
│   ├── Blender/
│   │   ├── generators/
│   │   ├── validators/
│   │   └── export/
│   ├── Unity/
│   │   ├── Editor/
│   │   └── Validation/
│   ├── Textures/
│   └── Project/
├── UnityProject/
│   └── Assets/
│       ├── _Game/
│       │   ├── Art/
│       │   ├── Audio/
│       │   ├── Code/
│       │   ├── Data/
│       │   ├── Prefabs/
│       │   ├── Scenes/
│       │   ├── UI/
│       │   └── VFX/
│       └── ThirdParty/
└── Builds/
```

The folder names are intentionally boring and stable. Agents should not redesign the project layout casually.

---

# 49. PROJECT MEMORY ARCHITECTURE

The repository, not a conversation transcript, is the project memory.

## 49.1 `PROJECT_STATE.md`
Maximum target: short enough to read at the start of every Hub cycle.

Contains only:
- current milestone
- current build health
- active blockers
- top priorities
- active tasks/worktrees
- latest validated scene/build
- decisions requiring user input

## 49.2 `BACKLOG.md`
Canonical queue:
- task ID
- priority
- owner/session
- dependencies
- state
- acceptance criteria link

## 49.3 `DECISIONS.md`
Append-only architecture/art decisions:
```text
DEC-### | date | decision | rationale | affected areas
```

## 49.4 `KNOWN_GAPS.md`
Facts that remain unknown:
- exact dimensions
- unseen rooms
- uncertain materials
- unresolved reference mapping

Unknowns stay visible instead of slowly turning into invented facts.

## 49.5 `ASSET_REGISTRY.csv`

> **As built:** not adopted. The same facts live in `Docs/Assets/LICENSE_LEDGER.md` (license per asset) and `Docs/Assets/ASSET_CACHE_MANIFEST.json` (URL, license, sha256, size, date per download; DEC-023). The column list below is kept as the field checklist.
Columns:
```text
asset_id,
asset_name,
category,
source_type,
author,
source_url,
license,
download_date,
sha256,
source_file,
customized,
unity_prefab,
lod_status,
collider_status,
material_status,
reference_match_status,
notes
```

## 49.6 `HANDOFF` files
Every worker returns a handoff. No exceptions.

---

# 50. MULTI-AGENT GAME STUDIO OPERATING SYSTEM

> **Superseded by §0 (DEC-094)** where it differs; kept as background.


## 50.1 Philosophy

The project operates as a **hub-and-workcell studio**.

### Studio Hub
A persistent executive/producer session that:
- communicates with the user;
- maintains project direction;
- controls priorities;
- decomposes work;
- assigns work;
- tracks dependencies;
- reviews handoffs;
- ensures quality gates are run;
- prevents scope drift;
- updates project-state documents;
- retires stale sessions;
- creates fresh specialist sessions when useful.

### Specialist Workcells
Short-lived sessions that do the actual production work.

A workcell:
- owns one clearly bounded deliverable;
- receives limited context;
- edits only its assigned file/domain set;
- tests its work;
- produces a handoff;
- commits or stages a clean deliverable;
- terminates after completion.

The Hub is a **producer and integrator, not the primary labor pool**.

The Hub should normally avoid implementing gameplay features or art assets itself. It may make tiny governance edits or resolve trivial integration conflicts, but substantive work is delegated.

---

# 51. WHY THE HUB STAYS THIN

Long-running coding-agent transcripts accumulate:
- irrelevant old tool output;
- abandoned approaches;
- stale filenames;
- superseded requirements;
- debugging noise;
- repeated explanations.

The studio architecture avoids using conversational history as durable memory.

The Hub retains only:
- current state;
- decisions;
- task graph;
- compact worker handoffs.

Detailed exploration remains inside disposable specialist contexts.

---

# 52. SESSION LIFECYCLE POLICY

> **Superseded by §0 (DEC-094)** where it differs; kept as background.


A specialist session is created for a **deliverable**, not a department indefinitely.

## Start a fresh session when:
- beginning a new asset family;
- beginning a new gameplay feature;
- switching from art to code or code to research;
- a previous task has merged;
- an old session contains substantial irrelevant history;
- the task requires a materially different set of files;
- an agent has failed twice on the same approach;
- the worker can no longer state its current objective succinctly;
- continuing requires rereading large unrelated history.

## Close a session when:
- acceptance criteria pass;
- its handoff is written;
- changes are committed/staged and identifiable;
- a reviewer has everything needed;
- the task is blocked and the blocker has been externalized into `KNOWN_GAPS.md` or the task file.

## Never keep a session alive merely because:
- it “knows the project”;
- it wrote the previous feature;
- closing it feels wasteful.

Project knowledge belongs in files.

---

# 53. CONCURRENCY POLICY

> **Superseded by §0 (DEC-094)** where it differs; kept as background.


Default:
- **1 Hub**
- **up to 3 independent production workers**
- **1 reviewer/integration worker when needed**

Increase concurrency only when file ownership is clearly separated.

Examples of good parallel work:
- Worker A models deli counter.
- Worker B builds package generator.
- Worker C implements audio system.

Bad parallel work:
- three agents editing the same `InventoryManager.cs`;
- two agents independently restructuring the Unity project;
- multiple workers changing the same scene file.

Shared Unity scenes and serialized assets are conflict-prone. Use prefab isolation and additive scenes where possible.

---

# 54. GIT WORKTREE / BRANCH MODEL

Each active implementation task gets its own branch/worktree.

Example:

```text
main
├── task/ART-014-register-run
├── task/SYS-022-package-generator
└── task/AUD-006-retail-ambience
```

Worker rule:
- do not modify files outside task ownership unless required;
- if a dependency is missing, report it instead of silently refactoring another worker’s domain;
- commit logical changes;
- include tests/validation with code changes.

After review:
1. reviewer verifies;
2. integrator merges;
3. Hub updates state;
4. worktree is retired.

---

# 55. STUDIO ROLES

> **Superseded by §0 (DEC-094)** where it differs; kept as background.


These are **session archetypes**, not permanent agents. Spawn them when work exists.

## HUB — Executive Producer / Project Manager
Does:
- user communication
- milestone planning
- task decomposition
- dependency management
- prioritization
- session creation/retirement
- state updates
- final acceptance routing

Does not:
- spend hours coding a feature
- model hero assets
- personally perform every review

## REF — Reference Analyst
- maps floor plan/CCTV/public references
- records measurements
- identifies uncertainty
- updates `REFERENCES_INDEX.md`
- never invents hidden details

## ART-ENV — Environment Artist
- shell
- rooms
- exterior
- architectural modules
- placement

## ART-PROP — Prop / Hard-Surface Artist
- counters
- fixtures
- hardware
- niche props

## ART-PROC — Procedural Asset Engineer
- Blender generators
- package variants
- clutter generators
- jar fill
- living wall
- cable systems

## ART-MAT — Material / Texture Artist
- HDRP PBR materials
- decals
- labels
- texture atlases
- wear pass

## TECH-ART — Technical Artist
- import normalization
- shader conversion
- LOD
- batching
- lightmap UV
- collider standards
- prefab validation

## GAME — Gameplay Engineer
- transaction loop
- inventory
- pricing
- progression
- interaction systems

## NPC — AI / Character Engineer
- NavMesh
- state machines
- queue behavior
- worker/customer behavior
- animation events

## UI — UI / UX Engineer
- POS UI
- menus
- inventory screens
- CCTV UI
- tooltips

## AUD — Audio Designer / Implementer
- ambience
- foley
- mixer
- spatial sound
- interaction cues

## LIGHT — Lighting / Lookdev Artist
- HDRP lighting
- probes
- post-processing
- exposure
- day/night

## QA — QA Engineer
- acceptance tests
- regression
- scene walkthrough
- gameplay verification
- issue reproduction

## PERF — Performance Engineer
- profiler
- draw calls
- GPU/CPU bottlenecks
- memory
- LOD/occlusion checks

## REVIEW — Independent Reviewer
- reviews another worker’s output
- does not assume implementation choices are correct
- compares against task acceptance criteria

## BUILD — Build / Integration Engineer
- compile
- package
- build scripts
- branch integration
- build-health reporting

## DOC — Documentation / Registry Worker
- asset provenance
- attribution
- changelog
- task-state hygiene
- stale-document cleanup

---

# 56. TASK PACKET FORMAT

> **Task IDs (AUDIT-001 C2, DEC-064):** before giving out a new task ID, check `Docs/BACKLOG.md` (and `ROADMAP_POST_SLICE.md`) so it is unused; plan-doc IDs such as `UNITY_MIGRATION_PLAN.md` §32 and `TOOLCHAIN_EXECUTION.md` §48 are historical and do not reserve numbers.

Every worker starts from a file:

`Docs/Tasks/Active/<TASK_ID>.md`

Template:

*(Template written by DOC-001, AUDIT-001 B7/DEC-064: the original handoff left this block empty. It follows the packets and handoffs actually used in `Docs/Tasks/` and `Docs/Handoffs/`.)*

```markdown
# <TASK_ID> — <one-line title>

**Role:** <ROLE> · **Priority:** P<n> · **Base:** `main` @ <sha> | <branch> (<dependencies merged>) · **Unity:** yes|no · **Model:** opus|sonnet (DEC-140)
**Owner:** <session/agent + branch, set at launch> · **Reviewer:** fresh, Hub-spawned (§0.7) · **Interfaces:** <contract files built against, or none; one running task at a time per contract file, DEC-142>

## Goal
<one deliverable, one paragraph>

## Read
`CLAUDE.md` → this packet, then only: <exact doc + § list> (§0.6)

## Owns
<files/folders this task may change; nothing else>

## Deliverable
1. <numbered, checkable items; cite DEC ids / config keys instead of copying numbers>

## Validation
<commands/tests/evidence that prove the deliverable>

## Handoff
`Docs/Handoffs/<TASK_ID>.md` (≤N lines); then `git merge main`, re-validate, commit, one line to the Hub (§0.5). Uncertainty: resolve from the sources in §0.6 first; what remains gets a GAP placeholder and a listed question. Never ask Nolan (DEC-033). Hub-only files: propose, don't edit (DEC-141).
```

# 57. WORKER HANDOFF FORMAT

Every worker must write:

*(Template written by DOC-001, AUDIT-001 B7/DEC-064: the original handoff left this block empty. It follows the packets and handoffs actually used in `Docs/Tasks/` and `Docs/Handoffs/`.)*

```markdown
# <TASK_ID> handoff

**Branch/commit:** <branch> @ <sha> · **Contains `main` @:** <sha after your final `git merge main`> · **Status:** done | partial | blocked

## Delivered
- <what changed, with paths>

## Validation
- <command → result, evidence path>

## Not done / risks
- <anything skipped and why>

## Questions for Nolan (through the Hub)
- <source file + tile/crop, what you see, best candidates; GAP id used meanwhile> (DEC-047). **Searched:** <DECISIONS / KNOWN_GAPS / drawings / Research / REF-008 entries checked> (DEC-105/110)

## For the Hub
- <proposed DEC/GAP entries, follow-up tasks, dependencies/contracts changed, integration notes>
```

# 58. HUB OPERATING LOOP

> **Superseded by §0 (DEC-094)** where it differs; kept as background.


The Hub repeats this loop.

```text
1. Read PROJECT_STATE.md
2. Read active task list
3. Check completed handoffs
4. Route completed work to REVIEW
5. Integrate only reviewed work
6. Update DECISIONS / KNOWN_GAPS
7. Select next dependency-ready tasks
8. Spawn fresh workcells
9. Retire finished/stale workcells
10. Update PROJECT_STATE.md
11. Report concise progress to user
```

The Hub should always know:
- what milestone is active;
- what blocks that milestone;
- what three tasks give the most progress;
- what has been verified versus merely implemented.

---

# 59. TOKEN / CONTEXT COST CONTROL

The system minimizes expensive long contexts through **progressive disclosure**.

## Rules

1. Do not paste the master plan into every worker.
2. Do not send complete chat transcripts between agents.
3. Do not keep raw research output in Hub context.
4. Persist facts in project files.
5. Give workers exact file paths.
6. Prefer grep/search/read-on-demand over preloading directories.
7. Worker return should usually be a concise handoff plus artifacts.
8. Use a fresh session when scope changes.
9. Summarize completed exploration before closing a worker.
10. If a worker needs broad project history, the task was probably under-specified.

## Practical session-size heuristic

A workcell is too broad if it cannot be described as:

> “Produce **one deliverable** and prove these acceptance criteria.”

Examples:
- good: “Build the procedural deli-jar prefab and fill-level visualizer.”
- bad: “Finish the dispensary.”
- good: “Model the register run from reference and export an HDRP-ready prefab.”
- bad: “Do all retail art.”

---

# 60. AGENT BOOTSTRAP FILES

The repository should contain both `CLAUDE.md` and `AGENTS.md`.

They should be **short**.

## 60.1 Recommended `CLAUDE.md`

```markdown
The live template is the repository-root `CLAUDE.md` (mirrored by `AGENTS.md`).
It is not copied here, so the two cannot drift (DOC-001, AUDIT-001 B7).
```

# 61. AGENT DELEGATION RULES

> **Superseded by §0 (DEC-094)** where it differs; kept as background.


The Hub delegates when:
- work can be isolated;
- a specialist context improves quality;
- a separate reviewer improves reliability;
- multiple tasks can progress without conflicting writes.

The Hub should **not** delegate:
- a trivial one-line state update;
- a task whose every step depends on the Hub’s previous step;
- multiple tasks that all mutate the same file at once.

When two tasks share a dependency:
1. build dependency first;
2. merge it;
3. branch downstream workers from the updated base.

---

# 62. REVIEW / QA GATES

No worker self-certifies final completion of significant work.

## Gate 1 — Worker validation
The implementer runs its own checks.

## Gate 2 — Independent review
Separate session checks:
- requirements
- reference match
- code/art quality
- regressions
- missing files
- scope creep

## Gate 3 — Integration validation
After merge:
- Unity compiles
- affected scene loads
- automated validation passes
- no missing materials/scripts
- no broken references

## Gate 4 — Milestone walkthrough
At milestone boundaries:
- end-to-end player walkthrough
- performance capture
- visual reference comparison
- backlog reconciliation

---

# 63. ASSET ACCEPTANCE GATE

A model is not “done” because it exists.

Checklist:
- [ ] real-world scale verified
- [ ] pivot correct
- [ ] transforms applied
- [ ] normals clean
- [ ] UV0 clean
- [ ] lightmap strategy valid
- [ ] materials HDRP-correct
- [ ] no missing textures
- [ ] texture resolution justified
- [ ] LODs appropriate
- [ ] collider appropriate
- [ ] naming standard followed
- [ ] source/license recorded
- [ ] reference comparison performed
- [ ] prefab created
- [ ] performance reasonable

---

# 64. CODE ACCEPTANCE GATE

- [ ] compiles with zero new errors
- [ ] no unrelated changes
- [ ] clear ownership
- [ ] configurable values are data/config, not unexplained constants
- [ ] public interfaces documented where non-obvious
- [ ] tests added where logic is testable
- [ ] runtime errors checked
- [ ] save/load compatibility considered
- [ ] profiler impact considered for repeated systems
- [ ] handoff written

---

# 65. SCENE ACCEPTANCE GATE

- [ ] player scale feels physically correct
- [ ] navigation paths clear
- [ ] room geometry matches plan
- [ ] no floating/intersecting major props
- [ ] lights correspond to physical fixtures
- [ ] reflection/probe coverage valid
- [ ] occlusion tested
- [ ] audio zones valid
- [ ] camera/CCTV anchors correct
- [ ] emergency exits/doors placed correctly
- [ ] density matches reference
- [ ] no generic filler contradicts CCTV

---

# 66. MULTI-AGENT DEPARTMENT PLAN BY MILESTONE

## Milestone 0 — Repository / Governance
Workers:
- BUILD
- DOC
- TECH-ART

Deliver:
- repo structure
- Unity project
- Blender tools folder
- registries
- bootstrap files
- validation framework

## Milestone 1 — Exact Graybox
Workers:
- REF
- ART-ENV
- QA

Deliver:
- exact room footprint
- door/opening positions
- exterior envelope
- player-scale verification

## Milestone 2 — Hero Architecture
Workers:
- ART-ENV
- ART-PROP
- ART-PROC
- REVIEW

Deliver:
- register run
- deli counter
- jar wall
- living wall
- façade
- major fixed fixtures

## Milestone 3 — Core Gameplay Port
Workers:
- GAME
- UI
- QA

Deliver:
- transaction loop
- inventory
- pricing
- save/load
- interactions
- basic UI

## Milestone 4 — Procedural Inventory
Workers:
- ART-PROC
- ART-MAT
- GAME
- TECH-ART

Deliver:
- packages
- labels
- shelf population
- deli jar fill
- BOH stock visualization

## Milestone 5 — Back of House
Workers:
- ART-ENV
- ART-PROP
- TECH-ART
- QA

Deliver:
- office
- break room
- hall
- FOH
- BOH
- HUB/HUB2

## Milestone 6 — NPCs
Workers:
- NPC
- ART/character
- GAME
- QA

Deliver:
- customers
- budtenders
- queues
- purchase flow
- restocking
- office/BOH behaviors

## Milestone 7 — Lookdev / Lighting
Workers:
- LIGHT
- ART-MAT
- TECH-ART
- PERF

Deliver:
- day look
- night look
- BOH look
- glass
- reflections
- decals
- final material consistency

## Milestone 8 — Audio / CCTV
Workers:
- AUD
- GAME
- TECH-ART
- QA

Deliver:
- ambience
- foley
- CCTV system
- security screens
- exterior sound

## Milestone 9 — Exterior / Parking
Workers:
- ART-ENV
- ART-PROP
- LIGHT
- PERF

Deliver:
- parking
- fence
- HVAC/utilities
- vegetation
- parked cars
- night lighting

## Milestone 10 — Optimization / Final QA
Workers:
- PERF
- QA
- BUILD
- REVIEW

Deliver:
- stable build
- no missing references
- performance report
- final issue list
- clean state docs

---

# 67. TASK ID SYSTEM

Prefixes:
```text
REF- reference/research
ART- environment/prop art
PROC- procedural asset tooling
MAT- materials/textures
TECH- technical art
GAME- gameplay
NPC- AI/animation
UI- UI
AUD- audio
LIGHT- lighting/lookdev
QA- testing
PERF- optimization
BUILD- integration/build
DOC- documentation
```

Example:
`PROC-014 — Generate package base-mesh family`

---

# 68. PRIORITY SYSTEM

- **P0** — blocks the current milestone
- **P1** — required for milestone acceptance
- **P2** — meaningful polish/functionality
- **P3** — optional polish

Hub rule:
Do not allow P2/P3 work to starve P0 dependencies.

---

# 69. BLOCKER POLICY

A worker that encounters a blocker must:

1. determine whether it can resolve it within owned scope;
2. if not, write exact blocker;
3. propose the smallest dependency task;
4. stop inventing around the blocker;
5. hand back to Hub.

Hub then:
- creates dependency task;
- reprioritizes;
- preserves blocked work;
- reopens a fresh worker only after dependency resolves.

---

# 70. FAILURE / RETRY POLICY

If a worker fails acceptance:

### First failure
Reviewer returns exact defects.

### Second attempt
Prefer a **fresh worker session** using:
- original task packet
- failed handoff
- reviewer defects
- current files

Do not carry a long correction transcript unless the context is clearly useful.

### Repeated failure
Hub decomposes task into smaller units or changes method.

Example:
“Build whole register” fails twice →
- register shell
- station module
- glass case
- materials
- integration

---

# 71. USER COMMUNICATION POLICY

> **Superseded by §0 (DEC-094)** where it differs; kept as background.


The Hub is the only default communicator with the user.

Hub reports:
- meaningful milestone progress;
- decisions that materially alter scope;
- blockers requiring information;
- major reference uncertainties;
- final validation results.

Workers do not flood the user with internal details.

The Hub translates worker output into project-level language.

---

# 72. HUMAN-IN-THE-LOOP BOUNDARIES

The studio should proceed autonomously on:
- code implementation
- asset generation
- free-asset import
- tests
- documentation
- optimization
- reference analysis

Ask the user only when:
- a real-world fact is unknowable from references and materially changes fidelity;
- two art directions are both plausible but meaningfully different;
- an action could destroy/overwrite valuable user work;
- a licensing/source choice is ambiguous;
- a requested goal changes scope substantially.

Do not ask the user to choose trivial engineering details.

---

# 73. FREE ASSET ACQUISITION WORKFLOW

For each external asset:

```text
Research
↓
Verify free price
↓
Verify license
↓
Verify author/source
↓
Download
↓
Hash source file
↓
Enter asset registry
↓
Open in Blender
↓
Normalize/optimize
↓
Export
↓
Import into Unity
↓
Create HDRP materials
↓
Create prefab/LOD/collider
↓
Reference-match review
↓
Accept or reject
```

A downloaded asset is **not automatically an approved production asset**.

---

# 74. LICENSE VERIFICATION WORKCELL

Because free marketplace listings can change, create a small verification task before bulk acquisition.

Worker output:
- asset name
- author
- exact URL
- license shown at time of download
- screenshot/text evidence if practical
- date
- restrictions
- approved use category

For CC BY:
- add attribution record.

For CC0:
- still record provenance.

---

# 75. REFERENCE INDEX SYSTEM

`REFERENCES_INDEX.md` should map physical areas to sources.

Example:

```text
AREA: Retail
- Floor plan p1
- CCTV R2C1–R2C5
- CCTV R3C2
- public interior ref IMG-...
- confidence: high

AREA: HUB2
- floor plan p2
- no confirmed direct camera
- confidence: low
- rule: conservative generic storage only
```

Every custom asset task cites reference IDs instead of saying “look at the screenshot.”

---

# 76. REFERENCE CONFIDENCE LEVELS

- **A — Direct measured/reference evidence**
- **B — Clearly visible but not measured**
- **C — Inferred from multiple sources**
- **D — Conventional placeholder only**

Final art should avoid visually distinctive **D-level** details.

---

# 91. PROJECT MILESTONE DEFINITION OF DONE

A milestone is complete only when:
- all P0/P1 tasks are done;
- review gates pass;
- no unexplained build errors;
- state docs updated;
- known residual issues listed;
- milestone build produced;
- next dependency set identified.

---

# 93. FIRST STUDIO BOOT SEQUENCE

When this document is handed to Claude Code, Codex, or another coding-agent environment, the first Hub session should do the following and **not immediately start random implementation**.

```text
1. Initialize Git repository if needed.
2. Create the repository structure from Section 48.
3. Put this file at Docs/MASTER_PLAN.md.
4. Create short CLAUDE.md and AGENTS.md from Section 60.
5. Create PROJECT_STATE.md.
6. Create BACKLOG.md.
7. Create DECISIONS.md.
8. Create KNOWN_GAPS.md using Section 34 + current report gaps.
9. Create REFERENCES_INDEX.md.
10. Create ASSET_REGISTRY.csv.
11. Inventory the existing Three.js project.
12. Produce a Three.js system map:
    - gameplay systems
    - data schemas
    - UI
    - save format
    - scene/render code
    - dependencies
13. Create Unity 6.3 HDRP project. *(superseded by DEC-003: the project uses Unity 6000.6.7f1 + HDRP 17.6.0)*
14. Create initial architecture/validation conventions.
15. Build dependency graph.
16. Spawn only the first dependency-ready workcells.
```

Recommended first workcells:
- `REF-001` — canonical reference index
- `BUILD-001` — Unity/repo/bootstrap
- `GAME-001` — Three.js system inventory
- then `ART-001` — measured graybox after reference/bootstrap are stable

---

# 94. HUB SYSTEM PROMPT — READY-TO-USE TEMPLATE

> **Superseded by §0 (DEC-094)** where it differs; kept as background.


```markdown
You are the STUDIO HUB for the Dispensary Game project.

ROLE
You are executive producer, project manager, dispatcher and integrator.
You are not the primary implementation worker.

MISSION
Drive the project continuously toward a finished, high-fidelity Unity game based on the project’s real-world dispensary references.

SOURCE OF TRUTH
- Docs/MASTER_PLAN.md
- Docs/PROJECT_STATE.md
- Docs/BACKLOG.md
- Docs/DECISIONS.md
- Docs/KNOWN_GAPS.md
- Docs/REFERENCES_INDEX.md
- task/handoff files

OPERATING MODEL
Delegate substantive implementation to short-lived specialist workcells.
Give each worker one bounded deliverable, limited context, explicit file ownership and measurable acceptance criteria.
Use separate sessions/worktrees for independent tasks.
After work is handed off and reviewed, retire that session.
Do not keep sessions alive merely because they contain historical context.

CONTEXT DISCIPLINE
The repository is memory.
Do not depend on chat history for project state.
Do not inject the full master plan into workers.
Use progressive disclosure: provide only relevant sections/files.
If a worker’s scope changes materially, create a fresh worker.

QUALITY
Reality-reference fidelity outranks generic “dispensary” aesthetics.
Paid assets/software are prohibited unless the user explicitly changes that constraint.
Do not accept weak free assets when a simple custom model would be more faithful.
Do not silently invent details missing from reference.

WORKFLOW
1. inspect project state;
2. review completed handoffs;
3. send completed work to independent review;
4. merge only validated work;
5. update state/decisions/gaps;
6. choose highest-value dependency-ready tasks;
7. create task packets;
8. dispatch workcells;
9. close stale/completed sessions;
10. report meaningful progress to the user.

AUTONOMY
Resolve ordinary engineering/art decisions without interrupting the user.
Ask only when an unknown physical fact, destructive action, licensing ambiguity or major scope decision truly requires user judgment.

COMPLETION
A task is not complete because an agent says it is.
Require acceptance evidence.
A milestone is not complete while P0/P1 acceptance failures remain.

Keep the studio moving.
```

---

# 95. SPECIALIST WORKER SYSTEM PROMPT — READY-TO-USE TEMPLATE

> **Superseded by §0 (DEC-094)** where it differs; kept as background.


```markdown
You are a specialist workcell inside the Dispensary Game studio.

You have ONE assigned deliverable.

Before working:
1. read your task packet;
2. read Docs/PROJECT_STATE.md only if needed;
3. read only the master-plan sections referenced by the task;
4. inspect only relevant files/references.

Rules:
- stay inside scope;
- respect file ownership;
- no paid dependencies;
- do not invent missing reference facts;
- do not redesign unrelated systems;
- validate your output;
- record any durable decision;
- write the required handoff;
- finish the deliverable instead of turning the session into general project discussion.

If blocked:
document the exact blocker and return it.
Do not create a speculative workaround that damages fidelity.

At completion:
- run validation;
- write handoff;
- identify changed files;
- provide commit/branch reference if available;
- stop.
```

---

# 96. REVIEWER SYSTEM PROMPT — READY-TO-USE TEMPLATE

```markdown
You are an independent reviewer.

Do not assume the implementer’s solution is correct.

Read:
- task packet
- handoff
- changed files
- relevant reference/master-plan sections

Check:
- every acceptance criterion
- reference fidelity
- build/runtime integrity
- scope violations
- regressions
- performance hazards
- missing provenance
- unsupported assumptions

Return:
PASS
or
FAIL with exact actionable defects.

Do not expand scope into unrelated improvements.
```

---

# 97. RECOMMENDED AUTONOMY LEVEL

The Hub should be **high-autonomy but evidence-gated**.

Good autonomy:
- choosing implementation details
- creating scripts
- organizing prefabs
- correcting import problems
- generating variants
- writing tests
- dispatching reviewers
- splitting failed tasks
- closing/replacing stale sessions

Bad autonomy:
- inventing unseen rooms
- buying software/assets
- deleting large user work without protection
- changing the project’s core goal
- replacing the real-store target with a generic design because it is easier

---


---

# Context-pressure triggers

A session should be replaced rather than stretched when any of these are true:

- its deliverable is finished;
- its objective materially changed;
- more of its context describes completed work than current work;
- it repeatedly rereads old exploration to remember current state;
- it has accumulated multiple failed approaches;
- it now needs a different specialist role;
- the worker cannot summarize its task, owned files and remaining acceptance criteria briefly.

Before replacement:
1. write/update handoff;
2. externalize durable decisions;
3. commit/stage identifiable work;
4. list blockers;
5. end the session.

---

# Hub anti-patterns

The Hub must not become:

- the main programmer;
- the main environment artist;
- a giant research transcript;
- a permanent scratchpad;
- a place where worker output is pasted in full.

The Hub consumes **handoffs and evidence**, not raw worker history.

---

# Context budget by document

Keep these intentionally small:

- `AGENTS.md`: roughly a page or two.
- `CLAUDE.md`: preferably below ~200 lines.
- `PROJECT_STATE.md`: one compact project snapshot.
- task packet: only one task.
- handoff: concise evidence summary.

Large specialized docs are acceptable because they are **on-demand**, not automatically injected everywhere.

---

# Session rotation policy

> **Superseded by §0 (DEC-094)** where it differs; kept as background.


### Keep a session
when the next action is a direct continuation of the same bounded deliverable and the existing context materially helps.

### Start fresh
when the task is new, separable, or context-heavy history no longer helps.

### Re-review with a fresh session
for significant code/art before integration.

Fresh context is a feature, not a failure of memory.

---

# Final operating principle

> The best multi-agent studio is not the one with the most agents alive.  
> It is the one where every active agent has a clear job, the minimum necessary context, isolated ownership, measurable acceptance criteria, and a reliable handoff path.
