# REVIEW-W5P — ASSET-003: customer characters + animation sourcing (licences)

**Verdict: PASS with minors (GO).** Branch `review/wave-5p` (off `main` 18d0326) merges `claude/objective-archimedes-e3d973` @ 8ea901d (be746d4 → a320a38 → 8ea901d) cleanly (8e93ed5). 5 files, +7034, all `.md`/`.json`: spec `CHARACTERS.md`, ledger §1c, fetch list, manifest rows, handoff. **No binaries in git** ✔. Reviewer: standing Docs reviewer (DEC-085), 2026-10-30. (Review ID W5P = next free; the Hub may renumber.) No model was opened or looked at by me.

## Licence checks
1. **Rocketbox = MIT ✔.** The cached `LIC-RB-MIT/LICENSE.md` and `README.md` are byte-identical (sha256, CRLF-normalised) to the live `raw.githubusercontent.com/microsoft/Microsoft-Rocketbox/master/` files. The GitHub API reports `spdx_id: MIT`. The README records that the library was research/academic-only at launch and "Updated license to MIT" in 12/2020. MIT allows commercial use and redistribution with the notice. Under DEC-023 (git = CC0/OFL only) the avatar/clip rows are `redistributable: false` and import via `_LocalThirdParty/`, which is correct. The MIT notice must ship in the build's third-party notices (in the GAME-CHR-002 plan) ✔.
2. **Quaternius:** pack pages and bundled `License.txt` say CC0, while `quaternius.com/license.html` says QAL. The conflict is documented, and every Quaternius row is SUPERSEDED (DEC-084) and unused ✔. Leave it that way: with an unresolved conflict, treat them as QAL (local-only) if they are ever revived.
3. **Scans rejected** (Renderpeople free, in3D, a self-scan, a "resembles a named person" model) under the no-likeness rule ✔. Children are never fetched (21+ store) ✔.
4. **MPFB2/MakeHuman:** the licence page says "All core assets are shared under … CC0"; the MPFB code is GPL and MakeHuman AGPL (tool code, not outputs). CC-BY community packs are flagged per item ✔. CharMorph: MB-Lab AGPL → never, as stated ✔.
5. **Mixamo rejected** (Adobe ID, not CC0, no raw redistribution) ✔. The Sketchfab "Just man" CC BY 4.0 is deferred with a credit line ✔.

## Hashes and validation
- `python -I Tools/Assets/fetch_assets.py --verify` → **515 rows, 0 bad** (hashes every row and checks its ledger ID exists) ✔. Independent hashlib spot-check of 6 random Rocketbox rows (FBX clips, TGA maps, the `.cs`): all match ✔. 198 Rocketbox manifest rows.

## Minors
- **m1 `LIC-RB-MIT` is `redistributable: true`** (LICENSE.md, README.md, `FixRocketboxMaxImport.cs`). Under DEC-023 that flag is what lets a file into git, and MIT isn't on the git allow-list. Set it to `false` like the other Rocketbox rows (or the Hub extends the allow-list, handoff Q1). Related: GAME-CHR-002's "port of the MIT fix script" puts MIT-derived **code** in the repo. That is fine legally if the MIT notice sits with it, but it needs the same Hub ruling as Q1.
- **m2** Ledger: "All Rocketbox avatars are hand-modelled (not scans)". Neither the README nor the licence says this, so it is plausible but unsourced. Either cite the Rocketbox paper or soften it to "no scan provenance stated". It matters for the no-likeness rule.
- **m3** The spec's 80-adult pool includes `Medical` (8) and `Business` professions as customers. Fine, but scrubs on a customer may read as staff/medical-card cues. Let the roster quota cap them, and remember GAP-CHR-1 (no visual medical cue) when choosing.

## For the Hub (handoff questions)
Q1 MIT into git or local-only (reviewer: local-only now; decide before GAME-CHR-002 ports the import script) · Q2 Rocketbox ~8k-tri geometry vs DEC-084 (Rocketbox for PS2 + MPFB2 CC0 pilot, as proposed, is sensible) · Q3 staff uniform (GAP-CHR-2) · Q4 cultural garments kept as ordinary customers with no behaviour tied to appearance: reviewer agrees. **Nobody has looked at the models in-engine yet**; register-distance quality is unverified.
