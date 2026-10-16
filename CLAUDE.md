# Working rules (token-efficient by default)

These rules load into every session, so they are kept short on purpose.

## Look before reading
- Find code with Grep/Glob first. Read only the line range you need, not whole files.
- Don't re-read a file you just read or edited, and don't re-run a command whose output you already have.
- Skip generated or vendored paths (node_modules, dist, build, coverage, lockfiles, *.min.*) unless the task is about them.
- Make independent tool calls in parallel, in one message.

## Do the work
- When you have enough to act, act. Don't restate the request or list options you won't pursue.
- Ask a question only when the answer changes what you do. Otherwise pick the sensible default and say so in one line.
- Make the smallest change that fully solves the task. No drive-by refactors and no speculative abstractions.
- Validate narrowly: run the tests, lint or typecheck for the files you changed, not the whole suite. Run the whole suite only before a push or when asked.
- Pipe noisy commands through `tail`, `head` or `grep`, and use quiet flags (`-q`, `--silent`, `--reporter=dot`).
- Spawn subagents only when asked, or when a search would otherwise flood the context with file dumps.

## Answer briefly
- Lead with the result. Use a short summary, the changed files as `path:line`, and anything the user must do.
- Don't paste back code you just wrote, whole files, or long logs. Quote only the lines that matter.
- No preamble, no recap of earlier turns, no closing pleasantries.
