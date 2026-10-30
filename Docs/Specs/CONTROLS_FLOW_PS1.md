# CONTROLS_FLOW_PS1 — Playtest 1 controls, pause, doors and customer flow (DES-005)

**Owner:** DES-005 · **Consumers:** GAME-025 (§1–§3), GAME-026 (§4–§6), World (§7 Contract) · **Status:** draft for review · 2026-10-30
**Inputs:** `Docs/Design/PLAYTEST_2026-10-30.md` (Nolan, build slice-38b9e5c), DEC-096, DEC-086, DEC-076, DEC-048, DEC-036 M2, DEC-039; `Specs/UX_PS1.md` §4, §7; `Design/SPEC_COMP002.md` §3; `Design/SPEC_SHIFT_DAY.md` §5–§7; `Research/OFFICE_FINDINGS.md` O2; code at `UnityProject/Assets/_Game/Code/` (`Presentation/Graybox/GrayboxTestPlayer.cs`, `Editor/Graybox/GrayboxBuilder.cs`, `Presentation/Slice/SliceGame.cs`, `Simulation/Slice/ShiftSim.cs`).

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
- **Closing:** a door with `selfClosing = true` closes `doorAutoCloseDelay` 1.5 s [GDD] after both triggers are empty; `selfClosing = false` stays where it was left. Until World states closer hardware, every door is placeholder `selfClosing = true` (GAP-CF-03).
- **Collision:** a closed leaf blocks (box collider). While swinging and while open, the leaf collider is off and the opening is walkable; the leaf never pushes the player or an NPC (kinematic, no physics).
- **Locked doors:** `lock` ≠ `none` and the actor is not allowed (§3.4) → the door does not open; the player gets the prompt "Locked" (or "Staff only" for staff-only doors that the *player* may use — the player is staff, so staff-only doors open for the player).
- **NPCs use doors:** an NPC whose path crosses a door's trigger opens it the same way (same animation, same auto-close). Customers only ever use doors with `npcUse` including `customer` (in PS1: the entry). Ambient staff (SPEC_SHIFT_DAY §5) use `staff` doors. Pathing through doors is waypoint-based (anchors), not NavMesh, until a navigation task exists.
- **Entry lock at 22:00 (DEC-076):** the entry door gets lock state `entryLockedAfter = 22:00` game clock: after it, nobody new enters; the door still opens **outward-going** for customers leaving (`npcUse` exit allowed). In the Quick shift (no game-clock lock) it never locks.
- **Emergency exits:** `npcUse = none`; the player may open them (no alarm modelled; GAP-CF-04).

### 3.3 Controls added by GAME-025
| Control | Keyboard / mouse | Controller |
|---|---|---|
| Look | mouse (always on in `World`) | right stick (not in PS1) |
| Pause / resume | **Esc** | Start |
| Back (was Esc) | **Backspace** / Back button | Ⓑ |
| Toggle door in reach | E (when no talk / ID / call prompt has priority) | Ⓐ |

`E` priority in `World` (one key, one action, by context): ID stand (`CanCheckId`) > talk to the customer at the counter (`CanTalk`) > call next (§5, GAME-026) > door toggle.

## 4. Customer flow overview (GAME-026)
PT: "the customer was already waiting at my register. I did not call them over." / "Customers should move through the actual entry/ID-check flow … no security guard checking IDs." / "Calling the next customer should feel like part of the player's workflow."

Today (`ShiftSim.Tick`): an arrival spawns inside the entry, joins the queue, and the moment the counter is free `Queue[0]` becomes `Serving` and walks to the register by itself. Covered (GAME-008) arrivals wait at the ID stand; everyone else skips any check.

### 4.1 New state path
`NotArrived → Arriving → AtCheckIn → Queued → Called → Serving → Done`

| State | Where | Who drives it | Patience |
|---|---|---|---|
| `Arriving` | `Anchor_CustomerSpawn` (outside) → through the entry door (`Door_<Id>` of the entry row) → check-in wait point | walk | not draining (off-screen-equivalent; SPEC_SHIFT_DAY §6 "wait outside is off-screen") |
| `AtCheckIn` | `Anchor_CheckIn_Wait_<n>`, then `Anchor_CheckIn` | **the guard** (§4.2) or the **player** when covering (GAME-008) | **drains** (as today's stand rule) |
| `Queued` | one line, `Anchor_Queue_<n>` (0 = front) | waits | **drains** |
| `Called` | walks from the line to `Anchor_Register_<n>_Call` | the player's call (§5) | **frozen** — a called customer never walks out |
| `Serving` | at the counter | the player (dialogue/terminal/POS as today) | active-service patience is GAME-019's (SPEC_SHIFT_DAY §6) |
| `Done` | → the entry door (`Door_<Id>` of the entry row) → `Anchor_CustomerExit` | walk | — |

`QueueWait` = time from entering `AtCheckIn` to being **called**. `ServiceStart` = arrival at the call point (not the moment of the call), so walk time never counts against service speed.

### 4.2 Entry check-in and the guard (DEC-086, DEC-048, DEC-036 M2)
- **Canon:** IDs are checked at an **entrance check-in ID stand**, directly left inside the entrance, by a security guard (DEC-048, DEC-086); the counter **never re-checks** (DEC-086, DEC-036 M2). Every customer passes through it.
- **Guard NPC** `NPC_Guard` (spawned by Gameplay at `Anchor_Guard_Post`, faces `Anchor_CheckIn`). Customers are checked **one at a time**, in arrival order. Each check takes `guardCheckSeconds` = 10 s [GDD] (GAP-CF-05), then the customer joins the line. The guard's checks have **no ID events and no strikes**: in PS1 the guard is always right (ID mistakes are only possible when the player covers).
- **Overflow:** waiting customers stand at `Anchor_CheckIn_Wait_<n>` (0 = next); more than the anchors → they wait at the last one (stacked, as today's queue overflow at spawn).
- **Coexistence with the GAME-008 stand:** it is **the same stand**. GAME-008's `Anchor_CheckInDesk` *is* `Anchor_CheckIn` (looked up by the new name with the old one as fallback). The cover mechanic stays exactly as SPEC_COMP002 §3 / UX_PS1 §4 define it: at rush start the prompt fires with `coverCheckInChance`; **accept** → the next `coverCheckInCount` arrivals are routed to the **player** at the stand (ID panel, Admit/Refuse, strikes), the guard keeps checking everyone else in parallel [GDD presentation: the player works a second spot at the same stand]; **decline** → those arrivals are checked by the guard, each taking `guardCheckSeconds + declineCheckInDelaySec` (the existing [GDD] delay becomes real wait at check-in).
- **Wait penalty:** because the decline delay is now physical wait inside `QueueWait`, the separate `CheckInDelay` term is **removed** from the `WaitPenalty(...)` sums in `ShiftSim` (it would count twice). The field may stay for telemetry.
- Admit by the player → `Queued` (end of the line). Refuse → leaves via the entry, outcomes as today.

### 4.3 One line (DEC-096)
One shared line for the player's register, `Anchor_Queue_0..N`. `queueSlots` (today 4) becomes the number of queue anchors World provides; overflow waits at the last check-in wait point. Line shape and location in the real store: GAP-CF-02 (placeholder: World's queue anchors). Other registers' ambient customers (SPEC_SHIFT_DAY §5, PS2) are not in this line.

## 5. Calling the next customer (GAME-026)
**Nobody walks to a register unprompted.** `ShiftSim` no longer promotes `Queue[0]` on its own.

### 5.1 Input
- **Where:** the player is within `InteractReach` (3 m, existing) of their own terminal (`Interact_Terminal`), the counter is empty (`Serving == null` and nobody `Called`), and the line is non-empty.
- **How:** prompt `E  Call next` (HUD interaction prompt, same style as `E  Talk`). Controller Ⓐ. Also a **Call next** button in the counter HUD cluster so it can be clicked from the terminal view.
- **Not allowed:** while a customer is `Called` or `Serving`; from away from the register (no remote calling); while paused.
- **Sim API:** `ShiftSim.CallNext()` (requires the conditions above; `Require` like the other flow methods) → `Queue[0]` becomes `Called`. `ShiftSim.ArriveAtCounter(c)` (called by the presentation when the NPC reaches the call point; the bot calls it directly) → `Serving`, `ServiceStart = Time`.

### 5.2 Feedback
| Beat | What happens |
|---|---|
| Press | subtitle toast with the player's line `callNext` = "Next guest, please!" [GDD copy; real wording GAP-CF-01] (UX toast rules, 2 s) |
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
| `guardCheckSeconds` | 10 s (GAP-CF-05) | GAME-026 (SliceConfig) |
| `declineCheckInDelaySec` | existing value, now physical wait | GAME-026 |
| `callNextDelay` (assist only) | 2 s | GAME-026 |
| `npcWalkSpeed` | existing 1.2 m/s | — |
| `queueSlots` | = number of `Anchor_Queue_<n>` found (fallback 4) | GAME-026 |

## 7. Contract — scene anchors Gameplay needs from World
**Status: needs; World commits names.** Names below that World has proposed but not yet merged are marked *proposed by World, not yet on main*. Gameplay finds every object by name at runtime and falls back to a `TEMP_` placeholder with a warning (today's `SliceGame.Anchor` pattern), so GAME-025/026 can start before World lands them.

### 7.1 Doors (World task REF-012 → `Docs/Reference/DOORS.json`)
| Name | Need | Status |
|---|---|---|
| `Door_<Id>` | the door leaf (or leaves) object, one per DOORS.json row; `<Id>` = the row id | proposed by World, not yet on main |
| `Door_<Id>_Hinge` | pivot transform at the hinge jamb; leaf is its child; rotate about local Y | proposed by World, not yet on main |
| DOORS.json `closedRotation`, signed `openAngle` | the swing Gameplay animates | proposed by World, not yet on main |
| `Anchor_Door_<Id>_A` / `_B` | one trigger anchor per side; Gameplay builds the trigger volume around each (≈ 1.2 m × leaf width [GDD]) | proposed by World, not yet on main |
| DOORS.json `type`, `staffOnly`, leaf width | already in REF-012's row | proposed by World, not yet on main |

**Extra per-door fields Gameplay needs in DOORS.json** (World to add, or GAP if unknown):
| Field | Values | Used for |
|---|---|---|
| `leaves` | 1 / 2 (pair: `Door_<Id>_L` / `_R` with `_Hinge` each) | entry storefront is 6'-0" wide (DEC-037) — pair or single is GAP |
| `selfClosing` | true / false / unknown | §3.2 auto-close |
| `lock` | `none` / `staffOnly` / `keyed` / `entryTimeLock` | §3.2 locked doors; the entry's DEC-076 22:00 lock |
| `npcUse` | any of `customer`, `staff`; empty = nobody | §3.2 NPC door use |
| `hardware` | `lever` / `pushBar` / `storefrontPull` / `none` | prompt text and swing feel |
| `defaultState` | `closed` / `proppedOpen` | doors the store normally keeps open |

### 7.2 Entry, check-in and line
| Name | Need | Status |
|---|---|---|
| `Anchor_CustomerSpawn` | **outside** the entry door (parking side), so customers walk through the entry door (`Door_<Id>` of the entry row) | exists; **position change needed** (today's fallback is inside the entry) |
| `Anchor_CustomerExit` | outside the entry door | exists; position check needed |
| `Anchor_Guard_Post` | where the guard stands, facing the check-in point | proposed by World, not yet on main |
| `Anchor_CheckIn` | where the customer stands to be checked = the DEC-048 ID stand; replaces GAME-008's `Anchor_CheckInDesk` (old name kept as fallback) | proposed by World, not yet on main |
| `Anchor_CheckIn_Wait_<n>` | n = 0.. ordered waiting points before check-in (inside the entrance; outside if the real line forms outside, GAP-CF-02) | **new need** |
| `Anchor_Queue_<n>` | n = 0 (front) .. N, the one line to the registers | proposed by World, not yet on main; `Anchor_QueueSlot_0..3` (exist) stay as aliases until GAME-026 merges |

### 7.3 Registers (stations 2–12, DEC-039)
| Name | Need | Status |
|---|---|---|
| `Anchor_Register_<StationNo>_Call` | where a called customer stands at that station | proposed by World, not yet on main |
| `Anchor_Register_<StationNo>_Operator` | where the operator (player or ambient staff) stands | proposed by World, not yet on main |
| player's station | the station the player works = the one holding `Interact_Terminal` / `Interact_Scale` (exist); its `_Call`/`_Operator` replace `Anchor_ServiceCustomer` / `Anchor_ServicePlayer` (old names kept as fallback). Which real station: GAP-CF-06 | **needs World to state the station number** |

Gameplay owns (not World): `NPC_Guard`, NPC customers, trigger volumes, door animation.

## 8. Gaps and placeholders (for KNOWN_GAPS via the Hub)
| Gap | Unknown | Placeholder in use | Ask |
|---|---|---|---|
| GAP-CF-01 | How a budtender actually calls the next guest (by name from the Dutchie Guest List, "next please", a wave, a screen) — O2 says guests are checked in to the Dutchie Guest List | spoken "Next guest, please!" + walk-up | Nolan |
| GAP-CF-02 | Where and how the line forms after check-in (standing line on the floor, waiting area, outside); GAP-DAY-04 one-vs-per-register is taken as **one line** from DEC-096 | World's `Anchor_Queue_<n>` | Nolan |
| GAP-CF-03 | Which interior doors are self-closing, which are normally propped open | all `selfClosing = true`, `closed` | Nolan / World |
| GAP-CF-04 | Emergency exit alarm behaviour | not modelled | Nolan |
| GAP-CF-05 | Typical time for the guard to scan an ID and check a guest in | 10 s | Nolan |
| GAP-CF-06 | Which register the player works | the station with `Interact_Terminal` | Nolan / World (REF-011 register audit) |
| GAP-CF-07 | O2 says staff verify ID "before the door to the sales area opens": is there a second (buzzed/locked) door between the check-in stand and the sales floor? DEC-086 rejected an invented vestibule | no second door | Nolan |
| GAP-CF-08 | Who covers check-in when it backs up in reality (budtenders, a manager), and whether the guard stays at the stand meanwhile | guard keeps checking; the player works a second spot | Nolan |
