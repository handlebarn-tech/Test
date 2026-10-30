# REVIEW-DES6 — DES-006, recommendation depth audit (PS1b vs the TFS tool)

**Verdict: PASS with minors (GO).** I reviewed `worktree-agent-aad768800c956f13b` @ caebbd3: 6 files, +170 lines, docs only. This file is committed on `review/des6`, cut from caebbd3. I named it REVIEW-DES6 because no wave number was given; rename it if the Hub numbers it. Inputs read: the packet, the handoff, the diff, the lead's rulings (`GAMEPLAY.md` @ 0826172), the tool source `tfs-budtender/dev/v7114/tool.html` (read-only), and the game code the audit cites.

## Checks
1. **Tool claims cite file and line, spot-checked against the source: PASS (15/15).** Every check matched what the audit says:
   - L1559: the "Type what the customer needs…" welcome text.
   - L1585-1589: the New/Experienced buttons.
   - L2196-2200: the Customer-language decode cards.
   - L2263-2264: the follow-up "Had anxiety with cannabis before?".
   - L16085-16086: "sleep but gotta work" stays a sleep ask.
   - L16227-16229: the indica/sativa/hybrid fuzzy map.
   - L16234: "good" → mood boost.
   - L16541-16554: strain lookup plus in-stock nearest.
   - L16662-16667: the budget-only "What effect…?" prompt.
   - L16677: the Help "Try:" line.
   - L19583: the `REFINE` table.
   - L19612: `buildFollowUpChips`.
   - L16047-16050: like-X.
   - L21744: `detectPriceIntent`.
   - L15619: `INTENTS`.
   - The game code checks also match: `ShiftSim.cs:136-146` and `:505-506` (the 6-family `Recommender.Recommend`); no `QueryParser`, `Responder`, `Refine` or `Similarity` call anywhere in `Simulation/` or `Presentation/`; the `SliceView.cs:12` header; `Responder.cs:39-40`.
   - No PII. The tool's Help line names two strains, and the audit did not copy them; strains are `{strain}` slots.
2. **Audit table complete: PASS.** It has all 5 deliverable columns and 21 rows. It covers every input the packet names: free text, intents, refine, compare, similar, exclusions, price and details. It also covers lookup, the New-customer toggle, tiers, more-options, role tags and drive notices.
3. **Amendments consistent with each other and with DEC-001/067: PASS.**
   - None of them edits `Code/Domain/`. The Refine chip selection stays a placeholder behind an off flag until B1. That matches the lead's B1 ruling (add-only port as its own task).
   - The oracle (`trueQuery` parse) is the same in GAME-017, 019 and 017a.
   - The said/term fields run consistently from GAME-017 through 019 and 020.
   - Chip-only queries must still equal the DEC-017 goldens. Gate A stays on every PR, and the new goldens are additive and tool-captured.
4. **GAME-017a cut coherent: PASS.** In and Out are clearly split. Its Owns are a subset of GAME-017's plus the golden tooling. The lead's sequence GAME-009 → 025 → 017a → 026 serialises the shared `SliceGame`, `SliceView` and `ShiftSim` files.

## Minors
- m1 **GAME-017a will change the slice goldens.** New lines for tier ≥ 2 customers, the need-based Fit and the tiles-only penalty all change them. Unlike GAME-026, the cut does not say so. When packeting 017a, add "regenerate the slice goldens, list old → new, QA sign-off", as GAME-026 does.
- m2 **GAME-017's amendment says Phase A "may be cut out".** The lead has ruled it is split out now (Q5). Change the wording to "is GAME-017a" when that packet is written.
- m3 **GAME-017 puts the New-customer toggle in the snapshot hash unconditionally**, citing handoff Q3. The ruling makes it conditional: include it if the tool's results depend on it. They do (`T:14827-14845`, anxiety filter plus onset sort), so the result is the same. Cite the ruling and that tool line instead of the handoff.
- m4 **The audit's §2 summary says "6 rows marked H (1, 2, 4, 5, 12, plus the composer half of 3)".** Row 3 is graded M, so it is 5 H rows plus part of row 3. This is wording only.
