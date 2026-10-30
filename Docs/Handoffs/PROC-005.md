# PROC-005 handoff (partial; usage limit reached 2026-10-30)

**Branch:** claude/clever-lamport-837e7f. **Done:** core slice 4ef04ae (C1–C11, Q0.5): manifest collision boxes, validation JSON on failure, mesh_stats diagnostics (manifest re-baselined; every existing FBX export_sha256 unchanged), opt-in checks with planted-bad-mesh self-test (`Tools/Blender/tests/test_validation.py`, passes), helpers (deterministic cylinder roll, sweep, lathe, round-wire grid, hinge/slide).

**WIP (next commit):** `generators/wire_shelving.py` + `params/wire_shelving.json` (8 RF racks, W1–W8 design). Validation currently FAILS on size: caster fork sweep profile axes are swapped (fork plate width lands on X, +0.024 m), and LOD3 shelf boxes use D-2cr not D. Fix those, rerun, check tri figures vs DEC-084, contact sheet, commit.

**Left:** every other checklist family (§4–§20), Q0.2/Q0.3 textures, Unity import check (verify `to_unity` X negation with an EditMode test), PP doc update.

## Questions for Nolan (through the Hub)
- None new. Pipeline note for Hub: Unity "Generate Lightmap UVs" writes uv2 (channel 1), which is our `UVMap_Label`; DEC-084 UV2 needs a decision (separate lightmap channel).
