# BACKLOG

Priority P0 = vertical-slice critical path. State: Ready / Active / Review / Done / Blocked.

| ID | P | Title | Depends on | State |
|---|---|---|---|---|
| REF-001 | P0 | Canonical reference index | — | Done |
| MIG-001 | P0 | Budtender reconstruction contract + triage | — | Done |
| BUILD-001 | P0 | Unity HDRP project, scenes, studio.ps1 | — | Done |
| REVIEW-W1 | P0 | Independent review of wave 1 | wave 1 | Done (GO with notes) |
| ART-001 | P0 | Measured graybox + QA-001 capture/PlayMode harness + test player | wave 1 (DEC-012) | Done |
| GAME-001 | P0 | DATA-001 importer + C# domain engine slice + golden tests | wave 1 (DEC-012) | Done |
| DES-001 | P0 | Vertical-slice design spec + GAME-002 draft packet | wave 1 | Done |
| UX-001 | P1 | Slice UX spec + wireframes (terminal, HUD, dialogue) | wave 1 | Done |
| ASSET-001 | P1 | $0 asset license ledger + acquisition list | — | Done |
| GAME-002 | P0 | Vertical-slice shift loop: customer intent → recommend UI → sale → inventory/visual change | ART-001, GAME-001, DES-001, UX-001 | Active |
| GAME-003 | P1 | Full NL parser port (all RC goldens), exclusions, compare, Similar | GAME-001 | Active |
| PERF-001 | P2 | Machine performance baseline in graybox | ART-001 | Later |
| PROC-001 | P1 | Blender headless wrapper + first generators (deli jar / package base) | — | Done |
| REVIEW-W2A | P0 | Review GAME-001 + PROC-001 | GAME-001, PROC-001 | Done (GO with notes) |
| REVIEW-W2B | P0 | Review DES-001 + UX-001 + ASSET-001 | DES/UX reconcile | Done (GO with notes) |
| REVIEW-W2C | P0 | Review ART-001 + commit HDRP-normalized ProjectSettings | ART-001 | Done (GO with notes) |
| ASSET-002 | P1 | Fetch P0 assets into shared cache (DEC-023) + LFS setup | ASSET-001 | Active |
| REF-002 | P0 | HUB CCTV evidence + register scale stand (DEC-019..022) | — | Done |
| REVIEW-W2D | P0 | Review REF-002 | REF-002 | Done (GO with notes) |
| REF-003 | P0 | Index back-of-register CCTV stills (scale stand) | — | Active |
| ART-002 | P1 | Graybox update: HUB rooms + register scale stands from REF-002 | REF-002, ART-001 merge | Active |
| BUILD-002 | P2 | Build manifest (TOOLCHAIN §14) + fuller result schema (§8) | BUILD-001 | Active |
