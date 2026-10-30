# REVIEW-ASSET4 — ASSET-004, MPFB2 customer pipeline

**Verdict: FAIL (1 major; quick fix-check).** Everything else passes. The major is a single uncited value; under the Hub rule of 2026-10-30, an uncited store value is MAJOR.

I reviewed `worktree-agent-ae6487dd8e469d31b` @ 02e7a5e. This file is committed on `review/asset4`, cut from 02e7a5e. Inputs read: the packet, the handoff, the diff, DEC-084/087/089/113, and main's `SCENE_ANCHORS.json`. I also used the local cache read only: the licence index, the 60 `<id>.validation.json` files and the extracted MPFB data. The lead's rulings 1–5 are taken as given.

## Checks
1. **Store facts cited (Hub rule, first check): FAIL, see M1.**
   - Staff uniform and print side cite DEC-089/113.
   - Formal ≤ 20 % cites W5P m3.
   - Age 21+ is the legal minimum.
2. **Licence audit: PASS.**
   - `BAD_HEADER` catches `# license AGPL3`, `licensed AGPLv3`, `licensed under AGPL` and `license: CC-BY`.
   - Independent check: I ran a broad keyword scan (AGPL, GPL, Affero, LGPL, Attribution, CC-BY, non-commercial) over the top-level text files of all 190 allowed units. It found 0 hits, and no LICENSE or COPYING files exist in them.
   - The AGPL-headed alternative materials (for example `clothes/male_casualsuit01/*`) are correctly separate, refused sub-units.
   - Index: 296 units, 106 refused.
   - Across all 60 validation JSONs: 82 distinct units used, all allowed, each audit entry identical to the index. Every roster item, hair, hat, glasses and skin appears in that customer's audit. No refused unit is used.
3. **Roster: PASS.**
   - `roster.py` run twice gives 0 errors with exit code 0, and the two outputs are byte-identical. Both are JSON-equal to the committed roster; the only byte difference is the CRLF from git checkout.
   - Quotas: sex 30/30; age bands 15/30/15; ancestry 13/12/12/12/11; builds 21/19/20.
4. **CHARACTERS.md vs DEC-084/087/089/113: PASS.**
   - DEC-084: realistic quality, with LODs carrying performance.
   - DEC-087: MIT allowed, MPFB as the main path, Rocketbox as the interim crowd.
   - §9 staff: black pants and a green tee with "The Flower Shop" on the **wearer's left chest** (viewer's top-right), which is DEC-089 + DEC-113.
   - The budget table matches the handoff's measured figures.
5. **GAP-CHR-4..10 honest, no hue-shifted skins: PASS** (m2).
   - GAP-CHR-8 is verified: the allowed South-Asian skins are both female (`cutoff3d_indian_female_*`) and there is exactly one Eurasian male skin.
   - GAP-CHR-9 is verified: all 5 beard and moustache clothes units are refused (AGPL).
   - Ruling 3 (no hue shift) is recorded.
6. **`manifest_rows.py` reproduces the 60 rows: PASS.** Running it rewrote `ASSET_CACHE_MANIFEST.json` with 60 rows, sha256-checked against each validation JSON. `git diff` against 02e7a5e was empty, and I restored the file afterwards.

## Major
- **M1 The register viewing distance is uncited** (CHARACTERS.md §3: "from about 1.2–2 m"). It is a store-geometry value that Rule D and the GAP-CHR-5 reasoning depend on. The handoff calls it an ASSET-003 planning figure, but the doc presents it as fact.
  - Fix (one line): cite the floor data. On main's `SCENE_ANCHORS.json` (REF-011, Low), the distance from `Anchor_Register_<NN>_Call` to `_Operator` is **1.34 m** at stations 02/05/08/11. State "≈1.3 m across the counter (SCENE_ANCHORS, REF-011, Low; GAP-129)", or mark the range as a GAP placeholder.
  - Also label the LOD distance bands in §4 (≤ 3 / 3–8 / 8–15 / > 15 m) as [GDD], since they are design values and not measurements.

## Minors
- m1 **Design quotas need a [GDD] label.** These are design choices, not store facts: hats 10 %, glasses 30 %, beards ~30 %, the 85 % brown-eye and dark-hair shares, and the age-band year ranges. Mark them [GDD] so nobody later reads them as demographics of the real store.
- m2 **GAP-CHR-9 misses a candidate already in the index.** Two **allowed** CC0 skins have a beard painted into the skin texture: `skins/jartur69_middleage_slavic_male_with_genitals_and_beard` and `skins/jartur69_old_slavic_male_with_genitals_and_beard`. List them as option (c) for some customers, or say why they are unsuitable.
- m3 **GAP-CHR-4..10 live only in CHARACTERS.md.** Add rows to `Docs/KNOWN_GAPS.md` (Assets rows) so the Hub's gap list sees them.

## Fix-check (264b535): PASS
- **M1 fixed.** §3 now gives "1.34 m (SCENE_ANCHORS Call↔Operator, REF-011, Low, GAP-129)". Checked against main's `SCENE_ANCHORS.json`: the distance is 1.34 m at all 11 stations (02–12). The §4 LOD distance bands are labelled [GDD].
- **m1 fixed.** The age-band years, hats/glasses/beards shares and the 85 % eye and hair shares are labelled [GDD].
- **m2 fixed.** GAP-CHR-9 lists both jartur69 bearded skins as candidate (a), with the clothed-body note.
- **m3 fixed.** GAP-CHR-4..10 are added to `KNOWN_GAPS.md`. This fix commit adds only those lines there and touches no other rows.
- Nit, no action: station 08's anchors carry GAP-134 in SCENE_ANCHORS rather than GAP-129. The cited value is the same at every station.

**Final verdict: PASS (GO to merge).** Merge worker branch `worktree-agent-ae6487dd8e469d31b` @ 264b535 together with this review branch.
