# Earnstack — Roadmap

**Goal:** earn something every single day. Start with coffee money, scale to £1000/month, then £4000/month.

---

## Phase 0 — Earning from day one (this week)

These require no waiting, no approval, no application. Sign up and earn today.

| Platform | Type | Est. pay | Sign-up time | Link |
|---|---|---|---|---|
| **Freecash** | Offers, surveys, videos | £0.10–£2/task | 5 min | freecash.com |
| **Swagbucks** | Offers, surveys, videos | £0.10–£2/task | 5 min | swagbucks.com |
| **PrizeRebel** | Offers, surveys | £0.10–£1.50/task | 5 min | prizerebel.com |
| **InboxDollars** | Surveys, videos, emails | £0.05–£1/task | 5 min | inboxdollars.com |

**Daily target from Phase 0:** £2–£5 (a coffee, reliably)

---

## Phase 1 — Core platforms (this week, 1–3 day wait)

Higher quality, better pay, slightly more setup.

| Platform | Type | Est. pay | Wait | Notes |
|---|---|---|---|---|
| **Prolific** | Academic surveys | £6–12/hr avg | 1–2 days | Best survey platform. Demographic questionnaire unlocks studies. |
| **Clickworker** | Micro-tasks | £5–9/hr | Same day | Skills assessment (~15 min). Volume builds with rating. |
| **UserTesting** | Usability tests | £8–10/20min test | 2–3 days | Short practice test required. Tests arrive by email. |

**Daily target from Phase 0 + 1:** £8–£20

---

## Phase 2 — High-value platforms (apply this week, start next week)

These have an application or short test. Worth prioritising given your background.

| Platform | Type | Est. pay | Notes |
|---|---|---|---|
| **Outlier.ai** | AI training (writing/coding tasks) | £15–25/hr | Best hourly rate of any micro-platform. Apply at outlier.ai — writing sample required. |
| **DataAnnotation.tech** | AI annotation | £12–18/hr | Similar to Outlier, more consistent volume. Short skills test. |
| **Appen** | AI data labelling | £10–14/hr | Established, UK-friendly. Project-based — availability varies. |
| **Respondent.io** | Research interviews (phone/video) | £50–150/interview | Low volume but very high pay per session. Apply to studies that match your profile. |

**Monthly target from Phase 0–2:** £600–£1000

---

## Phase 3 — Stack to £1000/month

Once Phase 0–2 are running, optimise the mix.

- Prioritise Outlier + DataAnnotation for hourly rate
- Use Prolific for consistent daily studies
- Treat Freecash/Swagbucks as passive fill (while waiting for kettle to boil)
- Accept 1–2 Respondent interviews per month when they come in
- Log everything in Earnstack — use the earnings data to cut platforms that underperform

---

## Phase 4 — Scale to £3000–£4000/month (freelance hybrid)

Micro-tasks alone cap out around £900/month at sustainable effort.
Closing the gap requires stacking freelance income on top.

| Income stream | Target |
|---|---|
| Micro-tasks (all platforms) | £600–£900/month |
| Micro-gigs (Upwork/Fiverr) | £400–£800/month |
| Small freelance contracts | £1500–£2500/month |
| **Total** | **£3000–£4000/month** |

Earnstack v0.2.0 will surface micro-gig opportunities automatically (Upwork RSS, Fiverr search scraping).

---

## Earnstack Roadmap

### v0.1.0 — current build
- [x] Freecash poller
- [x] Prolific poller (session cookie)
- [x] Clickworker poller
- [x] Task scoring engine
- [x] SQLite storage + CSV earnings log
- [x] Streamlit dashboard
- [x] Claude Haiku AI summarisation (cached)
- [x] Manual task entry

### v0.2.0 — full platform coverage

**Phase 0 pollers (instant sign-up, low pay)**
- [ ] Swagbucks poller (scrape or API)
- [ ] PrizeRebel poller (scrape)
- [ ] InboxDollars poller (scrape)

**Phase 1 pollers (1–3 day wait, higher quality)**
- [ ] UserTesting poller (email parsing via IMAP)

**Phase 2 pollers (application required, best hourly rate)**
- [ ] Outlier.ai poller (scrape available tasks post-login)
- [ ] DataAnnotation.tech poller (scrape)
- [ ] Appen poller (project feed scrape)
- [ ] Respondent.io poller (API or scrape — study listings)

**System improvements**
- [ ] UHRS automation (Playwright)
- [ ] Historical speed modelling (actual vs estimated minutes)
- [ ] Micro-gig discovery (Upwork RSS, Fiverr)
- [ ] Push notifications (task alert when high-score study appears)
- [ ] Personalised earning forecasts
- [ ] ROI prediction per platform
- [ ] Time-tracking integration
- [ ] Weekly/monthly summary report (auto-generated)

### v0.3.0 — SaaS scaleup

Move from a personal local tool to a hosted, multi-user product on a subscription paywall.

**Infrastructure**
- [ ] Replace Streamlit with a proper web frontend (React or HTMX)
- [ ] FastAPI backend — expose pollers and scoring as an API
- [ ] Cloud hosting (single server to start — Railway, Render, or VPS)
- [ ] Central poller infrastructure — pollers run server-side, not on user machines

**User accounts & monetisation**
- [ ] User authentication (email + password, or OAuth)
- [ ] Stripe integration — subscription paywall (target: £3–5/month)
- [ ] Per-user credential storage (encrypted platform credentials)
- [ ] Free tier: Prolific + Freecash only; paid tier: all platforms

**Product**
- [ ] Onboarding flow — platform account setup guide baked into the UI
- [ ] Platform health indicators (poller last seen, known breakages)
- [ ] Public landing page + pricing page

---

## Daily routine (target: 20–30 min/day)

| Time | Action | Expected earn |
|---|---|---|
| Morning (10 min) | Check dashboard, start best Prolific/Outlier task | £2–£8 |
| Passive | Freecash/Swagbucks in background (videos, offers) | £0.50–£2 |
| Midday (5 min) | Grab any new Prolific studies | £1–£5 |
| Evening (5 min) | Log completions, check tomorrow's pipeline | — |

**Conservative daily floor: £3–£5 (coffee money, every day)**
**Good day: £15–£25**
