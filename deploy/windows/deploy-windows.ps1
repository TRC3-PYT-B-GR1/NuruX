[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SourceRoot,

    [string]$SiteRoot = 'C:\inetpub\NuruX',

    [string]$PythonLauncher = 'py',

    [string]$NodeLauncher = 'npm',

    [string]$ApkDownloadUrl = '',

    [switch]$CreateSuperuser
)

$ErrorActionPreference = 'Stop'

$resolvedSource = (Resolve-Path -LiteralPath $SourceRoot).Path
$backendRoot = Join-Path $resolvedSource 'backend'
$frontendRoot = Join-Path $resolvedSource 'frontend'
$venvRoot = Join-Path $resolvedSource '.venv-windows'
$venvPython = Join-Path $venvRoot 'Scripts\python.exe'
$deploymentConfig = Join-Path $resolvedSource 'deploy\windows\web.config'

foreach ($requiredPath in @(
    (Join-Path $backendRoot 'manage.py'),
    (Join-Path $backendRoot 'requirements.txt'),
    (Join-Path $frontendRoot 'package.json'),
    $deploymentConfig
)) {
    if (-not (Test-Path -LiteralPath $requiredPath)) {
        throw "Required project file not found: $requiredPath"
    }
}

if (-not (Test-Path -LiteralPath (Join-Path $backendRoot '.env'))) {
    throw 'backend/.env is missing. Copy deploy/windows/backend.env.example, replace its placeholders, and rerun this script.'
}

if (-not (Test-Path -LiteralPath $venvPython)) {
    Write-Host 'Creating the Windows Python environment...'
    if ($PythonLauncher -eq 'py') {
        & $PythonLauncher -3 -m venv $venvRoot
    } else {
        & $PythonLauncher -m venv $venvRoot
    }
    if ($LASTEXITCODE -ne 0) { throw 'Python virtual environment creation failed.' }
}

Write-Host 'Installing backend dependencies...'
& $venvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw 'pip upgrade failed.' }
& $venvPython -m pip install -r (Join-Path $backendRoot 'requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'Backend dependency installation failed.' }

Push-Location -LiteralPath $backendRoot
try {
    Write-Host 'Checking and migrating the Django API...'
    & $venvPython manage.py check --deploy
    if ($LASTEXITCODE -ne 0) { throw 'Django deployment checks failed.' }
    & $venvPython manage.py migrate --noinput
    if ($LASTEXITCODE -ne 0) { throw 'Database migration failed.' }
    & $venvPython manage.py collectstatic --noinput
    if ($LASTEXITCODE -ne 0) { throw 'Django static-file collection failed.' }

    if ($CreateSuperuser) {
        Write-Host 'Creating the first administrator. Django will prompt for the account details.'
        & $venvPython manage.py createsuperuser
        if ($LASTEXITCODE -ne 0) { throw 'Administrator creation failed.' }
    }
} finally {
    Pop-Location
}

Push-Location -LiteralPath $frontendRoot
$previousApiUrl = $env:VITE_API_URL
$previousApkUrl = $env:VITE_APK_DOWNLOAD_URL
try {
    Write-Host 'Building the React web application...'
    $env:VITE_API_URL = '/api'
    if ($ApkDownloadUrl) {
        $env:VITE_APK_DOWNLOAD_URL = $ApkDownloadUrl
    } else {
        Remove-Item Env:VITE_APK_DOWNLOAD_URL -ErrorAction SilentlyContinue
    }

    & $NodeLauncher ci
    if ($LASTEXITCODE -ne 0) { throw 'Frontend dependency installation failed.' }
    & $NodeLauncher run build
    if ($LASTEXITCODE -ne 0) { throw 'Frontend production build failed.' }
} finally {
    if ($null -eq $previousApiUrl) { Remove-Item Env:VITE_API_URL -ErrorAction SilentlyContinue } else { $env:VITE_API_URL = $previousApiUrl }
    if ($null -eq $previousApkUrl) { Remove-Item Env:VITE_APK_DOWNLOAD_URL -ErrorAction SilentlyContinue } else { $env:VITE_APK_DOWNLOAD_URL = $previousApkUrl }
    Pop-Location
}

$distRoot = Join-Path $frontendRoot 'dist'
if (-not (Test-Path -LiteralPath (Join-Path $distRoot 'index.html'))) {
    throw "The frontend build did not produce $distRoot\index.html"
}

Write-Host "Publishing the web files to $SiteRoot..."
New-Item -ItemType Directory -Force -Path $SiteRoot | Out-Null
Copy-Item -Path (Join-Path $distRoot '*') -Destination $SiteRoot -Recurse -Force
Copy-Item -LiteralPath $deploymentConfig -Destination (Join-Path $SiteRoot 'web.config') -Force

Write-Host ''
Write-Host 'Deployment files are ready.' -ForegroundColor Green
Write-Host "Site root: $SiteRoot"
Write-Host 'Next: run register-backend-task.ps1 from an elevated PowerShell session, then point IIS at the site root.'
