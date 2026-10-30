# DISPENSARY GAME — STUDIO OPERATING SYSTEM
## Multi-Agent Hub, Workcells, Context Lifecycle, Reviews & Repository Memory

**Version:** 2.0  
**Date:** 2026-10-29  
**Parent:** `MASTER_PLAN.md`  
**Target environments:** Claude Code, Codex-style coding agents, or comparable repository-capable agent systems

---

# 0. OPERATING MODEL: Hub → Department Leads → Workers (DEC-094, current)

> **This section is the one authority** for roles, authority, escalation, session lifecycle, task ownership, context loading and reporting. Where a later section (§3, §50–53, §55, §58, §61, §71, §94–97, "Session rotation") says otherwise, §0 wins; those sections are background only. Do not restate these rules in other docs: point here.

## 0.1 Chain and principle
Nolan → **Hub** (product manager, overall authority under Nolan) → **Department Leads** → **Workers**. Reviewers are a shared pool staffed by the Hub. Context gets narrower going down and more compressed going up. **Roles live in files; conversations are disposable:** any Hub or lead session can be killed and rebuilt from its role file plus its state file.

## 0.2 Departments (elastic)
A department exists only while it has substantial ongoing work, room for parallel workers, specialist context the Hub should not carry, and a clear ownership boundary. The Hub creates, merges, suspends and retires departments. The live roster (lead sessions, status, capacity, Unity slots) is in `Docs/PROJECT_STATE.md` → "Studio roster". Each department's charter and domain state is `Docs/Departments/<DEPT>.md`, written by its lead; owned paths and contracts are listed there.

| Dept | Task prefixes | Scope (detail in the dept file) |
|---|---|---|
| Gameplay | GAME, UX, DES, QA, DATA, COMP, BUILD, PERF | simulation/domain/presentation code, controls, customer flow, recommendation gameplay, gameplay design specs, UX, test gates, catalog data, playtest builds |
| World | REF, ART | store reference evidence + `ROOM_FIXTURES.json`, graybox/lookdev scenes, room/layout accuracy, set dressing |
| Assets | PROC, ASSET, IMP, BRAND, AUDIO | Blender generators and the ChatGPT toolkit intake, characters, licenses, brands/labels, audio |
| Hub (no lead) | DOC, OPS, AUDIT, REVIEW | studio docs and rules, studio tooling, audits, the reviewer pool |

The task prefix names the owning department unless the packet says otherwise. A new prefix is assigned by the Hub.

## 0.3 Authority
**Hub** owns product direction, priorities and sequencing, scope, roadmap, major architecture/product decisions, cross-department coordination, final integration (only the Hub merges to `main`), escalation to Nolan, staffing (which departments exist, lead sessions, capacity per department), rule and source-of-truth discipline. It may override any lead or worker. It does **not** write department packets, launch routine workers or read worker handoffs.

**Lead** has real delegated authority in its domain: sequence work, write packets, launch/redirect/replace/retire workers within its capacity, answer routine questions from the docs, make implementation decisions inside approved scope, review worker output, reject or return incomplete work, require or run validation, handle internal dependencies, accept domain work and send it to review, keep its dept file accurate, and report upward. Leads coordinate **directly with each other** on normal interface and implementation issues (SendMessage) and record what they agreed in the packets' "Interfaces" line.

**Worker** executes one packet: decides implementation details inside it, edits only its "Owns" paths, validates, writes the handoff, reports to the lead that launched it.

**A lead escalates to the Hub only for:** scope change; priority conflict; a decision outside its authority or a material deviation from an approved spec/DEC; an unresolved cross-department conflict or unclear ownership; needing more capacity than allotted; information no doc holds (every question for Nolan); architectural or product decisions that affect other departments. Anything else the lead decides and, if durable, records.

## 0.4 Sessions and lifecycle
- **Hub session:** started by Nolan or a scheduled resume; reads `Docs/HUB_RESUME.md`. Starts, replaces and retires lead sessions and reviewers; removes stale or duplicate sessions.
- **Lead session:** one per active department, titled `Dispo · Lead <Dept>`, runs in the **main checkout** and does no hands-on work (the DEC-045 hub guard applies to it too): it reads, plans, reviews and edits its own state docs. Standard brief from the Hub: *"You are the <Dept> lead of the Dispo Game studio. Read `CLAUDE.md`, `Docs/STUDIO_OS.md` §0 and `Docs/Departments/<DEPT>.md`, reconcile with `list_sessions {"linked": true}` and git branches, then run your queue. You report to the Hub `<id>`."*
- **Workers:** a lead launches workers with the **Agent tool** (background; `isolation: "worktree"` for anything that edits code/assets or runs Unity/Blender; no isolation for read-only research). Leads are driven by messages, and the app refuses `start_session` on message-triggered turns, so subagents are the normal worker; they also keep worker transcripts out of every other context. A lead may also hand work to an existing idle worker session of its department with SendMessage. A full worker session (visible to Nolan, outliving the lead) is started only by the Hub on a Nolan-typed turn, then belongs to the lead.
- **Brief = packet path.** "Read `CLAUDE.md`, then `Docs/Tasks/Active/<ID>.md`; report to me (your lead) with a ≤15-line summary; commit as `git -c user.name=Nolan_Bradford -c user.email=handlebarn@gmail.com commit`." Never paste canonical docs into a brief.
- **Capacity:** the Hub sets each department's max concurrent workers and Unity slots in the roster. Studio-wide limit: 2 Unity editors (DEC-013). A lead stays inside its allotment and asks the Hub to exceed it.
- **Launch a worker only when** the task is bounded with acceptance criteria, its dependencies are merged or its interface is fixed, its Owns overlaps no active task, and the lead can review and integrate the result soon. Otherwise don't: more agents is not more throughput.
- **Retire a worker** once its output is reviewed, validation passed, the handoff is accepted and its decisions are persisted.
- **Context ceiling (Nolan, DEC-102):** the Hub checks every lead's and reviewer's context (`get_usage` with its session id) on each Hub turn, and replaces any above **~300k tokens** (fire and re-hire, standard brief). Leads apply the same ceiling to worker sessions they adopted. A worker close to finishing may finish first, if it hands off right after.
- **Replace a lead (or Hub) session** when it re-reads old history to remember state, carries mostly finished work, has been compacted, or costs more than it helps. Before ending, it brings its state file up to date (in-flight workers with branch and id, queue, blockers, questions). The Hub then starts a fresh lead with the standard brief and archives the old one. Ending a session never loses knowledge if the state file is current.

## 0.5 Task ownership, overlap and integration
- **One registry:** `Docs/BACKLOG.md` + packets in `Docs/Tasks/{Ready,Active,Done}`. A lead edits only its own department's rows and packets, and allocates IDs only in its prefixes (check BACKLOG first). Move a packet and its BACKLOG row in the same commit (DEC-064).
- **Packet header** (§56) adds: `Dept`, `Owner` (worker id + branch once launched), `Touches` (paths owned by another department, with that lead's OK), `Interfaces` (contract files both sides build against), `Reviewer`.
- **No overlapping edits:** the Owns sets of active tasks never overlap. The lead checks its own active packets; for another department's paths it gets that lead's OK first. Shared Unity scenes and serialized assets have one owner at a time.
- **Contracts first:** when two sides would build against an interface (schema, anchor/object names, params/manifest, asset spec), the owning side commits it first as a small task; the other side builds against the committed version, never an assumption. Contract owners: `ROOM_FIXTURES.json` + `REFERENCES_INDEX.md` (World); generator params, FBX/prefab names and the asset manifest (Assets); scene anchor/object names that code uses (World); catalog/data schema and `Reconstruction/` (Gameplay).
- **Hub-owned files** (leads propose, the Hub edits): `CLAUDE.md`, `AGENTS.md`, `README_FIRST.md`, `Docs/MASTER_PLAN.md`, this file, `HUB_RESUME.md`, `PROJECT_STATE.md`, `DOCS_INDEX.md`, `Design/ROADMAP_POST_SLICE.md` (scope). `DECISIONS.md` and `KNOWN_GAPS.md` are shared registries: leads append their domain entries (department in the "Affects" column); cross-department entries are the Hub's.
- **State commits:** leads and the Hub commit state docs straight to `main` from the main checkout, staging only their own paths (`git commit -- <paths>`); retry if `index.lock` is held. Everything else goes through review.
- **Integration path:** worker branch → lead accepts → reviewer from the pool (lead sends branch + commit + handoff path; verdict comes back to the lead) → lead merges accepted branches onto `review/<dept>-<n>` → lead tells the Hub "merge-ready" → the Hub merges into `main` (`--no-ff`, git identity above) without re-reviewing detail. Cross-department integration is the Hub's. **Centralized merges are the rollout setting (DEC-099):** once lead-managed workers and worktrees prove stable, the Hub reassesses letting leads merge routine domain-local work themselves; cross-domain integration and mainline/release decisions stay with the Hub either way.

## 0.6 Context loading
| Role | Reads at start | On demand | Not by default |
|---|---|---|---|
| Hub | `HUB_RESUME.md`, `PROJECT_STATE.md`, newest cross-department DECs, lead messages | a dept file's "Status for Hub" section; a full dept file only to settle an escalation | packets, handoffs, code, assets, worker transcripts, large plan docs |
| Lead | `CLAUDE.md`, §0, its dept file, its Active/Ready packets | its workers' handoffs and diffs; the domain docs its dept file lists; another dept file's "Contracts" section | other departments' state, large plan docs in full |
| Worker | `CLAUDE.md`, its packet, the exact § the packet cites | repo files the task needs | `PROJECT_STATE.md`, dept files, BACKLOG, DECISIONS beyond the cited entries |
| Reviewer | packet, handoff, diff, the acceptance sources cited | — | everything else |

Packets reference authoritative files by path + §; they never copy canonical text.

## 0.7 Reporting (compress at every step up)
- **Worker → lead:** `Docs/Handoffs/<ID>.md` (§57) + a ≤15-line final message: result, files changed, validation, decisions, deviations from spec, blockers, dependencies created/changed, integration notes, questions.
- **Lead → Hub:** a SendMessage of ≤12 lines, only when something matters: merge-ready branches, decisions needed, blockers/risks, cross-department dependencies, material deviations, major status change. The lead also keeps its dept file's "Status for Hub" (≤15 lines) current. Never forward transcripts or routine progress.
- **Hub → Nolan:** only what he needs to know or decide, batched per milestone unless blocking (DEC-085). **The chain filters routing, not importance (DEC-098):** anything Nolan should know or decide reaches him. A lead marks such an item `FOR NOLAN` in its message to the Hub; the Hub forwards it at once if it is blocking or important, and never drops one without telling him.
- **Questions for Nolan:** workers list them in their handoff (DEC-047) → the lead answers what the evidence answers (**search `DECISIONS.md`/`KNOWN_GAPS.md` first; never re-ask an answered question**) and keeps the rest in its dept file → the Hub batches them to Nolan. Nobody below the Hub asks Nolan (DEC-033); if Nolan writes to a lead or worker directly, it answers and records what he said for the Hub.

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

**Dept:** <Gameplay|World|Assets|Hub> · **Role:** <ROLE> · **Priority:** P<n> · **Branch:** worktree off `main` (<dependencies merged>)
**Owner:** <worker id + branch, set at launch> · **Reviewer:** <pool reviewer> · **Touches:** <other-dept paths + that lead's OK, or none> · **Interfaces:** <contract files built against, or none>

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
`Docs/Handoffs/<TASK_ID>.md` (≤N lines) + ≤15-line summary for your lead (§0.7). Questions go to your lead, never to Nolan (DEC-033); unsure facts get a GAP placeholder (DEC-047).
```

# 57. WORKER HANDOFF FORMAT

Every worker must write:

*(Template written by DOC-001, AUDIT-001 B7/DEC-064: the original handoff left this block empty. It follows the packets and handoffs actually used in `Docs/Tasks/` and `Docs/Handoffs/`.)*

```markdown
# <TASK_ID> handoff

**Branch/commit:** <branch> @ <sha> · **Status:** done | partial | blocked

## Delivered
- <what changed, with paths>

## Validation
- <command → result, evidence path>

## Not done / risks
- <anything skipped and why>

## Questions for Nolan (through the Hub)
- <source file + tile/crop, what you see, best candidates; GAP id used meanwhile> (DEC-047)

## For the lead
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
