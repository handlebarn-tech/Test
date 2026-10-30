# REVIEW-W4H — DES-002 (post-slice roadmap, COMP-002 and GAME-004 specs, six Ready packets)

**Verdict: PASS with minors (GO to merge).** Docs only. Reviewed `claude/task-des-002-8eda66` @ a8b8993, merged `--no-ff` into `review/wave-4h` off main. Merge note: main had already moved the DES-002 packet to `Docs/Tasks/Done/`, and git relocated the branch's `Active/DES-002.md` there. No conflict left. No blockers or majors; two minors need a Hub touch when the rows are registered.

## 1. Legal numbers trace to sources — PASS
Checked against `AZ_COMPLIANCE.md` (A1–A9, B1–B4, E1–E2, F1–F4, H1) and `OFFICE_FINDINGS.md` (O1–O16):
- 28.0 g cap / 5 g concentrate / "ounce" ambiguity → A1, A4, A8, O4. ✔
- Medical 2.5 oz per 14 days, 70.87 g → A5, O4; the gram figure comes from `AZ_COMPLIANCE_CHANGES.md` (2.5 oz). ✔ Derived as 2.5 × 28.35 while the adult cap uses 28.0 g; the spec says so itself (GAP-COMP-06). The inconsistency is real but labelled and low-risk.
- Medical tax 9.1 % → F4 (provisional with OPEN-4, stated). Out-of-state card → A7. $2,000 fine text → B4. 21+ and the 30-day vertical rule → B1, B2, O3. Edible 10/100 mg → E1. ✔
- The ID-case table is consistent with B2 and O3. The out-of-state vertical case is store policy O3 and is flagged as a possible conflict (GAP-COMP-03).
- Everything else is tagged [GDD] with a reason (e.g. `overLimitAskChance` 0.06 against COMP-001 L1's ~3 %). No invented law found.
- Departure from COMP-001 L1 ("sell over = strike"): over-limit Confirm stays blocked, as the real POS does (O4). This is consistent with DEC-032 and DEC-036 M1, and is proposed as a new DEC (handoff action 4).

## 2. Store facts, DEC-034, brands, tool parity — PASS
- Store facts are cited by RES-001 row (A1, A2, F4–F6, F8, O8, O9, O11–O13, P2, P7–P9) or tagged GAP-PKG-01..08 / GAP-COMP-01..08. Spot-checked rows say what the specs claim.
- DEC-034 is respected: the slice stays deli-only, and the 8 packaged categories are PS3.
- All prices are placeholders marked GAP-PKG-04; no packaged catalog is invented. Prepack and preroll prices reuse the tool's `TIER_DEFAULTS`.
- Tool parity is stated clearly: the tool scores deli flower only. Strain-linked prepack/preroll use the engine; vape/extract get an explicit [GDD] `concentrateFitFactor`; strain-less items are constraint matches with no effect claims (H1).
- Generic labels: §6 requires generic art and no brand marks, and GAP-PKG-07 defers the trademark call. Real brand names (DGT, High Tide, High Variety/tōk) appear only in the "Known facts" column as citations of RES-001 A2.

## 3. Roadmap order and collisions — PASS with minors
- Order PS1 → PS2 → PS3 → PS4 (gated) fits DEC-008 and spec §104. The "decisions per art/data" table is sound.
- **m1 ID collision: ART-005.** BACKLOG ART-005 is "W4F m1/m2 fixes + Retail_Lookdev in AdditiveScenes" (queued). The roadmap re-uses ART-005 for "BOH/HUB stock dressing" (PS2) and `ART-006` for FOH racks (PS3). Rename the roadmap rows (e.g. ART-007/ART-008) when the Hub registers them. `UX-003/004`, `GAME-011..016`, `DES-003`, `DATA-002`, `PERF-002` are free in BACKLOG.
- **m2 Roadmap says "PROC-004 … depends on PROC-001, PROC-003"; BACKLOG says PROC-002 and the row is already Active** (a different session is running it). Treat the roadmap's PROC-004 row as informational and keep BACKLOG's text.
- **m3 File ownership vs GAME-005.** GAME-005 (active) will edit slice jar view code (SliceScreen/jar fill hook). GAME-006/007/008/009 own `Presentation/Slice/` and `Simulation/Slice/`. No overlap in the current files, but queue GAME-006 after GAME-005 merges (packet already says `off main`); GAME-010 owns `SliceConfig.json` values, which GAME-006..009 add keys to. Run GAME-010 first or rebase carefully. REF-008, PROC-003/004, ART-005 and PERF-001 touch art/scenes/tools and do not collide.
- **m4 Editor budget (DEC-013).** GAME-005 and PERF-001 are using the 2 Unity editors now. Every PS1 packet except UX-002 is a Unity task; start UX-002 (docs only) now and queue the others.

## 4. Ready packets — PASS
UX-002, GAME-006..010 use the house format (Role/Priority/Branch, Goal, Read, Owns, Deliverable, Validation, Handoff ≤ 40 lines, DEC-033 line). Each has concrete validation (studio.ps1 compile / EditMode / PlayMode, named test cases, boundary dates, DEC-013 gate). Ownership is explicit and keeps Domain untouched (DEC-001).
- m5 Count mismatch: the roadmap's GAME-008 row says "7 ID cases"; SPEC_COMP002 §3 and the handoff list 8. Use 8.
- m6 Roadmap exit test "≥ 30 % of customers buy packaged" is derived from A1's 70 % of net *sales*; a share of sales is not a share of customers. It is labelled [GDD], but the PS3 playtest should say "≥ 30 % of sales lines".
- n1 The packets point at `Docs/Specs/UX_PS1.md`, which UX-002 creates; the packets say "once merged". Fine.

## 5. The 7 questions for Nolan — PASS
Each is concrete, tied to a GAP id, and asks for a fact or an export, not an opinion. None lead toward an answer. Q4 uses "OPEN-2" shorthand; the Hub should restate it as "does the store limit repeat adult-use purchases in a day?" when passing it on. Q6 should say the export must have no customer or employee data (the spec already says PII-free).

## Hub actions (beyond the handoff's list)
1. Renumber the roadmap's ART-005/ART-006 before adding rows (m1).
2. Order the editor queue: UX-002 now; GAME-006 after GAME-005 merges; GAME-010 first of the Unity PS1 tasks (m3, m4).
3. Fix "7 ID cases" → 8 and the packaged-share wording in the roadmap (m5, m6) when merging, or leave to DES-003.
