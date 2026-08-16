# NuruX

NuruX is an HRMS with a Django REST API, React administration portal, and Flutter employee app. It covers identity and role-based access, employee and organization management, QR/geofenced attendance, two-stage leave approval, payroll estimates, performance, training, assets, and optional AI assistance.

## Authoritative applications

- `backend/manage.py` + `backend/config/`: the API used by the web and mobile clients.
- `frontend/`: the Vite/React administration portal.
- `nurux_app/`: the Flutter employee application.

The root `manage.py` WorkForge tree and `backend/nuruX`/`backend/manteki` recruitment tree are retained as legacy prototypes. They are not part of the deployed NuruX runtime.

## Local setup

Create a Python virtual environment at the repository root, install `backend/requirements.txt`, then run these commands from `backend/`:

```powershell
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py runserver
```

Copy `.env.example` to `backend/.env` for overrides. SQLite is used locally when `DATABASE_URL` is absent.

Run the web portal from `frontend/`:

```powershell
Copy-Item .env.example .env.local
npm ci
npm run dev
```

For Flutter, an Android emulator automatically uses `http://10.0.2.2:8000/api`. A physical device needs a reachable URL:

```powershell
flutter run --dart-define=API_BASE_URL=http://YOUR-LAN-IP:8000/api
```

A release build should receive the deployed API URL:

```powershell
flutter build apk --release --dart-define=API_BASE_URL=https://nurux-api.onrender.com/api
```

## Verification

```powershell
cd backend
..\.venv\Scripts\python.exe manage.py check
..\.venv\Scripts\python.exe manage.py test

cd ..\frontend
npm run build
npm run lint

cd ..\nurux_app
flutter analyze
flutter test
```

## Recommended deployment: AWS Windows + Supabase

The primary deployment target is an AWS Windows Server running IIS, with Django behind IIS through Waitress, Supabase PostgreSQL, and APK releases stored in private S3 behind CloudFront. The full repeatable setup is in [deploy/windows/README.md](deploy/windows/README.md).

This layout provides persistent application hosting, same-origin web/API routing, a Windows startup task for the backend, production Android signing, and a stable APK download URL. Keep Django as the only authentication and application API; Supabase is used as PostgreSQL rather than as a second auth system.

## Optional Render deployment

The root `render.yaml` deploys the Django API, React static site, and a free Render Postgres database as one Blueprint. In Render, create a Blueprint from this repository and confirm the generated service names/URLs. If Render adds a suffix to either service name, update `VITE_API_URL`, `CORS_ALLOWED_ORIGINS`, and `CSRF_TRUSTED_ORIGINS` in the dashboard.

Free Render hosting is appropriate for a demo, not durable production:

- the API sleeps after 15 minutes without inbound traffic and cold-starts on the next request;
- the free Postgres database expires after 30 days and has no managed backups;
- the service filesystem is ephemeral, so APKs and employee documents must use durable external storage;
- free web services cannot send SMTP traffic on ports 25, 465, or 587.

For APK updates, create an `AppVersion` using a durable `download_url`, such as a GitHub Release asset. The web sign-in and employee profile screens expose that release automatically; `VITE_APK_DOWNLOAD_URL` is available as a build-time fallback. For long-lived free testing, point `DATABASE_URL` at a separately managed durable Postgres provider instead of creating `nurux-db`.

## Production notes

Payroll outputs use deployment-configured estimate rates; they are not a statutory payroll engine. Verify jurisdictional calculations before paying staff. Configure an API-based email provider and durable private object storage before handling real users or documents.
