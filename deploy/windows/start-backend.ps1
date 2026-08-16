[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SourceRoot,

    [int]$Port = 8000,

    [int]$Threads = 8
)

$ErrorActionPreference = 'Stop'

$resolvedSource = (Resolve-Path -LiteralPath $SourceRoot).Path
$backendRoot = Join-Path $resolvedSource 'backend'
$waitress = Join-Path $resolvedSource '.venv-windows\Scripts\waitress-serve.exe'

if (-not (Test-Path -LiteralPath (Join-Path $backendRoot 'manage.py'))) {
    throw "The source root does not contain backend/manage.py: $resolvedSource"
}
if (-not (Test-Path -LiteralPath $waitress)) {
    throw "Waitress is not installed in $waitress. Run deploy-windows.ps1 first."
}
if (-not (Test-Path -LiteralPath (Join-Path $backendRoot '.env'))) {
    throw "backend/.env is missing. Copy deploy/windows/backend.env.example and configure it first."
}

Set-Location -LiteralPath $backendRoot
& $waitress `
    "--listen=127.0.0.1:$Port" `
    "--threads=$Threads" `
    '--url-scheme=https' `
    '--ident=NuruX' `
    'config.wsgi:application'

exit $LASTEXITCODE
