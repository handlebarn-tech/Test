<#
.SYNOPSIS
  Dispo Game studio wrapper (Windows PowerShell 5.1). One stable entry point for agents.
.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File Tools/Studio/studio.ps1 unity-compile
.NOTES
  Every command writes a log under <config.logs> and a JSON result
  {command, ok, exitCode, durationSec, log, summary} to Artifacts/Results/<stamp>-<command>.json.
  Exit code: 0 ok, 1 failed, 2 blocked (e.g. Unity already has the project open).
#>
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet('doctor', 'unity-compile', 'unity-test-edit', 'unity-build', 'status')]
    [string]$Command,
    [int]$SmokeSeconds = 90
)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$ConfigPath = Join-Path $PSScriptRoot 'studio.config.json'
if (-not (Test-Path $ConfigPath)) {
    throw "Missing $ConfigPath. Copy studio.config.example.json to studio.config.json and fix the paths."
}
$Cfg = Get-Content $ConfigPath -Raw | ConvertFrom-Json

function Resolve-RepoPath([string]$p) { if ([IO.Path]::IsPathRooted($p)) { $p } else { Join-Path $Root $p } }
function Get-RelPath([string]$p) { if ($p -and $p.StartsWith($Root)) { $p.Substring($Root.Length + 1) -replace '\\', '/' } else { $p } }

$Unity      = $Cfg.unityExecutable
$Project    = Resolve-RepoPath $Cfg.unityProject
$LogDir     = Resolve-RepoPath $Cfg.logs
$TestDir    = Resolve-RepoPath $Cfg.testResults
$BuildDir   = Resolve-RepoPath $Cfg.builds
$ResultDir  = Join-Path $Root 'Artifacts\Results'
foreach ($d in @($LogDir, $TestDir, $BuildDir, $ResultDir)) { New-Item -ItemType Directory -Force $d | Out-Null }

$Stamp   = Get-Date -Format 'yyyyMMdd-HHmmss'
$Log     = Join-Path $LogDir "$Stamp-$Command.log"
$Started = Get-Date

function Write-Line([string]$text) {
    Write-Host $text
    Add-Content -Path $Log -Value $text -Encoding UTF8
}

function Test-ProjectLocked {
    # Unity holds Temp/UnityLockfile open exclusively while an editor has the project open.
    $lock = Join-Path $Project 'Temp\UnityLockfile'
    if (-not (Test-Path $lock)) { return $false }
    try { $fs = [IO.File]::Open($lock, 'Open', 'ReadWrite', 'None'); $fs.Close(); return $false } catch { return $true }
}

function Invoke-Unity([string[]]$UnityArgs, [string]$UnityLog) {
    $all = @('-batchmode', '-nographics', '-projectPath', $Project, '-logFile', $UnityLog) + $UnityArgs
    $argLine = ($all | ForEach-Object { if ($_ -match '\s') { '"' + $_ + '"' } else { $_ } }) -join ' '
    $p = Start-Process -FilePath $Unity -ArgumentList $argLine -Wait -PassThru -NoNewWindow
    return $p.ExitCode
}

function Get-CsErrorCount([string]$path) {
    if (-not (Test-Path $path)) { return -1 }
    return @(Select-String -Path $path -Pattern 'error CS\d+' | Select-Object -ExpandProperty Line -Unique).Count
}

function Complete([bool]$ok, [int]$exitCode, [string]$summary, [int]$scriptExit = -1) {
    $result = [ordered]@{
        command     = $Command
        ok          = $ok
        exitCode    = $exitCode
        durationSec = [math]::Round(((Get-Date) - $Started).TotalSeconds, 1)
        log         = Get-RelPath $Log
        summary     = $summary
    }
    $json = $result | ConvertTo-Json
    $resultPath = Join-Path $ResultDir "$Stamp-$Command.json"
    [IO.File]::WriteAllText($resultPath, $json)  # UTF-8 without BOM
    Write-Host $json
    Write-Host "result: $(Get-RelPath $resultPath)"
    if ($scriptExit -lt 0) { $scriptExit = $(if ($ok) { 0 } else { 1 }) }
    exit $scriptExit
}

function Assert-UnityReady {
    if (-not (Test-Path $Unity)) { Complete $false -1 "Unity executable not found: $Unity" }
    if (-not (Test-Path (Join-Path $Project 'ProjectSettings'))) { Complete $false -1 "Unity project not found: $Project" }
    if (Test-ProjectLocked) { Complete $false -1 'blocked: another Unity instance has the project open' 2 }
}

switch ($Command) {
    'doctor' {
        $checks = [ordered]@{}
        $checks['config'] = $ConfigPath
        $checks['unityExecutable'] = Test-Path $Unity
        $checks['unityProject'] = Test-Path (Join-Path $Project 'ProjectSettings\ProjectVersion.txt')
        if ($checks['unityProject']) {
            $projVer = ((Get-Content (Join-Path $Project 'ProjectSettings\ProjectVersion.txt'))[0] -split ':\s*')[1]
            $checks['unityVersionMatch'] = $Unity -like "*\$projVer\*" -or $Unity -like "*/$projVer/*"
        }
        $checks['git'] = [bool](Get-Command git -ErrorAction SilentlyContinue)
        $drive = Get-PSDrive -Name ($Root.Substring(0, 1))
        $checks['freeDiskGB'] = [math]::Round($drive.Free / 1GB, 1)
        $checks['projectUnlocked'] = -not (Test-ProjectLocked)
        $checks.GetEnumerator() | ForEach-Object { Write-Line ("{0,-18} {1}" -f $_.Key, $_.Value) }
        $failed = @($checks.GetEnumerator() | Where-Object { $_.Value -is [bool] -and -not $_.Value } | ForEach-Object { $_.Key })
        if ($checks['freeDiskGB'] -lt 20) { $failed += 'freeDiskGB<20' }
        Complete ($failed.Count -eq 0) 0 $(if ($failed.Count) { "failed: $($failed -join ', ')" } else { 'all checks passed' })
    }

    'status' {
        Push-Location $Root
        try {
            Write-Line "branch: $(git rev-parse --abbrev-ref HEAD 2>$null)"
            Write-Line "commit: $(git rev-parse --short HEAD 2>$null)"
            Write-Line "dirty:  $(@(git status --porcelain 2>$null).Count) paths"
        } finally { Pop-Location }
        Write-Line 'latest results:'
        Get-ChildItem $ResultDir -Filter '*.json' | Sort-Object Name |
            Group-Object { ($_.BaseName -split '-', 3)[2] } | ForEach-Object {
                $r = Get-Content ($_.Group | Select-Object -Last 1).FullName -Raw | ConvertFrom-Json
                Write-Line ("  {0,-16} ok={1,-5} {2}s  {3}" -f $r.command, $r.ok, $r.durationSec, $r.summary)
            }
        Complete $true 0 'status printed'
    }

    'unity-compile' {
        Assert-UnityReady
        $code = Invoke-Unity @('-quit', '-executeMethod', 'Dispo.Editor.CI.StudioCI.CompileCheck') $Log
        $errors = Get-CsErrorCount $Log
        $ci = Select-String -Path $Log -Pattern '\[StudioCI\] CompileCheck (OK|FAILED.*)' | Select-Object -Last 1
        $ok = ($code -eq 0) -and ($errors -eq 0) -and ($null -ne $ci) -and ($ci.Line -match 'OK')
        Complete $ok $code "csErrors=$errors; $(if ($ci) { $ci.Line.Trim() } else { 'CompileCheck did not run' })"
    }

    'unity-test-edit' {
        Assert-UnityReady
        $xml = Join-Path $TestDir "$Stamp-editmode.xml"
        # -runTests quits on its own; -quit would skip the run.
        $code = Invoke-Unity @('-runTests', '-testPlatform', 'EditMode', '-testResults', $xml) $Log
        if (-not (Test-Path $xml)) { Complete $false $code "no test results written (csErrors=$(Get-CsErrorCount $Log))" }
        $run = ([xml](Get-Content $xml -Raw)).'test-run'
        $ok = ($code -eq 0) -and ([int]$run.failed -eq 0) -and ([int]$run.total -gt 0)
        Complete $ok $code "total=$($run.total) passed=$($run.passed) failed=$($run.failed) skipped=$($run.skipped) xml=$(Get-RelPath $xml)"
    }

    'unity-build' {
        Assert-UnityReady
        $exe = Join-Path $BuildDir 'Windows64-Dev\DispoGame.exe'
        if (Test-Path (Split-Path $exe)) { Remove-Item (Split-Path $exe) -Recurse -Force }
        $code = Invoke-Unity @('-quit', '-buildTarget', 'StandaloneWindows64', '-executeMethod', 'Dispo.Editor.CI.StudioCI.BuildWindows64', '-buildPath', $exe) $Log
        $errors = Get-CsErrorCount $Log
        if ($code -ne 0 -or -not (Test-Path $exe)) { Complete $false $code "build failed (csErrors=$errors, exe exists=$(Test-Path $exe))" }

        # Smoke launch: windowed run until the Bootstrap ready marker appears, then kill.
        $playerLog = Join-Path $LogDir "$Stamp-player-smoke.log"
        $p = Start-Process -FilePath $exe -ArgumentList "-screen-fullscreen 0 -screen-width 1280 -screen-height 720 -logFile `"$playerLog`"" -PassThru
        $deadline = (Get-Date).AddSeconds($SmokeSeconds)
        $ready = $false
        while ((Get-Date) -lt $deadline -and -not $p.HasExited) {
            Start-Sleep -Seconds 1
            if ((Test-Path $playerLog) -and (Select-String -Path $playerLog -Pattern 'STUDIO_SMOKE_READY' -Quiet)) { $ready = $true; break }
        }
        Start-Sleep -Seconds 3  # let a few frames render after ready
        $exitedEarly = $p.HasExited
        if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force }
        $crash = (Test-Path $playerLog) -and (Select-String -Path $playerLog -Pattern 'Crash!!!|Unhandled exception|NullReferenceException' -Quiet)
        $marker = if ($ready) { (Select-String -Path $playerLog -Pattern 'STUDIO_SMOKE_READY.*' | Select-Object -First 1).Matches[0].Value } else { 'no ready marker' }
        $ok = $ready -and -not $exitedEarly -and -not $crash
        Complete $ok $code "exe=$(Get-RelPath $exe); smoke: $marker, exitedEarly=$exitedEarly, crash=$crash, playerLog=$(Get-RelPath $playerLog)"
    }
}
