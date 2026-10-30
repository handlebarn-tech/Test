# OPS-001 self-check for studio.ps1 Wait-UnityExit (no Unity needed):
#   powershell -NoProfile -ExecutionPolicy Bypass -File Tools/Studio/studio_runlimit_test.ps1
$ErrorActionPreference = 'Stop'
$ast = [Management.Automation.Language.Parser]::ParseFile((Join-Path $PSScriptRoot 'studio.ps1'), [ref]$null, [ref]$null)
$fn = $ast.FindAll({ param($n) $n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'Wait-UnityExit' }, $true)
if ($fn.Count -ne 1) { throw 'Wait-UnityExit not found in studio.ps1' }
Invoke-Expression $fn[0].Extent.Text

$ps = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe"
$fail = 0
function Check([string]$name, [bool]$ok) { "$(if ($ok) { 'PASS' } else { 'FAIL' }) $name"; if (-not $ok) { $script:fail++ } }

# A run that finishes inside the limit is left alone.
$p = Start-Process $ps -ArgumentList '-NoProfile -Command exit 0' -PassThru -WindowStyle Hidden
Check 'fast run returns true' (Wait-UnityExit $p 1)

# An overrunning "editor" with a helper child (like AssetImportWorker) is killed as a tree.
$p = Start-Process $ps -ArgumentList '-NoProfile -Command "Start-Process powershell.exe -ArgumentList ''-NoProfile -Command Start-Sleep 120'' -WindowStyle Hidden; Start-Sleep 120"' -PassThru -WindowStyle Hidden
Start-Sleep -Seconds 3  # let it spawn the helper
$child = Get-CimInstance Win32_Process -Filter "ParentProcessId=$($p.Id)"
Check 'helper child spawned' (@($child).Count -ge 1)
Check 'overrun returns false' (-not (Wait-UnityExit $p 0.02))
Check 'editor killed' $p.HasExited
Check 'helper killed' (@($child | Where-Object { Get-Process -Id $_.ProcessId -ErrorAction SilentlyContinue }).Count -eq 0)

if ($fail) { "FAILED $fail"; exit 1 } else { 'ALL PASS' }
