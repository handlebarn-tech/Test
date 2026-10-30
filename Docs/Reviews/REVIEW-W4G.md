# REVIEW-W4G — BUILD-005 (Git LFS for generated procedural FBX)

**Verdict: PASS (GO to merge).** Reviewed `claude/task-build-005` @ a526d0f merged `--no-ff` onto main 837990b (branch `review/wave-4g`). No blockers, no majors.

## Checks
1. **Patterns** — PASS. `.gitattributes` adds exactly `Art/Exports/**/*.fbx` and `UnityProject/Assets/_Game/Art/Procedural/**/*.fbx` (lines 52-53, after `*.fbx binary`). `git check-attr`: other FBX dirs, PNG and .blend in Art/Exports are unaffected. All tracked FBX sit under an LFS-covered path (none left as plain blobs). `main` is an ancestor of the merge: no history rewrite; the 15 FBX become 131-byte pointers only in the new commit.
2. **doctor** — PASS. `studio.ps1 doctor` → `lfsPatterns 11/11 tracked`, `gitLfs True`, status pass.
3. **Re-export** — PASS. `jar_fill` re-export with unchanged params is byte-identical (no diff). With `jitter_m` 0.010→0.011 all 6 fills changed and stage as 4-line LFS pointer diffs (`git lfs status`: `LFS: old -> LFS: new`, e.g. Frosty 88aa57b, 747356 B); history cost per tweak is now ~1 KB per file instead of ~750 KB. Tweak reverted. Unity gate on the merge: `unity-compile` csErrors=0; `unity-test-edit` 149/149 (incl. 8 JarFillImportTests), run through `studio.ps1` (DEC-013 gate; I ran one editor).
4. **Worktree/clone** — PASS. This worktree resolves LFS objects (Frosty sha256 `31960aff…`). A fresh `git clone` + checkout of the branch smudged real FBX (`Kaydara FBX Binary`, same sha) and `git lfs fsck` OK.

## Notes (non-blocking)
- n1 LFS objects exist only in this machine's local store. If/when the repo is pushed, `git lfs push --all origin` is needed or other clones get missing objects. No remote check was done.
- n2 `Art/Exports/Procedural/manifest.json` shows full-file diffs on every regeneration (CRLF/LF churn, 428 lines); consider `.gitattributes` `eol` for it (BUILD follow-up, cosmetic).
- n3 Old history still carries the ~9 MB of pre-LFS FBX blobs (by design, no rewrite).
- n4 `studio.config.json` already present; nothing copied.
