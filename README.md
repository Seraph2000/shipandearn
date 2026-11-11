# Ship & Earn

**Turn what you build into stacked income — products, gigs, and services from every asset.**

Ship & Earn is an income command centre. You add the things you build or do (tools, plugins, templates, SaaS products, freelance work, rentals, creative projects). It then helps you earn from each one in three ways, tracks what you're earning, and writes your marketplace copy for you.

Live at [shipandearn.com](https://shipandearn.com).

---

## Who it's for

- **Indie developers and creative engineers** who ship side projects and want to turn each one into income
- **Freelancers and gig workers** juggling several platforms (Fiverr, Upwork, Mercor, direct clients) who want one place to see what's coming in
- **Anyone with several small income streams** — including non-tech ones such as rentals, creative work or tasks — who wants to see their monthly total at a glance

---

## The Triple Loop

Every asset you build has three income streams waiting to be activated:

| Stream | What it is | Example platforms |
|---|---|---|
| **Product** | Sell the thing itself | Gumroad, Ko-fi, Itch.io |
| **Gig** | Sell setup, customisation, integration | Fiverr, Upwork |
| **Service** | Sell bespoke builds using the same skills | Upwork, direct clients |

---

## Features

- **Asset Library** — track tech assets, non-tech assets and freelance/gig work, with status, stack or client, and time invested (with a built-in timer)
- **Triple Loop tracker** — log the product listing, gig and service offering for each asset, with platform, pricing and status
- **Sprint Board** — organise builds into 4-week sprints or release cycles and assign assets by week
- **Gig Generator** — AI-written Fiverr gigs, Upwork listings, product descriptions and GitHub READMEs for each asset (powered by Claude)
- **Income log** — record, edit and delete payments by asset, stream and platform
- **Goal tracking** — set a monthly income target and watch it fill up
- **Accounts and plans** — email/password auth, with Stripe checkout for the Lifetime and Pro plans

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
| `ANTHROPIC_API_KEY` | Gig Generator | [console.anthropic.com](https://console.anthropic.com) |
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
meo/ai.py         Claude-powered Gig Generator
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
