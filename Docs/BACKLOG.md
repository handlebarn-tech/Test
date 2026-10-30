# BACKLOG

Priority P0 = vertical-slice critical path. State: Ready / Active / Review / Done / Blocked.

| ID | P | Title | Depends on | State |
|---|---|---|---|---|
| REF-001 | P0 | Canonical reference index (floor plan, CCTV, BAND photos, live site) | — | Active |
| MIG-001 | P0 | Budtender reconstruction contract + PRESERVE/FIX/TRANSFORM/DEFER/DROP triage | — | Active |
| BUILD-001 | P0 | Unity 6000.6 HDRP project, scene skeleton, studio.ps1 doctor/compile/test/build, test asmdef | — | Active |
| ART-001 | P0 | Measured graybox of retail + BOH from floor plan (scripted) | REF-001, BUILD-001 | Waiting on deps |
| DATA-001 | P0 | Deterministic importer: tool inventory master + terpene DB → PII-free game data | MIG-001, BUILD-001 | Waiting on deps |
| GAME-001 | P0 | Pure C# domain engine: batches, intent → domains, scoring, similarity, pricing, golden tests | MIG-001, BUILD-001, DATA-001 | Waiting on deps |
| GAME-002 | P0 | Vertical-slice shift loop: customer intent → recommend UI → sale → inventory change | GAME-001, ART-001 | Later |
| QA-001 | P1 | Test runner wrappers + result summary JSON | BUILD-001 | Waiting on deps |
| PLAYER-001 | P1 | First-person controller + interaction at correct scale in graybox | ART-001 | Later |
| PERF-001 | P2 | Machine performance baseline in graybox | ART-001 | Later |
| PROC-001 | P2 | Blender headless wrapper + first generator (deli jar / package base) | BUILD-001 | Later |
