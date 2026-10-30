# REVIEW-W4V — IMP-002 (DESIGN_V2 integrated as a DP add-on), docs only

**Verdict: PASS with minors (GO to merge).** `claude/task-imp-002` @ 6d1518b merged `--no-ff` into `review/wave-4v` off main fabd154; clean merge, 40 files (28 pack files, QA_TEST_PLAN, handoff, 8 packets, ROADMAP, GSS). No blockers or majors. I did not run any `.py`.

## 1. Verbatim copy — PASS
- The source pack manifest verifies 27/27 OK. In the repo, the git blobs of all 27 manifest files hash to their manifest lines except `README_FIRST.md`, whose only difference is the 3-line provenance/precedence header (diff checked: additions at the top, nothing else). The same file list as the source, plus the new `QA_TEST_PLAN.md`.
- A raw `sha256sum -c` in a Windows checkout fails for every file because of CRLF autocrlf; the handoff's 27/27 was on LF content. Not a content difference (my compare was CRLF-insensitive and found only README).
- `VALIDATION/*.py` are 100644 and reference-only; the README header says never run them.

## 2. Binding rules
- **A1 (oracle = shipped engine) — PASS.** In the README header, ROADMAP cross-cutting, GSS header, GAME-019/020/021 and `QA_TEST_PLAN.md`: v7.11.4 + DEC-015/016, DEC-060; V2 15's "never snapshot v7.11.5" is void; expected output is captured from the shipped engine.
- **A2 (parser input) — PASS.** GAME-018 and GAME-020 say the TFS input is the query text + chip + inventory snapshot id, hashed, never a structured fact-ID path (DEC-057). GAME-018 also adds the stale-result check and a redundant same-hash re-run flag. QA_TEST_PLAN repeats the rule.
- **A3 (no TFS scores/ranks in the report) — PASS.** GAME-019 and GAME-020 acceptance: the report may name the question that would have mattered, but never TFS scores, ranks or result lists (DEC-052). The counterfactual feeds DecisionRegret and is not a separate DQ term (audit C2), and DP's regret-based DecisionQuality stays.
- **A4 (EMPTY_WITH_BACKSTOCK) — PASS.** GAME-012's row cites DEC-055/061; V2 08 §13 is cited as gating the physical path, not TFS.
- **DEC-063a/b/d — PASS.** DP wins on conflicts (README, GSS, ROADMAP, every packet's header). GAME-024 uses the median of the last 6 eligible shifts, at most one below gate − 10, under 4 shifts means insufficient evidence, repeated seed gives no new evidence, with the gentler DP §80 gate values. PS4 items (06, 07) stay parked. Ambiguity stays DP tiers 0–4 (audit C1).

## 3. Scope and "no rule removed" — PASS
- No PS1 packet changed (GAME-006..010 not in the diff); no `Code/` edit; Hub-owned files untouched.
- The 8 GAME packets have additions only ("V2 additions" before Handoff); 70 lines added, none removed. In the ROADMAP, the 4 changed lines (DES-004, GAME-011, GAME-012, PS4) keep their old text as a prefix with nothing removed. The one explicit replacement is GAME-024's rolling-update gating, replaced by the DEC-063b model and cited; the DP §79 value may remain for the career screen.
- Every added bullet cites a V2 file+section, an audit row, an EX/QA id, or A1–A3/C-ids (script check: none uncited). DES-004's 32-minute Standard shift is inside DEC-056's 25–40 min, and the single-server caveat vs 11 registers (DEC-039) is stated.

## Minors
- m1 The copied V2 files keep their original text where it conflicts with A1/A2 (15: "do not snapshot v7.11.5"; 01 §4 and `CONFIG/data_contracts.yaml`: structured TFS input). The override lives in the README header, ROADMAP, GSS and the packets. A builder who opens only 01 or the YAML misses it. Keep the copy verbatim, but add `DESIGN_V2/` to DOCS_INDEX with the A1–A4 override line, and put a "Read: DESIGN_V2/QA_TEST_PLAN.md + README header" line in QA-002 and the packets (handoff already notes this).
- m2 GAME-022's ambiguity remap "Standard 25/40/20/10/5" is labelled an example, but V2 Standard is 25/40/25/10; "tier 3 split" does not produce 20/10/5. Correct to 25/40/25/5/5 (or state the intended re-weighting) before GAME-022 uses it.
- m3 Hub follow-ups from the handoff: ratify or drop the proposed DEC (exploit test before a system is complete) and register GAP-V2-01; BACKLOG/DOCS_INDEX do not list `DESIGN_V2/` yet.
- n1 Consider dropping the `.py`/`.csv` under `VALIDATION/` if the Hub prefers no executable-looking files in the repo; they are inert.
