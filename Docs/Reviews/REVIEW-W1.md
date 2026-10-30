# REVIEW-W1 — Wave 1 independent review (REF-001, MIG-001, BUILD-001)

**Reviewer:** REVIEW specialist · **Date:** 2026-10-29 · **Branch reviewed:** `review/wave-1` @ 667ebd1 (clean worktree checkout)

## Verdict: **GO with notes**

No blockers. Every acceptance gate re-ran green on a fresh checkout, the goldens reproduce byte-identically, and the spot-checked constants and dimensions match their sources. The notes below are for GAME-001 / ART-001 and do not block the merge.

## Findings by severity

### Blocker
None.

### Major
- **M1 (MIG-001 → GAME-001 packet).** The slice says "direct `INTENTS` key lookup, skip the NL layer", but two slice goldens do not come from a bare INTENTS entry:
  - RC-04 `pain` → golden `neg.sedation=55` comes from the pain-functional default (L16211-16216), not from `INTENTS.pain` (which has `neg:{}`).
  - RC-11 `insomnia` → golden `crit {sedation 55, anxiety_relief 40}` comes from the PHRASE_MAP entry (L16107), not `INTENTS.insomnia` (`sedation 45, anxiety_relief 35`).
  - **Fix (Hub, in GAME-001):** the golden tests should feed each case's recorded parse (`crit`/`neg`/`primary` in `golden_cases.json`) into `findStrains`, or the slice must also port the pain-functional rule + the `insomnia` phrase. Otherwise RC-04/RC-11 cannot pass by construction.
- **M2 (REF-001).** R5C1/R5C2/R5C5 are mapped to HUB, but the plan's own text says HUB has no camera feed, and the plan's "second office camera" (two safes, IT rack, white door with coat hooks, scale cart) has no matched tile. GAP-105 records it; I added an inline pointer in §2. ART-001 should treat the HUB interior as unconfirmed.

### Minor
- **m1.** HUB 2 width: vector 18.49 ft vs printed 18'-9¼" (18.77 ft), Δ0.28 ft, so "all within 0.25 ft" was false. The printed area (541.34 SF ÷ 29.24 ft = 18.51 ft) supports the vector. Fixed in text.
- **m2.** HUB width: the reviewer measured 158.88 pt = 28.32 ft vs the index's 28.29 ft. 0.03 ft, left unchanged (not worth changing ART coordinates); noted here only.
- **m3.** Queue stanchions (§1.5) are labelled "raster-read", but they are vector (fill at x 5.95–15.07, y 11.0–19.71). Confidence can rise to Med. Left for REF to update; harmless for graybox.
- **m4.** Photo rows 05 and 10 described body traits (tattoos, hair colour), outside the attire/role-only rule. Removed.
- **m5.** GAP-105 and the REF-001 handoff said "8" storage tiles; the list is 7 (R4C3, R4C4, R5C1–C5). Fixed.
- **m6 (BUILD-001).** On a fresh clone every `studio.ps1` command throws until `studio.config.example.json` is copied to `studio.config.json`. That is by design (the real config is gitignored), but `doctor` could report it as a failed check with the copy hint instead of a stack trace. Not fixed (code, not doc).
- **m7 (BUILD-001).** First `unity-compile` on a fresh checkout took 207 s (Library import), not the 56 s in BUILD_STATUS. Expected for a cold Library; worth noting for worktree-based workers.

### Nit
- REFERENCES_INDEX line 12 ties the 2012 NVR timestamps to wall A only; a wall 2 tile (R2C3) shows 03/31/2012 too.

## Evidence

### REF-001
- **Inventory:** all 6 top-level items under `References/` (PDF, 2 CCTV PNGs, BAND folder with 13 photos, 2 MD files) are in §0; all 56 derived files are listed. All 10 printed rooms (Retail, Restroom, Hall, Office, Break room, JC, FOH, BOH, HUB, HUB 2) are in the §4 matrix, plus vestibule and exterior.
- **Scale re-derived:** the retail filled rectangle on p1 spans x 99.60–364.32 = 264.72 pt; printed 47'-2¼" = 47.1875 ft → 5.6100 pt/ft (index 5.6095, rounding only). Stitch offset 555.84 pt confirmed.
- **Rooms:** Office 13.71 × 9.80 ft (index 13.70 × 9.80) ✔; Break room 9.22 × 16.79 (9.20 × 16.80) ✔; BOH 10.29 × 16.79 (10.29 × 16.80) ✔. Overall depth 76.0 ft ✔. Fixtures (display case, 6 pendants, ATM, entry arcs, arches, columns) match vector geometry.
- **CCTV (wall 2):** R3C3 office ✔ (R4C5 is its repeat), R2C3 registers ✔, R4C1 FOH ✔, R4C3 storage ✔ (Low is right).
- **Photos:** _01 ✔, _05 ✔, _12 ✔ (also _09 ✔).
- **PII:** no names, badge text or name tags transcribed; body-trait lines removed (m4).

### MIG-001
- **Source md5s match:** `index.html` 228684e9…, master JSON 09bfa4f0….
- **12 constants confirmed at the cited lines:** `getTierW` L15041; `NF=2.7765` L15121; `BA_SCALARS` L15127ff (all 18 values); `getBaScalar` defaults sesqui .46 / else .55; dominant bonus `1+min(1,(pct−.20)/.60)` (scoreDomains); `CLUSTER_BONUS` L15327-15333; `_tierVal` nudge (smalls/house/premium .18, fttp .16, t1 .08, t2 .04, t3 .01, t4 0) L15408; recency `K=LN2/8, CAP=20` (averageProfile); fallback `floor(crit×.60)` L16639 / `min(99,neg+12)` L16640; `EXCL_MAX_PCT=0.01` L15975; `STD_WEIGHTS` L21010; `taxRate 25.1` L21061 + `priceFloor` floor-to-$0.05; `TIER_DEFAULTS` L21018ff; `FB_DUP_MS=10 min` L22615.
- **Goldens:** extracted engine.js / golden.js from the appendix (md5 1efb4d4f… / a139b45c…, matching the doc), ran `node golden.js` (Node 22.14) on read-only copies in my temp dir → `782427de4f75c910e8448e52b5a06bc3`, **byte-identical** to the committed `golden_cases.json` (`cmp` clean). Note: the working-tree file hashes differently (d565d2d3…) only because `core.autocrlf=true` checks it out with CRLF; the committed blob is the LF original.
- **Triage counts** (34/4/8/3/6/8 = 63) check out. PII/CRM: Supabase/accounts/roles DROP (#61); feedback (#51) and sold/search log (#52) become in-game NPC/POS events with no employee/location ids carried. `golden_cases.json` has no PII-like keys (employee_id, uid, customer*, email, phone, location_id) and no emails.
- **Slice sufficiency:** enough for GAME-001 once M1 is handled.

### BUILD-001 (re-run here, one Unity instance at a time; only the Hub's `unity.exe serve` helper was running)
| Gate | Result |
|---|---|
| `studio.ps1 doctor` | ok, all checks passed (after copying the example config, m6) |
| `studio.ps1 unity-compile` | ok, `csErrors=0`, `[StudioCI] CompileCheck OK`, log `defaultRenderPipeline=…HDRenderPipelineAsset globalSettings=HDRenderPipelineGlobalSettings`, 207 s |
| `studio.ps1 unity-test-edit` | ok, total 1 / passed 1 / failed 0, 23 s |
| `studio.ps1 unity-build` | ok, `Builds/Windows64-Dev/DispoGame.exe`; smoke `STUDIO_SMOKE_READY scenes=9`, exitedEarly=False, crash=False; 632 s (cold Library) |
- `Dispo.Domain.asmdef`: `noEngineReferences: true`, `references: []` ✔.
- Tracked files under `UnityProject/{Library,Temp,UserSettings,Logs,obj}/`: **0** ✔.

### Repo hygiene
- No tracked file over 10 MB (largest in `References/Index/` is 336 KB).
- No tfs-budtender files copied in (no `index.html`, inventory master, xlsx or eml tracked).
- No secrets: `git grep` for key/secret/token/JWT/supabase URL patterns hits only pre-existing prose in `References/Review_Budtender_Tool_Comprehensive_Chat_Record.md`. No email addresses in Docs/References/Tools.

### Hub main checkout: untracked `UnityProject/`
It holds only `Library/` (1.8 GB), `Logs/`, `UserSettings/`, five `Dispo.*.csproj` and `UnityProject.slnx` (left over from BUILD-001 running in the main checkout; no Assets/Packages/ProjectSettings). Against the `review/wave-1` `.gitignore` every one of these is ignored (`git check-ignore` confirmed for Library, Logs, UserSettings, Temp, *.csproj, *.slnx). It shows as `??` on `main` today only because `main`'s `.gitignore` lacks the `*.slnx` line that wave 1 adds. None of these paths are tracked on `review/wave-1`, so the merge will not hit untracked-file conflicts. Nothing was deleted.

## Doc fixes made in this review (trivial, allowed by the packet)
- `Docs/REFERENCES_INDEX.md`: HUB 2 tolerance text (m1); body traits removed from photo rows 05/10 (m4); GAP-105 pointer on R5C1/R5C2 (M2).
- `Docs/KNOWN_GAPS.md` GAP-105: 8 → 7 tiles (m5).
- `Docs/Handoffs/REF-001.md`: tolerance sentence (m1); 8 → 7 storage tiles (m5).

## Not checked
BAND photos 02–04, 06–08, 10 (beyond the trait fix), 11, 13; wall 1 tiles beyond R2C2/R4C2; HUB raster rack/desk positions; harness fidelity against a real browser (GAP-207, by design).
