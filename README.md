# Ship & Earn

**See all your income in one place, whatever you earn it from.**

Ship & Earn is a dashboard to track your path to financial freedom. It started out for indie devs, and now covers your non-tech gigs too. It's your productivity, finance and accountability app, all in one.

Live at [shipandearn.com](https://shipandearn.com).

---

## Who it's for

- **People with several side incomes**: a room on Airbnb, a weekend catering job, selling art at markets, odd jobs, plus a bit of online work
- **Freelancers and gig workers** spread across several platforms or clients (Fiverr, Upwork, Mercor, direct clients)
- **Makers and developers** who build apps, tools, templates or plugins and want to earn from them

---

## What you can track

| Type | Examples |
|---|---|
| **Things you've built** | Apps, tools, plugins, templates, websites |
| **Non-tech income** | Rentals (e.g. Airbnb), creative work (art, crafts, photography), tasks and odd jobs, small businesses (e.g. catering), grants and funding |
| **Freelance and gig work** | AI training, contract development, writing, consulting |

If something doesn't fit a category, you can make up your own.

---

## Features

- **Your income sources:** add everything that earns you money, with its status, the platform or client, and how much time you've put in (there's a built-in timer)
- **Where you sell it:** record where each one is listed (e.g. Etsy, Fiverr, Airbnb, direct clients), at what price, and whether it's live
- **Income log:** record every payment as it comes in, and edit or delete entries later
- **Monthly goal:** set a monthly target and see how close you are
- **Planner:** plan your work in 4-week blocks, week by week
- **Listing writer:** AI drafts listings and descriptions for you (Fiverr, Upwork, product pages, GitHub READMEs), powered by Claude
- **Accounts and plans:** sign up with email and password, and pay for the Lifetime or Pro plan with Stripe

---

## Tech stack

- **Backend:** Python 3.11, Flask, SQLAlchemy, Flask-Migrate (Alembic), Flask-Login
- **Database:** PostgreSQL 15
- **Frontend:** Jinja2, HTMX, Tailwind CSS
- **AI:** Claude (Anthropic) via the official Python SDK
- **Payments:** Stripe
- **Deployment:** Docker, Gunicorn, Nginx on a DigitalOcean Droplet, behind Cloudflare

---

## Running locally

**Prerequisites:** Docker with Docker Compose.

```bash
git clone https://github.com/Seraph2000/shipandearn.git
cd shipandearn
cp .env.example .env
```

Edit `.env` and set at least:

| Variable | Needed for | Where to get it |
|---|---|---|
| `SECRET_KEY` | Sessions (required) | Any long random string |
| `ANTHROPIC_API_KEY` | AI listing writer | [console.anthropic.com](https://console.anthropic.com) |
| `STRIPE_*` | Checkout/upgrades (optional locally) | Stripe Dashboard → test mode |

Then start the app and database:

```bash
docker compose up --build
```

Open <http://localhost:5000>. Database migrations run automatically when the container starts. Sign up for an account to get started.

For production deployment, see [runbook.md](runbook.md).

---

## Project layout

```
app.py            Flask routes and app setup
models.py         SQLAlchemy models
config.py         Settings loaded from .env
meo/ai.py         AI listing writer (Claude)
templates/        Jinja2 templates (HTMX + Tailwind)
migrations/       Alembic database migrations
scripts/          One-off admin scripts (e.g. Stripe promo prices)
deploy/           Server provisioning, deploy script, Nginx config
```

---

## Roadmap

What's shipped and what's next is in [roadmap.md](roadmap.md), with smaller open tasks in [TODO.md](TODO.md).

---

## Licence

Licensed under the [Apache License 2.0](LICENSE). © 2026 Seraphina Anderson.
