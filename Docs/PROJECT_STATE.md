# PROJECT STATE

Hub-owned, project level only (`Docs/STUDIO_OS.md` §0). Department detail (workers, packets, domain queue) lives in `Docs/Departments/<DEPT>.md`. Workers do not need this file.

**Milestone:** vertical slice playable on `main` (2026-10-29). **PS1** (cart, limit meter, ID checks, medical, tuning; `Design/ROADMAP_POST_SLICE.md`) is one task from done (GAME-009). Next: PS1b, re-prioritised by playtest 1 (DEC-096).
**Main:** see `git log`; every code/asset merge is a reviewed `review/*` branch.
**Updated:** 2026-10-30 by Hub `local_c6267ff5-2acb-4b09-83a7-53541a088c66`: studio reorganised into departments (DEC-094); all old workcells idle, adopted by their leads.

## Studio roster
| Dept | Lead session | Status | Max workers | Unity slots |
|---|---|---|---|---|
| Hub | `local_c6267ff5-2acb-4b09-83a7-53541a088c66` | active | DOC/OPS/AUDIT tasks only | 0 |
| Gameplay | `local_5bcd6ccf-64c1-464e-9fb9-40ad2e27afb4` | active | 3 | 1 |
| World | `local_d19eda58-a105-4379-aada-4bf61066f717` | active | 2 | 1 (lends to Assets for imports) |
| Assets | `local_172b2109-6384-4914-800b-6dc37226e046` | active | 3 | 0 (borrows World's) |
| Reviewer pool | Unity A `local_0dd63bac-df1d-448d-9203-641ead6b6837`, Unity B2 `local_041172fa-72b8-4943-b69e-72fc7a83b9fd`, Docs `local_b073ffa0-2129-4b65-9193-95f27fcfc0f7` | idle | — | Unity reviewers use the owning dept's slot |

Unity editors studio-wide: 2 (DEC-013). Old workcells adopted: Gameplay ← GAME-009 `local_7f8c95e9…`, DES `local_82d327a2…`; Assets ← PROC-005 `local_6c216f80…`, ASSET-004 `local_d31ad4c5…`, IMP-003 `local_13653ae5…`. Leads may reuse or retire them.

## Priorities (DEC-096, from Nolan's playtest 1)
1. **Controls** (camera/look feel, Esc pause menu, doors): Gameplay (+ World for door geometry).
2. **Store/layout accuracy** (registers, HUB, office walkability, deli walls): World.
3. **Believable customer flow** (entry ID check with a guard, one line, player calls the next customer): Gameplay.
4. **Recommendation depth** (keep the TFS tool's depth; interpret needs, follow-up questions): Gameplay, PS1b.
5. Asset integration that unblocks the above (PROC-005, register workstation kit): Assets.

## Cross-department dependencies
- Assets PROC-005 → World final-asset placement and the lived-in pass.
- World `ROOM_FIXTURES` corrections → Assets generator sizes (registers, deli walls, office).
- World door geometry ↔ Gameplay door interaction: agree the contract first (§0.5).
- World entry/check-in area ↔ Gameplay customer flow (guard post, queue line anchors).

## Blockers / risks
- DEC-094 rollout under validation (DEC-099): Hub-only merges until lead-run subagent workers/worktrees prove stable; then reassess lead merges for domain-local work.
- ChatGPT toolkit drops lack our research and room evidence (DEC-095): every round needs fixes; round 3 must be re-audited.
- Several BACKLOG rows are stale; each lead reconciles its prefixes first.

## Pending from Nolan
- Approval of each audited ChatGPT round (3 rebuilt, 4, 5, 6) after IMP-003 + review. Round 7 is the studio's (DEC-095).
- Playtest of the next build after PS1 completes.
- Any ChatGPT-built mechanics he drops in Imports: audit → review → **his approval** before use.

## Open questions for Nolan
- None open. (REF-008 Q1–15 answered, DEC-051/062. Phoenix TPT rate OPEN-4: 25.1 % kept until a receipt settles it.)

## Builds
- Last build Nolan played: `Downloads/Dispo Game Builds/slice-38b9e5c/` (feedback = playtest 1). New builds come from a Gameplay worker, never the Hub (DEC-045).

## Cross-project
- GAP-206 relayed to the TFS tool hub. When TFS ships v7.11.5: re-import, regenerate goldens and diff (GAP-210, DEC-014/038).

## Hub-direct backlog
- DOC-002 (AUDIT-001 batch D) in a gap between waves; DOC-003 (batch E, in review W4Z); DOC-004 (GSS §28 "fast recommendation").
