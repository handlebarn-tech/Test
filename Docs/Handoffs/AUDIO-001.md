# HANDOFF — AUDIO-001 (audio plan + CC0 sourcing, no Unity)

**Date:** 2026-10-30 · **Branch:** `claude/compassionate-davinci-c4d4cf`

## Delivered
- `Docs/Assets/Specs/AUDIO_PLAN.md`: mixer (Music/SFX/UI/Ambience + Calm/Rush snapshots), loudness/format targets, `PressureLevel` → ambience layer table (read-only, never TFS; DP §64), 37-cue list with priority (P0 slice / P1 PS1 / P2 PS2), group, LUFS target and source, synthesis recipes, gaps.
- 16 new CC0 ledger rows (`LICENSE_LEDGER.md` §1b): 10 BigSoundBank (murmur ×2, HVAC ×2, fridge ×2, POS beeps ×2, shop doorbell, supermarket), 6 OpenGameArt (LEGIT Audio fridge drones, air vent, glass jar open/close, 202 home foley, coin drop, 100 CC0 SFX). CC0 checked on each page 2026-10-30.
- `Docs/Assets/fetch_list_audio.json` + 17 manifest rows (~85 MB in `Dispo Game Assets Cache/{bigsoundbank,opengameart}/<id>/`). Already-cached Kenney Interface/Digital Audio and ORIG-CHIME cover all UI cues.
- Validation: `python -I Tools/Assets/fetch_assets.py --verify` → 266 rows, 0 bad.

## Not done / limits
- Nothing auditioned by ear (no listening in this session); cues marked "audition" need a pick at integration. Durations/channels not measured.
- No synthesis scripts written (task asked for notes; recipes in plan §5).
- Skipped (login): Freesound, Sonniss. BigSoundBank pages need a browser (Cloudflare); files download directly from `/UPLOAD/flac|ogg/<id>`.

## Proposed packet: AUDIO-002 (Unity integration, 1 editor)
1. Convert sources (FLAC/MP3 → WAV/OGG, loudness per plan §2) into `UnityProject/Assets/_Game/Art/ThirdParty/Audio/<ledger id>/` (LFS, DEC-023); synthesise SFX-SCALE-BEEP, SFX-RECEIPT, SFX-CASH-DRAWER as `ORIG-*` with a `Tools/Assets/` script like `make_chime.py`.
2. `AudioMixer` with the 4 groups + Calm/Rush snapshots; exposed volumes.
3. A Presentation-side cue bank (ScriptableObject: cue id → clips, group, pitch/vol jitter) and hooks for all P0 cues on slice events (POS add/complete, cash, jar open/close, scale settle, customer enter, report open).
4. `PressureLevel` adapter: placeholder from queue length (`GAP-AUD-01`) until GAME-011; reads only, EditMode test that audio never writes sim state.
5. P1 cues land with GAME-007/008 (meter, strike, ID card); P2 with GAME-011 (phases, rush layers, music).
Depends on nothing open; best after GAME-007 to avoid `SliceScreen` conflicts.

## Questions for Nolan (through the Hub)
1. Door chime: keep the project-original 2-note ding-dong (ORIG-CHIME) or the recorded shop doorbell (AUD-BSB-3588)? Does the real store even have an entry chime? Source: none (no reference audio). Placeholder: ORIG-CHIME.
2. Footsteps (P2): accept a CC BY 3.0 set (OGA "footsteps-on-different-surfaces", needs a credit line) or synthesise? Placeholder: `GAP-AUD-03`.
3. Any background music in store (radio/playlist) in reality? Plan assumes none in slice/PS1 and an optional rush pulse in PS2.
