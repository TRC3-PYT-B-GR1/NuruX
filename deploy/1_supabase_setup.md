# 1. Supabase Database Setup

Supabase is a fantastic, free service that provides a managed PostgreSQL database. Follow these steps to get your database running.

## Step 1: Create an Account & Project
1. Go to [Supabase](https://supabase.com/) and click **Start your project**.
2. Sign in with GitHub or your email.
3. Click **New Project**.
4. Choose an Organization (or create a new one).
5. Enter a Project Name (e.g., `nurux-db`).
6. **Important:** Enter a strong **Database Password** and save it somewhere safe (you will need this later).
7. Choose a Region close to your AWS Server (e.g., US East).
8. Click **Create new project**.

## Step 2: Get your Connection String
Supabase takes a few minutes to provision your database. Once it's ready:
1. In your Supabase dashboard, click the **Settings** gear icon on the left sidebar.
2. Under "Configuration", click **Database**.
3. Scroll down to the **Connection string** section.
4. Check the **Use connection pooling** box and ensure the mode is set to **Transaction** or **Session**.
5. Copy the connection string. It will look like this:
   `postgresql://postgres.yourprojectid:[YOUR-PASSWORD]@aws-0-region.pooler.supabase.com:5432/postgres`

## Step 3: Prepare the String for Deployment
Replace `[YOUR-PASSWORD]` with the database password you created in Step 1. **Note:** If your password contains special characters (like `@`, `#`, or `/`), you must URL-encode them (e.g., `@` becomes `%40`).

Save this final connection string. You will need it in Step 3 when setting up your AWS Server!
