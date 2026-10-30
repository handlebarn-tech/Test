# GAME-025 — Controls: mouse look, Esc pause menu, doors (playtest 1)

**Dept:** Gameplay · **Role:** GAME · **Owner:** worker subagent (id + branch once launched) · **Reviewer:** pool (lead assigns) · **Touches:** none · **Interfaces:** `Docs/Specs/CONTROLS_FLOW_PS1.md` §7 (CF§7), `Docs/Reference/DOORS.json` (REF-012), `Docs/Reference/SCENE_ANCHORS.json` (REF-011) (header fields: REVIEW-W5U m2)
**Priority:** P0 · **Branch:** `task/GAME-025` worktree off `main` (after GAME-009 merges — same `SliceGame.cs`/`SliceView.cs`; World door contract REF-012 optional, see Dependencies)

## Goal
Playtest 1 (DEC-096, `Docs/Design/PLAYTEST_2026-10-30.md`): looking/turning feels clunky, Esc must always pause, and doors must make moving through the store feel natural. Spec: `Docs/Specs/CONTROLS_FLOW_PS1.md` (cited **CF§n**).

## Read
CF§1, §2, §3, §6 (GAME-025 rows), §7.1; `Docs/Specs/UX_PS1.md` §7 (key map; its Esc rows are superseded by CF§2.4); `Docs/Specs/UX_SLICE.md` §4 (Back), §6 (tokens), §7 (settings); `Docs/Design/SPEC_SHIFT_DAY.md` §7 (pause freezes the sim); DEC-076 (entry lock); REF-012's `Docs/Reference/DOORS.json`; DEC-103 (propped-open doors).

## Owns
- `Assets/_Game/Code/Presentation/Graybox/GrayboxTestPlayer.cs` (look, cursor, FOV, pitch; keep its public fields and `ScriptedWorldMove` so `GrayboxWalkTests` stays green)
- `Assets/_Game/Code/Presentation/Slice/SliceGame.cs` (Esc → pause, Backspace → `Back()`, cursor lock per screen, E priority CF§3.3), `SliceView.cs` (pause menu, settings, controls list, "Locked" prompt)
- new `Assets/_Game/Code/Presentation/Slice/SliceDoor.cs` (door runtime: finds `Door_<Id>` by name, triggers, swing, auto-close, locks, NPC use)
- `UI/Slice/Slice.uss` (pause menu styles)
- `Tests/EditMode/Slice/`, `Tests/PlayMode/Slice/` new tests
No edits to World files (`GrayboxBuilder.cs`, `graybox_layout.json`, scenes' geometry, `DOORS.json`): FOV is set at runtime (CF§1.2). No `Code/Domain/` or `Simulation/` edits except a pause flag the sim reads, if needed.

## Deliverable
1. Mouse look always on in `World`; cursor locked/hidden in `World`, free elsewhere; settings sensitivity / invert Y / FOV persisted in `PlayerPrefs`; pitch clamp; no smoothing, acceleration or head-bob (CF§1.2).
2. Esc opens the pause menu from every `SliceScreen` and Esc again resumes; pause freezes sim, NPCs, doors, cover countdown and cancels a POS hold; Resume restores the exact screen (CF§2.1–2.3). Backspace / Back button take over `Back()` (CF§2.4).
3. Doors per CF§3.2: walk-through open for the player, E toggle, signed swing about the hinge, auto-close, collider rules, locks incl. the entry `entryTimeLock` (DEC-076; inactive in the Quick shift), NPC use by `npcUse`. Read door data from `DOORS.json` when present; missing fields use the CF§7.1 placeholders (log one warning listing them).
   - Spawn leaves, triggers and interaction **only for rows with `leaves` = 1 or 2**; `0` / `null` (arches, the grille) is an open passage with nothing to spawn; rows marked not placed are skipped until their GAP closes (CF§3.2, CF§7.1).
   - Pairs use `leafObjects` (`Door_<Id>_L` / `_R`, each with its own `_Hinge`): the entry is `Door_Entry_L` / `Door_Entry_R`, swinging out (west), `lock = entryTimeLock` (REF-012; DEC-076).
   - `hardware` and `npcUse` as DOORS.json gives them (DEC-110: push bars only on emergency exits + delivery door, levers elsewhere; `Hall_Restroom` staff only, customers never path through it); report any data mismatch to World, no code override (CF§7.1).
   - `defaultState = proppedOpen` (DEC-103: `Vest_FOH`, `Vest_BOH`, `Hall_Office`, `HUB2_HUB`) loads open, collider off, no auto-close; if the player closes one, its own `selfClosing` / `lock` apply (CF§3.2).
4. Until World's `Door_<Id>` objects exist, the slice runs with no doors (openings as today) and logs one `[Slice] doors: none found` line — no TEMP door geometry in the store.

## Validation
Compile / EditMode / PlayMode green; slice goldens unchanged (pause and doors must not change sim results); QA-002 gate and DEC-013 gate green.
- EditMode: door state machine (closed → opening → open → closing; locked refuses; `npcUse` rules; `entryTimeLock` lets an exiting customer out after 22:00 but nobody in; `leaves` 0/null spawns nothing; a `proppedOpen` door starts open and never auto-closes); pause stops `Tick` and the hold timer.
- PlayMode: (a) a test-built door (hinge + leaf + two anchors, built in the test) opens when the scripted player walks into trigger A, lets it through, and closes after the delay; (b) Esc from each of `World`, `Query`, `Pos`, `IdCheck`, `Report` shows the pause menu and `Sim.Time` does not advance for 2 s; Resume returns to the same screen; (c) `GrayboxWalkTests` green.
- Capture: `SliceCaptureTests` adds the pause menu over the counter (1920×1080) and, if World doors are on `main`, one door mid-swing.

## Dependencies
GAME-009 merged (shared Presentation files). World REF-012 `DOORS.json` + scene `Door_<Id>` objects: **not blocking** — deliverables 1–2 and the door runtime with its test door ship without them; the in-store door check runs when they land. UX: no wireframe needed; UX may restyle later.

## Handoff
`Docs/Handoffs/GAME-025.md` (≤40 lines). Questions go to your department lead (DEC-033, DEC-094).
