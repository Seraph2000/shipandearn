# Ship & Earn — Runbook

## Local Development

Everything runs inside Docker — identical to production, no local Python/Postgres setup needed.

**Start / restart the app (normal):**
```bash
docker compose up --build --remove-orphans
```

Open `http://localhost:5000`. Same command whether starting fresh or restarting after code changes — matches what prod does. No separate `down` needed. The database is untouched.

The first run takes ~2 minutes (builds the Docker image, installs dependencies, compiles CSS). Subsequent starts are much faster unless you change `requirements.txt` or `package.json`.

**If you get a stale container error:**
```bash
docker compose up --build --force-recreate --remove-orphans
```

`--force-recreate` tears down and recreates containers but never touches named volumes (DB data is safe).

**Stop the app:**
```bash
docker compose down
```

**⚠️ Database persistence — read this:**

The database lives in a named Docker volume (`postgres_data`). It is **NOT** deleted by:
- `docker compose down` ✓ safe
- `docker compose up --build` ✓ safe
- Rebuilding the image ✓ safe
- Deploying a new version to prod ✓ safe

The **only** command that destroys the volume (and all data) is:
```bash
docker compose down -v   # ← NEVER run this in prod. Deletes the database.
```

Only use `down -v` locally when you deliberately want a clean slate (e.g. resetting after a DB rename). Never run it on the Droplet.

**View logs:**
```bash
docker compose logs -f web
```

**When you change template CSS classes** (new Tailwind classes), the image rebuild handles it automatically on the next `docker compose up --build`.

**Schema changes (local):**
```bash
# Generate a migration (run against your local DB inside the container)
docker compose exec web flask db migrate -m "describe change"
docker compose exec web flask db upgrade
# Then commit migrations/ and push
```

---

## Production Deployment

### 1. Create the Droplet (DigitalOcean console)

1. Log in to [cloud.digitalocean.com](https://cloud.digitalocean.com)
2. **Create → Droplet**
   - Image: **Ubuntu 22.04 LTS**
   - Size: **Basic — $6/mo** (1 vCPU, 1GB RAM, 25GB SSD)
   - Region: LON1 (UK)
   - Authentication: **SSH key** (add your public key — `~/.ssh/id_rsa.pub`)
   - Hostname: `shipandearn`
3. Note the Droplet's public IP address (currently: `<DROPLET_IP>`)

**SSH key used for this Droplet:** `~/.ssh/shipandearn_do` (previously `earnstack_do` — renamed June 2026).

**SSH config (local `~/.ssh/config`)** — add this so you don't need to specify the key every time:
```
Host shipandearn
    HostName <DROPLET_IP>
    User seraphina
    IdentityFile ~/.ssh/shipandearn_do

Host <DROPLET_IP>
    User seraphina
    IdentityFile ~/.ssh/shipandearn_do
```

After adding this, you can SSH with just:
```bash
ssh shipandearn
```

---

### 2. Point your domain

Domains **shipandearn.com** and **shipandearn.dev** are registered with Cloudflare.

In the Cloudflare dashboard (dash.cloudflare.com → shipandearn.com → DNS), add two **A records**:
```
@   →   <DROPLET_IP>
www →   <DROPLET_IP>
```

Proxy status: **Proxied** (orange cloud). SSL mode: **Flexible** (required for `.dev` HSTS).

---

### 3. Provision the server (run once)

```bash
ssh root@<DROPLET_IP>
apt-get update && apt-get upgrade -y
curl -fsSL https://get.docker.com | sh
apt-get install -y docker-compose-plugin
mkdir -p /opt/shipandearn
```

**Create the seraphina user (run once):**
```bash
adduser seraphina
usermod -aG sudo seraphina
mkdir -p /home/seraphina/.ssh
cp /root/.ssh/authorized_keys /home/seraphina/.ssh/authorized_keys
chown -R seraphina:seraphina /home/seraphina/.ssh
chmod 700 /home/seraphina/.ssh
chmod 600 /home/seraphina/.ssh/authorized_keys
```

Give seraphina ownership of the app directory:
```bash
sudo chown -R seraphina:seraphina /opt/shipandearn
```

---

### 4. Set up a GitHub deploy key

The repo is private — the server needs its own SSH key with read access.

**On the Droplet:**
```bash
ssh-keygen -t ed25519 -C "shipandearn-droplet-deploy" -f ~/.ssh/github_deploy
cat ~/.ssh/github_deploy.pub   # copy this output
```

**On GitHub:**
1. Go to **github.com/Seraph2000/shipandearn → Settings → Deploy keys**
2. Click **Add deploy key**
   - Title: `shipandearn-droplet`
   - Key: paste the output above
   - Allow write access: **No**
3. Click **Add key**

**Back on the Droplet:**
```bash
nano ~/.ssh/config
```
Add:
```
Host github.com
    IdentityFile ~/.ssh/github_deploy
    IdentitiesOnly yes
```

Test:
```bash
ssh -T git@github.com
# Should respond: Hi Seraph2000/shipandearn! You've successfully authenticated...
```

---

### 5. Clone the repo and configure environment

```bash
cd /opt/shipandearn
git clone git@github.com:Seraph2000/shipandearn.git .
cp .env.example .env
nano .env   # fill in all values
```

**Required `.env` values for production:**
```env
SECRET_KEY=<long-random-string>
DATABASE_URL=postgresql://shipandearn:<password>@db:5432/shipandearn
POSTGRES_USER=shipandearn
POSTGRES_PASSWORD=<same-password>
ANTHROPIC_API_KEY=<your-key>
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_LIFETIME=price_...
STRIPE_PRICE_PRO=price_...
```

**Note on Stripe keys:** local `.env` uses test keys (`sk_test_...`). Prod must use live keys (`sk_live_...`) from the Stripe Dashboard with Live mode toggled on. Price IDs are also different between test and live — copy them from the live Product catalogue.

**Note on database credentials:** the Postgres user/database is named `earnstack` in the existing prod volume (set up before the rename). Leave these as-is — changing them would break the existing database. The naming is internal only.

Generate a secret key:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

### 6. First deploy

```bash
ssh shipandearn
cd /opt/shipandearn
sudo docker build -t shipandearn:latest .
sudo docker compose -f docker-compose.prod.yml up -d
```

This builds the image (including CSS), starts all three containers (web, db, nginx), and runs `flask db upgrade` automatically.

**Important:** `docker-compose.prod.yml` references `image: shipandearn:latest` with no `build:` directive — it does NOT build automatically on `up`. You must always run `docker build` first, then `docker compose up`. The `--build` flag on `docker compose up` will not work here.

Verify:
```bash
sudo docker compose -f docker-compose.prod.yml ps
```

Visit `https://shipandearn.com`.

---

### 7. Subsequent deploys

```bash
ssh shipandearn
cd /opt/shipandearn
sudo bash deploy/deploy.sh
```

`deploy.sh` pulls latest code, rebuilds the image, and restarts containers in one command. Schema migrations run automatically on startup via `entrypoint.sh`.

**Downtime during deploys:** the current setup has ~5-10 seconds of downtime per deploy. This is acceptable at current scale. The deploy script minimises this by building the new image first (while the old app is still running), then doing a fast container swap.

**⚠️ Never delete the database volume.** The `shipandearn_postgres_data` Docker volume holds all production data. It survives `docker compose down`, image rebuilds, and deploys. The only command that destroys it is `docker compose down -v` — never run that on the Droplet.

**Zero-downtime deploys (future, when traffic justifies it):**
Use a blue-green approach — run two web containers (blue + green) on different ports. Nginx proxies to the active one. Deploy to the idle container, verify it's healthy, then update the nginx upstream to point to it. The old container stays live until the switch completes. Requires updating `nginx.conf` and `docker-compose.prod.yml` to support two web instances.

---

### 8. Update git remote on the Droplet (if needed)

```bash
git remote set-url origin git@github.com:Seraph2000/shipandearn.git
```

---

### 9. Useful ops commands

```bash
# View live logs
sudo docker compose -f docker-compose.prod.yml logs -f web

# Restart web container only
sudo docker compose -f docker-compose.prod.yml restart web

# Shell inside the running container
sudo docker compose -f docker-compose.prod.yml exec web sh

# Connect to the database
sudo docker compose -f docker-compose.prod.yml exec db psql -U shipandearn shipandearn
```

---

## Pushing to GitHub from WSL (local machine)

**The remote is set to SSH** — this is the permanent solution and never requires re-authentication:

```bash
git remote set-url origin git@github.com:Seraph2000/shipandearn.git
```

Verify it's set correctly:
```bash
git remote get-url origin
# Should show: git@github.com:Seraph2000/shipandearn.git
```

If the remote shows `https://github.com/...` instead, run the `set-url` command above — that's why pushes fail with "No such device or address".

**To push:**
```bash
git push origin main
```

**To tag and push a release:**
```bash
git tag v1.0.0
git push origin main
git push origin v1.0.0
```

**If push fails with "Permission denied (publickey)"**, your SSH key isn't added to the agent:
```bash
ssh-add ~/.ssh/id_ed25519   # or whichever key is registered with GitHub
```

**Avoid HTTPS remotes** — `gh auth login` sessions expire and break pushes silently. SSH is permanent.

---

## Stripe CLI Setup (local testing)

### Install (WSL2 / Ubuntu — run each line separately)

```bash
curl -s https://packages.stripe.dev/api/security/keypair/stripe-cli-gpg/public | gpg --dearmor | sudo tee /usr/share/keyrings/stripe.gpg > /dev/null
```

```bash
echo "deb [signed-by=/usr/share/keyrings/stripe.gpg] https://packages.stripe.dev/stripe-cli-debian-local stable main" | sudo tee /etc/apt/sources.list.d/stripe.list
```

```bash
sudo apt update && sudo apt install stripe -y
```

### Authenticate

```bash
stripe login
```

Follow the browser link to connect to your Stripe account.

### Forward webhooks locally

```bash
stripe listen --forward-to localhost:5000/stripe/webhook
```

The CLI prints a `whsec_...` signing secret. Copy it into your local `.env`:

```
STRIPE_WEBHOOK_SECRET=whsec_...
```

Then restart the app:

```bash
docker compose up --build --remove-orphans
```

Keep the `stripe listen` terminal running while testing.

### Test Stripe flows

**Lifetime (£4.99 one-time):**
1. Sign up as a new user (demo tier)
2. Trigger the upgrade prompt (click any gated action or go to `/upgrade`)
3. Click **Get Lifetime Access — £4.99**
4. Use test card `4242 4242 4242 4242`, any future expiry, any CVC
5. After payment: sidebar should show `Lifetime`, all core features unlocked

**Pro (£12.99/mo):**
1. From the upgrade page click **Upgrade to Pro**
2. Same test card
3. After payment: sidebar should show `Pro`, Gig Generator accessible

**Verify webhook fired:**
- Check the `stripe listen --forward-to` terminal — `checkout.session.completed` should show `[200]`
- A `[400]` or `[500]` means the webhook secret is wrong or the handler errored

### Troubleshooting webhooks

**Tier doesn't update after payment**

Work through in order:

1. **Wrong command** — `stripe listen` (no `--forward-to`) just logs events, it does NOT forward them to the app. Always use:
   ```bash
   stripe listen --forward-to localhost:5000/stripe/webhook
   ```

2. **Wrong webhook secret** — each `stripe listen` session prints its own `whsec_...`. If `.env` has a stale or placeholder value, every webhook returns `400`. Copy the exact secret printed in the terminal into `.env`, then restart the app before testing.

3. **Correct order of operations** — must do all four steps in sequence:
   1. Update `STRIPE_WEBHOOK_SECRET` in `.env`
   2. Restart app: `docker compose up --build --remove-orphans`
   3. Start forwarding: `stripe listen --forward-to localhost:5000/stripe/webhook`
   4. Replay or make a new payment

4. **Replay a missed event** — if the payment completed but the webhook wasn't forwarded, replay it using the event ID from the `stripe listen` terminal output:
   ```bash
   stripe events resend evt_xxxxxxxxxxxxxxxx
   ```
   The event ID appears in the terminal next to the event type, e.g. `checkout.session.completed [evt_1TjLgt...]`

5. **Check app logs** to confirm what the webhook handler received:
   ```bash
   docker compose logs web --tail=30
   ```
   Look for `POST /stripe/webhook` — `200` means success, `400` means signature mismatch (wrong secret).

---

## Stripe Webhooks (production)

Register the webhook endpoint in the Stripe Dashboard:
- **Endpoint URL:** `https://shipandearn.com/stripe/webhook`
- **Events to listen for:** `checkout.session.completed`, `customer.subscription.deleted`

Copy the signing secret into `.env` on the Droplet as `STRIPE_WEBHOOK_SECRET`.

---

## Troubleshooting

### SSH: permission denied connecting to Droplet

The Droplet was provisioned with the `shipandearn_do` key (originally `earnstack_do`). If you get permission denied:

```bash
ssh -i ~/.ssh/shipandearn_do seraphina@<DROPLET_IP>
```

If that works but bare `ssh seraphina@<DROPLET_IP>` doesn't, your `~/.ssh/config` is missing — add it (see section 1 above).

---

### Git: "dubious ownership" error after SSH into Droplet

Happens if the `/opt/shipandearn` directory was created as root but you're logged in as seraphina:

```bash
git config --global --add safe.directory /opt/shipandearn
```

If you then get `cannot open '.git/FETCH_HEAD': Permission denied`, fix ownership:

```bash
sudo chown -R seraphina:seraphina /opt/shipandearn
```

---

### Docker: "pull access denied for shipandearn" on `docker compose up`

`docker-compose.prod.yml` uses `image: shipandearn:latest` with no registry — it expects a locally built image. Build it first:

```bash
sudo docker build -t shipandearn:latest .
sudo docker compose -f docker-compose.prod.yml up -d
```

Never use `docker compose up --build` with the prod compose file — the `--build` flag has no effect without a `build:` directive.

---

### Stripe: tier doesn't update after live payment

1. Check the webhook destination is registered in Stripe Dashboard → Developers → Webhooks → your endpoint
2. Confirm `STRIPE_WEBHOOK_SECRET` in prod `.env` matches the signing secret shown on that endpoint (not the local `stripe listen` secret)
3. Check logs: `sudo docker compose -f docker-compose.prod.yml logs web --tail=50` — look for `POST /stripe/webhook 200`
4. If the event fired but the app was down, replay it: Stripe Dashboard → Developers → Webhooks → your endpoint → find the event → Resend

---

## Functional Tests

Run these against `http://localhost:5000` before each release.

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

---

### 6. Auth & Stripe

- Sign up with a new email — verify account is created with `lifetime` tier, dashboard loads
- Click **Upgrade** in sidebar — verify redirect to Stripe Checkout
- Complete a test payment (use Stripe test card `4242 4242 4242 4242`) — verify tier upgrades and success flash shows
- Sign out and sign back in — verify session persists correctly
