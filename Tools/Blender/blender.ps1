<#
.SYNOPSIS  Run a PROC-001 procedural generator in headless Blender (DEC-007).
.EXAMPLE   Tools/Blender/blender.ps1 deli_jar Tools/Blender/params/deli_jar.json
.EXAMPLE   Tools/Blender/blender.ps1 contact_sheet
Exits non-zero if Blender, the generator, or validation fails. Override the exe with $env:BLENDER_EXE.
#>
param(
    [Parameter(Mandatory)][string]$Generator,
    [string]$Params
)
$ErrorActionPreference = 'Stop'
$blender = if ($env:BLENDER_EXE) { $env:BLENDER_EXE } else { 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' }
if (-not (Test-Path $blender)) { Write-Error "Blender not found: $blender (set BLENDER_EXE)"; exit 2 }
$script = Join-Path $PSScriptRoot 'run_generator.py'
$genArgs = if ($Generator -eq 'contact_sheet') { @($Generator) } else {
    if (-not $Params -or -not (Test-Path $Params)) { Write-Error "params file required: $Params"; exit 2 }
    @($Generator, (Resolve-Path $Params).Path)
}
& $blender --background --factory-startup --python-exit-code 10 --python $script -- $genArgs
if ($LASTEXITCODE -ne 0) { Write-Error "Blender exited $LASTEXITCODE ($Generator)"; exit $LASTEXITCODE }
