# REVIEW-W3C — Review COMP-001 + RES-001 + ASSET-002 (research and assets)

**Role:** REVIEW (docs/research) · **Priority:** P0 · **Branch:** worktree off `main`; local branch `review/wave-3c`.

## Setup
`git merge --no-ff` each of `claude/task-comp-001-c5bcd5`, `claude/task-res-001-6aa95e`, `claude/task-asset-002-ed2b8b` onto `review/wave-3c`.

## Checks
1. **PII first (DEC-006/031):** RES-001 files must hold store facts only: grep for emails, phone numbers, personal names, personal drive paths, license/permit/registration numbers, credentials and security details. Any hit is a blocker; fix by deletion on this branch.
2. **COMP-001:** re-verify 8 rule rows at their primary sources (azleg.gov, azdor.gov, azdhs.gov, apps.azsos.gov); confirm the must-fix list matches DEC-036; note the open ambiguities (Phoenix TPT rate, ounce definition).
3. **RES-001:** spot-check that 6 findings are consistent with the existing references and DEC-034…038; findings marked Superseded are not used as current facts.
4. **ASSET-002:** `python -I Tools/Assets/fetch_assets.py --verify` passes; no binaries committed; Sketchfab rows `redistributable: false`; the `.gitignore` edit matches DEC-023; LFS patterns only under `UnityProject/Assets/_Game/Art/ThirdParty/`.
5. Conflicts between the three merges: resolve trivially or report.

## Owns
`Docs/Reviews/REVIEW-W3C.md`; trivial doc fixes and PII deletions on `review/wave-3c`.

## Done when
`review/wave-3c` holds the three merges and the review with a verdict. Report the verdict and a ≤12-line summary to the Studio Hub.
