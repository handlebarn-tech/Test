# ASSET-004 — MPFB2 customer pipeline (finish)

**Dept:** Assets · **Role:** ASSET/PROC-CHR · **Priority:** P1 · **Owner:** Assets lead subagent (2026-10-30 resume), worktree off `main`; first merge `claude/task-asset-004` (225ac4a; done/not-done list in its `Docs/Handoffs/ASSET-004.md`) · **Reviewer:** Docs reviewer `local_99d7e5b7-ef60-4076-9821-58f16ce3bec0` (pipeline/spec), Unity A2 `local_4e865bb8-479c-41c5-8628-7f3e7cb2a4c3` later for import · **Touches:** none · **Interfaces:** `Docs/Assets/Specs/CHARACTERS.md` + `customer_roster_mpfb.json` (Gameplay's GAME-CHR-002 import builds against them). Shared files also edited by PROC-005: `Docs/Assets/ASSET_CACHE_MANIFEST.json`, `LICENSE_LEDGER.md`, `Tools/Blender/blender.ps1`. Append rows only, keep edits minimal.

## Goal
Finish the paused MPFB2 pipeline (DEC-087/089, DEC-084 realism): rewrite `CHARACTERS.md` for MPFB (pipeline, budgets, variation, import), manifest rows for derived samples, a committed contact sheet of the previews, hair tint, and scale the roster export toward 60 (PROC-CHR-004 scope) as budget allows.

## Rules
- CC0/MIT only (DEC-023/087). Keep the per-asset licence index; refused (AGPL-headed) units stay refused. Binaries stay in the shared cache, never in git (contact sheet PNG ≤ 1 MB is fine).
- No real-person likeness. Staff uniform per DEC-089 if staff are touched.
- Isolated Blender profile as already set up. Never touch the user's Blender config.
- Texture gaps (2K diffuse without normals, 1K eyes, 512 brows, no South-Asian male skin): list them, with candidate CC0 fixes, as `GAP-CHR-<n>`. Don't invent.
- No Unity work. Write the GAME-CHR-002 import packet outline in the handoff for the lead.

## Deliverables
Updated `CHARACTERS.md`, roster, generator fixes, manifest rows, contact sheet, `Docs/Handoffs/ASSET-004.md` (done / deferred / questions for Nolan through the Hub).

## Validation
Roster self-check 0 errors, deterministic. Each exported customer has 0 validation errors and LOD0–3 tri figures recorded. CC0 audit passes.
