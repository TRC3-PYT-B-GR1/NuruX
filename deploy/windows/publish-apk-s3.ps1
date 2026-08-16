[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ApkPath,

    [Parameter(Mandatory = $true)]
    [string]$Bucket,

    [Parameter(Mandatory = $true)]
    [ValidatePattern('^\d+\.\d+\.\d+$')]
    [string]$VersionName,

    [Parameter(Mandatory = $true)]
    [string]$CloudFrontDomain,

    [string]$DistributionId = ''
)

$ErrorActionPreference = 'Stop'

$resolvedApk = (Resolve-Path -LiteralPath $ApkPath).Path
if ([IO.Path]::GetExtension($resolvedApk) -ne '.apk') {
    throw "Expected an .apk file: $resolvedApk"
}
if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
    throw 'AWS CLI is not installed or is not available on PATH.'
}

$domain = $CloudFrontDomain.Trim().TrimEnd('/')
$domain = $domain -replace '^https?://', ''
$versionedKey = "releases/$VersionName/nurux-$VersionName.apk"
$stableKey = 'downloads/nurux.apk'
$contentType = 'application/vnd.android.package-archive'
$contentDisposition = 'attachment; filename="nurux.apk"'

Write-Host "Uploading immutable release s3://$Bucket/$versionedKey..."
& aws s3 cp $resolvedApk "s3://$Bucket/$versionedKey" `
    --content-type $contentType `
    --content-disposition $contentDisposition `
    --cache-control 'public,max-age=31536000,immutable' `
    --only-show-errors
if ($LASTEXITCODE -ne 0) { throw 'The versioned S3 upload failed.' }

Write-Host "Updating stable download s3://$Bucket/$stableKey..."
& aws s3 cp $resolvedApk "s3://$Bucket/$stableKey" `
    --content-type $contentType `
    --content-disposition $contentDisposition `
    --cache-control 'no-cache,max-age=0' `
    --only-show-errors
if ($LASTEXITCODE -ne 0) { throw 'The stable S3 upload failed.' }

if ($DistributionId) {
    Write-Host 'Invalidating the stable CloudFront download path...'
    & aws cloudfront create-invalidation `
        --distribution-id $DistributionId `
        --paths "/$stableKey" | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'CloudFront invalidation failed.' }
}

$downloadUrl = "https://$domain/$stableKey"
Write-Host ''
Write-Host "APK download URL: $downloadUrl" -ForegroundColor Green
Write-Host 'Publish this URL with: python manage.py set_app_version --version-code <code> --version-name <name> --download-url <url>'
