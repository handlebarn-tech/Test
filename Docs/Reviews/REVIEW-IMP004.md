# REVIEW-IMP004: IMP-004 audit of "Bender & Asset new plan"

**Reviewer:** fresh one-shot · **Verdict to:** Hub · **Date:** 2026-10-30
**Reviewed:** `worktree-agent-a2ff4c7a134881fd4` @ 625ff5c, merged `--no-ff` onto `review/imp004` from main 369f157 (merge f2d22eb, no conflicts).
**Sources:** `Docs/Tasks/Active/IMP-004.md`, `Docs/Handoffs/IMP-004.md`, the diff, `Docs/Imports/IMP-004_AUDIT.md`, IMP-003 handoff and audit, DEC-023/047/051/062/084/114/122, REFERENCES_INDEX, ROOM_FIXTURES, BACKLOG, and the import itself (read-only; nothing run from it).

## Verdict: PASS with minors (0 MAJOR, 3 minor)

## Checks
1. **Scope.** The diff touches only the two `Owns` files (`Docs/Imports/IMP-004_AUDIT.md`, `Docs/Handoffs/IMP-004.md`). No canonical file changed.
2. **Import matches the audit.** Size 48,582 B, mtime 11:25 and sha256 `a082696…4f9e` match. The "Hub integration directive" (lines 6–28) is real and is correctly treated as a proposal (DEC-095), not acted on.
3. **Every item has a verdict and a citation.** P1–P18, roadmap items 1–53, audio and 18.15–17 are all in tables with a verdict and a DEC, RI, RF, BACKLOG or checklist citation. I spot-checked:
   - living wall 9.2 × 1.2 ft, merch rack 4.6 × 1.4 ft and hand-wash sink 1.4 × 2.2 ft are in RI §1.5, with GAP-106 for the north-wall order;
   - ATM 2.2 × 1.8 ft is in RI §1.5 and RF `Trash_Big_West_ATM`;
   - the RI §7 exclusions ("alarm items", safes, cash-handling equipment, screen contents) and DEC-062's bulletin board ("contents not modelled") are quoted accurately;
   - dustpan, thermostat and wet-floor sign exist at the import lines the audit relies on, and the dustpan rejection (no repo evidence) is consistent with DEC-047.
4. **Subfolders are the IMP-003 rounds: verified.** Live counts and newest-file times are 11 / 12 / 9 / 40 / 33 / 65 / 106 / 149 files; the newest file in each is 03:11–05:53, none after 06:00. IMP-003's audit records 65, 106 and 149 for drops 7–9 (lines 779, 874, 948), and the drop 1–4 and 6 contents match its sections. IMP-003 kept no hashes, which the audit says, so the match is on names, counts and dates. The package passes as "no new content", with a caveat in minor 1.
5. **No conflict with a DEC.**
   - DEC-023: nothing downloaded or added, so no licence or cost exposure.
   - DEC-047: A1–A4 add no store values. PROC-015 sizes come from RI §1.5 / REF-016, and the logo is "sourced or GAP".
   - DEC-051 / DEC-062: money counter, safes, deposit bags and cash bands, bulletin contents and the matching sounds are rejected.
   - DEC-084 / DEC-114 / DEC-122: PROC-014 adds review renders and planted-fault tests, and keeps visual review as the quality judge. Stage gates are not adopted, and the audit says why.
   - DEC-117: the Skill, the agent file and the Stop hook / `gate.json` are rejected as a second rules layer.
   - DEC-070/095: the plan doc is not canon, and the Hub applies A1–A4.
6. **New IDs.** PROC-014 and PROC-015 are free in BACKLOG and `Docs/Tasks`. The only PROC-014 hit is the illustrative example in STUDIO_OS §67 (history below §0), so it is harmless. Dependencies (PROC-005, REF-016) are sensible.

## Minors (non-blocking)
1. **Round 6 `Tools/Blender/patches/` is an empty directory with mtime 12:02**, after the plan doc and after every IMP-003 commit, while its parent is 05:18. The audit notes it and reasons that the count still equals 149 and IMP-003 lists no patch there. That is sound, but an empty directory can mean something was removed after the audit. The Hub should treat "no new content" as high confidence, not proven, until a hash baseline exists (PROC-005 could record one before archiving, DEC-092).
2. **H1 (ATM) recommendation is soft.** DEC-051 excludes "cash-handling equipment even where Nolan named them; generic props only" (REF-009), and an ATM is a cash machine. DEC-086 is a card terminal, so the precedent is imperfect. PROC-015 correctly makes the ATM conditional on the ruling. The Hub should decide H1 before the packet is cut, and defaulting to "not modelled" is the safer reading.
3. **§18 statuses were not checked against their source.** The ~1,899-line "consolidated standards" doc is not in the repo. The audit says so and checks RI/RF/BACKLOG instead, which is the right call. Audio is mapped at category level only (also disclosed). Neither affects a verdict.

## Not checked
I did not re-read the whole import line by line; I sampled the headings, the directive and about ten roadmap items, not all 53. I did not hash the subfolder files, because there is no IMP-003 baseline.
