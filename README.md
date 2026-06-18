# Ship & Earn

**Turn what you build into stacked income — products, gigs, and services from every asset.**

Ship & Earn is an income command centre for creative engineers. You add your builds — tools, plugins, templates, SaaS products — and it helps you monetise each one three ways, tracks what you're earning, and generates your marketplace copy for you.

---

## The Triple Loop

Every asset you build has three income streams waiting to be activated:

| Stream | What it is | Example platforms |
|---|---|---|
| **Product** | Sell the thing itself | Gumroad, Ko-fi, Itch.io |
| **Gig** | Sell setup, customisation, integration | Fiverr, Upwork |
| **Service** | Sell bespoke builds using the same skills | Upwork, direct clients |

---

## What Ship & Earn does

- **Asset Library** — track every tool, plugin, template, micro-SaaS, and SaaS you build with status, tech stack, and time invested
- **Triple Loop tracker** — log the product listing, gig, and service offering for each asset with platform, pricing, and status
- **Sprint Board** — organise builds into 4-week onboarding sprints or release cycles, assign assets by week
- **Gig Generator** — AI-powered copy generation: Fiverr gig, Upwork listing, product description, and GitHub README per asset (powered by Claude)
- **Income log** — track every payment by asset, stream, and platform
- **Goal tracking** — set a monthly income target and watch it fill up

---

## Tech stack

- **Backend:** Python, Flask, SQLAlchemy, Flask-Migrate
- **Database:** PostgreSQL
- **Frontend:** Jinja2, HTMX, Tailwind CSS
- **AI:** Claude (Anthropic) via the official SDK
- **Payments:** Stripe

---

## Running locally

```bash
docker compose up --build
```

Open `http://localhost:5000`. See [runbook.md](runbook.md) for the full deployment guide.

---

## Roadmap

See [roadmap.md](roadmap.md).

---

## Licence

Proprietary — All Rights Reserved. © Seraphina Anderson 2026. See [LICENSE](LICENSE).
