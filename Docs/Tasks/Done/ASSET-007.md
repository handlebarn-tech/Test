# ASSET-007 — Studio-built nitrile glove overlay

**Owner:** worker (Hub-dispatched). **Reviewer:** fresh, Hub-spawned. **Unity:** not needed (Blender + exported FBX only).

## Goal
Replace the rejected ChatGPT R4.7 gloves (DEC-111) with a studio-built nitrile glove overlay for the MPFB2 staff/customer characters (ASSET-004 pipeline), at the DEC-084 quality bar.

## Read (canonical, directly)
- `Docs/DECISIONS.md`: DEC-084, DEC-114, DEC-023/087, DEC-111, DEC-032.
- `Docs/Imports/IMP-003_PROC_FIX_CHECKLIST.md` row R4.7 (why it was rejected; rebuild checklist).
- `Docs/Tasks/Active/ASSET-004.md` and `Tools/Blender/characters/` (MPFB2 pipeline conventions; reuse, don't fork).
- `Docs/ASSET_PRODUCTION_PLAN.md`; `Docs/Assets/LICENSE_LEDGER.md` if a CC0 source is used.
- Glove colour/who wears them: only from `Docs/Research/`, KNOWN_GAPS, CCTV handoffs; otherwise a labelled GAP.

## Deliverable
- Hand vertex-group mask approach or a CC0 glove proxy fitted to the MPFB2 hand rig; LODs matching the character chain; contact sheet.
- Do not edit ASSET-005/006 files (wardrobe/hair are in flight in another session).
- Handoff `Docs/Handoffs/ASSET-007.md`; committed branch; one line to the Hub.
