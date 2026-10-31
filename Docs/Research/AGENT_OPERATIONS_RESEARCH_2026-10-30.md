# Running large multi-agent Claude Code projects: research report (2026-10-30)

> Gathered for RECOVERY-001 by a research subagent of the recovery architect (Fable). Evidence base for the operating model in `Docs/STUDIO_OS.md` §0 and `Docs/HUB_RESUME.md`. Legend: **[A]** official Anthropic docs/engineering post · **[P]** practitioner opinion/experience · **[R]** research paper. Figures marked single-source are heuristics, not measured on this repo.

## 1. Official Anthropic guidance

**CLAUDE.md** [A]
- "Target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence." `@imports` organise a long file but do not reduce its context cost. — https://code.claude.com/docs/en/memory
- Write only "what Claude can't find by reading the repo, or what it would otherwise spend time rediscovering every session." If Claude ignores a line, adding IMPORTANT will not fix it: either the file is too long or the line is a rule with no exceptions, which belongs in a hook. — https://code.claude.com/docs/en/best-practices
- Nested CLAUDE.md files load on demand when a file in that folder is touched. Root CLAUDE.md is re-injected after compaction; nested ones are not until re-triggered. — https://code.claude.com/docs/en/memory, https://code.claude.com/docs/en/context-window
- `.claude/rules/*.md` with `paths:` frontmatter loads only when matching files are touched; skills load name + description only until invoked. — https://code.claude.com/docs/en/best-practices, https://code.claude.com/docs/en/sub-agents
- Large repos: root = repo-wide rules, per-subsystem CLAUDE.md = that area's stack; `Read` deny rules for generated code. Plan files are re-injected after compaction, "so the plan survives where conversation history may not." — https://code.claude.com/docs/en/large-codebases

**Auto memory** [A]: `~/.claude/projects/<project>/memory/MEMORY.md` index, first 200 lines / 25 KB loaded per session; topic files read on demand; shared across worktrees of one repo; not passed to subagents. — https://code.claude.com/docs/en/memory

**Subagents** [A]: own context window; return only the summary; get the CLAUDE.md hierarchy and the delegation prompt, not the conversation. Frontmatter `model`, `tools`, `isolation: worktree`, `maxTurns`, `background`. "A fresh subagent first has to gather context your conversation already had." Haiku fits simple jobs. — https://code.claude.com/docs/en/sub-agents

**Hooks vs instructions** [A]: "If something has to happen every time, make it a hook, a deny rule, or a managed setting. CLAUDE.md is for guidelines, and Claude is allowed to decide a guideline doesn't apply." — https://code.claude.com/docs/en/best-practices

**Context and compaction** [A]: `/clear` between unrelated tasks; compaction keeps decisions and unresolved bugs, discards redundant tool output; after two failed corrections, clear and write a better prompt. — https://code.claude.com/docs/en/context-window, https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

**Context engineering** [A]: context is a finite attention budget; "context rot" = recall degrades as tokens grow. Claude Code is the hybrid model: CLAUDE.md pre-loaded, everything else just-in-time. Subagents may burn tens of thousands of tokens but return 1–2k-token summaries. Durable strategies: compaction, structured note-taking, sub-agents. — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

**Long-running harnesses** [A]
- Initializer + coding agent; feature list in JSON (models are "less likely to inappropriately overwrite it"), a progress file, one feature per commit. Session-start ritual: `pwd`, git log, progress file, pick the highest-priority unfinished feature, smoke test before new work. Failure modes: doing too much at once; declaring done prematurely. — https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Planner / generator / evaluator: "agents reliably skew positive when grading their own work"; a standalone skeptical evaluator is more tractable. Fresh agent + structured handoff beat in-place compaction for drifting models. — https://www.anthropic.com/engineering/harness-design-long-running-apps
- Memory tool + context editing: +39% on an agentic search eval; context editing alone 84% fewer tokens over 100 turns. — https://claude.com/blog/context-management

## 2. Hub/orchestrator + worker architectures
- Orchestrator-workers only when subtasks cannot be predicted; otherwise the simplest design, adding complexity "only when it demonstrably improves outcomes." [A] — https://www.anthropic.com/engineering/building-effective-agents
- Briefing [A]: "Each subagent needs an objective, an output format, guidance on the tools and sources to use, and clear task boundaries." Multi-agent costs ~15× chat tokens; token usage explains 80% of performance variance. Avoid the lossy relay through the lead: subagents store outputs and return lightweight references. — https://www.anthropic.com/engineering/multi-agent-research-system
- Telephone game [P/R]: qualifiers, dead ends, implicit decisions and exact identifiers vanish first; loss compounds per hop (90% × 5 hops ≈ 59%). MAST (arXiv 2503.13657): ~37% of multi-agent failures are inter-agent misalignment. Mitigations: artifacts over summaries, verbatim lanes for constraints/IDs/decisions, typed handoffs. — https://tianpan.co/blog/2026-07-02-the-telephone-game-in-your-agent-pipeline
- Cognition [P]: "Share context, and share full agent traces"; parallel siblings with unstated assumptions produce incompatible work. — https://cognition.com/blog/dont-build-multi-agents
- Counter-view [P]: if handoff loss exceeds context degradation, subagents do not pay off; they fit fan-out research, mechanical work and fresh-eyes review. — https://12gramsofcarbon.com/p/agent-orchestrators-are-bad
- Depth: practitioners converge on one hub + one layer of workers + a separate reviewer; add a hop "only when it buys parallelism, needed context capacity, or defensible isolation."

## 3. Persistent project knowledge
- CLAUDE.md as router [P]: root file < 60 lines; models follow ~150–200 instructions reliably and the system prompt already uses ~50; task docs in a docs folder with one-line triggers; `file:line` references instead of snippets. — https://understandingdata.com/posts/writing-a-good-claude-md
- Progressive disclosure one level deep; "deeper trees leave agents lost"; a compressed docs index in the root file hit 100% in Vercel's evals while skills were never invoked in 56% of cases (secondhand). — https://alexop.dev/posts/stop-bloating-your-claude-md-progressive-disclosure-ai-coding-tools/
- Research → Plan → Implement [P]: humans review research and plans, not code; "a bad line in a plan can produce hundreds or thousands of bad lines." Keep context utilisation 40–60%. — https://www.humanlayer.com/blog/advanced-context-engineering
- Ralph loop [P]: a disposable implementation plan regenerated when the agent drifts; one task = one commit; operational AGENTS.md ~60 lines. — https://claytonfarr.github.io/ralph-playbook
- ADRs: no 2025–26 source treats ADRs specifically as agent memory; closest official analogue is the JSON feature list + progress file.

## 4. Stale-agent prevention and lifecycle
- Context Rot (Chroma, Jul 2025) [R]: 18 models degrade with input length even on trivial retrieval; distractors compound. — https://www.trychroma.com/research/context-rot. NoLiMa (ICML 2025): at 32k tokens 10 of 12 models fall below 50% of short-context performance without literal matches. — https://huggingface.co/papers/2502.05167
- Compaction loses file paths, error messages, debugging state and "the thing you said not to do again"; durable facts must live on disk. — https://www.morphllm.com/claude-code-auto-compact
- Fresh-agent resets with a structured handoff beat in-place compaction; workers short-lived; the hub survives by re-reading disk state, not by living forever. — harness-design post; best-practices doc.

## 5. Git-backed state, worktrees, review loops
- Worktrees [A]: a second session is "the easiest independent reviewer you can get"; `/code-review` runs in a fresh subagent "never swayed by the reasoning that produced the code." Ask for evidence: "'All tests pass' on its own tells you very little." — https://code.claude.com/docs/en/best-practices
- What worktrees do not isolate [P]: semantic conflicts that merge cleanly, shared ports/DBs, lockfile merges; define shared contracts first, one integrator, verify the merged result. — https://dev.to/naw103/running-multiple-claude-code-agents-in-parallel-what-worktrees-cannot-see-4le7
- Coordination files edited by many agents become a conflict surface; task claims and serialised same-module work removed conflicts (43% → 0%). — https://github.com/indiekitai/claude-orchestrator
- Anthropic C compiler [A]: 16 agents, ~2,000 sessions. What broke: agents fixing the same bug and overwriting each other; test output flooding context. What worked: a near-perfect verifier, terse greppable output, independent units of work. — https://www.anthropic.com/engineering/building-c-compiler
- Preventing redefinition of truth [A]: workers may edit only a `passes` field of the feature list; enforce via PreToolUse hooks blocking protected paths and a Stop hook running the check. Imbue split implementation vs non-implementation commits so the integrator merges the safe half directly. — https://imbue.com/blog/mngr_part_2

## 6. Token-efficient delegation
- Brief = objective, output format, tools/sources, boundaries [A], plus verbatim constraints, identifiers and ruled-out approaches [P]. Point workers at exact files/sections.
- Structured handoffs with file references, not prose summaries.
- Model tiering [A]: Haiku for lookups, Sonnet for implementation, top model for the hub, planning and review; Opus lead + Sonnet workers beat solo Opus by 90.2% in Anthropic's research system. Practitioner tables: real Haiku savings ~12× because of extra turns. — https://code.claude.com/docs/en/best-practices, https://dev.to/aobaworks/claude-code-subagents-model-selection-role-by-role-table-3o4j
- Avoid re-reading: deny rules on generated code, terse tool output logged to files. Prompt cache lasts ~1h on subscription, 5 min for subagents.

## 7. Practitioner experience (what broke / what worked)
- C compiler: "Parallelism needs independent units of work. One giant task causes collisions."
- Imbue: confused agents signal unclear interfaces/docs; let agents report "blocked"; develop at ~10 agents before scaling.
- Harness design: an evaluator "talked itself into approving" real issues until calibrated.
- Ralph: stubs and "assume not implemented" are the recurring failures; regenerate the plan file periodically.
- A shared notes file without a claim step caused duplicate work.

## Top 15 rules for a hub that must stay smart without reading the whole repo
1. Always-loaded hub set = a small rules file + one resume file + one state file; everything else fetched on demand.
2. The state file is a one-line-per-item index with links, never accumulated narrative.
3. Pre-load stable facts; load task docs just-in-time, one level deep.
4. Record every durable decision on disk the moment it is made.
5. Hub restarts are normal: git log + state file + smoke check, designed for that reader.
6. Workers are short-lived: one packet, one deliverable, done.
7. Every brief carries objective, output format, sources, boundaries, verbatim constraints and ruled-out approaches.
8. Workers return structured handoffs with file references; the hub reads the handoff, not the transcript.
9. Fresh reviewer, no sight of the worker's reasoning, command output as evidence.
10. Protect truth with hooks and deny rules, not CLAUDE.md lines.
11. Shared contracts first, then fan out; serialise same-module work; one integrator verifies the merged result.
12. Task claims, not a shared editable checklist, prevent duplicate work.
13. Tier models; check usage per subagent.
14. Terse, greppable tool output; details to files.
15. Add a hop or an agent only when it buys parallelism, context capacity or isolation.

Not verified first-hand: the MAST paper, the Vercel skills eval and claude-orchestrator's full guide (figures are secondhand).
