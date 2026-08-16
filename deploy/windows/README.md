# NuruX on AWS Windows + Supabase

This deployment keeps Django as the only API and authentication authority. Supabase provides PostgreSQL, IIS serves the React build over HTTPS, and IIS proxies Django requests to a localhost-only Waitress process.

## Target layout

```text
https://nurux.example.com/          React static site in IIS
https://nurux.example.com/api/      IIS -> Waitress -> Django
https://nurux.example.com/admin/    IIS -> Waitress -> Django admin
https://downloads.example.com/...   CloudFront -> private S3 APK bucket
                                      Django -> Supabase PostgreSQL
```

## 1. Prepare AWS and Supabase

1. Attach an Elastic IP to the Windows EC2 instance and point the application domain at it.
2. Allow inbound TCP `80` and `443` from the internet. Restrict RDP `3389` to the administrator's fixed IP or VPN range.
3. Create the Supabase project in a region close to the EC2 instance.
4. In Supabase, open **Connect** and copy the **Session pooler** connection string on port `5432`. This is the compatible choice for a persistent Django server using IPv4.
5. If Supabase network restrictions are enabled, allow the EC2 Elastic IP.

Do not put Supabase service-role or anonymous API keys in the web application. NuruX connects to Supabase as PostgreSQL through Django only.

## 2. Install server prerequisites

Install these on Windows Server:

- Python 3.12 x64 with the Python launcher;
- Node.js LTS;
- Git;
- IIS with Static Content;
- IIS URL Rewrite;
- IIS Application Request Routing (ARR).

In IIS Manager, open **Application Request Routing Cache**, choose **Server Proxy Settings**, and enable the proxy. The supplied `web.config` depends on URL Rewrite and ARR.

## 3. Configure the application

Clone the repository into a stable location such as `C:\Apps\NuruX`. Then create the private environment file:

```powershell
Copy-Item C:\Apps\NuruX\deploy\windows\backend.env.example C:\Apps\NuruX\backend\.env
notepad C:\Apps\NuruX\backend\.env
```

Replace every placeholder, especially `SECRET_KEY`, the domain, and `DATABASE_URL`. A password containing characters such as `@`, `:`, `/`, `#`, or `%` must be URL-encoded inside `DATABASE_URL`.

Restrict the file after editing it:

```powershell
icacls C:\Apps\NuruX\backend\.env /inheritance:r /grant:r "SYSTEM:(R)" "Administrators:(F)"
```

## 4. Build, migrate, and publish the site

From an elevated PowerShell window:

```powershell
Set-ExecutionPolicy -Scope Process RemoteSigned
cd C:\Apps\NuruX
.\deploy\windows\deploy-windows.ps1 `
  -SourceRoot C:\Apps\NuruX `
  -SiteRoot C:\inetpub\NuruX `
  -CreateSuperuser
```

The script creates `.venv-windows`, installs Waitress and the backend packages, runs deployment checks and migrations against Supabase, collects Django static files, creates the first administrator interactively, builds React with `/api` as its same-origin API URL, and copies the site to IIS.

Register the API to start with Windows and restart after failures:

```powershell
.\deploy\windows\register-backend-task.ps1 -SourceRoot C:\Apps\NuruX
```

The backend listens only on `127.0.0.1:8000`. Do not open port `8000` in the EC2 security group or Windows Firewall.

## 5. Configure IIS and HTTPS

1. Create an IIS website whose physical path is `C:\inetpub\NuruX`.
2. Add the application hostname as the site binding.
3. Install a trusted TLS certificate and add the HTTPS binding.
4. Redirect the public HTTP binding to HTTPS.
5. Confirm that `https://nurux.example.com/api/health/` returns `{"status":"ok"}`.
6. Confirm that `/login`, `/app`, and `/admin/` all load.

Waitress is deliberately configured with an HTTPS URL scheme because IIS terminates TLS before proxying requests locally. Keep IIS as the only publicly reachable HTTP server.

## 6. Configure production Android signing

Create the permanent keystore once and keep multiple secure backups. Losing it prevents future APKs from upgrading existing installations.

```powershell
New-Item -ItemType Directory -Force C:\secure
keytool -genkeypair -v `
  -keystore C:\secure\nurux-release.jks `
  -keyalg RSA -keysize 2048 -validity 10000 -alias nurux
```

Copy the template and replace its values:

```powershell
Copy-Item .\nurux_app\android\key.properties.example .\nurux_app\android\key.properties
notepad .\nurux_app\android\key.properties
```

The real `key.properties` and keystore are ignored by Git. The Android application ID is `com.nurux.workforce`, and release builds now fail instead of silently using a debug key.

Build a tested, signed APK on a machine with Flutter and the Android SDK:

```powershell
.\deploy\windows\build-apk.ps1 `
  -SourceRoot C:\Apps\NuruX `
  -ApiBaseUrl https://nurux.example.com/api `
  -VersionName 1.0.0 `
  -VersionCode 1
```

The output is `artifacts\android\nurux.apk` with a SHA-256 checksum beside it. Increase `VersionCode` for every release.

## 7. Publish the APK through S3 and CloudFront

Create a private S3 bucket and a CloudFront distribution that uses the bucket as an origin with Origin Access Control. Do not make the whole bucket public.

After configuring AWS CLI credentials with permission to upload to that bucket:

```powershell
.\deploy\windows\publish-apk-s3.ps1 `
  -ApkPath .\artifacts\android\nurux.apk `
  -Bucket nurux-releases `
  -VersionName 1.0.0 `
  -CloudFrontDomain downloads.example.com `
  -DistributionId E123EXAMPLE
```

The script uploads an immutable versioned object and refreshes the stable URL:

```text
https://downloads.example.com/downloads/nurux.apk
```

Advertise the release from the Windows server:

```powershell
cd C:\Apps\NuruX\backend
& ..\.venv-windows\Scripts\python.exe manage.py set_app_version `
  --version-code 1 `
  --version-name 1.0.0 `
  --download-url https://downloads.example.com/downloads/nurux.apk `
  --release-notes "Initial NuruX release"
```

The web download buttons and the mobile update checker read this record automatically. No React rebuild is needed for later APK releases.

## Updating NuruX

Pull the approved code, rerun `deploy-windows.ps1` without `-CreateSuperuser`, then restart the scheduled task:

```powershell
Stop-ScheduledTask -TaskName "NuruX Django API"
Start-ScheduledTask -TaskName "NuruX Django API"
```

Before material database changes, take a Supabase backup or logical dump. Free Supabase projects can pause after low activity and do not provide the same downloadable backup guarantees as paid projects.
