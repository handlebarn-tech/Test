# PROC-003 — Jar fill follow-ups: F010 visible pile, natural packing, REF-007 sizes, house-smalls jar

**Role:** PROC · **Priority:** P2 · **Branch:** `claude/task-proc-003` off `main` (a245942)

## Goal
Close the PROC-002 follow-ups from REVIEW-W4E and DEC-046 in the deterministic Blender generators.

## Read
`Docs/Handoffs/PROC-002.md`, `Docs/Reviews/REVIEW-W4E.md` (m1, m2, n1, n3), DEC-019/027/042/043/046, `Docs/REFERENCES_INDEX.md` §2.4 (REF-007 jar sizes), `Docs/Assets/Specs/PROC_PIPELINE.md`.

## Owns
`Tools/Blender/generators/{deli_jar,jar_fill}.py`, `Tools/Blender/params/{deli_jar,deli_jar_smalls,jar_fill}.json`, `Art/Exports/Procedural/`, `UnityProject/Assets/_Game/Art/Procedural/`, `Code/Tests/EditMode/ProcArt/`, the PROC contact sheets and `PROC_PIPELINE.md`. Not `Code/Simulation|Presentation`, scenes or `studio.ps1`.

## Deliverable
1. **DEC-046:** every fill step above 0 g shows a pile visibly above the base band from the front; only F000 (SOLD OUT) looks empty. Enforced at build time on every LOD.
2. **Packing (W4E n1):** full jars no longer read as 3 neat columns: seeded per-layer offsets, more x/y/z jitter, wider bud-size spread. Still deterministic and within the per-step tri budgets.
3. **Canister size:** take REF-007's estimate (≈6 × 5–6" footprint × ≈10–10.5" tall, Low–Med); the fill cavity follows automatically.
4. **House-smalls jar:** a second jar type, `PROC_DeliJar_Smalls`, from REF-007's published Amazon B0GX12Q9G8 dimensions (6.1 × 5.3 × 10.4", 4 L, High), as another params file for `deli_jar`.
5. Optional (W4E m2): give the jar FBXs a `unity_dir` so GAME can parent the fill to them.

## Validation
Every changed generator and both contact sheets run twice → identical sha256. EditMode `JarFillImportTests` updated to the new cavity and passing. `studio.ps1 unity-compile` and `unity-test-edit` (DEC-013 gate).

## Handoff
`Docs/Handoffs/PROC-003.md` (≤40 lines). Questions for the Hub go there (DEC-033).
