# Proposal — playtest 1 long-term ideas (DES-005)

**Status:** proposal; **the Hub decides scope and phase** (DEC-096). Source: Nolan, `Docs/Design/PLAYTEST_2026-10-30.md` (cited **PT**). Phases refer to `Docs/Design/ROADMAP_POST_SLICE.md` (PS1 counter decisions, PS1b decision pressure GAME-017..020, PS2 full shift day per `SPEC_SHIFT_DAY.md`, PS4 staffing per DEC-063d). "Rough phase" is a suggestion. Nothing here invents store facts; unknowns are listed as asks for Nolan.

## 1. Parking-lot throughput
- **What:** customers arrive by car into real parking spaces; a full lot makes new arrivals circle or wait; leaving frees a space; side-of-building parking can block others from backing out (PT). Lot occupancy becomes a visible pressure gauge outside.
- **Why:** Nolan calls it "one of the real operational problems"; it turns slow transactions and thin staffing into a consequence you can see, and closes the loop volume → congestion → pressure → staffing/speed → turnover (PT).
- **Rough phase:** after PS4 (needs staffing to have the "more servers" lever); a presentation-only lot (cars come and go with arrivals, no feedback) could ride PS2's arrival model.
- **Depends on:** PS2 arrival process (SPEC_SHIFT_DAY §4); PS4 staffing; World: parking-lot layout, number of spaces, the side-of-building spot (asks for Nolan: space count and layout, typical dwell time); vehicle assets ($0 budget); a simple car pathing system.

## 2. Character setup / start screen
- **What:** a start screen with character customisation, starting role, difficulty, and maybe a starting-experience choice (PT).
- **Why:** gives the run an identity and a clean place for difficulty (SPEC_SHIFT_DAY profiles already exist as data) and role (budtender now; lead/manager later).
- **Rough phase:** difficulty select can land with PS2 (the profiles exist); customisation needs the character pipeline (ASSET-004 / DEC-091 R4); role select only once a second playable role exists.
- **Depends on:** PS2 difficulty profiles; character body/wardrobe pipeline; staff uniform rule (DEC-089); first-person game means the body is mostly seen in mirrors/cutscenes — UX to decide where customisation shows.

## 3. Store condition over the day
- **What:** the store visibly degrades and changes over a shift: messier counters, emptier jars, accumulating bags/boxes, fuller trash, moved supplies, skipped cleaning; closing looks different from opening (PT).
- **Why:** sells the passage of a real shift and gives closing-lite tasks (SPEC_SHIFT_DAY §10) something to visibly fix; feeds the lived-in pass Nolan asked for (DEC-096).
- **Rough phase:** PS2 (jar depletion already exists via GAME-005/012; add a small "mess" state per zone driven by transactions and skipped tasks).
- **Depends on:** PS2 phases and closing-lite; prop state variants (DEC-091 R7 "state variants"); lived-in props (Assets); PERF budget for dynamic clutter.

## 4. Coworker personalities
- **What:** named coworkers with strengths, weaknesses and habits (fast but messy, great with customers but slow, vanishes into the back, loves deli, hates register, the rush-hour rock) that feed scheduling, breaks, call-outs, training, morale, promotions and delegation (PT).
- **Why:** makes staff people rather than NPC workers, gives management gameplay its decisions, and is a main source of the grounded humour (§8).
- **Rough phase:** PS4 staffing (first a few trait axes that change service speed/quality/mess), management layer later.
- **Depends on:** PS4 staffing model (V2 03 §5 warns single-server tuning must be redone); character pipeline; dialogue/bark system. No real employees are modelled (no PII).

## 5. TV / advertising wall
- **What:** the FOH TV wall cycles dispensary-style product ads, a new one every **5–10 s** (PT; [GDD] default 7 s, randomised within the range).
- **Why:** cheap, high-visibility life on the sales floor.
- **Rough phase:** any time after the TV wall is modelled (World); small task (render-texture slideshow).
- **Depends on:** World TV wall fixture and screen count; ad art that uses only approved/fictional brands (DEC-071/081, DEC-091 R5 label art) and passes copy rule H1 (no effect claims); ask for Nolan: what the real wall shows (ads only, menu boards, mixed).

## 6. Break room / downtime
- **What:** an occupied break room: coworkers eating, sitting, talking, leaving drinks and personal items, escaping a bad rush (PT). Mostly ambient.
- **Why:** makes coworkers and the building feel real; a natural home for PS4 breaks.
- **Rough phase:** ambient props with the lived-in pass (now-ish, World/Assets); ambient NPC use with PS2 ambient staff (SPEC_SHIFT_DAY §5); break gameplay with PS4.
- **Depends on:** break-room layout (lockers per DEC-047; REF work); ambient NPC animation; PS4 breaks.

## 7. Neighbourhood activity
- **What:** cars, delivery drivers, pedestrians, people waiting outside, traffic, nearby businesses, weather (PT).
- **Why:** the store should exist in a living world, not an isolated map (PT: "I hope the outside world becomes much more lively").
- **Rough phase:** ambient layer after the exterior/site plan exists (no site plan yet: graybox ground is a flat placeholder); grows with §1.
- **Depends on:** exterior/site reference (asks for Nolan: neighbouring businesses, street layout, how much of it is visible); vehicle/pedestrian assets; weather/time-of-day lighting (DEC-091 R6); PERF budget.

## 8. Grounded, deadpan humour (tone pillar)
- **What:** comedy that comes from the simulation and is played straight: awkward customers, bad parking, equipment failing at the worst time, odd requests, clutter, staffing trouble, situations escalating into the ridiculous but believable (PT). Never joke-a-minute, never corny.
- **Why:** a tone pillar to steer writing, events and coworker design consistently.
- **Rough phase:** adopt as a **pillar now** (a short tone note for all dialogue/event writers); content arrives with PS1b dialogue (GAME-017..020), PS2 events (SPEC_SHIFT_DAY §9) and §1/§4.
- **Depends on:** a Hub decision to record it as a pillar; copy review against copy rule H1 and the no-PII rule (no real customers or staff as material).
