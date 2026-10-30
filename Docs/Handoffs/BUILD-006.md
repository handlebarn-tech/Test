# Handoff: BUILD-006 playtest build (DEC-085)

**Status:** done. Branch `claude/task-build-006` (off main 38b9e5c). Only this handoff is committed; the build itself lives outside the repo.

## Build
- **Exe:** `C:/Users/handl/Downloads/Dispo Game Builds/slice-38b9e5c/DispoGame.exe`, 228 MB. It sits beside the earlier `slice-c867cd5`, which is unchanged.
- **Built with:** `studio.ps1 unity-build` (DEC-013 gate), Unity 6000.6.7f1, Windows64 dev build, from commit 38b9e5c. Details are in `BUILD_MANIFEST.json` next to the exe.
- **Smoke tests:**
  - The build smoke run passed: `STUDIO_SMOKE_READY scenes=11`, no crash, did not exit early.
  - I also launched the copied exe on its own. It logged `[Slice] shift ready: 16 customers, 77 jars, seed 1` with no crash, and I killed the process. No player process is left running.
- During the build, Unity re-serialised `HDRenderPipelineGlobalSettings.asset` (runtime settings list). I reverted it; it is an editor side effect, not part of this task.

## New since slice-c867cd5
- **Cart:** you can build a multi-item order before ringing it up.
- **Limit meter:** a 1 oz limit meter with trims and strikes for going over.
- **ID checks at the door:** customers wait at the ID stand; you admit or refuse them.
- **Deli jars:** real deli jars with coloured bud fill (procedural jar fill).
- **Back rooms:** the back-room scenes are now in the build.
- **Tuning (GAME-010):** a 16-customer shift lasting about 25–40 minutes.
- **Brands:** only the approved brands appear (BRAND-001b).

## Controls
| Action | Key |
|---|---|
| Move | WASD |
| Run | Shift |
| Look | hold right mouse |
| Interact (ID stand, or talk to the customer at the counter) | E |
| At the ID check: admit / refuse | A / R |
| Cover prompt: yes / no | Y / N |
| From query or results, go to the register | R |
| More results | M |
| Back | Esc |
| Debug overlay | F3 |

## 10-minute playtest script for Nolan
1. **Minutes 0–1:** launch the exe and walk the floor and back rooms. *Look for:* anything about the layout, scale or jars that feels wrong compared with the real store.
2. **Minutes 1–3:** go to the ID stand and press E to check a few customers; refuse one. *Look for:* whether the ID check feels like the real door flow, and whether it's clear who is valid.
3. **Minutes 3–6:** serve 2–3 customers at the register. Press E to talk, use the query and results to recommend, add items to the cart, then ring it up. *Look for:* whether the recommendations match what you'd suggest, whether the cart flow is clear, and whether the prices are right.
4. **Minutes 6–8:** take one order over the limit on purpose. *Look for:* whether the meter, trim and strike behaviour matches how the real 1 oz limit is handled.
5. **Minutes 8–10:** keep serving into the rush. *Look for:* pacing (too fast or too slow for a 25–40 min shift) and whether customer patience feels fair.
6. **Afterwards:** list the three biggest "that's not how it works" moments and anything that broke. Press F3 for debug info if something looks off.

## Known gaps
- **No medical customers yet:** the shift is recreational only.
- **No audio.**
- **Placeholder customers:** stand-in NPC models and animation.
- The check-in desk uses a temporary fallback anchor (log: "TEMP fallback anchors (ART-002 pending)").
- Assets are pre-DEC-084: many props are graybox or lookdev placeholders, not the final high-quality set.
- The other registers have no ambient coworkers yet (GAP-DAY-03 / GAME-011).

## Validation
`unity-build` exit 0. The result is in `Artifacts/Results/20261030-040650-232-41476-unity-build.json`, and both launches of the copied exe passed.
