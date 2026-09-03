# Ship & Earn — Marketing Strategy

**Positioning:** *"The income cockpit for indie developers."*
**Target customer:** Creative engineers who build tools, plugins, and side projects and want to turn them into stacked income streams.

---

## Channel 1 — Product Hunt

Post a proper launch when you're ready to drive traffic. Product Hunt rewards good copy and a compelling demo.

**What to prepare:**
- A 60-second screen recording showing the full flow: add an asset → log income → run the Gig Generator → see dashboard totals
- A punchy tagline: *"Track every income stream from every build — products, gigs, and services in one place"*
- First comment from your account explaining the backstory (built it for yourself, now opening it up)
- Ask friends/community to upvote on launch day — timing matters (launch at 00:01 PST)

**When:** when you have time to engage comments on launch day.

---

## Channel 2 — Indie Hackers

Write a "how I built it" post. Indie Hackers audiences love:
- Honest revenue numbers (even if it's just yourself paying £17.98 to start)
- The pivot story (from micro-task scraper to income cockpit)
- The tech stack and why you chose it

**Post structure:**
1. What problem it solves
2. How you built it (Flask, Docker, Stripe, Claude API)
3. First revenue (even if it's you)
4. What's next

Link to shipandearn.com and the GitHub repo (once open-sourced).

---

## Channel 3 — GitHub (Open Source)

Open-source the core under **AGPL v3** post-v1.0. This drives:
- Developer trust (they can inspect the code)
- Organic discovery via GitHub search and stars
- A second Product Hunt launch: *"self-host free / hosted from £4.99"*

**What to open-source:** dashboard, sprint board, income tracker, asset library, Docker setup, migrations.
**What stays closed:** AI Gig Generator prompts, Stripe integration, team features.

Don't open-source until v1.0 is stable and taking payments. ✓ (Done — deploy first, open-source second.)

---

## Channel 4 — Reddit / Communities

Target subreddits and communities where indie developers hang out:
- r/SideProject
- r/indiehackers
- r/webdev
- r/freelance
- Hacker News (Show HN post)

Be genuinely helpful — don't just drop a link. Share the income tracking system, the Triple Loop model, lessons learned. The product link is secondary.

---

## Channel 5 — Facebook Groups

### Post copy (direct link, pre-Product Hunt)

**Version A — personal/story:**
> I've been quietly building a tool for people like me — freelancers and indie devs juggling multiple income streams with no clear picture of what's actually earning.
>
> It's called Ship & Earn. You track your income-generating assets (products, content, clients, gigs), plan your week in a sprint board, and watch your monthly income goal fill up in real time.
>
> Lifetime access is £4.99 right now — no subscription needed.
>
> Would love to know what you think: https://shipandearn.com

**Version B — problem-first:**
> Does anyone else track their income in a mess of spreadsheets? Freelance here, a product there, a few gigs somewhere else...
>
> I built Ship & Earn to fix that — one dashboard for all your income streams, with sprint planning and a live goal tracker built in.
>
> £4.99 lifetime access. Happy to answer any questions! https://shipandearn.com

**Version C — short & punchy:**
> Just launched Ship & Earn — a personal income cockpit for freelancers and indie makers.
> Track assets. Plan sprints. Hit your income goal.
> £4.99 lifetime. https://shipandearn.com

---

### Good Facebook groups to target

- **Indie Hackers & Side Hustlers** (search this — several large groups)
- **Female Founders & Entrepreneurs UK**
- **Freelancers UK**
- **Digital Nomads & Remote Workers**
- **Web Developers & Designers (UK)**
- **Make Money Online (legitimate/serious ones)**
- **Solo Founders & Bootstrappers**

---

### FB group posting tips

1. **Lead with the problem, not the product** — "anyone else struggle with X?" gets far more engagement than "I made a thing"
2. **Check group rules first** — many groups have specific days for self-promotion (e.g. "Share your project Sundays")
3. **Reply to every comment** — early engagement boosts reach in the algorithm
4. **Don't post the same copy to every group** — FB can suppress duplicate content; tweak each one slightly
5. **Post at peak times** — weekday evenings (7–9pm UK) or Saturday mornings tend to perform best
6. **Personal profile, not a page** — posts from real people outperform business page posts in groups

---

## UTM Tracking

Facebook (and many other platforms) strip the referrer header when users click links, so GA4 sees the traffic as "Direct" rather than the correct source. Fix this by adding UTM parameters to every link you share publicly.

**Instead of:** `https://shipandearn.com`
**Use:** `https://shipandearn.com?utm_source=facebook&utm_medium=social&utm_campaign=groups_launch`

GA4 reads UTM tags even when the referrer is stripped.

### Key UTM parameters

| Parameter | Example | Purpose |
|---|---|---|
| `utm_source` | `facebook`, `producthunt`, `indiehackers` | Where the traffic comes from |
| `utm_medium` | `social`, `referral`, `email` | The channel type |
| `utm_campaign` | `groups_launch`, `ph_launch` | The specific campaign |
| `utm_content` | `version_a`, `version_b` | Optional — for A/B testing post copy |

### Ready-to-use links

**Facebook groups:**
```
https://shipandearn.com?utm_source=facebook&utm_medium=social&utm_campaign=groups_launch
```

**Product Hunt:**
```
https://shipandearn.com?utm_source=producthunt&utm_medium=referral&utm_campaign=ph_launch
```

**Indie Hackers:**
```
https://shipandearn.com?utm_source=indiehackers&utm_medium=social&utm_campaign=ih_launch
```

Use the **Google Campaign URL Builder** to generate new tagged links for any channel. View results in GA4 under **Reports → Acquisition → Traffic acquisition**.

---

## Pricing reminder

| Tier | Price | Hook |
|---|---|---|
| Lifetime | £1.99 flash sale until 2026-09-30, then £6.99 one-time | Low barrier, forever access |
| Pro | 14 days free then £7.99/mo until 2026-09-30, then £12.99/mo | AI Gig Generator — the power feature |
| Studio | £29.99/mo | Coming Soon — teams + white-label |

Note: the £4.99 lifetime copy earlier in this doc (Facebook post drafts) reflects the price at the time those posts went out and hasn't been rewritten — new copy going forward should use the flash-sale price above.
