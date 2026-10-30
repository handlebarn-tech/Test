# OPS-003 self-check for studio.ps1 slots / Get-SlotInfo (no Unity needed):
#   powershell -NoProfile -ExecutionPolicy Bypass -File Tools/Studio/studio_slots_test.ps1
$ErrorActionPreference = 'Stop'
$ast = [Management.Automation.Language.Parser]::ParseFile((Join-Path $PSScriptRoot 'studio.ps1'), [ref]$null, [ref]$null)
function Fn([string]$name) { $ast.FindAll({ param($n) $n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name }, $true) }
Invoke-Expression (Fn 'Get-SlotInfo')[0].Extent.Text

$fail = 0
function Check([string]$name, [bool]$ok) { "$(if ($ok) { 'PASS' } else { 'FAIL' }) $name"; if (-not $ok) { $script:fail++ } }

$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$branch = git -C $root rev-parse --abbrev-ref HEAD
$now = Get-Date
$exe = '"C:\Program Files\Unity\Hub\Editor\6000.6.7f1\Editor\Unity.exe" -batchmode -nographics'
function Editor([string]$rest, [double]$ageMin) { [pscustomobject]@{ ProcessId = 42; CommandLine = "$exe $rest"; CreationDate = $now.AddMinutes(-$ageMin) } }
$proj = "-projectPath `"$root\UnityProject`""

# Launched by `powershell -File studio.ps1 unity-test-edit`: command from the parent, worktree + branch from -projectPath.
$r = Get-SlotInfo (Editor "$proj -logFile `"$root\Artifacts\Logs\x.log`" -runTests" 3) 'powershell.exe -NoProfile -File Tools/Studio/studio.ps1 unity-test-edit' $now
Check 'command from parent' ($r.Command -eq 'unity-test-edit')
Check 'worktree from -projectPath' ($r.Worktree -eq (Split-Path $root -Leaf))
Check 'branch of that worktree' ($r.Branch -eq $branch)
Check 'elapsed minutes' ([math]::Abs($r.ElapsedMin - 3) -lt 0.1)
Check 'not over at 3 min' (-not $r.Over)

# studio.ps1 run inside an agent shell (parent hides the script): command from the stamped log name.
$r = Get-SlotInfo (Editor "$proj -logFile `"$root\Artifacts\Logs\20261030-040130-618-27068-unity-test-play.log`"" 25) 'powershell.exe -Command "Invoke-Expression $s"' $now
Check 'command from studio log name' ($r.Command -eq 'unity-test-play')
Check 'flagged over 20 min' $r.Over

# An editor launched without studio.ps1 (unquoted path, foreign log): flagged as bypassing the gate.
$r = Get-SlotInfo (Editor '-projectPath C:\nowhere\UnityProject -logFile C:\tmp\mine.log' 1) 'cmd.exe' $now
Check 'bypass flagged' ($r.Command -eq '? (not studio.ps1)')
Check 'unknown worktree has no branch' ($r.Worktree -eq 'nowhere' -and $r.Branch -eq '?')

# The slot gate and the monitor count editors with one filter, and `slots` stays read-only.
Check 'Wait-UnitySlot uses Get-UnityEditors' ((Fn 'Wait-UnitySlot')[0].Extent.Text -match 'Get-UnityEditors')
$body = ($ast.FindAll({ param($n) $n -is [Management.Automation.Language.SwitchStatementAst] }, $true) |
    ForEach-Object { $_.Clauses } | Where-Object { $_.Item1.Value -eq 'slots' } | Select-Object -First 1).Item2.Extent.Text
Check 'slots case exists' ([bool]$body)
Check 'slots never kills' ($body -notmatch 'Stop-Process|taskkill|\.Kill\(')

if ($fail) { "FAILED $fail"; exit 1 } else { 'ALL PASS' }
