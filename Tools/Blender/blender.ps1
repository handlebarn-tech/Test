<#
.SYNOPSIS  Run a PROC-001 procedural generator in headless Blender (DEC-007).
.EXAMPLE   Tools/Blender/blender.ps1 deli_jar Tools/Blender/params/deli_jar.json
.EXAMPLE   Tools/Blender/blender.ps1 contact_sheet
.EXAMPLE   Tools/Blender/blender.ps1 textures   # PROC-005 PBR finish maps (proctex.py)
.EXAMPLE   Tools/Blender/blender.ps1 contact_sheet jar_fill   # that generator's own grouped sheet
.EXAMPLE   Tools/Blender/blender.ps1 character Tools/Blender/params/customers_mpfb.json C001,C002   # MPFB2 customers (ASSET-004)
Exits non-zero if Blender, the generator, or validation fails. Override the exe with $env:BLENDER_EXE.
#>
param(
    [Parameter(Mandatory)][string]$Generator,
    [string]$Params,
    [string]$Ids
)
$ErrorActionPreference = 'Stop'
$blender = if ($env:BLENDER_EXE) { $env:BLENDER_EXE } else { 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' }
if (-not (Test-Path $blender)) { Write-Error "Blender not found: $blender (set BLENDER_EXE)"; exit 2 }
if ($Generator -eq 'character') {
    # MPFB2 lives in an isolated Blender profile in the asset cache (not the user's Blender); no --factory-startup, so it loads.
    $env:BLENDER_USER_RESOURCES = 'C:/Users/handl/Downloads/Dispo Game Assets Cache/mpfb/blender_user'
    if (-not $Params -or -not (Test-Path $Params)) { Write-Error "params file required: $Params"; exit 2 }
    $charArgs = @((Resolve-Path $Params).Path) + @($Ids | Where-Object { $_ })
    & $blender --background --python-exit-code 10 --python (Join-Path $PSScriptRoot 'characters/customer_gen.py') -- $charArgs
    if ($LASTEXITCODE -ne 0) { Write-Error "Blender exited $LASTEXITCODE (character)"; exit $LASTEXITCODE }
    exit 0
}
$script = Join-Path $PSScriptRoot 'run_generator.py'
$genArgs = if ($Generator -eq 'textures') { @($Generator) } elseif ($Generator -eq 'contact_sheet') { @($Generator) + @($Params | Where-Object { $_ }) } else {
    if (-not $Params -or -not (Test-Path $Params)) { Write-Error "params file required: $Params"; exit 2 }
    @($Generator, (Resolve-Path $Params).Path)
}
& $blender --background --factory-startup --python-exit-code 10 --python $script -- $genArgs
if ($LASTEXITCODE -ne 0) { Write-Error "Blender exited $LASTEXITCODE ($Generator)"; exit $LASTEXITCODE }
