# 1. Install IIS
Write-Host "Installing IIS..." -ForegroundColor Green
Install-WindowsFeature -name Web-Server -IncludeManagementTools

# Note: URL Rewrite and ARR modules still require manual download and installation if you don't have Chocolatey.
Write-Host "Please ensure you have installed the URL Rewrite and ARR modules manually from Microsoft's website." -ForegroundColor Yellow
Write-Host "Once installed, we will enable the ARR Proxy." -ForegroundColor Yellow
Pause

# 2. Enable ARR Proxy (Requires ARR to be installed first)
Write-Host "Enabling ARR Proxy..." -ForegroundColor Green
Set-WebConfigurationProperty -pspath 'MACHINE/WEBROOT/APPHOST' -filter "system.webServer/proxy" -name "enabled" -value "True"

# 3. Setup Python Backend
Write-Host "Setting up Python Backend..." -ForegroundColor Green
Set-Location C:\NuruX\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input

# 4. Setup React Frontend
Write-Host "Setting up React Frontend..." -ForegroundColor Green
Set-Location C:\NuruX\frontend
npm install
npm run build

# 5. Configure IIS Site
Write-Host "Configuring IIS Site..." -ForegroundColor Green
Import-Module WebAdministration

$SiteName = "NuruX"
$PhysicalPath = "C:\NuruX\frontend\dist"
$DuckDnsDomain = "your-name.duckdns.org" # CHANGE THIS TO YOUR ACTUAL DOMAIN!

# Ensure the IIS_IUSRS group has read permissions
icacls "C:\NuruX" /grant "IIS_IUSRS:(OI)(CI)RX"

# Create the IIS Website
if (Get-Website -Name $SiteName -ErrorAction SilentlyContinue) {
    Write-Host "Website $SiteName already exists. Removing it to recreate..." -ForegroundColor Yellow
    Remove-Website -Name $SiteName
}

New-WebSite -Name $SiteName -Port 80 -HostHeader $DuckDnsDomain -PhysicalPath $PhysicalPath

# Copy the web.config to the dist folder
Copy-Item -Path "C:\NuruX\deploy\web.config" -Destination "$PhysicalPath\web.config" -Force

Write-Host "IIS Configuration Complete! You can now run the start_backend.ps1 script to launch the backend on port 8001." -ForegroundColor Green
