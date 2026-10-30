# CONTROLS_FLOW_PS1 — Playtest 1 controls, pause, doors and customer flow (DES-005)

**Owner:** DES-005 (amended DES-005b) · **Consumers:** GAME-025 (§1–§3), GAME-026 (§4–§6), World (§7 Contract) · **Status:** draft for review · 2026-10-30
**DES-005b amendment (DEC-103, DEC-109; Nolan's real-store answers):** call lines (§5.2), no second door, guard scans the back of the ID with a green light + sound (§4.2), the ID is shown again at the register (§4.4; corrects DEC-086 / DEC-036 M2 "the counter never re-checks"), check-in takes seconds and never backs up (backlog/helper logic dropped, §4.2), four doors propped open (§3.2, §7.1), GM floor-map register assignment (§5.0, DEC-079). GAPs closed in §8. ID checks split by what each check can see (§4.2, §4.4; lead ruling DEC-109). Anchor names from REF-011 `SCENE_ANCHORS.json` and doors from REF-012 `DOORS.json` (both pending merge).
**Inputs:** `Docs/Design/PLAYTEST_2026-10-30.md` (Nolan, build slice-38b9e5c), DEC-103, DEC-096, DEC-086, DEC-079, DEC-076, DEC-048, DEC-036 M2, DEC-039; `Specs/UX_PS1.md` §4, §7; `Design/SPEC_COMP002.md` §3; `Design/SPEC_SHIFT_DAY.md` §5–§7; `Research/OFFICE_FINDINGS.md` O2; code at `UnityProject/Assets/_Game/Code/` (`Presentation/Graybox/GrayboxTestPlayer.cs`, `Editor/Graybox/GrayboxBuilder.cs`, `Presentation/Slice/SliceGame.cs`, `Simulation/Slice/ShiftSim.cs`).

Every number marked **[GDD]** is a design starting value, tunable, not a store fact. Unknown store facts are **GAP-CF-nn** placeholders listed in §8. Nolan's playtest quotes are cited as **PT** (the playtest file).

---

## 1. Camera and look (GAME-025)

### 1.1 Why it feels clunky today (causes from the code)
PT: "WASD itself is mostly fine; my bigger issue is the camera movement and how looking/turning feels."

| # | Cause | Where |
|---|---|---|
| C1 | **Look only works while the right mouse button is held** (`mouse.rightButton.isPressed`). Every turn is a hold-and-drag, which is the main source of "clunky". | `GrayboxTestPlayer.Update` |
| C2 | **The cursor is never locked.** `SliceGame.Show()` sets `CursorLockMode.None` + visible on *every* screen change, including back to `World`, so the cursor stays free over the game view and leaves the window at the edges. | `SliceGame.Show` |
| C3 | **FOV is Unity's default 60° vertical** (≈ 91° horizontal at 16:9). The builder never sets `fieldOfView` on the player camera, so the view feels narrow and turning feels faster than it is. | `GrayboxBuilder` player build (`Eye` camera) |
| C4 | **Fixed sensitivity** 0.1°/count, no setting, no invert-Y. Not wrong as a default, but nobody can tune it. | `GrayboxTestPlayer.LookSensitivity` |
| C5 | Pitch clamp ±80°: looking down at the scale/counter is cut short. | `GrayboxTestPlayer` |
| C6 | Smoothing: **none**; acceleration: **none**; head-bob: **none**. These are *not* causes and stay that way (raw mouse is the PC norm; bob costs comfort). | — |
| C7 | Input is polled straight from `Keyboard.current` / `Mouse.current`; no controller look. Out of scope for PS1 (no controller target yet). | both files |

### 1.2 Targets
| Key | Value | Label | Note |
|---|---|---|---|
| Look mode | **always-on mouse look while the `World` screen is up**; no button hold | [GDD] | fixes C1 |
| Cursor | `World` = locked + hidden; any UI screen or the pause menu = free + visible; regaining window focus in `World` re-locks on the first click | [GDD] | fixes C2 |
| `lookSensitivity` | default 0.10 °/count; settings range 0.02–0.40 | [GDD] | units unchanged from today |
| `invertY` | off; setting | [GDD] | |
| `fovVertical` | default **70°** (≈ 102° horizontal at 16:9); settings range 60–90 | [GDD] | set at runtime on the player camera, not in the World-owned builder |
| `pitchClamp` | ±85° | [GDD] | |
| `lookSmoothing` | 0 (off); no setting | [GDD] | C6 |
| `mouseAcceleration` | none | [GDD] | C6 |
| `headBob` | none | [GDD] | C6 |
| Walk / run speed | unchanged: 1.4 / 3.0 m/s | (existing) | PT: WASD is fine |
| Settings persistence | `PlayerPrefs` (per machine) | [GDD] | not sim config; never read by the sim |

Look input is ignored while any non-`World` screen or the pause menu is open (today's `ScriptedWorldMove` freeze already does this for movement).

## 2. Esc and the pause menu (GAME-025)
PT: "Esc should always open a pause/menu screen."

### 2.1 Rule
**Esc opens the pause menu from every state**: walking (`World`), `Dialogue`, `Query`, `Results`, `Detail`, `Pos`, `CoverPrompt`, `IdCheck` and `Report`. Esc inside the pause menu = **Resume**. Esc never closes or backs out of anything else any more.

### 2.2 What pause does
- Freezes every sim-affecting system (SPEC_SHIFT_DAY §7 "Pause freezes every sim-affecting system"): `ShiftSim.Tick`, arrivals, patience, NPC movement, door animation, the cover-prompt countdown and the POS hold-to-confirm. Implementation note: the sim already ticks on `Time.deltaTime`; the hold-to-confirm uses `unscaledDeltaTime` and the pause must stop it too (a hold in progress is cancelled on pause).
- The screen underneath stays as it was; Resume returns to it unchanged (same screen, same focus, same cart).
- Cursor free + visible while paused; on Resume the cursor state of the underlying screen is restored (§1.2).
- Pause time is not counted in service time, queue wait or the shift clock.

### 2.3 Pause menu items
| Item | Action |
|---|---|
| Resume (default focus) | close the menu |
| Settings | look sensitivity, invert Y, FOV (§1.2); the existing UX_SLICE §7 accessibility settings (text scale etc.) move here |
| Controls | read-only key list (§3.3 + UX_PS1 §7) |
| Quit to desktop | `Application.Quit` (Editor: stop play mode) after a confirm |

Visual: centred panel on a dimmed world, UX_SLICE §6 tokens. Layout is UX's call; no wireframe is required for GAME-025 to start.

### 2.4 What replaces Esc as "Back" **[GDD]**
Today Esc is Back (`SliceGame.Back`) and UX_PS1 §7 binds Esc to "Close ID panel" and "Close report". New binding: **Backspace** and the on-screen **Back** button do what Esc did (same `Back()` routing); Enter still closes the report. Controller Ⓑ is unchanged. **UX_PS1 §7's Esc rows are superseded by this section** (UX owns that file's text; see handoff).

## 3. Doors (GAME-025)
PT: "Doors need to be addressed so movement through the store feels natural."

### 3.1 Today
Doors are **empty openings**: `graybox_layout.json` walls list `openings` and `GrayboxBuilder` cuts a gap with a header above it. There is no leaf, no swing, no collision and no interaction, so the store reads as open holes and the entry has no door at all.

### 3.2 Interaction model **[GDD]**
- **Walk-through for the player.** A closed, unlocked door opens when the player is inside either trigger (`Anchor_Door_<Id>_A` / `_B`, §7) **and** moving toward the door (velocity · door-normal > 0). No key press on the common path. `E` also toggles any unlocked door in reach (for a door you want to close behind you).
- **Swing:** the leaf rotates about `Door_<Id>_Hinge` from its closed rotation to the **signed open angle from DOORS.json** (the real swing side; never flipped to suit the player). Open time `doorOpenSeconds` 0.45 s, ease-out [GDD]. A double-leaf door opens both leaves.
- **Closing:** a door with `selfClosing = true` closes `doorAutoCloseDelay` 1.5 s [GDD] after both triggers are empty; `selfClosing = false` stays where it was left. Until World states closer hardware, every other door is placeholder `selfClosing = true` (GAP-CF-03).
- **Propped open (DEC-103):** the **FOH door, the BOH door, the north-facing office door and the HUB connector** are almost always propped open. In REF-012's `DOORS.json` (pending merge) these are `Vest_FOH`, `Vest_BOH`, `Hall_Office` and `HUB2_HUB`, with `defaultState = proppedOpen`: they load at their open angle, collider off, and do not auto-close while propped. `E` still toggles them; once the player closes one, its own `selfClosing` / `lock` values apply (DOORS.json rule) until the next shift.
- **What gets a leaf (REF-012, pending merge):** GAME-025 spawns leaves, triggers and interaction **only for rows with `leaves` = 1 or 2**. Any other value (`0` = opening, `null` = unknown; e.g. the arches `Arch_W` / `Arch_E` and the grille `Grille_101B`) is an **open passage with nothing to spawn**. Rows the JSON marks not placed (their `notes` / `gap`) are skipped until that GAP closes.
- **The entry (REF-012, pending merge):** a **double door**, leaves `Door_Entry_L` / `Door_Entry_R` (each with its own `_Hinge` pivot), swinging **out (west)**, `lock = entryTimeLock` (DEC-076).
- **Collision:** a closed leaf blocks (box collider). While swinging and while open, the leaf collider is off and the opening is walkable; the leaf never pushes the player or an NPC (kinematic, no physics).
- **Locked doors:** `lock` ≠ `none` and the actor is not allowed (§3.4) → the door does not open; the player gets the prompt "Locked" (or "Staff only" for staff-only doors that the *player* may use — the player is staff, so staff-only doors open for the player).
- **NPCs use doors:** an NPC whose path crosses a door's trigger opens it the same way (same animation, same auto-close). Customers only ever use doors with `npcUse` including `customer` (in PS1: the entry). Ambient staff (SPEC_SHIFT_DAY §5) use `staff` doors. Pathing through doors is waypoint-based (anchors), not NavMesh, until a navigation task exists.
- **Entry lock at 22:00 (DEC-076):** the entry door gets lock state `entryLockedAfter = 22:00` game clock: after it, nobody new enters; the door still opens **outward-going** for customers leaving (`npcUse` exit allowed). In the Quick shift (no game-clock lock) it never locks.
- **Emergency exits:** `npcUse = none`; the player may open them. No alarm is modelled: GAP-CF-04 was asked and not answered (DEC-103), so this placeholder is the working answer and is not re-asked (DEC-105).

### 3.3 Controls added by GAME-025
| Control | Keyboard / mouse | Controller |
|---|---|---|
| Look | mouse (always on in `World`) | right stick (not in PS1) |
| Pause / resume | **Esc** | Start |
| Back (was Esc) | **Backspace** / Back button | Ⓑ |
| Toggle door in reach | E (when no talk / ID / call prompt has priority) | Ⓐ |

`E` priority in `World` (one key, one action, by context): register ID check (§4.4, when one is pending) > talk to the customer at the counter (`CanTalk`) > call next (§5, GAME-026) > door toggle. (DEC-103: the entry stand is the guard's alone, so it no longer takes `E`.)

## 4. Customer flow overview (GAME-026)
PT: "the customer was already waiting at my register. I did not call them over." / "Customers should move through the actual entry/ID-check flow … no security guard checking IDs." / "Calling the next customer should feel like part of the player's workflow."

Today (`ShiftSim.Tick`): an arrival spawns inside the entry, joins the queue, and the moment the counter is free `Queue[0]` becomes `Serving` and walks to the register by itself. Covered (GAME-008) arrivals wait at the ID stand; everyone else skips any check.

### 4.1 New state path
`NotArrived → Arriving → AtCheckIn → Queued → Called → Serving → Done`

| State | Where | Who drives it | Patience |
|---|---|---|---|
| `Arriving` | `Anchor_CustomerSpawn` (outside) → through the entry door (`Door_<Id>` of the entry row) → check-in wait point | walk | not draining (off-screen-equivalent; SPEC_SHIFT_DAY §6 "wait outside is off-screen") |
| `AtCheckIn` | `Anchor_CheckIn_Wait_<n>` (only if the guard is mid-scan), then `Anchor_CheckIn` | **the guard** (§4.2) | **drains** (as today's stand rule; in practice a few seconds, DEC-103) |
| `Queued` | one line, `Anchor_Queue_<n>` (0 = front) | waits | **drains** |
| `Called` | walks from the line to `Anchor_Register_<n>_Call` | the player's call (§5) | **frozen** — a called customer never walks out |
| `Serving` | at the counter; starts with the register ID beat (§4.4) | the player (ID beat, then dialogue/terminal/POS as today) | active-service patience is GAME-019's (SPEC_SHIFT_DAY §6) |
| `Done` | → the entry door (`Door_<Id>` of the entry row) → `Anchor_CustomerExit` | walk | — |

`QueueWait` = time from entering `AtCheckIn` to being **called**. `ServiceStart` = arrival at the call point (not the moment of the call), so walk time never counts against service speed.

### 4.2 Entry check-in and the guard (DEC-103, DEC-048, DEC-086)
- **Canon:** IDs are checked at an **entrance check-in ID stand**, directly left inside the entrance, by a security guard (DEC-048, DEC-086). Every customer passes through it. There is **no second (buzzed) door** between the stand and the sales floor (DEC-103 (3); DEC-086 already rejected an invented vestibule).
- **The scan (DEC-103 (4)):** the guard **scans the back of the ID**; a **green light and a sound** mean the guest may join the line. Presentation: `NPC_Guard` holds the ID to a scanner prop; the scanner shows a green light for `scanLightSeconds` 0.6 s [GDD] and raises the `OnIdScanOk` event (AUDIO hook; GAME-026 ships no sound, so the light is the only required cue). Then the guest walks to the end of the line.
- **Guard NPC** `NPC_Guard` (spawned by Gameplay at `Anchor_Guard_Post`, faces `Anchor_CheckIn`). One guest at a time, in arrival order. Each check takes `guardCheckSeconds` = **3 s** [GDD; DEC-103 (5): "a few seconds at most"]. The guard's checks have **no player decision and no strikes**.
- **Red light at the door (DEC-109):** the scanner reads the back of the ID, so it catches **expired and underage** IDs: an automatic **red light** (`OnIdScanFail` hook), the guard turns the guest away, and the guest leaves via the entry. No player action, no strike. Rare and ambient: `scanRejectChance` 0.02 per arrival [GDD]; drawn from GAME-008's expired / under-21 cases. Outcome `TurnedAwayAtDoor` (excluded from satisfaction and wait averages like `Refused`); report Compliance block counts it.
- **No backlog, no helpers (DEC-103 (5)):** check-in never backs up, so there is **no overflow queue, no cover prompt and no helper logic** at the stand. A guest who arrives while the guard is mid-scan waits at `Anchor_CheckIn_Wait_<n>` (0 = next; REF-011 places 0..3 inside the entrance; more arrivals stack at the last one); with 3 s checks this is rare and needs no backlog logic.
- **GAME-008's stand:** it is **the same stand**: GAME-008's `Anchor_CheckInDesk` *is* `Anchor_CheckIn` (looked up by the new name with the old one as fallback). The player no longer works it: the cover prompt's premise ("the ID stand is backed up", UX_PS1 §4, SPEC_COMP002 §3) contradicts DEC-103, so GAME-008's player ID decisions move to the register (§4.4) and its expired/underage cases become the door's red light (DEC-109).
- **Wait penalty:** with no decline path, `declineCheckInDelaySec` and the `CheckInDelay` term are **retired**: remove `CheckInDelay` from the `WaitPenalty(...)` sums in `ShiftSim` (the field may stay for telemetry, always 0). Real check-in time is now inside `QueueWait`.

### 4.3 One line (DEC-096, DEC-103 (2), DEC-079)
One shared line for the player's register, `Anchor_Queue_0..N`; guests wait **in line** after check-in (DEC-103 (2)). `queueSlots` (today 4) becomes the number of queue anchors World provides; overflow stacks at the last queue anchor. Where the line stands on the real floor is World's to place from evidence (REF-011 `SCENE_ANCHORS.json`); it is not a store question any more. Other registers' ambient customers (SPEC_SHIFT_DAY §5, PS2) are not in this line.

### 4.4 The ID again at the register (DEC-103 (4), DEC-109)
**The guest shows the ID again at the register.** This corrects DEC-086's and DEC-036 M2's "the counter never re-checks" (and SPEC_COMP002 §3 / UX_PS1 §4, which now carry a DEC-103 note).
- **Every guest:** on arrival at the call point (`Serving` starts) the guest hands over the ID: a **register ID beat** of `registerIdSeconds` 2 s [GDD], counted in service time. Most guests: the beat plays (ID held out, the player glances, HUD line `ID shown ✓`) with no decision, and it is what backs the existing POS line "21+ ID verified".
- **Lead ruling (DEC-109): the register re-check covers what a scanner can't see.** These stay **player decisions** with GAME-008's ID panel at the counter (`E`, §3.3), Admit/Refuse and strikes (CP§3 outcomes):
  | Register case | Valid? | Note |
  |---|---|---|
  | Photo mismatch / borrowed ID | no | new [GDD] case: the panel shows the card photo next to the guest's face portrait |
  | Medical card name ≠ ID name | no (for the medical sale) | new [GDD] case; refuse = adult-use only if 21+, as CP§4 |
  | Out-of-state medical card | adult-use only | existing GAME-009 decision (CP§4, A7), now framed as part of the register check |
  | Damaged / unreadable ID | no | new [GDD] case: the card art is worn/cracked so a field can't be read |
  | AZ vertical, turned 21 > 30 days ago | no | GAME-008 case kept here: a format rule the guard's age scan does not apply [GDD, flagged to the lead] |
  | Valid IDs (all other GAME-008 valid cases) | yes | the "nothing wrong" answers that keep it a real decision |
- **Selection [GDD]:** at rush start, with `coverCheckInChance` (key kept to avoid churn; reads as "ID-event chance"), the next `coverCheckInCount` guests **called to the register** carry an `IdCard` drawn from the register cases (weights [GDD], GAME-026 sets them in SliceConfig). GAME-009's out-of-state medical cards keep their own frequency. **Expired and under-21 cases are never drawn here** (the door caught them, §4.2).
- **Admit** → service continues; **Refuse** → the guest leaves via the entry; strikes exactly as CP§3. No prompt, no walk to the stand. The `AtStand` state and the `Stand` list are no longer reached (GAME-026 may delete them or leave them unused; no save data depends on them).

## 5. Calling the next customer (GAME-026)
**Nobody walks to a register unprompted.** `ShiftSim` no longer promotes `Queue[0]` on its own.

### 5.0 Which register is the player's (DEC-079, DEC-103 (7))
The **GM assigns registers on a floor map** and budtenders follow it (DEC-079; DEC-103 (7)). Model [GDD]:
- `RegisterAssignment` (sim data, set at shift start, read-only during the shift): `playerStation` = one station number from DEC-039's floor registers 2–12, plus the stations given to ambient staff (PS2, SPEC_SHIFT_DAY §5).
- PS1 uses SliceConfig `assignedStation` = **08** [GDD placeholder, matching REF-011's player station]; the stations' anchors are `Anchor_Register_<NN>_Call` / `_Operator` with a **zero-padded** number (02..12). If station 08's anchors are missing, fall back to `Anchor_ServiceCustomer` / `Anchor_ServicePlayer` and log one warning. PS2 replaces the pick with the GM's floor map for the day's open-register count (RES-002, GAP-DAY-03).
- Presentation: a shift-start toast `Floor map: you're on Register {n}` [GDD copy] and a marker on that station until the player first reaches it. Where the paper map hangs is not a store fact we hold; nothing is modelled for it.
- Every "own register" rule below (call next, reach) means **the assigned station**: reach is measured from its `_Operator` anchor; `Interact_Terminal` / `Interact_Scale` stay single objects at the player's station (World/ART-007 places them there).

### 5.1 Input
- **Where:** the player is within `InteractReach` (3 m, existing) of the assigned station's terminal (§5.0), the counter is empty (`Serving == null` and nobody `Called`), and the line is non-empty.
- **How:** prompt `E  Call next` (HUD interaction prompt, same style as `E  Talk`). Controller Ⓐ. Also a **Call next** button in the counter HUD cluster so it can be clicked from the terminal view.
- **Not allowed:** while a customer is `Called` or `Serving`; from away from the register (no remote calling); while paused.
- **Sim API:** `ShiftSim.CallNext()` (requires the conditions above; `Require` like the other flow methods) → `Queue[0]` becomes `Called`. `ShiftSim.ArriveAtCounter(c)` (called by the presentation when the NPC reaches the call point; the bot calls it directly) → `Serving`, `ServiceStart = Time`.

### 5.2 Feedback
| Beat | What happens |
|---|---|
| Press | subtitle toast with the player's spoken call, picked at random from `callNext` = **"Next in line!"** / **"Next guest!"** (DEC-103 (1), real store lines) (UX toast rules, 2 s). DEC-103's third line, **"Online order!"**, is stored as `callOnlineOrder` and unused in PS1: there are no online-order pickups in the game yet |
| Customer | the front customer turns to the player, gets a 1 s highlight pulse on its capsule/body [GDD], and walks to `Anchor_Register_<n>_Call` |
| Line | everyone behind steps forward one anchor |
| HUD | counter cluster: `Called · walking up` until arrival, then the normal `E  Talk` prompt |
| Audio | a hook only (`OnCallNext` event) for AUDIO later; no sound required in GAME-026 |

### 5.3 Pressure and fairness
- The line's patience keeps draining until the player calls, so an idle player costs walkouts: calling promptly is part of the job (PT).
- Called customers' patience is frozen, so a long walk never causes a walkout.
- **Assist** `Auto-call next` (off by default, UX_SLICE §7 assists table): calls `CallNextDelay` 2 s [GDD] after the counter clears; tagged `assist` in the report like other assists.
- **Bots** (GAME-010 personas, QA-002 harness): call next as soon as allowed (the slow persona waits its 1.5× pacing, DEC-086).

### 5.4 Shift-end interaction (DEC-076)
After the entry lock no one new arrives; customers already inside (at check-in, in line or called) are still checked and served; closing starts when the last one is served. GAME-026 implements this only for the game-clock day mode if it exists on `main` by then; the Quick shift ends as today.

## 6. Numbers (all [GDD])
| Key | Value | Owner |
|---|---|---|
| `lookSensitivity` | 0.10 °/count (0.02–0.40) | GAME-025 |
| `fovVertical` | 70° (60–90) | GAME-025 |
| `pitchClamp` | ±85° | GAME-025 |
| `doorOpenSeconds` | 0.45 s | GAME-025 |
| `doorAutoCloseDelay` | 1.5 s | GAME-025 |
| `guardCheckSeconds` | **3 s** (DEC-103 (5): "a few seconds at most"; was 10 s) | GAME-026 (SliceConfig) |
| `scanLightSeconds` | 0.6 s (green / red scanner light, §4.2) | GAME-026 |
| `scanRejectChance` | 0.02 per arrival (red light, turned away, §4.2, DEC-109) | GAME-026 (SliceConfig) |
| `registerIdSeconds` | 2 s (register ID beat, §4.4) | GAME-026 (SliceConfig) |
| `declineCheckInDelaySec` | **retired** (no cover/decline path, DEC-103 (5)); key may stay, unused | GAME-026 |
| `assignedStation` | 8 (station 08, REF-011 placeholder) (§5.0) | GAME-026 (SliceConfig) |
| `callNextDelay` (assist only) | 2 s | GAME-026 |
| `npcWalkSpeed` | existing 1.2 m/s | — |
| `queueSlots` | = number of `Anchor_Queue_<n>` found (fallback 4) | GAME-026 |

## 7. Contract — scene anchors Gameplay needs from World
**Status: needs; World commits names.** Door names and fields come from REF-012's `Docs/Reference/DOORS.json` (**REF-012, pending merge**: passed review, not yet on `main`); anchor names from REF-011's `Docs/Reference/SCENE_ANCHORS.json` (**REF-011, pending merge**: passed review, not yet on `main`; 42 anchors, plus the old names as aliases). Most anchors are **Low confidence until ART-007 builds the objects**. Gameplay finds every object by name at runtime; a missing object falls back to its alias, then to the SCENE_ANCHORS.json position, then to a `TEMP_` placeholder, and logs **one warning listing what fell back; it never fails** (today's `SliceGame.Anchor` pattern), so GAME-025/026 can start before World lands them.

### 7.1 Doors (REF-012 → `Docs/Reference/DOORS.json`, pending merge)
| Name | Need | Status |
|---|---|---|
| `Door_<Id>` | the leaf object of a row with `leaves` = 1; `<Id>` = the row id | REF-012, pending merge |
| `Door_<Id>_L` / `_R` | the two leaves of a row with `leaves` = 2 (DOORS.json `leafObjects`; L/R as seen from side A); the entry is `Door_Entry_L` / `Door_Entry_R` | REF-012, pending merge |
| `<leaf object>_Hinge` | pivot at the hinge jamb, one per leaf; the leaf is its child; rotate about local Y | REF-012, pending merge |
| DOORS.json `closedRotation`, signed `openAngle` | the swing Gameplay animates (open yaw = closed yaw + `openAngle`); the entry pair swings **out (west)** | REF-012, pending merge |
| `Anchor_Door_<Id>_A` / `_B` | one trigger anchor per side; Gameplay builds the trigger volume around each (≈ 1.2 m × leaf width [GDD]) | REF-012, pending merge |
| DOORS.json `type`, `staffOnly`, leaf width | in every row | REF-012, pending merge |

**Per-door fields Gameplay reads** (all in REF-012's rows):
| Field | Values | Used for |
|---|---|---|
| `leaves` | 1 / 2 → spawn leaf(s), triggers and interaction; **0 or null → open passage, spawn nothing** (arches, grille) | §3.2 "what gets a leaf" |
| not-placed rows | rows whose `notes` / `gap` say not placed (e.g. `Grille_101B`) | skipped until their GAP closes |
| `selfClosing` | true / false / unknown (unknown → placeholder true) | §3.2 auto-close |
| `lock` | `none` / `staffOnly` / `keyed` / `entryTimeLock` | §3.2 locked doors; the entry is `entryTimeLock` (DEC-076) |
| `npcUse` | any of `customer`, `staff`; empty = nobody | §3.2 NPC door use; the guard counts as staff (REF-012 `_about`) |
| `hardware` | `lever` / `pushBar` / `storefrontPull` / `none` | prompt text and swing feel |
| `defaultState` | `closed` / `proppedOpen` (null for openings) | **proppedOpen per DEC-103 (6): `Vest_FOH`, `Vest_BOH`, `Hall_Office` (the north-facing office door), `HUB2_HUB` (the HUB connector)** |

No second (buzzed) door after the ID stand exists or is modelled (DEC-103 (3); REF-012 `_about`).

### 7.2 Entry, check-in and line
| Name | Need | Status |
|---|---|---|
| `Anchor_CustomerSpawn` | **outside** the entry door (parking side), so customers walk through `Door_Entry_L/_R` | REF-011, pending merge |
| `Anchor_CustomerExit` | outside the entry door | REF-011, pending merge |
| `Anchor_Guard_Post` | where the guard stands, facing the check-in point; the scanner light sits here + 0.4 m toward `Anchor_CheckIn` [GDD] | REF-011, pending merge |
| `Anchor_CheckIn` | where the customer stands to be scanned = the DEC-048 ID stand; alias `Anchor_CheckInDesk` (GAME-008) | REF-011, pending merge |
| `Anchor_CheckIn_Wait_<n>` | n = 0..3, waiting points **inside the entrance** for a guest who arrives mid-scan (check-in never backs up, DEC-103 (5)) | REF-011, pending merge |
| `Anchor_Queue_<n>` | n = 0 (front) .. N, the one line to the registers (DEC-096, DEC-103 (2)) | REF-011, pending merge (n = 0..11); aliases `Anchor_QueueSlot_0..3` |

### 7.3 Registers (stations 2–12, DEC-039)
| Name | Need | Status |
|---|---|---|
| `Anchor_Register_<NN>_Call` | where a called customer stands at that station, **zero-padded** `02`..`12`; the register ID beat plays here (§4.4) | REF-011, pending merge |
| `Anchor_Register_<NN>_Operator` | where the operator (player or ambient staff) stands | REF-011, pending merge |
| player's station | **08** [GDD placeholder] by GM floor-map assignment (§5.0; DEC-079/103 answer GAP-CF-06); aliases `Anchor_ServiceCustomer` / `Anchor_ServicePlayer` | REF-011, pending merge |

Gameplay owns (not World): `NPC_Guard`, the scanner green/red light, NPC customers, trigger volumes, door animation, `RegisterAssignment`.

## 8. Gaps and placeholders (registered in KNOWN_GAPS)
| Gap | Unknown | State after DEC-103 | Working value |
|---|---|---|---|
| GAP-CF-01 | How a budtender calls the next guest | **CLOSED by DEC-103 (1)**: out loud, "Next in line!" / "Online order!" / "Next guest!" | §5.2; "Online order!" unused until online orders exist |
| GAP-CF-02 | Where and how guests wait after check-in | **CLOSED by DEC-103 (2)**: in line (one line, DEC-079/096). The line's floor position is World's from evidence (REF-011), not a store question | `Anchor_Queue_<n>` |
| GAP-CF-03 | Which interior doors self-close / are propped open | **CLOSED**: propped by DEC-103 (6) (FOH, BOH, office, HUB connector); closers from TI A310 in REF-012 (pending merge). Rows with `selfClosing: unknown` are REF-012's own GAPs | `unknown` → self-closing placeholder |
| GAP-CF-04 | Emergency exit alarm behaviour | **OPEN, not re-asked**: unanswered in DEC-103, so per DEC-105 the placeholder is the working answer (OFFICE_FINDINGS also leaves alarms out as security-sensitive) | not modelled |
| GAP-CF-05 | Guard check-in time | **CLOSED by DEC-103 (5)**: a few seconds at most | `guardCheckSeconds` 3 s [GDD] |
| GAP-CF-06 | Which register the player works | **CLOSED by DEC-079** (restated DEC-103 (7)): the GM assigns registers on a floor map | §5.0 `RegisterAssignment`, station 08 [GDD] |
| GAP-CF-07 | A second (buzzed) door after the ID stand? | **CLOSED by DEC-103 (3)**: no | none modelled |
| GAP-CF-08 | Who helps when check-in backs up | **CLOSED by DEC-103 (5)**: it never backs up; no helper logic | §4.2: no backlog, no cover prompt |
