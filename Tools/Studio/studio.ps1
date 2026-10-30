<#
.SYNOPSIS
  Dispo Game studio wrapper (Windows PowerShell 5.1). One stable entry point for agents.
.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File Tools/Studio/studio.ps1 unity-compile
.NOTES
  Every command writes a log under <config.logs> and a JSON result to Artifacts/Results/<stamp>-<command>.json:
  {command, ok, exitCode, durationSec, log, summary} plus the TOOLCHAIN §8 fields
  {operation, status, startedUtc, finishedUtc, commit, worktree, logs, outputs}.
  Exit code: 0 ok, 1 failed, 2 blocked (Unity already has the project open, DEC-013 slot wait timed out, tool missing).
.EXAMPLE
  studio.ps1 blender deli_jar Tools/Blender/params/deli_jar.json   # forwards to Tools/Blender/blender.ps1
.EXAMPLE
  studio.ps1 assets-fetch --verify                                  # forwards to Tools/Assets/fetch_assets.py
#>
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet('doctor', 'unity-compile', 'unity-test-edit', 'unity-test-play', 'unity-graybox', 'unity-capture', 'unity-build', 'status', 'blender', 'assets-fetch')]
    [string]$Command,
    [int]$SmokeSeconds = 90,
    # Arguments forwarded by 'blender' and 'assets-fetch'.
    [Parameter(Position = 1, ValueFromRemainingArguments = $true)]
    [string[]]$Rest = @()
)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$ConfigPath = Join-Path $PSScriptRoot 'studio.config.json'
if (-not (Test-Path $ConfigPath)) {
    # Fresh worktree: the real config is gitignored and the example holds this machine's paths (REVIEW-W1 m6).
    Copy-Item (Join-Path $PSScriptRoot 'studio.config.example.json') $ConfigPath
    Write-Host "Created $ConfigPath from studio.config.example.json; edit it if paths differ on this machine."
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

# ms + PID: same-second runs in one worktree must not share a log Unity holds open (REVIEW-W3A n2).
$Stamp   = "$(Get-Date -Format 'yyyyMMdd-HHmmss-fff')-$PID"
$Log     = Join-Path $LogDir "$Stamp-$Command.log"
$Started = Get-Date
$Outputs = New-Object System.Collections.ArrayList  # paths reported in the result JSON
$Commit  = git -C $Root rev-parse HEAD 2>$null

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

function Invoke-Unity([string[]]$UnityArgs, [string]$UnityLog, [switch]$Graphics) {
    # Screenshot capture needs a GPU device; everything else runs headless.
    $all = @('-batchmode') + $(if ($Graphics) { @() } else { @('-nographics') }) + @('-projectPath', $Project, '-logFile', $UnityLog) + $UnityArgs
    $argLine = ($all | ForEach-Object { if ($_ -match '\s') { '"' + $_ + '"' } else { $_ } }) -join ' '
    $p = Start-Process -FilePath $Unity -ArgumentList $argLine -PassThru -NoNewWindow
    $null = $p.Handle  # cache the handle, or PS 5.1 loses ExitCode
    Exit-UnitySlot     # the editor now counts in other scripts' slot check
    $p.WaitForExit()
    return $p.ExitCode
}

function Get-CsErrorCount([string]$path) {
    if (-not (Test-Path $path)) { return -1 }
    return @(Select-String -Path $path -Pattern 'error CS\d+' | Select-Object -ExpandProperty Line -Unique).Count
}

function Complete([bool]$ok, [int]$exitCode, [string]$summary, [int]$scriptExit = -1) {
    Exit-UnitySlot
    if ($scriptExit -lt 0) { $scriptExit = $(if ($ok) { 0 } else { 1 }) }
    $result = [ordered]@{
        command     = $Command
        operation   = $Command
        ok          = $ok
        status      = $(if ($scriptExit -eq 2) { 'blocked' } elseif ($ok) { 'pass' } else { 'fail' })
        exitCode    = $exitCode
        startedUtc  = $Started.ToUniversalTime().ToString('o')
        finishedUtc = (Get-Date).ToUniversalTime().ToString('o')
        durationSec = [math]::Round(((Get-Date) - $Started).TotalSeconds, 1)
        commit      = $Commit
        worktree    = $Root
        log         = Get-RelPath $Log
        logs        = @(Get-RelPath $Log)
        outputs     = @($Outputs | ForEach-Object { Get-RelPath $_ })
        summary     = $summary
    }
    $json = $result | ConvertTo-Json
    $resultPath = Join-Path $ResultDir "$Stamp-$Command.json"
    [IO.File]::WriteAllText($resultPath, $json)  # UTF-8 without BOM
    Write-Host $json
    Write-Host "result: $(Get-RelPath $resultPath)"
    exit $scriptExit
}

function Assert-UnityReady {
    if (-not (Test-Path $Unity)) { Complete $false -1 "Unity executable not found: $Unity" }
    if (-not (Test-Path (Join-Path $Project 'ProjectSettings'))) { Complete $false -1 "Unity project not found: $Project" }
    if (Test-ProjectLocked) { Complete $false -1 'blocked: another Unity instance has the project open' 2 }
    Wait-UnitySlot
    # Another run on this worktree may have launched while we waited for the slot (REVIEW-W3A n3).
    if (Test-ProjectLocked) { Complete $false -1 'blocked: another Unity instance has the project open' 2 }
}

function Wait-UnitySlot {
    # DEC-013: at most 2 Unity editors on this machine; asset import workers and the Hub's `unity.exe serve` don't count.
    # A machine-wide lock (shared by all worktrees) spans check-then-launch; Invoke-Unity releases it once the editor started.
    $timeoutMin = $(if ($Cfg.unitySlotTimeoutMinutes) { [double]$Cfg.unitySlotTimeoutMinutes } else { 45 })
    $deadline = (Get-Date).AddMinutes($timeoutMin)
    $lockPath = Join-Path $env:LOCALAPPDATA 'DispoStudio\unity-slot.lock'
    New-Item -ItemType Directory -Force (Split-Path $lockPath) | Out-Null
    while ($true) {
        try { $script:SlotLock = [IO.File]::Open($lockPath, 'OpenOrCreate', 'ReadWrite', 'None') } catch { $script:SlotLock = $null }
        if ($script:SlotLock) {
            $n = @(Get-CimInstance Win32_Process -Filter "Name='Unity.exe'" |
                Where-Object { $_.ExecutablePath -like '*\Editor\Unity.exe' -and $_.CommandLine -notmatch 'AssetImportWorker|\sserve\b' }).Count
            if ($n -lt 2) { return }
            Exit-UnitySlot
            $wait = 60; $why = "$n Unity editors running"
        } else { $wait = 5; $why = 'another studio.ps1 is launching Unity' }
        if ((Get-Date) -ge $deadline) { Complete $false -1 "blocked: DEC-013 slot wait timed out after $timeoutMin min ($why)" 2 }
        Write-Line "DEC-013: $why, waiting $wait s"
        Start-Sleep -Seconds $wait
    }
}

function Exit-UnitySlot {
    if ($script:SlotLock) { $script:SlotLock.Dispose(); $script:SlotLock = $null }
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
        # Git LFS (DEC-023): hooks + filter in this repo's config, and the ThirdParty patterns routed to LFS.
        $ErrorActionPreference = 'Continue'  # PS 5.1 turns native stderr into terminating errors
        if (-not (git -C $Root config --local --get filter.lfs.process)) { git -C $Root lfs install --local 2>&1 | ForEach-Object { Write-Line "$_" } }
        $checks['gitLfs'] = [bool](git -C $Root config --local --get filter.lfs.process)
        $lfsExt = 'png', 'jpg', 'exr', 'hdr', 'fbx', 'glb', 'wav', 'ogg', 'ttf'
        $untracked = @($lfsExt | Where-Object { (git -C $Root check-attr filter -- "UnityProject/Assets/_Game/Art/ThirdParty/x/a.$_") -notmatch ': lfs$' })
        $ErrorActionPreference = 'Stop'
        # Reported, not failed: the patterns land with ASSET-002; make this a bool once that is on main.
        $checks['lfsPatterns'] = $(if ($untracked.Count) { "missing $($untracked -join ',') (ASSET-002 adds them)" } else { "$($lfsExt.Count)/$($lfsExt.Count) tracked" })
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
            Group-Object { $_.BaseName -replace '^\d{8}-\d{6}(-\d{3}-\d+)?-', '' } | ForEach-Object {
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

    { $_ -in 'unity-test-edit', 'unity-test-play' } {
        Assert-UnityReady
        $platform = if ($Command -eq 'unity-test-play') { 'PlayMode' } else { 'EditMode' }
        $xml = Join-Path $TestDir "$Stamp-$($platform.ToLower()).xml"
        # -runTests quits on its own; -quit would skip the run.
        $code = Invoke-Unity @('-runTests', '-testPlatform', $platform, '-testResults', $xml) $Log
        [void]$Outputs.Add($xml)
        if (-not (Test-Path $xml)) { Complete $false $code "no test results written (csErrors=$(Get-CsErrorCount $Log))" }
        $run = ([xml](Get-Content $xml -Raw)).'test-run'
        $ok = ($code -eq 0) -and ([int]$run.failed -eq 0) -and ([int]$run.total -gt 0)
        Complete $ok $code "total=$($run.total) passed=$($run.passed) failed=$($run.failed) skipped=$($run.skipped) xml=$(Get-RelPath $xml)"
    }

    'unity-graybox' {
        Assert-UnityReady
        $code = Invoke-Unity @('-quit', '-executeMethod', 'Dispo.Editor.Graybox.GrayboxBuilder.Build') $Log
        $line = Select-String -Path $Log -Pattern '\[Graybox\] Build (OK.*|FAILED.*)' | Select-Object -Last 1
        $ok = ($code -eq 0) -and ($null -ne $line) -and ($line.Line -match 'Build OK')
        Complete $ok $code "csErrors=$(Get-CsErrorCount $Log); $(if ($line) { $line.Line.Trim() } else { 'GrayboxBuilder did not run' })"
    }

    'unity-capture' {
        Assert-UnityReady
        $commit = (git -C $Root rev-parse --short HEAD 2>$null)
        $outDir = Join-Path (Resolve-RepoPath $Cfg.screenshots) $commit
        if (Test-Path $outDir) { $outDir = "$outDir-$Stamp" }  # a 2nd capture on one commit must not overwrite the 1st (ART-005)
        $code = Invoke-Unity @('-quit', '-executeMethod', 'Dispo.Editor.Graybox.GrayboxCapture.CaptureAll', '-outDir', $outDir, '-commit', $commit) $Log -Graphics
        [void]$Outputs.Add($outDir)
        $line = Select-String -Path $Log -Pattern '\[Graybox\] Capture (OK.*|FAILED.*)' | Select-Object -Last 1
        if ($code -ne 0 -or $null -eq $line -or $line.Line -notmatch 'Capture OK') {
            Complete $false $code "capture failed: $(if ($line) { $line.Line.Trim() } else { 'GrayboxCapture did not run' })"
        }
        # Contact sheet + top-down overlay against the 1-ft plan grid (Python + Pillow).
        $ErrorActionPreference = 'Continue'  # PS 5.1 turns native stderr into terminating errors
        $qa = & python (Join-Path $PSScriptRoot 'graybox_qa.py') $outDir (Join-Path $Root 'References/Index/floor_plan_grid_1ft.png') 2>&1
        $qa | ForEach-Object { Write-Line "$_" }
        $ok = $LASTEXITCODE -eq 0
        $ErrorActionPreference = 'Stop'
        $summary = "$($line.Line.Trim()); qa: $(($qa | Select-Object -Last 1))"

        # GAME-002 slice screenshots: a PlayMode test that needs a GPU, so it runs here and is skipped under unity-test-play.
        $hasSlice = [bool](Get-ChildItem (Join-Path $Project 'Assets') -Recurse -Filter '*.cs' |
            Select-String -Pattern 'Category\("SliceCapture"\)' -List)
        if (-not $hasSlice) { Complete $ok $code "$summary; slice: skipped (no SliceCapture test category)" }
        Assert-UnityReady
        $sliceDir = Join-Path $outDir 'slice'
        $sliceLog = Join-Path $LogDir "$Stamp-$Command-slice.log"
        $xml = Join-Path $TestDir "$Stamp-slicecapture.xml"
        $sliceCode = Invoke-Unity @('-runTests', '-testPlatform', 'PlayMode', '-testCategory', 'SliceCapture', '-testResults', $xml, '-sliceCaptureDir', $sliceDir) $sliceLog -Graphics
        [void]$Outputs.AddRange(@($sliceDir, $xml, $sliceLog))
        if (Test-Path $xml) {
            $run = ([xml](Get-Content $xml -Raw)).'test-run'
            $sliceOk = ($sliceCode -eq 0) -and ([int]$run.failed -eq 0) -and ([int]$run.passed -gt 0)
            $shots = @(Get-ChildItem $sliceDir -Filter 'SLICE_*.png' -ErrorAction SilentlyContinue).Count
            $sliceSummary = "passed=$($run.passed) failed=$($run.failed) skipped=$($run.skipped) shots=$shots"
        } else { $sliceOk = $false; $sliceSummary = "no test results written (csErrors=$(Get-CsErrorCount $sliceLog))" }
        Complete ($ok -and $sliceOk) $(if ($code -ne 0) { $code } else { $sliceCode }) "$summary; slice: $sliceSummary"
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
        $smoke = "$marker, exitedEarly=$exitedEarly, crash=$crash"

        # TOOLCHAIN §14 manifest next to the exe; md5s are over the committed (LF) bytes.
        $md5 = { param($rel) $f = Join-Path $Root $rel; if (Test-Path $f) { (Get-FileHash $f -Algorithm MD5).Hash.ToLower() } else { $null } }
        $buildSettings = Get-Content (Join-Path $Project 'ProjectSettings\EditorBuildSettings.asset') -Raw
        $manifest = [ordered]@{
            version               = "Windows64-Dev-$($Commit.Substring(0, 7))"
            target                = 'StandaloneWindows64'
            buildDateUtc          = (Get-Date).ToUniversalTime().ToString('o')
            commit                = $Commit
            dirtyPathCount        = @(git -C $Root status --porcelain 2>$null).Count
            unityVersion          = ((Get-Content (Join-Path $Project 'ProjectSettings\ProjectVersion.txt'))[0] -split ':\s*')[1]
            scenes                = @([regex]::Matches($buildSettings, '- enabled: 1\s+path: (\S+)') | ForEach-Object { $_.Groups[1].Value })
            catalogManifestMd5    = & $md5 'UnityProject/Assets/_Game/Data/Catalog/manifest.json'
            assetCacheManifestMd5 = & $md5 'Docs/Assets/ASSET_CACHE_MANIFEST.json'
            smoke                 = $smoke
            result                = "Artifacts/Results/$Stamp-$Command.json"
        }
        $manifestPath = Join-Path (Split-Path $exe) 'BUILD_MANIFEST.json'
        [IO.File]::WriteAllText($manifestPath, ($manifest | ConvertTo-Json))
        [void]$Outputs.AddRange(@($exe, $manifestPath, $playerLog))
        Complete $ok $code "exe=$(Get-RelPath $exe); smoke: $smoke, playerLog=$(Get-RelPath $playerLog); manifest=$(Get-RelPath $manifestPath)"
    }

    { $_ -in 'blender', 'assets-fetch' } {
        if ($Command -eq 'blender') {
            $env:BLENDER_EXE = $Cfg.blenderExecutable
            $tool = Join-Path $Root 'Tools\Blender\blender.ps1'
            $toolArgs = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $tool) + $Rest
            $exeName = 'powershell'
        } else {
            $tool = Join-Path $Root 'Tools\Assets\fetch_assets.py'
            $toolArgs = @('-I', $tool) + $Rest
            $exeName = 'python'
        }
        if (-not (Test-Path $tool)) { Complete $false -1 "blocked: $(Get-RelPath $tool) not present on this branch" 2 }
        $ErrorActionPreference = 'Continue'  # PS 5.1 turns native stderr into terminating errors
        & $exeName @toolArgs 2>&1 | ForEach-Object { Write-Line "$_" }
        $code = $LASTEXITCODE
        Complete ($code -eq 0) $code "$(Get-RelPath $tool) $($Rest -join ' ') exited $code"
    }
}
