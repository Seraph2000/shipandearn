# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

Ship & Earn: a Flask + PostgreSQL + HTMX/Tailwind income tracker, deployed with Docker on a DigitalOcean Droplet. This is a **public** repository licensed under Apache 2.0. See README.md, roadmap.md and runbook.md.

## RULE: Nothing confidential or private ever gets pushed to GitHub

This repository is public. Before every `git add`, commit or push, check that none of the following goes in:

- **Secrets:** API keys, tokens, passwords, webhook secrets, private keys, SSH keys, `.env` files. Use placeholders (`sk_live_...`, `price_...`) and keep real values in `.env`, which is gitignored. Add new variables to `.env.example` with placeholder values only.
- **Infrastructure details:** real server IPs, hostnames of private machines, SSH usernames beyond what's already documented. Use placeholders such as `<DROPLET_IP>`.
- **Personal information:** finances, budgets, home or family details, health, personal plans, contact details other than the public `hello@shipandearn.com`.
- **Real user or customer data:** database dumps, CSV exports, real emails or payment records. Use made-up sample data only.
- **Private business notes:** pricing negotiations, domain sales, anything not meant for the public.

Private notes belong in `private/` (gitignored), never in tracked files.

**If anything like this is found in a tracked file or in history:** stop, tell the user, and don't push. A committed secret must be revoked and removed from history (`git filter-repo`) before the next push.

When unsure whether something is private, ask before committing it.
