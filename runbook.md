# Earnstack Runbook

## Deployment

### 1. Create the Droplet (DigitalOcean console)

1. Log in to [cloud.digitalocean.com](https://cloud.digitalocean.com)
2. **Create → Droplet**
   - Image: **Ubuntu 22.04 LTS**
   - Size: **Basic — $6/mo** (1 vCPU, 1GB RAM, 25GB SSD)
   - Region: closest to your users (LON1 for UK)
   - Authentication: **SSH key** (add your public key — `~/.ssh/id_rsa.pub`)
   - Hostname: `earnstack`
3. Note the Droplet's public IP address

---

### 2. Point your domain

Domain **earnstack.dev** is registered with Cloudflare Registrar.

In the Cloudflare dashboard (dash.cloudflare.com → earnstack.dev → DNS), add two **A records**:
```
@   →   <droplet-ip>
www →   <droplet-ip>
```

Proxy status: **DNS only** (grey cloud) to start — switch to **Proxied** later if you want Cloudflare's CDN/DDoS protection.

---

### 3. Provision the server (run once)

SSH in and run the provision script:
```bash
ssh root@<droplet-ip>
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Seraph2000/earnstack/main/deploy/provision.sh)"
```

Or manually:
```bash
ssh root@<droplet-ip>
apt-get update && apt-get upgrade -y
curl -fsSL https://get.docker.com | sh
apt-get install -y docker-compose-plugin
mkdir -p /opt/earnstack
```

---

### 4. Set up a GitHub deploy key

The repo is private — the server needs its own SSH key with read access to clone and pull.

**On the Droplet:**
```bash
ssh-keygen -t ed25519 -C "earnstack-droplet-deploy" -f ~/.ssh/github_deploy
# Press Enter through all prompts (no passphrase)

cat ~/.ssh/github_deploy.pub   # copy this output
```

**On GitHub:**
1. Go to **github.com/Seraph2000/earnstack → Settings → Deploy keys**
2. Click **Add deploy key**
   - Title: `earnstack-droplet`
   - Key: paste the output of `cat ~/.ssh/github_deploy.pub`
   - Allow write access: **No** (read-only is enough)
3. Click **Add key**

**Back on the Droplet — configure SSH to use the deploy key for GitHub:**
```bash
nano ~/.ssh/config
```
Add:
```
Host github.com
    IdentityFile ~/.ssh/github_deploy
    IdentitiesOnly yes
```

Test it:
```bash
ssh -T git@github.com
# Should respond: Hi Seraph2000/earnstack! You've successfully authenticated...
```

---

### 5. Clone the repo and configure environment  

```bash
cd /opt/earnstack
git clone git@github.com:Seraph2000/earnstack.git .
cp .env.example .env
nano .env   # fill in all values — see below
```

**Required `.env` values for production:**
```env
SECRET_KEY=<long-random-string>
DATABASE_URL=postgresql://earnstack:<password>@db:5432/earnstack
POSTGRES_USER=earnstack
POSTGRES_PASSWORD=<same-password>
ANTHROPIC_API_KEY=<your-key>
```

Generate a secret key with:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

### 6. First deploy

```bash
cd /opt/earnstack
bash deploy/deploy.sh
```

This builds the image, starts all three containers (web, db, nginx), and runs `flask db upgrade` automatically inside the web container.

Verify everything is running:
```bash
docker compose -f docker-compose.prod.yml ps
```

Visit `http://<droplet-ip>` — you should see the Earnstack dashboard.

---

### 7. Subsequent deploys

From your **local machine**, push to main — then on the Droplet:
```bash
ssh earnstack "cd /opt/earnstack && sudo bash deploy/deploy.sh"
```

Or SSH in and run it directly:
```bash
cd /opt/earnstack && bash deploy/deploy.sh
```

---

### 8. Schema changes

```bash
# On your local machine — generate and commit the migration first
flask db migrate -m "describe change"
flask db upgrade                          # apply locally to verify
git add migrations/ && git commit
git push origin main

# Then deploy
ssh earnstack "cd /opt/earnstack && sudo bash deploy/deploy.sh"
# entrypoint.sh runs flask db upgrade automatically on container start
```

---

### 9. Useful ops commands

```bash
# View live logs
docker compose -f docker-compose.prod.yml logs -f web

# Restart web container only
docker compose -f docker-compose.prod.yml restart web

# Open a shell inside the running container
docker compose -f docker-compose.prod.yml exec web sh

# Connect to the database
docker compose -f docker-compose.prod.yml exec db psql -U earnstack earnstack
```

---

## Functional Tests

Run these against the local instance (`http://localhost:5000`) before each release.

---

### 1. Dashboard

- Open `/` — verify today / month / all-time income totals render
- Confirm income by-stream and by-asset breakdowns load
- Verify goal progress bar shows when a goal is active, absent when none is set

---

### 2. Assets

- Create a new asset (name, type, complexity tier, hours) — verify it appears in the list
- Update status and log additional hours via the form — verify values persist on reload
- Add a stream to the asset (type, platform, price range) — verify it shows under the asset

---

### 3. Sprints

- Create a new sprint — verify it appears as active on `/sprint`
- Assign an asset to the sprint with a week number — verify it shows on the board
- Mark the sprint complete — verify status changes and the board prompts for a new one

---

### 4. Income

- Log an income entry (asset, stream type, amount, date) — verify it appears in the recent entries table
- Confirm the summary totals on `/income` update to reflect the new entry
- Verify the same change is reflected on the dashboard totals

---

### 5. Gig Generator

> **Note:** This section may need tuning as AI output format and saved-content behaviour evolve.

- Select an asset and a single content type, hit Generate — verify AI copy renders in the result panel
- Run again with "all" content types — verify all four channel outputs (Fiverr, Upwork, product page, README) appear
- Reload `/gig` — verify previously generated content is still saved (pulled from DB, not regenerated)
