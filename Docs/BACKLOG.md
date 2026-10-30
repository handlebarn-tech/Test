# BACKLOG

Priority P0 = vertical-slice critical path. State: Ready / Active / Review / Done / Blocked.

| ID | P | Title | Depends on | State |
|---|---|---|---|---|
| REF-001 | P0 | Canonical reference index | — | Review (branch review/wave-1) |
| MIG-001 | P0 | Budtender reconstruction contract + triage | — | Review (branch review/wave-1) |
| BUILD-001 | P0 | Unity HDRP project, scenes, studio.ps1 | — | Review (branch review/wave-1) |
| REVIEW-W1 | P0 | Independent review of wave 1 | wave 1 | Active |
| ART-001 | P0 | Measured graybox + QA-001 capture/PlayMode harness + test player | wave 1 (DEC-012) | Active |
| GAME-001 | P0 | DATA-001 importer + C# domain engine slice + golden tests | wave 1 (DEC-012) | Active |
| DES-001 | P0 | Vertical-slice design spec + GAME-002 draft packet | wave 1 | Active |
| UX-001 | P1 | Slice UX spec + wireframes (terminal, HUD, dialogue) | wave 1 | Active |
| ASSET-001 | P1 | $0 asset license ledger + acquisition list | — | Active |
| GAME-002 | P0 | Vertical-slice shift loop: customer intent → recommend UI → sale → inventory/visual change | ART-001, GAME-001, DES-001, UX-001 | Later (draft by DES-001) |
| GAME-003 | P1 | Full NL parser port (all RC goldens), exclusions, compare, Similar | GAME-001 | Later |
| PERF-001 | P2 | Machine performance baseline in graybox | ART-001 | Later |
| PROC-001 | P1 | Blender headless wrapper + first generators (deli jar / package base) | — | Active |
| BUILD-002 | P2 | Build manifest (TOOLCHAIN §14) + fuller result schema (§8) | BUILD-001 | Later |
