# REVIEW-W5E — AUDIO-001: audio plan + 16 CC0 sources in the shared cache

**Verdict: PASS with minors (GO).** Branch `review/wave-5e` (off `main` 6559a51) merges `claude/compassionate-davinci-c4d4cf` @ 5fbf03e cleanly. Reviewer: independent review session, 2026-10-30.

## Scope
5 text files, +560: `AUDIO_PLAN.md`, LICENSE_LEDGER §1b (16 rows), `fetch_list_audio.json`, 17 new `ASSET_CACHE_MANIFEST.json` rows, handoff. No Unity, no code.

## License re-verification (each source page re-opened 2026-10-30)
- **BigSoundBank ×10** (3542, 0684, 1471, 0032, 1157, 0034, 1417, 3527, 3588, 0578): every page states "CC0 (public domain): Free and royalty-free" ✔.
- **OpenGameArt ×6** (THESHOP, AIRVENT, GLASSJAR, MORESOUNDS, COINDROP, 100CC0): each page's only license link is `creativecommons.org/publicdomain/zero/1.0/` ✔. The Shop: the page says CC0 covers only the OGA-hosted free sounds; the cached zip is that free-samples file and holds only the 2 fridge-drone WAVs, as the ledger note says ✔.
- No CC BY / BY-SA / GPL / unclear row was taken. The CC BY footsteps set is left as a Hub question, not fetched (DEC-023) ✔. No row is a recording of the reference store ✔.

## Hashes and repo hygiene
- All 17 new manifest rows (16 ledger rows; GLASSJAR has 2 files, open + close) match the cached files in `Dispo Game Assets Cache/` on sha256 and size, hashed independently with Python hashlib. No file missing ✔.
- **No audio committed:** the diff has 5 text files and no binaries; no `.wav/.ogg/.flac/.mp3/.zip` in the tree on main or the branch ✔.
- Every source ID cited in `AUDIO_PLAN.md` exists in the ledger (AUD-BSB-*, AUD-OGA-*, LIB-KEN-DA/IF, ORIG-CHIME) ✔. The plan converts FLAC/MP3 to WAV/OGG because only those are in the DEC-023 LFS patterns ✔. `PressureLevel` is read-only for audio, never TFS (DP §64) ✔.

## Minors
- **m1** AUD-BSB-3542 author: the page credits "Joseph SARDIN & Axeline T."; the ledger lists only Joseph SARDIN. Not a license issue; fix the ledger (and any later CREDITS line).
- **m2** AUD-OGA-GLASSJAR author is "sinny" (lowercase) on the page; the ledger has "Sinny".
- **m3** **Nobody has listened to any of these files yet** (handoff says so; spot-listening wasn't part of this review either). Loop suitability, noise, intelligible speech in the walla beds and durations/channels are unchecked; AUDIO-002 must audition before wiring cues.
- Not checked: the contents of the MoreSounds and 100-CC0 zips file by file; whether the servers still serve the same bytes (the cache is the record).

## For the Hub
- Handoff questions for Nolan: door chime (ORIG-CHIME vs recorded doorbell; does the store have one?), CC BY footsteps vs synthesis, any in-store music.
- Proposed AUDIO-002 Unity packet (handoff) is sound; best after GAME-007 (SliceScreen conflicts), 1 editor.
