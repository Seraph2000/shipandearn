# Earnstack

**Turn what you build into stacked income — products, gigs, and services from every asset.**

Earnstack is an income command centre for creative engineers. You add your builds — tools, plugins, templates, SaaS products — and it helps you monetise each one three ways, tracks what you're earning, and generates your marketplace copy for you.

---

## The Triple Loop

Every asset you build has three income streams waiting to be activated:

| Stream | What it is | Example platforms |
|---|---|---|
| **Product** | Sell the thing itself | Gumroad, Ko-fi, Itch.io |
| **Gig** | Sell setup, customisation, integration | Fiverr, Upwork |
| **Service** | Sell bespoke builds using the same skills | Upwork, direct clients |

The Triple Loop compounds: your product validates your gig credibility, your gig work funds your next build, your service work pays you while the products scale.

Each stream has a status:

| Status | Meaning |
|---|---|
| **draft** | Added to Earnstack, not yet published on the platform |
| **live** | Published and active — earning or available to earn |
| **paused** | Was live, temporarily taken down |

---

## What Earnstack does

- **Asset Library** — track every tool, plugin, template, micro-SaaS, and SaaS you build with status, tech stack, and time invested
- **Triple Loop tracker** — log the product listing, gig, and service offering for each asset with platform, pricing, and status
- **Sprint Board** — organise builds into 4-week onboarding sprints or release cycles, assign assets by week
- **Gig Generator** — AI-powered copy generation: Fiverr gig, Upwork listing, product description, and GitHub README per asset (powered by Claude)
- **Income log** — track every payment by asset, stream, and platform
- **Goal tracking** — set a monthly income target and watch it fill up

---

## Asset types & complexity tiers

**Types:** tool · plugin · template · micro-SaaS · SaaS

**Complexity tiers:**

| Tier | Build time | Income target |
|---|---|---|
| Quick Win | Hours to days | £5–£30 product, £15–£50 gig |
| Medium Build | Days to weeks | £30–£150 product, £50–£200 gig |
| Micro-SaaS | Weeks | £150–£500/mo, £200–£500 gigs |
| SaaS | Months | £500+/mo, £500+ services |

---

## Tech stack

- **Backend:** Python, Flask, SQLAlchemy
- **Database:** PostgreSQL
- **Frontend:** Jinja2, HTMX, Tailwind CSS
- **AI:** Claude (Anthropic) via the official SDK

---

## Setup

**Requirements:** Python 3.10+, PostgreSQL

```bash
git clone https://github.com/Seraph2000/earnstack.git
cd earnstack
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` — you need three values:

```
ANTHROPIC_API_KEY=sk-ant-...
DATABASE_URL=postgresql://postgres:yourpassword@localhost/earnstack
SECRET_KEY=any-random-string
```

Create the database:

```bash
sudo -u postgres createdb earnstack
```

---

## Running

```bash
source venv/bin/activate
python app.py
```

Open `http://localhost:5000`.

---

## Roadmap

See [roadmap.md](roadmap.md).

---

## Licence

Proprietary — All Rights Reserved. © Seraphina Anderson 2026. See [LICENSE](LICENSE).
