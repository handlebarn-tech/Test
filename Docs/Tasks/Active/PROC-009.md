# PROC-009 — Studio-built parked vehicles

**Owner:** worker (Hub-dispatched). **Reviewer:** fresh, Hub-spawned. **Unity:** not needed (Blender + exported FBX only).

## Goal
Replace the rejected ChatGPT R3b vehicles (DEC-111) with studio-built parked vehicles for the parking lot, at the DEC-084 quality bar.

## Read (canonical, directly)
- `Docs/DECISIONS.md`: DEC-084 (quality bar), DEC-114 (tri numbers are guides), DEC-023/087 (licences), DEC-111, DEC-032 (realism vs fun).
- `Docs/Imports/IMP-003_PROC_FIX_CHECKLIST.md` row R3b.7 and `Docs/Imports/IMP-003_BLENDER_TOOLKIT_AUDIT.md` (why the R3b vehicles were rejected).
- `Docs/ASSET_PRODUCTION_PLAN.md` (realism rule, LOD chain, export conventions); `Docs/Assets/LICENSE_LEDGER.md` if a CC0 source is used.
- Existing generators in `Tools/Blender/generators/` for house conventions.
- Store/parking-lot facts: only from `Docs/Research/`, KNOWN_GAPS and CCTV handoffs. No invented store facts; anything unsourced is a labelled GAP.

## Deliverable
- CC0 source (logged in LICENSE_LEDGER) or a scripted rebuild per R3b.7; generic unbranded makes (DEC-071), a few body/colour variants, LOD0–LOD3, PBR textures, contact sheet.
- Handoff `Docs/Handoffs/PROC-009.md` with sources, GAPs, `## Questions for Nolan (through the Hub)` if any.
- Committed branch; one line to the Hub.
