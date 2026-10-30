# Handoff — BUILD-005 (Git LFS for generated procedural FBX, REVIEW-W4E m3)

**Status:** done. Branch `claude/task-build-005` (off main 566cd77), not merged or pushed.

## Changed
- `.gitattributes`: `Art/Exports/**/*.fbx` and `UnityProject/Assets/_Game/Art/Procedural/**/*.fbx` → `filter=lfs diff=lfs merge=lfs -text`. These rules come after `*.fbx binary`, so they win.
- `Tools/Studio/studio.ps1 doctor`: `lfsPatterns` probes the 9 ThirdParty extensions plus the 2 new paths, so it reports **11/11 tracked**. It is still reported, not a failure, as before.
- The 15 existing FBX under those paths are LFS pointers in the new commit (`git add --renormalize`): 9 in `Art/Exports/Procedural`, 6 in `_Game/Art/Procedural/JarFill`. Older commits keep the full blobs; no history was rewritten.

## Validation
- PROC-002 re-export (`Tools/Blender/blender.ps1 jar_fill Tools/Blender/params/jar_fill.json`): exit 0. The FBX bytes match HEAD (Frosty sha256 `31960aff…` in both places). `manifest.json` differs only in line endings and is not committed.
- Round-trip: the staged blob is an LFS pointer (`size 747324`). I deleted the Unity copy and ran `git checkout` on it; the smudge restored the identical bytes (`31960aff…`).
- `doctor` pass (lfsPatterns 11/11) · `unity-compile` csErrors=0 · `unity-test-edit` **149/149**, including the 8 `JarFillImportTests`. DEC-013 gate through `studio.ps1`.

## Notes for the Hub / reviewer
- The LFS objects exist only in this machine's local LFS store until someone pushes. A push of this branch uploads the 15 objects (9.1 MB). Clones need `git lfs install` (the `doctor` command does that).
- The `.meta` files are unchanged. Unity sees the same bytes, so nothing reimports.
