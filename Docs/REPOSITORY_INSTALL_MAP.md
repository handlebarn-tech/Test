# REPOSITORY INSTALL MAP

> **Historical (AUDIT-001 C4, DEC-064):** describes the one-time install of the original handoff files; it is done. Current layout: `Docs/STUDIO_OS.md` §48 "As built" note.

The files in this handoff folder should be installed into a working repository approximately as follows:

```text
DispoGameRepo/
  AGENTS.md
  CLAUDE.md
  Docs/
    MASTER_PLAN.md
    UNITY_MIGRATION_PLAN.md
    ASSET_PRODUCTION_PLAN.md
    STUDIO_OS.md
    TOOLCHAIN_EXECUTION.md
    GAMEPLAY_SIMULATION_SPEC.md
    PROJECT_STATE.md
    MACHINE_PROFILE.md
    ...
  References/
    ...
```

Suggested mapping:

| Handoff file | Repository file |
|---|---|
| `Dispensary_Game_MASTER_PLAN.md` | `Docs/MASTER_PLAN.md` |
| `Dispensary_Game_UNITY_MIGRATION_PLAN.md` | `Docs/UNITY_MIGRATION_PLAN.md` |
| `Dispensary_Game_ASSET_PRODUCTION_PLAN.md` | `Docs/ASSET_PRODUCTION_PLAN.md` |
| `Dispensary_Game_STUDIO_OS.md` | `Docs/STUDIO_OS.md` |
| `Dispensary_Game_TOOLCHAIN_EXECUTION.md` | `Docs/TOOLCHAIN_EXECUTION.md` |
| `Dispensary_Game_GAMEPLAY_SIMULATION_SPEC.md` | `Docs/GAMEPLAY_SIMULATION_SPEC.md` |
| `PROJECT_STATE_TEMPLATE.md` | `Docs/PROJECT_STATE.md` |
| `MACHINE_PROFILE_TEMPLATE.md` | `Docs/MACHINE_PROFILE.md` |

The Hub should perform this organization once, then work from repository-native paths.
