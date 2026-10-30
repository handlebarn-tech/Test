# REVIEW-W3A — Review GAME-003 (parser port) + BUILD-002 (tooling)

**Role:** REVIEW · **Priority:** P0 · **Branch:** worktree off `main`; local branch `review/wave-3a`.

## Setup
`git merge --no-ff claude/task-game-003-738ff2`, then `git merge --no-ff claude/task-build-002-65a668` onto `review/wave-3a`.

## Checks
1. **GAME-003** (`Docs/Tasks/Active/GAME-003.md`): `studio.ps1 unity-compile` + `unity-test-edit` green (claimed 123/123); all 39 MIG-001 goldens pass from raw queries; spot-check 6 ported parser/feature functions against cited lines in the read-only v7.11.4 `index.html`; DEC-016 MC-7/GAP-206 double goldens present; `Dispo.Domain` still `noEngineReferences`; DEC-028 boundary respected (no changes to `Catalog.Groups()` caching, label code, rep-batch fields).
2. **BUILD-002** (`Docs/Tasks/Active/BUILD-002.md`): every existing command still works with the same arguments; new `blender`/`assets-fetch`; `Wait-UnitySlot` timeout + lock (try two concurrent invocations); result JSON + `BUILD_MANIFEST.json`; doctor's missing-config path; one `unity-build`.
3. Hygiene: no PII, no secrets, no tfs-budtender files copied in.

## Owns
`Docs/Reviews/REVIEW-W3A.md`; trivial doc fixes.

## Done when
`review/wave-3a` holds both merges and the review with a verdict. Report the verdict and a ≤12-line summary to the Studio Hub.
