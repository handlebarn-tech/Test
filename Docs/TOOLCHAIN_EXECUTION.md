# DISPENSARY GAME — TOOLCHAIN EXECUTION CONTRACT
## Headless Unity + Blender Automation, Build Health, Visual Evidence & Agent Execution Rules

**Version:** 1.0  
**Date:** 2026-10-29  
**Parent:** `MASTER_PLAN.md`  
**Primary consumers:** Studio Hub, BUILD, TECH-ART, ART-PROC, QA, PERF workers  
**Platform assumption for initial bootstrap:** Windows workstation unless machine discovery proves otherwise  
**Software-cost rule:** $0 required

---

# 1. Purpose

This document defines **how agents execute work on the machine**.

The project should not depend on an AI agent being good at manually clicking Unity or Blender.

The preferred production model is:

```text
agent
→ shell / PowerShell
→ deterministic script
→ Unity or Blender headless process
→ artifact/log/test result
→ machine-readable status
→ screenshot/render/build evidence
→ reviewer
```

GUI use is allowed for visual inspection or tasks that genuinely benefit from it, but automation should be the default for repeatable production.

---

# 2. Execution principles

1. **Scripts before clicks.**
2. **Every substantial operation produces evidence.**
3. **Non-zero exit code = failure unless explicitly documented otherwise.**
4. **Logs are files, not transient terminal history.**
5. **No worker edits the same Unity project/worktree concurrently with another Unity process.**
6. **Blender generation should be repeatable from source scripts where practical.**
7. **Generated assets do not become production assets until validated.**
8. **Build/test commands are wrappers committed to the repository.**
9. **The Hub consumes summaries, not raw multi-megabyte logs.**
10. **A worker must be able to reproduce its output from repository state plus declared external free assets.**

---

# 3. Official command-line capabilities used by this contract

Unity 6 command-line builds support:

- `-projectPath`
- `-batchmode`
- `-quit`
- `-logFile`
- `-buildTarget` or a build profile
- `-executeMethod` for custom static build/editor methods

Unity's Test Framework supports Edit Mode and Play Mode testing; command-line test execution uses the test-runner arguments installed with the package.

Blender supports:

- `--background`
- `--python <script>`
- `--python-expr`
- `--python-exit-code`
- `--render-frame`
- `--render-anim`
- `--` to pass remaining arguments to Python

Blender argument order matters: loading a `.blend` file can overwrite settings established earlier on the command line. Wrapper scripts should use a standardized order.

Official references:
- Unity command-line build documentation:  
  https://docs.unity3d.com/6000.0/Documentation/Manual/build-command-line.html
- Unity Editor command-line arguments:  
  https://docs.unity3d.com/6000.0/Documentation/Manual/EditorCommandLineArguments.html
- Unity Test Framework:  
  https://docs.unity3d.com/6000.0/Documentation/Manual/com.unity.test-framework.html
- Blender 4.5 LTS command line:  
  https://docs.blender.org/manual/en/4.5/advanced/command_line/
- Blender Python command-line workflow:  
  https://docs.blender.org/api/main/info_tips_and_tricks.html

---

# 4. First machine-bootstrap task: STUDIO-DOCTOR

Before production, BUILD-001 creates a machine profile.

Output:

`Docs/MACHINE_PROFILE.md`

It must record:

```text
OS
CPU
RAM
GPU
VRAM
display resolution
primary drive free space
Unity Hub path
Unity Editor path/version
Blender executable path/version
Git path/version
Python path/version
PowerShell version
available free disk space
project path
temporary/render path
build output path
```

Do not guess installation locations.

---

# 5. Windows software discovery

The bootstrap worker should search common locations, PATH and registry/Hub configuration.

Possible Unity location pattern:

```text
C:\Program Files\Unity\Hub\Editor\<VERSION>\Editor\Unity.exe
```

Possible Blender patterns:

```text
C:\Program Files\Blender Foundation\Blender <VERSION>\blender.exe
```

But these are examples, not assumptions.

Recommended PowerShell discovery concepts:

```powershell
Get-Command git -ErrorAction SilentlyContinue
Get-Command blender -ErrorAction SilentlyContinue
Get-ChildItem "C:\Program Files\Unity\Hub\Editor" -Directory -ErrorAction SilentlyContinue
Get-ChildItem "C:\Program Files\Blender Foundation" -Directory -ErrorAction SilentlyContinue
```

If multiple Unity 6000.3 installations exist, pin one exact version in machine/project configuration.

---

# 6. Repository execution configuration

Create:

```text
Tools/Studio/studio.config.json
```

Example schema:

```json
{
  "unityExecutable": "C:/Program Files/Unity/Hub/Editor/6000.3.xx/Editor/Unity.exe",
  "blenderExecutable": "C:/Program Files/Blender Foundation/Blender 4.5/blender.exe",
  "unityProject": "UnityProject",
  "logs": "Artifacts/Logs",
  "testResults": "Artifacts/TestResults",
  "screenshots": "Artifacts/Screenshots",
  "renders": "Artifacts/Renders",
  "builds": "Builds",
  "referenceImages": "References"
}
```

Machine-specific paths should be ignored by Git when appropriate.

Commit a template:

`Tools/Studio/studio.config.example.json`

---

# 7. Studio command surface

The studio should expose one predictable wrapper:

```text
Tools/Studio/studio.ps1
```

Target commands:

```text
studio.ps1 doctor
studio.ps1 unity-compile
studio.ps1 unity-test-edit
studio.ps1 unity-test-play
studio.ps1 unity-validate
studio.ps1 unity-capture
studio.ps1 unity-build
studio.ps1 blender-generate <asset-id>
studio.ps1 blender-validate <blend-or-asset-id>
studio.ps1 blender-render <asset-id>
studio.ps1 asset-import <asset-id>
studio.ps1 asset-review <asset-id>
studio.ps1 qa-smoke
studio.ps1 qa-full
studio.ps1 status
```

The exact interface may evolve, but one wrapper should remain stable so specialist prompts do not need to know low-level executable paths.

---

# 8. Standard process result contract

Each wrapper operation writes:

```text
Artifacts/Results/<timestamp>-<operation>.json
```

Recommended schema:

```json
{
  "operation": "unity-test-edit",
  "startedUtc": "...",
  "finishedUtc": "...",
  "status": "pass",
  "exitCode": 0,
  "commit": "...",
  "worktree": "...",
  "logs": ["Artifacts/Logs/..."],
  "outputs": ["Artifacts/TestResults/..."],
  "summary": {
    "tests": 143,
    "passed": 143,
    "failed": 0
  }
}
```

Valid status:

```text
pass
fail
blocked
partial
```

Workers and reviewers should reference this result file in their handoffs.

---

# 9. Unity concurrency rule

**Never run two Unity Editor processes against the same project directory.**

Parallel Unity work must use separate Git worktrees, each containing its own Unity project tree.

Safe:

```text
worktrees/
  GAME-014/
  ART-021/
  UI-008/
```

Unsafe:

```text
worker A opens UnityProject/
worker B simultaneously opens the same UnityProject/
```

Unity Library/import/cache state and serialized files make this unnecessarily risky.

Blender workers can run in greater parallelism when their files/outputs are isolated.

---

# 10. Unity compile validation

Create a custom editor entry point, for example:

```text
Game.Editor.CI.CompileCheck
```

The wrapper launches Unity with:

```powershell
& $Unity `
  -batchmode `
  -quit `
  -projectPath $Project `
  -logFile $Log `
  -executeMethod Game.Editor.CI.CompileCheck
```

The custom method should:

1. wait for compilation/import completion;
2. inspect compiler errors;
3. run project validators designated for compile gate;
4. write a result artifact;
5. exit failure on errors.

Do not infer compile success merely because the process opened.

---

# 11. Unity Edit Mode tests

Use the installed Unity Test Framework.

Wrapper requirements:

- explicit project path;
- batch mode;
- test platform Edit Mode;
- test-result XML path;
- log file;
- deterministic exit handling.

Expected artifacts:

```text
Artifacts/TestResults/editmode.xml
Artifacts/Logs/unity-editmode.log
Artifacts/Results/...unity-test-edit.json
```

Edit Mode should cover:

- domain recommendation logic;
- similarity;
- pricing;
- data validation;
- import logic;
- pure inventory logic;
- save serialization utilities.

---

# 12. Unity Play Mode tests

Play Mode covers:

- scene boot;
- customer transaction loop;
- navigation;
- inventory visual updates;
- UI bindings;
- jar fill;
- save/load integration;
- scene transitions;
- critical interaction prefabs.

Play Mode tests are slower and should not be the only feedback mechanism.

Worker default:

```text
Edit tests frequently
Play tests before handoff
```

---

# 13. Unity build automation

Create custom build entry points under:

```text
Assets/_Game/Editor/CI/
```

Recommended methods:

```text
BuildWindows64
BuildSmokeScene
CaptureReferenceViews
ValidateProject
```

Windows build wrapper concept:

```powershell
& $Unity `
  -batchmode `
  -quit `
  -projectPath $Project `
  -buildTarget StandaloneWindows64 `
  -executeMethod Game.Editor.CI.BuildWindows64 `
  -logFile $Log
```

The Hub should pin one exact Unity version after bootstrap.

A build is accepted only if:

- process succeeded;
- expected executable exists;
- build log contains no fatal errors;
- smoke launch passes;
- build manifest is generated.

---

# 14. Build manifest

Every milestone build writes:

`Builds/<version>/BUILD_MANIFEST.json`

Containing:

```text
version
git commit
Unity version
build date
target
master-plan version
migration-plan version
asset-plan version
known issues
test summary
```

Never hand around anonymous executables named `build2_final_new.exe`.

---

# 15. Unity smoke launch

After build:

1. launch executable with a QA mode/argument;
2. enter a deterministic smoke scene;
3. wait for a readiness marker;
4. capture log/screenshots;
5. exit cleanly.

Create a simple runtime heartbeat:

```text
Artifacts/Runtime/ready.json
```

or a log marker such as:

```text
STUDIO_SMOKE_READY
```

The QA wrapper times out if the marker does not appear.

---

# 16. Headless versus graphical Unity

Not every Unity operation should run fully invisible.

Use batch/headless-style automation for:

- compile;
- tests;
- imports;
- builds;
- validators;
- metadata generation.

Use graphical execution when required for:

- actual HDRP screenshot capture;
- visual walkthrough;
- GPU profiling;
- final lighting evaluation.

The automation still launches and controls the graphical process; the agent should not need to click manually.

---

# 17. Reference camera system

Create fixed QA cameras for important views.

Examples:

```text
REF_Retail_NorthEast
REF_Retail_Register
REF_Retail_Deli
REF_Office
REF_Hall
REF_BreakRoom
REF_FOH
REF_BOH
REF_HUB
REF_Exterior_01
...
```

Each has:

- stable ID;
- position;
- rotation;
- FOV;
- reference source ID;
- confidence level.

Do not casually move reference cameras once approved.

---

# 18. Automated Unity screenshot capture

Build an Editor/runtime capture tool:

```text
CaptureReferenceViews
```

Output:

```text
Artifacts/Screenshots/<commit>/
  REF_Retail_Register.png
  REF_Office.png
  REF_BOH.png
  ...
```

Each capture should record:

```text
camera ID
scene
resolution
commit
timestamp
lighting profile
```

Recommended review resolution:

- at least 1920×1080 for scene review;
- higher for hero comparison if practical.

---

# 19. Visual comparison pipeline

For each approved reference view:

```text
reference
current capture
difference image
review report
```

Do not use raw pixel difference as the only quality metric because:

- CCTV compression differs;
- lighting/exposure differs;
- reference FOV may be approximate;
- moving NPCs/stock vary.

Use automated image metrics only as **change detection/support**.

Final environment fidelity still requires visual review against:

- geometry;
- object presence;
- density;
- relative scale;
- material family;
- lighting intent.

---

# 20. Visual-review report

Each major environment task returns:

```text
Artifacts/VisualReview/<TASK_ID>/
  reference.png
  candidate.png
  overlay.png
  report.md
```

`report.md` records:

- camera;
- reference;
- matched elements;
- known mismatches;
- unresolved reference gaps;
- reviewer verdict.

No hero environment task should be accepted with only “looks good.”

---

# 21. Blender headless contract

Standard form:

```powershell
& $Blender `
  --background `
  --python-exit-code 10 `
  --python "Tools/Blender/<script>.py" `
  -- `
  <script arguments>
```

When operating on an existing `.blend`:

```powershell
& $Blender `
  "SourceAssets/Custom/Blender/<asset>.blend" `
  --background `
  --python-exit-code 10 `
  --python "Tools/Blender/validate_asset.py" `
  -- `
  --asset-id CA-FIX-001
```

The script must return non-zero on validation failure.

---

# 22. Blender generator contract

Each generator should be callable independently.

Example:

```text
Tools/Blender/generators/generate_register_run.py
```

Inputs:

```text
asset ID
spec file
output .blend
output export path
preview-render path
seed if procedural
```

Example conceptual invocation:

```powershell
studio.ps1 blender-generate CA-FIX-001
```

The wrapper:

1. loads asset spec;
2. executes generator;
3. saves `.blend`;
4. validates;
5. exports;
6. renders preview;
7. writes result JSON.

---

# 23. Blender asset specification is authoritative

Generators must use:

```text
Docs/Assets/Specs/<ASSET_ID>.md
```

or a machine-readable sidecar such as:

```text
Docs/Assets/Specs/<ASSET_ID>.json
```

Do not bury dimensions only inside Python source.

When better reference measurements arrive:

```text
update spec
→ regenerate
→ compare
→ reimport
```

---

# 24. Blender validation

`validate_asset.py` should inspect:

- unit scale;
- dimensions;
- applied transforms;
- object names;
- origin/pivot;
- non-manifold geometry where relevant;
- inverted normals;
- material count;
- UV presence;
- triangle count;
- hidden accidental export objects;
- missing external textures;
- collection/export membership;
- LOD naming.

Machine-readable output:

```text
Artifacts/AssetValidation/<ASSET_ID>.json
```

---

# 25. Blender preview renders

Every custom hero prop gets standardized previews.

Camera angles:

- front 3/4;
- rear 3/4;
- top/scale;
- optional close detail.

Render against a neutral scene with known scale markers.

Purpose:

- enable reviewer inspection without opening Blender;
- show generator output;
- catch shading/material problems early.

---

# 26. Blender → Unity conveyor

Canonical pipeline:

```text
Asset Spec
↓
Blender source/generator
↓
Blender validation
↓
Preview render
↓
FBX/glTF export
↓
Unity import
↓
HDRP material conversion/setup
↓
LOD/collider setup
↓
Prefab
↓
Unity asset validation
↓
Scene/reference screenshot
↓
Independent review
↓
Production-approved asset
```

A worker does not stop at “I created an FBX.”

---

# 27. Import staging

Third-party/custom assets enter:

```text
UnityProject/Assets/_Staging/
```

They move to production folders only after normalization.

Staging is allowed to be ugly.

Production folders are not.

---

# 28. Unity asset importer automation

TECH-ART should build import helpers that can:

- normalize material names;
- configure texture color space;
- assign HDRP Lit;
- set normal-map import;
- configure compression;
- create LODGroup;
- add simple colliders;
- create prefab;
- attach provenance metadata;
- validate scale.

Do not manually repeat the same import ritual hundreds of times.

---

# 29. Free-asset provenance gate

Before import, record:

```text
asset name
author
URL
license
download date
source filename
SHA-256
modifications
```

If provenance is unclear:

**reject the asset.**

The Asset Production Plan owns the catalog.

---

# 30. Log hierarchy

```text
Artifacts/
  Logs/
    Unity/
    Blender/
    Tools/
  Results/
  TestResults/
  Screenshots/
  Renders/
  VisualReview/
  AssetValidation/
  Performance/
  Runtime/
```

Ignore large/transient artifacts from Git as appropriate.

Keep small reports/metadata when useful.

---

# 31. Log summarization

Workers may inspect large logs.

Handoffs should contain only:

```text
status
main errors
warnings that matter
evidence paths
```

Do not paste 20,000-line Unity logs into the Hub context.

---

# 32. Unity Library directory

`UnityProject/Library/` is generated.

Do not commit it.

Do not share it between worktrees.

Each worktree's Unity project may regenerate its own Library state.

This costs disk/time but avoids cross-worker corruption.

---

# 33. Git rules for generated art

Commit:

- `.blend` source when reasonable;
- generator scripts;
- specs;
- exported production models if required by Unity project;
- textures;
- Unity `.meta` files;
- prefabs;
- materials.

Do not commit:

- temporary renders unless they are QA evidence worth preserving;
- caches;
- Blender autosaves;
- Unity Library;
- giant transient logs.

Use Git LFS only if the chosen repository host/storage model supports it and the Hub records that decision.

---

# 34. Worktree disk policy

Unity worktrees can become large because each can generate `Library/`.

Hub should limit concurrent Unity worktrees based on free disk.

`STUDIO-DOCTOR` reports free disk before spawning heavy parallel work.

If storage becomes tight:

- reduce parallel Unity editors;
- preserve code worktrees without opening Unity;
- clean retired worktree Libraries;
- never delete uncommitted source.

---

# 35. Machine performance target

The user’s actual PC becomes the primary performance target.

After `STUDIO-DOCTOR`, PERF-001 establishes:

```text
target resolution
target quality preset
target FPS
acceptable 1% low
VRAM ceiling
RAM ceiling
load-time target
```

Initial recommendation until measured:

```text
1920×1080
high/HDRP visual target
60 FPS desired
30 FPS hard failure threshold for normal gameplay
```

These are provisional.

Do not optimize around imaginary hardware.

---

# 36. Performance capture

For milestone scenes, record:

```text
average FPS
1% low or frame-time distribution
CPU frame time
GPU frame time
draw calls/batches
triangles
visible renderers
memory
VRAM where accessible
NPC count
active CCTV feeds
```

Save:

`Artifacts/Performance/<commit>.md`

---

# 37. Screenshot/render evidence is mandatory for art

Required at handoff:

### Environment
- affected reference camera(s).

### Hero prop
- Blender preview;
- Unity in-context screenshot.

### Material
- neutral sphere/plane;
- in-context use.

### Lighting
- before/after reference cameras;
- exposure profile.

No screenshots = not reviewable.

---

# 38. Runtime screenshot determinism

For comparison captures:

- fixed resolution;
- fixed quality;
- fixed time-of-day;
- deterministic random seed;
- disable transient NPCs when comparing architecture;
- fixed camera;
- fixed exposure where possible.

Separate:

**Architecture comparison mode**  
from  
**Live gameplay beauty capture.**

---

# 39. Automation safety

Agents must never:

- recursively delete directories without explicit scoped path checks;
- run cleanup against user Downloads generally;
- overwrite reference originals;
- modify free-source downloads in-place without keeping provenance/source;
- reset Git hard against uncommitted work unless task explicitly authorizes it;
- kill unrelated processes.

Wrappers should operate only inside project-defined paths.

---

# 40. Reference originals are immutable

`References/Original/` or supplied reference files are read-only source evidence.

Derived files belong in:

```text
References/Derived/
Artifacts/VisualReview/
```

Never “improve” the CCTV image and then overwrite the original.

---

# 41. CI without external paid services

A full local CI loop is sufficient:

```text
studio.ps1 qa-full
```

Target sequence:

```text
doctor sanity
→ Unity compile
→ Edit Mode tests
→ project validators
→ Play Mode critical tests
→ build
→ smoke launch
→ deterministic screenshots
→ result summary
```

This can be run by the Hub before milestone acceptance.

No paid cloud CI is required.

---

# 42. Fast worker loop

For ordinary C# task:

```text
edit
→ unity-compile
→ relevant Edit Mode tests
→ handoff when local scope passes
```

For gameplay integration:

```text
edit
→ compile
→ Edit tests
→ Play test
→ screenshot if visible
→ handoff
```

For Blender prop:

```text
spec
→ generate/model
→ validate
→ preview render
→ export
→ Unity import
→ context screenshot
→ handoff
```

---

# 43. Full milestone loop

Before the Hub declares a milestone done:

```text
merge reviewed tasks
→ clean checkout/worktree
→ qa-full
→ Windows build
→ smoke launch
→ visual reference captures
→ performance capture
→ QA walkthrough
→ known-gap reconciliation
→ tag known-good commit
```

---

# 44. Known-good tags

Recommended pattern:

```text
milestone/M0-doc-baseline
milestone/M1-unity-foundation
milestone/M2-graybox
milestone/M3-domain-engine
milestone/M4-vertical-slice
...
```

A known-good tag lets the Hub recover if later autonomous work destabilizes the project.

---

# 45. Failure classification

Wrappers should classify:

```text
CONFIGURATION
COMPILE
TEST
IMPORT
BUILD
RUNTIME
VISUAL
PERFORMANCE
LICENSE/PROVENANCE
REFERENCE_BLOCKED
```

This helps the Hub dispatch the right specialist rather than handing every failure to the same agent.

---

# 46. Toolchain-blocker behavior

If Unity fails because:

- executable missing;
- license/session unavailable;
- package install incomplete;
- GPU mode unsupported;

the worker:

1. records exact failure;
2. does not repeatedly retry blindly;
3. creates a BUILD blocker;
4. continues only work not requiring Unity if possible.

Likewise for Blender.

---

# 47. GUI fallback rule

A worker may use GUI interaction when:

- headless API cannot expose a required feature;
- visual inspection is the actual task;
- a one-time project setup requires it.

After successful GUI action, determine whether it should become scripted for future repetition.

One-time manual setup should not silently become a recurring dependency.

---

# 48. First toolchain task breakdown

> **Historical plan IDs (AUDIT-001 C2, DEC-059/064):** the IDs below are the original work breakdown. Live task IDs are in `Docs/BACKLOG.md` and several reuse these numbers for different work (e.g. live DATA-002 = Dutchie catalog importer, GAME-006 = cart, QA-002 = Gate A parity gate). Do not cite these headings as task IDs.

### BUILD-001 — STUDIO-DOCTOR
Discover software/hardware/paths.

### BUILD-002 — Studio PowerShell wrapper
Create `studio.ps1` and result contract.

### BUILD-003 — Unity CI methods
Compile, validate, build.

### QA-001 — Test-runner wrappers
Edit/Play tests + XML parsing.

### QA-002 — Screenshot harness
Reference cameras and captures.

### ART-PROC-001 — Blender wrapper
Background Python + validation + preview.

### TECH-ART-001 — Asset import pipeline
Staging → normalized prefab.

### PERF-001 — Machine performance baseline
Set actual FPS/resolution/memory targets.

---

# 49. Acceptance criteria for this execution layer

The toolchain is production-ready when a fresh agent can, without GUI clicking:

- identify Unity and Blender;
- run Unity compile validation;
- run Edit Mode tests;
- run critical Play Mode tests;
- build a Windows executable;
- launch a smoke test;
- capture a deterministic Unity screenshot;
- run a Blender Python asset generator;
- validate the generated `.blend`;
- export an asset;
- import/validate it in Unity;
- generate an evidence/result JSON;
- tell the Hub pass/fail with paths.

---

# 50. Final execution rule

> If an agent cannot prove what it did from files, logs, tests, builds, renders or screenshots, the studio should treat the work as unverified.

The goal is not merely to let AI use Unity and Blender.

The goal is to make Unity and Blender **reliable, scriptable production workers inside an auditable studio pipeline**.
