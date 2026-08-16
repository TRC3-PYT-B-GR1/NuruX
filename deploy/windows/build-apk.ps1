[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SourceRoot,

    [Parameter(Mandatory = $true)]
    [ValidatePattern('^https://')]
    [string]$ApiBaseUrl,

    [Parameter(Mandatory = $true)]
    [ValidatePattern('^\d+\.\d+\.\d+$')]
    [string]$VersionName,

    [Parameter(Mandatory = $true)]
    [ValidateRange(1, 2147483647)]
    [int]$VersionCode,

    [string]$OutputDirectory = ''
)

$ErrorActionPreference = 'Stop'

$resolvedSource = (Resolve-Path -LiteralPath $SourceRoot).Path
$mobileRoot = Join-Path $resolvedSource 'nurux_app'
$signingProperties = Join-Path $mobileRoot 'android\key.properties'
$builtApk = Join-Path $mobileRoot 'build\app\outputs\flutter-apk\app-release.apk'

if (-not (Test-Path -LiteralPath (Join-Path $mobileRoot 'pubspec.yaml'))) {
    throw "The source root does not contain nurux_app/pubspec.yaml: $resolvedSource"
}
if (-not (Test-Path -LiteralPath $signingProperties)) {
    throw 'Production signing is missing. Configure nurux_app/android/key.properties before building a release.'
}

if (-not $OutputDirectory) {
    $OutputDirectory = Join-Path $resolvedSource 'artifacts\android'
}

Push-Location -LiteralPath $mobileRoot
try {
    flutter pub get
    if ($LASTEXITCODE -ne 0) { throw 'Flutter dependency resolution failed.' }
    flutter analyze
    if ($LASTEXITCODE -ne 0) { throw 'Flutter analysis failed.' }
    flutter test
    if ($LASTEXITCODE -ne 0) { throw 'Flutter tests failed.' }
    flutter build apk `
        --release `
        "--build-name=$VersionName" `
        "--build-number=$VersionCode" `
        "--dart-define=API_BASE_URL=$($ApiBaseUrl.TrimEnd('/'))"
    if ($LASTEXITCODE -ne 0) { throw 'Signed APK build failed.' }
} finally {
    Pop-Location
}

if (-not (Test-Path -LiteralPath $builtApk)) {
    throw "Flutter completed without producing the expected APK: $builtApk"
}

New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$releaseApk = Join-Path $OutputDirectory 'nurux.apk'
Copy-Item -LiteralPath $builtApk -Destination $releaseApk -Force

$hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $releaseApk).Hash.ToLowerInvariant()
"$hash  nurux.apk" | Set-Content -LiteralPath (Join-Path $OutputDirectory 'nurux.apk.sha256') -Encoding ascii

Write-Host "Signed APK: $releaseApk" -ForegroundColor Green
Write-Host "SHA-256: $hash"
