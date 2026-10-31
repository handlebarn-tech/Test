# Dispo Game — Model Selection / Routing Audit

**Date:** 2026-10-31  
**Source reviewed:** `dispo_model_search.txt` supplied by Nolan  
**Purpose:** Identify every meaningful place in the supplied search export that discusses choosing or switching between Fable, Opus, Sonnet, Haiku, or stronger/cheaper model tiers; preserve exact wording and identify conflicts/amendments.

---

## 1. Important source limitation — why the root files were not visible

The supplied `dispo_model_search.txt` is a **partial recursive PowerShell search export**, not a reliable complete inventory of the current main checkout.

Evidence from the export:

- The file is approximately **30.5 MB** and contains about **174,494 rendered lines**.
- Its formatting matches PowerShell `Select-String -Context` output (`>` on matching lines, surrounding context indented).
- Every relevant path in the supplied export is under `.claude\worktrees\...`.
- The worktrees represented are:
  - `.claude\worktrees\adoring-bell-224eaa\`
  - `.claude\worktrees\agent-a30ffb90da0a3f699\`
  - `.claude\worktrees\agent-a31af9058f9ecbad2\`
  - `.claude\worktrees\agent-a718b1011f640a7ac\`

**Why this happened:** the recursive PowerShell search descended into the very large `.claude\worktrees` tree. That search was taking extremely long and was interrupted. The resulting export therefore contains a large amount of worktree material but does **not** establish that the root/main-checkout copies of these files do or do not contain the same rules.

Therefore:

> **Do not interpret “no root-level path in this export” as “the rule is absent from main.” The supplied search did not give reliable main-checkout coverage.**

The findings below are exact for the copies visible in the supplied export.

---

# 2. Executive finding

There are two generations of model-selection policy.

## Original policy — DEC-140

DEC-140 assigned models primarily by **task category**:

- Hub: Opus or Fable
- Unity/gameplay/Blender/visual work: Opus
- document-oriented work: Sonnet
- Unity/visual reviews: Opus
- doc-only reviews: Sonnet

## Governing amendment — DEC-143

DEC-143 explicitly changes that policy:

> **“Model selection is by the character of the work, not its category.”**

It specifies:

- cheaper model for **bounded, deterministic** work;
- strongest model for **ambiguous, architectural, cross-system, high-risk, or judgment-heavy** work;
- this applies regardless of whether the task is **docs, Unity, Blender, or data**;
- the Hub stays on the **strongest appropriate reasoning level**.

Most importantly, DEC-143 explicitly says:

> **“Amends DEC-140's category table.”**

`HUB_RESUME.md` and `STUDIO_OS.md` then implement the DEC-143 rule operationally.

### Main inconsistency found

`Docs\STUDIO_OS.md` still contains a packet template at line 602:

> `**Model:** opus|sonnet (DEC-140)`

That line still points only to DEC-140 and hardcodes only `opus|sonnet`, despite DEC-143 explicitly superseding DEC-140's category-based model table.

This is the clearest stale model-routing wording in the supplied material.

---

# 3. Exact governing and historical wording

## A. `Docs\DECISIONS.md`

Visible identically in all four supplied worktree copies.

### Line 145 — DEC-140 — original category-based model table

**Paths in supplied export:**

- `.claude\worktrees\adoring-bell-224eaa\Docs\DECISIONS.md:145`
- `.claude\worktrees\agent-a30ffb90da0a3f699\Docs\DECISIONS.md:145`
- `.claude\worktrees\agent-a31af9058f9ecbad2\Docs\DECISIONS.md:145`
- `.claude\worktrees\agent-a718b1011f640a7ac\Docs\DECISIONS.md:145`

**Exact wording:**

> - DEC-140 | 2026-10-30 | **Model tiers and caps.** Hub: Opus (or Fable) at high effort, replaced at ~300k context (DEC-102). Workers: Opus for Unity/gameplay code, Blender generators and visual asset work; Sonnet for REF/RES/DATA/DOC/DES document tasks. Reviewers: Opus for Unity/visual reviews, Sonnet for doc-only reviews. Caps: at most 4 concurrent worker/reviewer sessions and 2 Unity editors (DEC-013); no two running tasks with overlapping `Owns`. Caps exist for review bandwidth, collision risk and Hub event load; plan usage stays Nolan's call (DEC-100). **FOR NOLAN to set the numbers.** | Everything ran on Opus; 11 review rounds on 3 tasks came from parallel work on shared files. | Hub, briefs

**Interpretation:** historical/original routing rule. It is subsequently amended by DEC-143.

---

### Line 148 — DEC-143 — explicit amendment and current selection principle

**Paths in supplied export:**

- `.claude\worktrees\adoring-bell-224eaa\Docs\DECISIONS.md:148`
- `.claude\worktrees\agent-a30ffb90da0a3f699\Docs\DECISIONS.md:148`
- `.claude\worktrees\agent-a31af9058f9ecbad2\Docs\DECISIONS.md:148`
- `.claude\worktrees\agent-a718b1011f640a7ac\Docs\DECISIONS.md:148`

**Exact wording:**

> - DEC-143 | 2026-10-30 | **(Nolan) RECOVERY-001 §7 approved with adjustments.** (1) Background Agent fallback approved: when `start_session` is refused the Hub runs a bounded brief as an isolated background Agent in a worktree; its transcript stays out of the Hub, work is committed before it reports, the Hub keeps authority over integration and decisions, and the Hub is never filled with task work because session creation is blocked. (2) Concurrency: 4 worker/reviewer sessions **plus the Hub**. **Model selection is by the character of the work, not its category:** the cheaper model for bounded, deterministic work; the strongest model for ambiguous, architectural, cross-system, high-risk or judgment-heavy work, whether it is docs, Unity, Blender or data. The Hub itself stays on the strongest appropriate reasoning level. Amends DEC-140's category table. (3) Hub at high effort; ~300k context is an **upper bound**, not a target: on completed-task residue, re-reading, lost project awareness or other context pressure the Hub hands over to a fresh Hub sooner. (4) Clean cutover of all pre-recovery sessions (DEC-144). | Nolan's reply to RECOVERY-001. | Hub, briefs, STUDIO_OS §0.5, HUB_RESUME

**Interpretation:** this is the decisive rule. It explicitly amends DEC-140.

---

# 4. Operational implementation of DEC-143

## B. `Docs\HUB_RESUME.md`

### Older copies — line 19 or 20

**Paths:**

- `.claude\worktrees\agent-a31af9058f9ecbad2\Docs\HUB_RESUME.md:19`
- `.claude\worktrees\agent-a718b1011f640a7ac\Docs\HUB_RESUME.md:19`
- `.claude\worktrees\agent-a30ffb90da0a3f699\Docs\HUB_RESUME.md:20`

**Exact wording:**

> 8. **Caps and models** (DEC-140/143): at most **4** worker/reviewer sessions running at once (plus you) and **2** Unity editors (DEC-013, `studio.ps1 slots`); no two running tasks with overlapping `Owns`. Pick the model by the character of the work: cheaper (`sonnet`) for bounded, deterministic work; the strongest for ambiguous, architectural, cross-system, high-risk or judgment-heavy work, whatever its category. Caps are for review bandwidth and collision risk; usage is Nolan's call (DEC-100).

### Newer `adoring-bell-224eaa` copy — line 20

**Path:**

- `.claude\worktrees\adoring-bell-224eaa\Docs\HUB_RESUME.md:20`

**Exact wording:**

> 8. **Caps and models** (DEC-140/143/151/152): at most **4** worker/reviewer sessions or Agents running at once (plus you) and **2** Unity editors (DEC-013, `studio.ps1 slots`); no two running tasks with overlapping `Owns`. **Four is a maximum, not a target:** never manufacture work to fill capacity; dispatch only worthwhile, independent, dependency-ready tasks with checkable deliverables, and leave capacity idle otherwise. Pick the model by the character of the work: cheaper (`sonnet`) for bounded, deterministic work; the strongest for ambiguous, architectural, cross-system, high-risk or judgment-heavy work, whatever its category. Caps are for review bandwidth and collision risk; usage is Nolan's call (DEC-100).

**Finding:** both versions implement DEC-143 correctly. The newer copy adds Agent/cap language but does not change model selection.

---

### Reviewer-routing wording — line 25/26

**Paths:**

- `.claude\worktrees\agent-a31af9058f9ecbad2\Docs\HUB_RESUME.md:25`
- `.claude\worktrees\agent-a718b1011f640a7ac\Docs\HUB_RESUME.md:25`
- `.claude\worktrees\adoring-bell-224eaa\Docs\HUB_RESUME.md:26`
- `.claude\worktrees\agent-a30ffb90da0a3f699\Docs\HUB_RESUME.md:26`

**Exact wording:**

> - `<ID> ready for review: <branch> @ <sha>` → start a fresh reviewer (§0.5 brief); model by the character of the review (DEC-143).

**Finding:** reviewer model choice also follows DEC-143 rather than a fixed doc-vs-Unity table.

---

## C. `Docs\STUDIO_OS.md`

### Line 19 — reviewer rule

Visible in all four worktree copies.

**Exact wording:**

> - **Reviewer:** fresh per review, archived after the verdict. Verifies against the packet and the cited sources; never manages, never edits the worker's branch. Model by the character of the review (DEC-143).

**Finding:** direct operational adoption of DEC-143.

---

### Line 49 — session launch/model-selection rule

Visible in all four worktree copies.

Core model-selection wording is identical:

> - On Nolan's own turns the Hub uses `start_session` (`context: "fresh"`, `use_worktree: true`, title `Dispo · <ID> <what>`; model by the character of the work: cheaper for bounded, deterministic work, strongest for ambiguous, architectural, cross-system, high-risk or judgment-heavy work, DEC-143).

The newer `adoring-bell-224eaa` copy continues:

> On turns another session or an event triggered, the app refuses `start_session`; after that refusal the Hub may run the same bounded brief as a background `Agent` with `isolation: "worktree"` (DEC-139/DEC-151): preferred for reviews, sync/fix rounds, integration prep and doc tasks; long production work only when the critical path would otherwise stall. Sessions and Agents share the one cap and Agents are listed in PROJECT_STATE In flight. No spare sessions, no proposal cards unless Nolan asks.

The three older copies continue instead:

> On turns another session or an event triggered, the app refuses `start_session`; the Hub then runs the same brief as a background `Agent` with `isolation: "worktree"` (DEC-139). No spare sessions, no proposal cards unless Nolan asks.

**Finding:** this is the operational point where the Hub is told how to choose a model when launching work.

---

### Line 602 — stale packet template

Visible identically in all four worktree copies.

**Exact wording:**

> **Role:** <ROLE> · **Priority:** P<n> · **Base:** `main` @ <sha> | <branch> (<dependencies merged>) · **Unity:** yes|no · **Model:** opus|sonnet (DEC-140)

**Finding:** likely stale/inconsistent.

Reasons:

1. It cites only DEC-140.
2. DEC-143 explicitly says it amends DEC-140's category table.
3. It hardcodes the field to `opus|sonnet`.
4. It does not describe the DEC-143 selection criterion.
5. It potentially encourages the Hub to think in terms of the old two-model/category table when writing packets.

This is the strongest candidate for cleanup if the current main checkout still contains it.

---

# 5. High-level project brief also carries the amended rule

## D. `Docs\PROJECT_BRIEF.md`

### Older worktree copies — line 15

**Paths:**

- `.claude\worktrees\agent-a30ffb90da0a3f699\Docs\PROJECT_BRIEF.md:15`
- `.claude\worktrees\agent-a31af9058f9ecbad2\Docs\PROJECT_BRIEF.md:15`
- `.claude\worktrees\agent-a718b1011f640a7ac\Docs\PROJECT_BRIEF.md:15`

**Exact wording:**

> - **Budget and tools:** $0 assets, licences per DEC-023/087; max 2 Unity editors at once (DEC-013); Unity worktrees max 3 (disk). Concurrency: 4 worker/reviewer sessions plus the Hub; model by the character of the work (DEC-140/143).

### Newer `adoring-bell-224eaa` copy — line 19

**Exact wording:**

> - **Budget and tools:** $0 assets, licences per DEC-023/087; max 2 Unity editors at once (DEC-013); Unity worktrees max 3 (disk). Concurrency: 4 worker/reviewer sessions or background Agents plus the Hub, a maximum not a target; model by the character of the work (DEC-140/143/151/152).

**Finding:** consistent with DEC-143.

---

# 6. Recovery audit — origin of the model-routing change

## E. `Docs\Audits\RECOVERY-001.md`

### Line 57 — original proposed category table

Visible in all four worktree copies.

**Exact wording:**

> Hub on Opus (high effort); Unity/gameplay/Blender workers Opus; doc, REF, DATA, DOC workers and doc-only reviewers Sonnet; default cap 4 concurrent worker/reviewer sessions plus the 2-editor Unity limit. The cap is for review bandwidth, file-collision risk and Hub event load, not usage (DEC-100 unchanged); Nolan sets the number.

This is the proposal reflected in DEC-140.

---

### Line 76 — records Nolan's adjustment

Visible in all four worktree copies.

**Exact wording:**

> Nolan approved §7 items 1–4 with adjustments recorded as DEC-143 (model by the character of the work; 4 sessions plus the Hub; Hub at high effort with ~300k as an upper bound) and ordered a clean cutover, recorded as DEC-144: all sessions, branches and worktrees accounted for; uncommitted work committed on its branches (PROC-009b `aefadfc`, PROC-013 originals `788046a`, PROC-017 `7f4f7d6`, one PROC-005 json on `claude/clever-lamport-837e7f`); session-only context recovered to `Docs/Handoffs/Recovered/`; `PROJECT_STATE.md` made the sole resume point; every pre-recovery session (old Hub, PO session, side chat, spares, workers, reviewers) archived; a fresh Hub started from the repaired bootstrap. The PO communication session was archived with the rest; questions ride the Hub reply until Nolan designates a new channel.

**Finding:** the recovery audit itself confirms that the initial fixed category table was adjusted before becoming the final operating rule.

---

### Line 96 — evidence of the amended rule being used

Only visible in the newer `adoring-bell-224eaa` copy.

**Exact relevant portion:**

> **Background agents.** The first post-cutover Hub turn was triggered by the recovery session's brief, not by Nolan, so the app refused all four `start_session` calls ("Start sessions only on the user's own words to you here … the task another session gave you"). Only then did the Hub start four background Agents in worktrees, within the cap of 4: ART-013 (strongest model, Unity), GAME-026 round-4 sync, REVIEW PROC-013b and REVIEW DOC-006 (Sonnet).

**Finding:** model choices were already being made by task character rather than simply “Unity = Opus.”

---

# 7. Research material — informative, not governing project policy

## F. `Docs\Research\AGENT_OPERATIONS_RESEARCH_2026-10-30.md`

### Line 16

Visible in all four worktree copies.

**Exact wording:**

> **Subagents** [A]: own context window; return only the summary; get the CLAUDE.md hierarchy and the delegation prompt, not the conversation. Frontmatter `model`, `tools`, `isolation: worktree`, `maxTurns`, `background`. "A fresh subagent first has to gather context your conversation already had." Haiku fits simple jobs. — https://code.claude.com/docs/en/sub-agents

### Line 59

Visible in all four worktree copies.

**Exact wording:**

> - Model tiering [A]: Haiku for lookups, Sonnet for implementation, top model for the hub, planning and review; Opus lead + Sonnet workers beat solo Opus by 90.2% in Anthropic's research system. Practitioner tables: real Haiku savings ~12× because of extra turns. — https://code.claude.com/docs/en/best-practices, https://dev.to/aobaworks/claude-code-subagents-model-selection-role-by-role-table-3o4j

**Finding:** these are research notes supporting the recovery design. They are not themselves the final project authority. They mention Haiku explicitly, but the governing project rule visible in DEC-143 does not require “Haiku for lookups.”

---

# 8. Evidence of actual model assignments in `PROJECT_STATE.md`

These are state/history examples rather than general policy, but they show how the amended rule was applied.

## G. `Docs\PROJECT_STATE.md`

### Line 34 — ART-013

Newer copy:

> | `art013` local_62f68467 (Fable, Unity slot 1) | ART-013 | cut from `art013-r2` @ 6373613 (WIP + `main` merged; packet in Active with rulings) | working → fresh Unity reviewer on `ready for review` |

Older copies:

> | Dispo · ART-013 layout overhaul (Fable, Unity slot 1) | ART-013 | `claude/art013` from 14b3eb3, merges `main` | working → fresh Unity reviewer on `ready for review` |

### Line 35 — GAME-026

Newer copy:

> | `game026-r4` local_0ea24110 (Sonnet, Unity slot 2) | GAME-026 | cut from `task/GAME-026-r4` @ f65bf07 (060f4af + `main` merged; re-copy and tests to do) | working → fresh Unity reviewer (r4) on `ready for review`; a repeat of the stale-copy MAJOR is a Hub decision (DEC-142) |

Older copies:

> | Dispo · GAME-026 sync + tests (Sonnet, Unity slot 2) | GAME-026 | `task/GAME-026` from 060f4af, merges `main` | working → fresh Unity reviewer (r4) on `ready for review`; a repeat of the stale-copy MAJOR is a Hub decision (DEC-142) |

**Important:** this is direct evidence that a Unity-slot task was assigned to **Sonnet**, which is consistent with DEC-143 and inconsistent with treating DEC-140's old “Unity/gameplay = Opus” table as absolute.

### Lines 36–37 — reviewers

> | `rev-proc013b` local_d43b98f6 (Sonnet) | PROC-013b review | cut from `review/proc013b` @ 5784aed (worker branch merged) | reviewing → integrate on PASS |

> | `rev-doc006` local_12ca8f13 (Sonnet) | DOC-006 review | cut from `review/doc006` @ 98ec160 (worker branch merged) | reviewing → integrate on PASS; register the DOC-006 row (DOC-005 "LFS guard" row renamed) |

### Line 25 — queued work

> | **REF-015** exterior envelope | `claude/dazzling-jennings-baa5c9` @ 0afad5c | measurements done; rows/§10 not written | *queued* (Sonnet, doc only, no Unity: the filler when a slot frees). |

---

# 9. Other related references

## `Docs\BACKLOG.md:184`

Only visible in the newer `adoring-bell-224eaa` copy.

> | OPS-005 | P1 | Review the briefs and packet rulings the first post-cutover Hub wrote during the pause (ART-013 `## Hub rulings`, GAME-026 r4 scope, PROC-013b/DOC-006 review briefs) for scope, definition of done and DEC-142 sync discipline before those workers restart | — | Ready (DEC-152; doc-only; Hub or a Sonnet worker) |

This is an assignment example, not a general model-selection rule.

---

# 10. Authority / precedence assessment

Based strictly on the supplied material:

1. **DEC-140** establishes the original model-tier/category system.
2. **DEC-143** explicitly amends DEC-140's category table.
3. `HUB_RESUME.md` tells the Hub to choose models using DEC-143's character-of-work rule.
4. `STUDIO_OS.md` tells the Hub to use that same rule when starting sessions and reviewers.
5. `PROJECT_BRIEF.md` summarizes the same rule.
6. `PROJECT_STATE.md` demonstrates the rule being used in practice.
7. `RECOVERY-001.md` documents how the old rule became the amended rule.
8. `AGENT_OPERATIONS_RESEARCH_2026-10-30.md` is research/background, not the final authority.

Therefore, within the supplied material:

> **Current intended model-routing rule: choose by the character/difficulty/risk of the task, not by whether the task is docs, Unity, Blender, data, etc.**

The cheaper model is explicitly identified as `sonnet` in `HUB_RESUME.md`. The “strongest” model is intentionally expressed generically in the amended operational rule rather than permanently hardcoded to Opus/Fable.

---

# 11. Conflict / cleanup candidates

## High confidence issue

### `Docs\STUDIO_OS.md:602`

Current wording in all supplied worktree copies:

> `**Model:** opus|sonnet (DEC-140)`

Why it is stale:

- only cites DEC-140;
- does not cite DEC-143;
- DEC-143 explicitly amends DEC-140's category table;
- hardcodes model choices rather than expressing the character-of-work selection rule.

This is the main wording I would inspect in the **actual main checkout**.

## Not necessarily a problem

### DEC-140 remaining in `DECISIONS.md`

DEC-140 does not need to disappear merely because DEC-143 amended it. A decision ledger can legitimately preserve superseded history as long as the amendment is clear.

The problem would be any active instruction/template that still treats DEC-140's category table as current without respecting DEC-143.

---

# 12. What still needs verification in the actual main checkout

Because the attached export is partial and worktree-heavy, this audit does **not** prove which exact versions are presently in:

- `Docs\DECISIONS.md`
- `Docs\HUB_RESUME.md`
- `Docs\STUDIO_OS.md`
- `Docs\PROJECT_BRIEF.md`
- `Docs\PROJECT_STATE.md`
- `Docs\Audits\RECOVERY-001.md`
- `Docs\Research\AGENT_OPERATIONS_RESEARCH_2026-10-30.md`

at the root of the current main checkout.

The next verification should search only the current checkout while explicitly excluding `.claude\worktrees`, Unity generated folders, and other nested/generated trees.

Until that is done, the safest conclusion is:

> **The supplied worktree snapshots consistently show DEC-143 as the intended governing model-selection rule, with `STUDIO_OS.md:602` as a likely stale template reference. Main-checkout state still needs a targeted verification.**

---

## Bottom line

The project did not simply say “use Opus for important work and Sonnet for docs.”

It first said that in DEC-140, then Nolan-approved DEC-143 deliberately changed the rule to:

> **Model selection is by the character of the work, not its category.**

The active Hub/session instructions visible in the supplied worktrees correctly repeat that amended rule.

The one clear holdover is:

> **`Docs\STUDIO_OS.md:602` — `**Model:** opus|sonnet (DEC-140)`**

which should be checked against the current main checkout.
