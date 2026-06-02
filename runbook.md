# Earnstack Runbook

## Deployment

### First-time Droplet setup
```bash
bash deploy/provision.sh          # installs Docker on the server
git clone <repo> /opt/earnstack
cp .env.example /opt/earnstack/.env   # fill in all values

# Initialise migrations (once only — commit the migrations/ folder afterwards)
flask db init
flask db migrate -m "initial"
flask db upgrade

bash deploy/deploy.sh
```

### Subsequent deploys
```bash
bash deploy/deploy.sh   # pulls main, rebuilds image, restarts containers
```

### Schema changes
```bash
flask db migrate -m "describe change"   # generates migration file
flask db upgrade                        # applies to local DB
git add migrations/ && git commit       # commit before deploying
bash deploy/deploy.sh                   # entrypoint runs flask db upgrade automatically
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
