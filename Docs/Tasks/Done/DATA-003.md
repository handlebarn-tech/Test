# DATA-003 — Customer needs catalog + golden parses (GAME-017a data)

**Role:** DATA · **Dept:** Gameplay · **Priority:** P0 · **Branch:** worktree off `main`; first merge `worktree-agent-aad768800c956f13b` (DES-006, in review) into it to read the audit · **Owner:** lead subagent · **Reviewer:** Unity pool (data + tool script)
**Touches:** none · **Interfaces:** `Data/Slice/SliceNeeds.json` schema (this task defines it; GAME-017a loads it)

## Goal
Build the data half of the first playable recommendation depth (DEC-096, DES-006 §5): a catalog of customer needs written in the TFS tool's own vocabulary, each with a parse captured from the real tool, so GAME-017a can grade the player's reading against the truth.

## Read
`Docs/Design/RECOMMENDATION_DEPTH_AUDIT.md` §3–5 (on the DES-006 branch); DEC-001/002/014/016/017/057/067 in `Docs/DECISIONS.md`; `Tools/Data/golden_game003.js` and `Docs/Reconstruction/GOLDEN_CASES.md` (the capture pattern); the TFS tool `C:/Users/handl/Downloads/tfs-budtender` (read-only, no PII; v7.11.4); `Code/Domain/Engine/Parser/QueryParser.cs` (`ParserOptions.Game`).

## Owns
New `UnityProject/Assets/_Game/Data/Slice/SliceNeeds.json`; `Tools/Data/golden_game003.js` (add the needs cases, keep existing output byte-identical); new `Docs/Reconstruction/golden_cases_needs.json`; a short schema section appended to `Docs/Reconstruction/GOLDEN_CASES.md`; one new EditMode test file `Tests/EditMode/Gates/NeedsGoldenTests.cs` (C# parser == captured golden for every need term); `Docs/Handoffs/DATA-003.md`. No `Code/Domain/`, no `Simulation/`/`Presentation/` edits.

## Deliverable
1. `SliceNeeds.json`: 12 needs (audit §5 list) with `id`, `trueQuery`, base `family` (one of today's 6, so `TrueFamily` keeps working), 1–4 components, each with spoken variants per utterance style (audit §3: direct, vague, wrong term, story, product reference, last time, contradictory) and 2–3 terms; exactly one term per component reproduces it. Customer lines are written dialogue, not quotes from real people; no store/product facts invented.
2. Golden capture from the real tool with `ParserOptions.Game` for every `trueQuery` and every term and term-join the picker can produce, written to `golden_cases_needs.json`. Never hand-write a parse.
3. `NeedsGoldenTests`: the C# `QueryParser` matches each golden; mismatches are reported, not "fixed" in Domain (list them in the handoff as Gate A findings).
4. Existing goldens unchanged (`golden_cases*.json` byte-identical; Gate A green).

## Validation
`node Tools/Data/golden_game003.js` reproduces the files; EditMode green including the new tests and Gate A (DEC-067). Unity: Gameplay holds 1 slot. If GAME-009's editor is open, wait for the lock (DEC-013 gate in `TOOLCHAIN_EXECUTION.md`) and never run two editors on the same project.

## Handoff
`Docs/Handoffs/DATA-003.md` (≤40 lines). Report to the Gameplay lead; never ask Nolan (DEC-033).
