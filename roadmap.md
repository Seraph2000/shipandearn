# Earnstack — Roadmap

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

## Earnstack Release Roadmap

### v0.1.1 — completed (micro-earnings foundation)
- [x] Prolific poller (Bearer token auth)
- [x] Task scoring engine
- [x] SQLite storage + CSV earnings log
- [x] Streamlit dashboard
- [x] Claude AI summarisation (cached)
- [x] Manual task entry

> Pivoting away from micro-task scraping. v0.2.0 is a ground-up redesign.

---

### v0.2.0 — The Pivot (current milestone)

Strip out the micro-earnings layer. Redesign around the creative engineering income model.

**Core data model**
- [ ] Asset entity — name, type (tool / plugin / template / micro-SaaS / SaaS), complexity tier, status, time invested
- [ ] Triple Loop per asset — product listing, gig listing, service offering (links, status, income)
- [ ] Income log — earnings per asset per stream

**Sprint Board**
- [ ] 4-week onboarding sprint mode
- [ ] Complexity tiers: Quick Win / Medium Build / Micro-SaaS / Full SaaS
- [ ] Daily action queue — what to build or publish today

**Gig Generator** ← core feature
- [ ] Input: asset name, description, tech stack
- [ ] Output: Fiverr gig title + description + pricing tiers
- [ ] Output: Upwork project listing
- [ ] Output: Gumroad / product page description
- [ ] Output: README draft

**Dashboard**
- [ ] Asset library view
- [ ] Income per asset and per stream
- [ ] Sprint progress

---

### v0.3.0 — Triple Loop Tracker

Once assets are live, track all three streams properly.

- [ ] Marketplace status per asset (live / pending / draft) for each platform
- [ ] Income logging per stream (product vs gig vs service)
- [ ] Gig performance — views, orders, conversion (manual input or API where available)
- [ ] Service pipeline — enquiries, proposals sent, won/lost

---

### v0.4.0 — Pipeline + Analytics

Graduate from sprint mode into a continuous pipeline.

- [ ] Continuous pipeline mode (replaces sprint once you have assets running)
- [ ] Asset performance ranking — which builds earn most
- [ ] Marketplace performance — which platforms convert best
- [ ] AI-suggested next build — gaps in your stack, underserved tiers
- [ ] Monthly income summary (auto-generated)

---

### v0.5.0 — Portfolio

- [ ] Auto-generated portfolio page from asset library
- [ ] Shareable link — doubles as a hiring portfolio
- [ ] Case study generator per asset (AI-drafted, editable)

---

### v1.0.0 — Earnstack as a Product

Open Earnstack to other creative engineers. Position: *"The income cockpit for indie developers."*

**Pricing strategy**
Start at £4.99/month — utility pricing, low friction, validates before building premium tiers.

| Tier | Price | Features |
|---|---|---|
| **Starter** | £4.99/mo | Dashboard, sprint board, income tracker, gig templates, manual entry |
| **Pro** | £12.99/mo | API integrations (Upwork, Fiverr, Stripe), AI gig generator, weekly income reports |
| **Studio** | £29.99/mo | White-labelling, team dashboards, custom automations, priority support |

**Payments & access control**
- [ ] Stripe or Paddle (both handle EU VAT automatically)
- [ ] JWT-based auth — lock premium routes (Sprint Board, Gig Generator) behind tier check
- [ ] Feature flags (`is_paid_user`) to toggle advanced features
- [ ] 14-day free trial before requiring payment

**Infrastructure**
- [ ] Multi-user auth (email + password or OAuth via Clerk/Supabase Auth)
- [ ] Per-user data isolation
- [ ] Public landing page + pricing page

**Distribution**
- [ ] Fiverr/Upwork bundle: *"I'll set up your developer income dashboard (Earnstack-powered)"*
- [ ] GitHub Marketplace: open-source base with paid extensions
- [ ] Product Hunt / Indie Hackers: launch hosted version with free tier
- [ ] Self-hosted licence option: pay once, deploy your own instance

**Product**
- [ ] Onboarding sprint flow baked into signup
- [ ] Self-serve gig copy wizard (users generate their own output)
- [ ] Conversion dashboard — shows how much each asset has earned
