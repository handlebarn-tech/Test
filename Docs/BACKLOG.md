# BACKLOG

Priority P0 = vertical-slice critical path. State: Ready / Active / Review / Done / Blocked.

| ID | P | Title | Depends on | State |
|---|---|---|---|---|
| REF-001 | P0 | Canonical reference index | — | Review (branch review/wave-1) |
| MIG-001 | P0 | Budtender reconstruction contract + triage | — | Review (branch review/wave-1) |
| BUILD-001 | P0 | Unity HDRP project, scenes, studio.ps1 | — | Review (branch review/wave-1) |
| REVIEW-W1 | P0 | Independent review of wave 1 | wave 1 | Ready |
| ART-001 | P0 | Measured graybox + QA-001 capture/PlayMode harness + test player | REVIEW-W1 | Ready |
| GAME-001 | P0 | DATA-001 importer + C# domain engine slice + golden tests | REVIEW-W1 | Ready |
| GAME-002 | P0 | Vertical-slice shift loop: customer intent → recommend UI → sale → inventory/visual change | ART-001, GAME-001 | Later (packet not written) |
| GAME-003 | P1 | Full NL parser port (all RC goldens), exclusions, compare, Similar | GAME-001 | Later |
| PERF-001 | P2 | Machine performance baseline in graybox | ART-001 | Later |
| PROC-001 | P2 | Blender headless wrapper + first generator (deli jar / package base) | ART-001 | Later |
| BUILD-002 | P2 | Build manifest (TOOLCHAIN §14) + fuller result schema (§8) | BUILD-001 | Later |
