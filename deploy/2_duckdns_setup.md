# 2. DuckDNS Domain Setup

DuckDNS provides a free subdomain that you can point to your AWS Server's IP address. This allows your app to be accessed via `http://your-name.duckdns.org` instead of a raw IP address.

## Step 1: Find your AWS Server IP Address
1. In your AWS Console (or on your AWS Windows Server desktop), find the **Public IPv4 Address** of your server.
2. Write this IP address down (e.g., `192.168.1.100`).

## Step 2: Register a DuckDNS Domain
1. Go to [DuckDNS](https://www.duckdns.org/).
2. Log in using your preferred method (Google, GitHub, Reddit, etc.).
3. Under the "domains" section, type a name you want (e.g., `nurux-app`).
4. Click **add domain**. 
5. Your domain `nurux-app.duckdns.org` is now registered!

## Step 3: Point DuckDNS to your Server
1. In the DuckDNS dashboard, locate your newly created domain.
2. In the **current ip** column next to your domain, paste your **AWS Server Public IPv4 Address**.
3. Click the **update ip** button to save the change.

Wait about 5-10 minutes for the DNS changes to propagate across the internet. You will use this domain (e.g., `nurux-app.duckdns.org`) during the AWS Server setup in the next step.
