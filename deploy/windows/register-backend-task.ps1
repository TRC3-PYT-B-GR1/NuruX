[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SourceRoot,

    [string]$TaskName = 'NuruX Django API',

    [int]$Port = 8000,

    [int]$Threads = 8
)

$ErrorActionPreference = 'Stop'

$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($identity)
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    throw 'Run this script from an elevated PowerShell session.'
}

$resolvedSource = (Resolve-Path -LiteralPath $SourceRoot).Path
$startScript = Join-Path $resolvedSource 'deploy\windows\start-backend.ps1'
if (-not (Test-Path -LiteralPath $startScript)) {
    throw "Backend start script not found: $startScript"
}

$powerShell = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
$arguments = "-NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$startScript`" -SourceRoot `"$resolvedSource`" -Port $Port -Threads $Threads"

$action = New-ScheduledTaskAction -Execute $powerShell -Argument $arguments -WorkingDirectory $resolvedSource
$trigger = New-ScheduledTaskTrigger -AtStartup
$taskPrincipal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -RestartCount 20 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -ExecutionTimeLimit ([TimeSpan]::Zero) `
    -MultipleInstances IgnoreNew

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Principal $taskPrincipal `
    -Settings $settings `
    -Description 'Runs the NuruX Django API through Waitress on localhost.' `
    -Force | Out-Null

Start-ScheduledTask -TaskName $TaskName

$healthUrl = "http://127.0.0.1:$Port/api/health/"
$healthy = $false
for ($attempt = 1; $attempt -le 15; $attempt++) {
    Start-Sleep -Seconds 2
    try {
        $response = Invoke-RestMethod -Uri $healthUrl -TimeoutSec 5
        if ($response.status -eq 'ok') {
            $healthy = $true
            break
        }
    } catch {
        Write-Verbose "Health check attempt $attempt failed: $($_.Exception.Message)"
    }
}

if (-not $healthy) {
    $task = Get-ScheduledTaskInfo -TaskName $TaskName
    throw "The backend task was registered but did not become healthy. Last task result: $($task.LastTaskResult)"
}

Write-Host "The NuruX backend task is running and healthy at $healthUrl" -ForegroundColor Green
