# 3. AWS Windows Server Deployment Guide

Follow these steps exactly once you have Remote Desktop (RDP) access to your AWS Windows Server.

## Prerequisites
1. Download and install **Python 3.12** (or higher) from [python.org](https://www.python.org/downloads/windows/). **IMPORTANT:** During installation, check the box that says **"Add Python to PATH"**.
2. Download and install **Node.js** (LTS version) from [nodejs.org](https://nodejs.org/).
3. Copy your entire `NuruX` codebase (including the `deploy` folder) onto the server (e.g., to `C:\NuruX`).

## Step 1: Install IIS and Proxy Modules
1. Open **PowerShell** as Administrator on the server.
2. Run this command to install IIS:
   `Install-WindowsFeature -name Web-Server -IncludeManagementTools`
3. Download and install the **URL Rewrite** module for IIS: [Download Link](https://www.iis.net/downloads/microsoft/url-rewrite)
4. Download and install **Application Request Routing (ARR)** for IIS: [Download Link](https://www.iis.net/downloads/microsoft/application-request-routing)
5. **Enable Proxy:** Open **IIS Manager**, double-click **Application Request Routing Cache**, click **Server Proxy Settings...** on the right, check **Enable proxy**, and click **Apply**.

## Step 2: Set up the Backend (Django)
1. Open PowerShell and navigate to the backend folder:
   `cd C:\NuruX\backend`
2. Create and activate a virtual environment:
   `python -m venv venv`
   `.\venv\Scripts\activate`
3. Install the dependencies:
   `pip install -r requirements.txt`
4. Set up the `.env` file inside the `backend/` folder. Create a new file named `.env` and add:
   ```ini
   DEBUG=False
   SECRET_KEY=generate-a-long-random-string-here
   ALLOWED_HOSTS=localhost,127.0.0.1,your-name.duckdns.org
   CORS_ALLOWED_ORIGINS=http://your-name.duckdns.org,http://localhost
   DATABASE_URL=your-supabase-connection-string-here
   ```
5. Apply database migrations to your Supabase database:
   `python manage.py migrate`
6. Collect static files:
   `python manage.py collectstatic --no-input`

## Step 3: Set up the Frontend (React)
1. Open PowerShell and navigate to the frontend folder:
   `cd C:\NuruX\frontend`
2. Create a `.env` file in the `frontend/` folder with your domain:
   ```ini
   VITE_API_URL=http://your-name.duckdns.org/api
   ```
3. Install dependencies and build:
   `npm install`
   `npm run build`

## Step 4: Configure IIS to Serve the App
We will configure IIS to serve the frontend from the `frontend/dist` folder, and proxy `/api` requests to the Django backend (which will run locally on port 8001).

1. Open **Internet Information Services (IIS) Manager**.
2. In the left pane, expand your server node, right-click **Sites**, and click **Add Website...**.
3. Set the following:
   - **Site name:** NuruX
   - **Physical path:** `C:\NuruX\frontend\dist`
   - **Binding:** HTTP on port 80.
   - **IMPORTANT:** Because you have another project running on this server, you **MUST** enter your DuckDNS domain (e.g. `your-name.duckdns.org`) in the **Host name** field. This ensures IIS knows which traffic belongs to NuruX versus your other project.
4. Click **OK**. (You can stop or delete the "Default Web Site" if it conflicts on port 80).
5. Copy the `web.config` file from the `deploy` folder into `C:\NuruX\frontend\dist\web.config`.

## Step 5: Start the Backend Server
1. Navigate to the `deploy` folder and right-click `start_backend.ps1`, then select **Run with PowerShell**.
   *(Note: This starts Waitress in a window. For production, you may want to set this up as a Windows Service using NSSM).*

Your application should now be live at `http://your-name.duckdns.org`!
