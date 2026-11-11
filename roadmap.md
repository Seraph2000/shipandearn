# Ship & Earn — Roadmap

> **Domains:** `shipandearn.com` (primary) + `shipandearn.dev` (alias) — both on Cloudflare, pointing at the Droplet.
> `earnstack.dev` — owned by Seraphina, consider selling.

**Goal:** help creative engineers turn what they build into stacked income — products, gigs, and services from every asset.

---

## The Model

Every build generates three income streams — the Triple Loop:

| Stream | How | Platforms |
|---|---|---|
| **Product** | Sell the tool itself | Gumroad, Ko-fi, Etsy, Itch.io, GitHub Sponsors |
| **Gig** | Sell customisation / integration | Fiverr, Upwork |
| **Service** | Sell bespoke builds & deployments | Upwork, direct clients |

---

## Income Targets

| Stage | Monthly target |
|---|---|
| First assets live | £200–£500 |
| 10–20 tools + gigs running | £500–£1500 |
| Micro-SaaS + services | £1500–£3000 |
| Full SaaS + freelance | £3000–£5000 |

---

## Ship & Earn Release Roadmap

### v0.1.1 — completed (micro-earnings foundation)
- [x] Prolific poller (Bearer token auth)
- [x] Task scoring engine
- [x] SQLite storage + CSV earnings log
- [x] Streamlit dashboard
- [x] Claude AI summarisation (cached)
- [x] Manual task entry

> Pivoting away from micro-task scraping. v0.2.0 is a ground-up redesign.

---

### v0.2.0 — The Pivot ✓ shipped

Ground-up redesign around the creative engineering income model.

- [x] Asset library (type, complexity tier, status, time invested)
- [x] Triple Loop income tracking — product, gig, service streams per asset
- [x] Sprint Board — 4-week onboarding sprints with complexity tiers
- [x] Gig Generator — Claude-powered copy for Fiverr, Upwork, product pages, README
- [x] Goal tracking + progress dashboard
- [x] Docker + DigitalOcean Droplet deployment stack
- [x] Flask-Migrate for schema migrations

---

### v1.0.0 — Commercial Launch (next)

Open Ship & Earn to other creative engineers. Position: *"The income cockpit for indie developers."*

Scope is intentionally lean — get a paying user live, then let real usage drive v1.1+.

**Pricing**

| Tier | Price | Features |
|---|---|---|
| **Lifetime** | £4.99 one-time | Dashboard + income tracker + asset library + sprint board — forever |
| **Pro** | £12.99/mo | Everything + unlimited AI Gig Generator |
| **Studio** | £29.99/mo | Everything in Pro + white-labelling + teams — *Coming Soon* |

**Pay-as-you-go (v1.1)**
- **Gig Credits** — £1.99 per generation, no subscription needed
- Lowers barrier for casual users; power users upgrade to Pro

**Must-haves (launch blockers)**
- [x] Multi-user auth — email + password via Flask-Login + Werkzeug (no third-party auth services)
- [x] Per-user data isolation
- [x] Stripe checkout + webhook (lifetime one-time + Pro subscription)
- [x] Feature gating — Gig Generator behind Pro; everything else on Lifetime
- [x] Public landing page + pricing page
- [ ] Upgrade CTA on locked feature pages (not just a flash message)
- [ ] Gig Generator demo/preview for non-Pro users
- [ ] Stripe products created + price IDs in .env

**Distribution (at launch)**
- [ ] Product Hunt / Indie Hackers
- [ ] Fiverr/Upwork bundle: *"I'll set up your developer income dashboard"*
- [ ] GitHub: open-source base with paid hosted version

---

### v1.1.0 — Promo pricing + non-tech assets ✓ shipped

- [x] Non-Tech Asset class — rental, creative, task, venture, funding categories (+ custom)
- [x] Live promo pricing — flash-sale Lifetime price + Pro trial promo, config-driven end dates
- [x] Mobile layout fixes across sprint board, goal fields, and grid layouts

---

### v1.2.0 — Freelance tracking + full asset/income CRUD (in progress)

- [x] Freelance / Gig Work asset class — track contract/platform income (Mercor, Upwork, direct clients, etc.) alongside tech and non-tech assets, with its own categories (AI Training, Contract Dev, Writing, Consulting + custom) and a Client/Platform field
- [x] Delete assets — was create/edit only; deleting now cascades to that asset's income streams and income entries
- [x] Edit and delete income entries — was log-only; entries can now be corrected or removed after the fact
- [x] Fixed income history ordering — entries logged on the same date now sort deterministically (secondary sort by id), so edit/delete always act on the intended row

---

### Open Source Strategy (post-v1.0)

Don't open-source before v1.0.0. Get the hosted SaaS live and taking payments first.

**Sequence:**
1. v1.0.0 ships → first paying users
2. Open-source the core under **AGPL v3** — protects against commercial forks (anyone hosting a modified version must also open-source their changes)
3. Product Hunt launch: *"self-host free / hosted from £4.99/mo"*

**What to open:**
- Core app (dashboard, sprint board, income tracker, asset library)
- Data models + migrations
- Self-host docs + runbook
- Docker setup

**What stays closed (SaaS-only):**
- AI Gig Generator prompts
- Multi-user / team features
- Stripe integration
- Analytics + premium dashboard

**Licence change:** update `LICENSE` from proprietary → AGPL v3 at the point of open-sourcing. Until then the repo stays private and proprietary.

---

### Post-v1.0 Backlog

Features validated by real users before being scheduled into a release.

- Forgot password / reset flow — no recovery path exists today if a user forgets their password. Needs a transactional email provider first (none configured yet). See "Password Reset — Tech Spec" in [runbook.md](runbook.md).
- Triple Loop tracker — marketplace status, gig performance, service pipeline
- Continuous pipeline mode — replaces sprint once assets are running
- Asset performance analytics — which builds and platforms earn most
- AI-suggested next build — gaps in your stack, underserved tiers
- Auto-generated portfolio page + shareable link
- Case study generator per asset (AI-drafted, editable)
- Self-serve gig copy wizard
- API access + integrations (Upwork, Fiverr, Stripe income sync)
- Self-hosted licence option
- Marketing email opt-out for paying customers — separate transactional emails (receipts, account) from promotional ones (flash sales, etc.); let existing customers opt out of the latter without missing the former. Needed before we mailshot the customer base about pricing/promos — UK PECR/GDPR requires a clear unsubscribe path for marketing comms.

**Gig Generator — evolution**
Currently fun and novel — good enough for v1.0. Needs proper structure in a future release:
- Content-type specific intake forms — different questions per output type (Fiverr vs README vs product page need different inputs)
- Richer asset model — target audience, key features, pricing, screenshots, repo URL
- Separate gig assets from product assets — a SaaS shouldn't generate a Fiverr gig; a tool/plugin should
- Guardrails + quality scoring (integrate with guardrails + tech rubric as noted in earlier discussions)
