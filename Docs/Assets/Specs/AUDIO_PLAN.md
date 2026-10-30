# AUDIO PLAN — AUDIO-001 (2026-10-30)

Cue list, sources, mix targets for the slice, PS1 and PS2. No Unity work yet; the integration packet is in `Docs/Handoffs/AUDIO-001.md`.
Inputs: `ASSET_PRODUCTION_PLAN.md` §17 "Audio target list", `ROADMAP_POST_SLICE.md` §2/§3, DP §61–64 (`SPEC_DECISION_PRESSURE.md`), DEC-023.
Licences: every sourced file is CC0 1.0 or project-original; rows in `LICENSE_LEDGER.md` §1 (LIB-KEN-*, AUD-BSB, ORIG-CHIME) and §1b (AUDIO-001), hashes in `ASSET_CACHE_MANIFEST.json`. Re-fetch: `python -I Tools/Assets/fetch_assets.py --list Docs/Assets/fetch_list_audio.json`.
**No recording of the reference store is used or wanted.** Generic CC0 recordings (a French restaurant, a supermarket, an air-conditioner) are the beds.

## 1. Mixer
`Master` → four groups, one exposed volume each (settings menu later):

| Group | Holds | Default | Ducking |
|---|---|---|---|
| **Ambience** | HVAC, fridge, room tone, murmur/walla, rush layers | 0 dB | ducked −4 dB by UI modal panels (ID inspect, report) |
| **SFX** | world one-shots: POS, scale, jar, cash, door, bag, footsteps | 0 dB | none |
| **UI** | button clicks, toasts, meter warnings, strike, report stings | 0 dB | none (always audible) |
| **Music** | not in slice/PS1; PS2 optional rush stem (§4) | −6 dB | ducked −6 dB under report VO-free stings |

Two snapshots on Ambience: **Calm** and **Rush**, blended by `PressureLevel` (§3). No reverb send in slice; PS2 may add one small "retail room" reverb on SFX (Unity built-in SFX Reverb, wet −18 dB).

## 2. Loudness and format targets
Measured on the **source clip after normalising** (Audacity: Loudness Normalization / Normalize, both free), before mixer gain. All peaks ≤ −1 dBTP.

| Class | Target | Unity import |
|---|---|---|
| Ambience bed (loop) | −30 LUFS integrated (murmur −32, HVAC −30, fridge −34) | 44.1 kHz **stereo**, Vorbis q≈0.5, **Streaming**, loop points cut on zero crossings with ≥ 50 ms crossfade |
| World SFX one-shot | −18 LUFS short-term (loud events ≤ −14) | 44.1 kHz **mono**, WAV/PCM or ADPCM, **Decompress On Load**, 3D spatial blend 1, min 1 m / max 12 m log rolloff |
| UI one-shot | −20 LUFS short-term, ≤ 300 ms unless a sting | 44.1 kHz mono, ADPCM, Decompress On Load, 2D |
| Sting (report, strike) | −16 LUFS short-term, ≤ 2.5 s | as UI |

Git: only `.wav`/`.ogg` are in the DEC-023 LFS patterns, so FLAC/MP3 sources are converted to WAV (SFX) or OGG (beds) on import into `UnityProject/Assets/_Game/Art/ThirdParty/Audio/<ledger id>/`. All rows here are redistributable.

## 3. Rush intensity (`PressureLevel`)
`PressureLevel` 0–1 is computed by GAME-011 (DP §64: arrival rate, queue, active tasks, stock problems, staff coverage, events). Audio only **reads** it; nothing in audio feeds back into the sim, and it never touches TFS recommendation inputs or outputs (DP §64, QA-002 parity gate).
Until GAME-011 exists, the slice drives it from queue length: `p = clamp01(queueLength / 6)` (placeholder, label `GAP-AUD-01`).

| Layer | p = 0 | p = 0.5 | p = 1 |
|---|---|---|---|
| AMB-HVAC, AMB-FRIDGE | 0 dB | 0 dB | −2 dB (masked) |
| AMB-WALLA-LO | −8 dB | 0 dB | 0 dB |
| AMB-WALLA-HI | off | −10 dB | 0 dB |
| AMB-RUSH (supermarket texture) | off | off | −6 dB |
| MUS-RUSH (PS2, optional) | off | −12 dB | −6 dB |

Smoothing: one-pole, 4 s rise / 8 s fall, so the store does not "breathe" with each arrival. Recovery phase (DP §62) audibly settles because of the 8 s fall.

## 4. Cue list
P0 = slice must have, P1 = PS1, P2 = PS2. "Source" names the ledger row and the file inside it; **audition** = pick at integration by ear.

| ID | Cue | Trigger (game) | P | Group | Target | Source |
|---|---|---|---|---|---|---|
| UI-CLICK | button / menu click | any UI button | P0 | UI | −20 | LIB-KEN-IF `click_001..005` (random of 3) |
| UI-HOVER | hover tick (optional) | pointer enters button | P2 | UI | −26 | LIB-KEN-IF `tick_001/002` |
| UI-BACK | close / back | panel close | P0 | UI | −20 | LIB-KEN-IF `back_001`, `close_001` |
| UI-CONFIRM | sale complete, accept | POS "Complete", accept ID | P0 | UI | −18 | LIB-KEN-IF `confirmation_001/002` |
| UI-ERROR | invalid action | blocked action, wrong tender | P0 | UI | −18 | LIB-KEN-IF `error_004/006` |
| UI-TOAST | info toast | KNOWN fact revealed, notices | P1 | UI | −22 | LIB-KEN-IF `pluck_001`, `select_002` |
| UI-METER-WARN | purchase-limit meter crosses warn | GAME-007 meter ≥ warn | P1 | UI | −18 | LIB-KEN-DA `lowThreeTone` (audition) or LIB-KEN-IF `question_001` |
| UI-STRIKE | compliance strike | GAME-007/008 strike | P1 | UI | −16 | LIB-KEN-IF `error_008` layered with LIB-KEN-DA `lowDown` |
| SFX-POS-SCAN | POS item add / scan beep | line added to cart | P0 | SFX | −18 | AUD-BSB-1417 (alt AUD-BSB-3527) |
| SFX-POS-KEY | POS key press | POS keypad / tender keys | P0 | SFX | −22 | LIB-KEN-IF `click_003`, `switch_002` (audition) |
| SFX-CASH-DRAWER | cash drawer opens | cash tender | P0 | SFX | −14 | **synthesise** (§5) or AUD-OGA-100CC0 `metal_*` / `wooden_box_open` (audition) |
| SFX-CASH-COINS | change / coins | cash tender complete | P0 | SFX | −18 | AUD-OGA-COINDROP; AUD-OGA-MORESOUNDS `Money/*` |
| SFX-CASH-BILLS | bills handled | cash tender | P1 | SFX | −20 | AUD-OGA-MORESOUNDS `Money/*` (paper ones), `Paper/*` |
| SFX-RECEIPT | receipt printer | sale complete | P1 | SFX | −20 | **synthesise** (§5); tear from AUD-OGA-MORESOUNDS `Paper/*` |
| SFX-SCALE-BEEP | scale tare / settle beep | jar fill step settles, tare | P0 | SFX | −20 | **synthesise** (§5), alt AUD-BSB-3527 pitched up |
| SFX-SCALE-PLACE | item set on scale pan | weighing starts | P1 | SFX | −20 | AUD-OGA-100CC0 `glass_*`/`plop_*`, AUD-OGA-MORESOUNDS `Plastic/*` (audition) |
| SFX-JAR-OPEN | jar lid off | JarFillStep open | P0 | SFX | −18 | AUD-OGA-GLASSJAR `glass_bottle_open` |
| SFX-JAR-CLOSE | jar lid on | JarFillStep close | P0 | SFX | −18 | AUD-OGA-GLASSJAR `glass_bottle_close` |
| SFX-JAR-SET | jar set down on counter | jar placed | P1 | SFX | −20 | AUD-OGA-100CC0 `glass_01..05` |
| SFX-SCOOP | tongs / product into container | fill increments | P1 | SFX | −24 | AUD-OGA-MORESOUNDS `Plastic/*`, `Cloth/*` soft (audition); else synthesise soft rustle |
| SFX-BAG | exit bag handed over | hand-off | P1 | SFX | −20 | AUD-OGA-MORESOUNDS `Plastic/*` / `Paper/*` |
| SFX-ID-CARD | ID card slid on counter | GAME-008 ID check opens | P1 | SFX | −22 | AUD-OGA-MORESOUNDS `Plastic/*` (short) |
| SFX-DOOR-CHIME | entry chime | customer enters (vestibule door) | P0 | SFX | −16 | ORIG-CHIME (cached, ASSET-002) vs AUD-BSB-3588 shop doorbell (audition). AUD-BSB (metro bell) rejected as weak match |
| SFX-DOOR | door open/close | door anim | P1 | SFX | −20 | AUD-OGA-100CC0 `door_open`, `door_close_01..04` |
| SFX-STEPS | footsteps on tile | NPC walk | P2 | SFX | −26 | gap: no CC0 tile set fetched; OGA "footsteps-on-different-surfaces" is CC BY 3.0 (credit needed). Synthesise or accept CC BY via Hub |
| AMB-HVAC | HVAC / air handler bed | always (FOH) | P0 | Ambience | −30 | AUD-BSB-1471; alts AUD-OGA-AIRVENT, AUD-BSB-0032 (BOH) |
| AMB-FRIDGE | beverage/deli cooler hum | 3D at cooler, 4 m radius | P0 | Ambience | −34 | AUD-OGA-THESHOP `..._fridge_drone.wav`; alts AUD-BSB-1157, AUD-BSB-0034 |
| AMB-ROOMTONE | quiet room tone | always, very low | P1 | Ambience | −40 | AUD-OGA-THESHOP `..._fridge_drone_2.wav` low-passed, or synthesise pink noise (§5) |
| AMB-WALLA-LO | customer murmur | scaled by PressureLevel (§3) | P0 | Ambience | −32 | AUD-BSB-3542 (French; keep low so words are not intelligible) |
| AMB-WALLA-HI | busier murmur | PressureLevel > 0.3 | P2 | Ambience | −30 | AUD-BSB-0684 |
| AMB-RUSH | busy-store texture | PressureLevel > 0.7 | P2 | Ambience | −32 | AUD-BSB-0578 (generic supermarket) |
| MUS-RUSH | light rush pulse | PressureLevel (§3) | P2 | Music | −24 | none sourced; synthesise (§5) or Hub picks a CC0 OGA track later |
| UI-REPORT-OPEN | shift-end report appears | report screen opens | P0 | UI | −16 | LIB-KEN-IF `maximize_003` + LIB-KEN-DA `twoTone1` (audition) |
| UI-REPORT-TICK | report rows count up | each row reveal | P1 | UI | −24 | LIB-KEN-IF `tick_001` |
| UI-REPORT-STARS | star / grade reveal | star gate (GAME-020) | P1 | UI | −16 | LIB-KEN-DA `powerUp*` (audition; keep subtle, not arcade) |
| UI-REPORT-FLAG | severe flag in report | DP severe flag | P1 | UI | −18 | LIB-KEN-IF `error_001` |
| SFX-PHASE | shift-phase change (open/rush/close) | GAME-011 phase banner | P2 | UI | −20 | LIB-KEN-IF `bong_001` |

Variation: every repeated one-shot gets random pitch ±3 % and volume ±1.5 dB; scan beep excluded (real POS beeps don't vary).

## 5. Free synthesis where no CC0 source fits
Tools: Python + numpy (already used by `Tools/Assets/make_chime.py`), Audacity (Generate → Tone/Noise/Chirp, free), optionally Surge XT / LMMS (free, GPL tools; their output is ours). Output = project-original, ledger rows `ORIG-*` like ORIG-CHIME.

| Cue | Recipe |
|---|---|
| SFX-SCALE-BEEP | 2.7 kHz sine, 90 ms, 5 ms attack/release; tare = two beeps 80 ms apart |
| SFX-RECEIPT | thermal printer: band-passed noise (2–6 kHz) gated at ~40 Hz for 0.8–1.2 s + 120 Hz motor hum at −20 dB; end with paper tear from AUD-OGA-MORESOUNDS |
| SFX-CASH-DRAWER | spring-release click (short noise burst, 3 kHz HP) → 250 ms low thunk (80–120 Hz decaying sine) → metal rattle (layer AUD-OGA-100CC0 `metal_*`) |
| AMB-ROOMTONE | pink noise, LP 800 Hz, −40 LUFS, 30 s loop |
| MUS-RUSH | 90–100 BPM soft pulse (muted pluck + shaker) in Surge XT/LMMS, 32-bar loop, rendered to OGG |
| SFX-STEPS | only if the Hub refuses CC BY: short filtered noise heel/toe pairs, 6 variants |

## 6. Gaps
- `GAP-AUD-01` PressureLevel placeholder from queue length until GAME-011 (§3).
- `GAP-AUD-02` real POS / scale / door-chime sounds of the reference store are unknown and will not be recorded (task rule); generic sounds stand in. Ask Nolan only if fidelity matters (handoff question).
- `GAP-AUD-03` no CC0 tile footsteps fetched (SFX-STEPS, P2).
- Sources skipped because they need sign-in: Freesound (any download), Sonniss GDC bundle (email registration). Not used: OGA CC BY / BY-SA / GPL audio.
