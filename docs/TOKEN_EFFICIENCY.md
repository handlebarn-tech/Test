# Token Efficiency Playbook

Goal: spend fewer Claude tokens on every task without losing quality.

Every message resends the whole conversation, including system prompt, CLAUDE.md, earlier turns and tool output, so most savings come from **keeping context small** and **choosing the right model or effort**, not from typing shorter prompts.

## 1. What this repo already does

| File | What it saves |
| --- | --- |
| `CLAUDE.md` | Rules Claude follows every session: grep before reading, read only line ranges, no re-reads, narrow tests, short answers. It is kept short because it loads into every session. |
| `.claude/settings.json` → `env` | Truncates Bash output at 20k characters and MCP tool output at 15k tokens, so one noisy command can't flood the context. |
| `.claude/settings.json` → `permissions.deny` | Blocks reads of `node_modules`, build output, minified files, source maps and `.env`. These are large, low-value files and the most common context sinks. |
| `.claude/settings.json` → `permissions.allow` | Read-only commands run without a prompt, so turns aren't spent on approve-and-retry. |

To apply these rules to **every** project, copy `CLAUDE.md` to `~/.claude/CLAUDE.md` on each machine where you run Claude Code. Copy the `env` block into `~/.claude/settings.json` too.

## 2. Habits with the biggest payoff (in order)

1. **Start fresh per task.** In Claude Code, run `/clear` between unrelated tasks. In claude.ai, open a new chat. Long threads are the biggest hidden cost.
2. **Compact long tasks.** Mid-task, run `/compact keep: <what matters>` so the history shrinks to a summary.
3. **Match model and effort to the task.** Use a smaller or faster model (Sonnet or Haiku, via `/model`) for routine edits, renames, docs and Q&A. Switch to Opus or high effort only for hard debugging, architecture or subtle bugs, then switch back.
4. **Point at the code.** Write "Fix the null check in `src/api/user.ts` `getUser`", not "find why users break". Exact files, functions and error lines save whole exploration rounds.
5. **Batch related asks.** Put three related changes in one message rather than three round trips, each of which resends the context.
6. **Paste excerpts, not dumps.** Paste the 20 relevant log lines, not 2,000.
7. **Ask for the format you need.** For example, "Just the diff", "Answer in 3 bullets" or "No explanation".
8. **Plan big work once.** For multi-step features, ask for a short plan first (or use plan mode), approve it, then execute. That costs less than rework after a wrong turn.
9. **Avoid fan-out unless it's worth it.** Subagents and "deep research" each start with a cold context and re-read files. Use them only for broad searches whose raw output you don't need.
10. **Turn off unused connectors and MCP servers.** Each enabled tool adds schema tokens to every request.

## 3. Habits in claude.ai chat

- Put recurring reference material in a **Project's** knowledge instead of pasting it into each chat.
- Upload only the pages or sections you need, not whole PDFs.
- Edit and resend your last message instead of adding a correction turn. This replaces the branch, so the bad answer stops costing context.
- Turn off extended thinking and web search when the task doesn't need them.

## 4. Check that it's working

- Run `/cost` (API billing) or `/context` in Claude Code to see where tokens go. Large "tool output" or "messages" figures mean you should `/clear` or `/compact` sooner.
- If one command keeps getting truncated, filter it (`| grep`, `| tail -50`) rather than raising the limit.
- Review `CLAUDE.md` every few months. Delete rules Claude already follows and add any repeated correction you find yourself typing.
