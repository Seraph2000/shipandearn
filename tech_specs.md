Perfect — if this is a personal tool for you, then we can design it to be lean, fast, spreadsheet‑driven, and Claude‑friendly.Below is a full technical specification + daily task breakdown, structured exactly the way Claude digests best: clear sections, explicit components, and zero ambiguity.

This is ready to paste straight into Claude as an implementation brief.

📘 TECHNICAL SPECIFICATION — “Micro‑Earnings Optimiser (MEO)”A lightweight personal platform for automating micro‑task discovery, scoring, and tracking.

1. System OverviewMEO is a Python‑based micro‑earnings command centre that:

polls micro‑task platforms

extracts available tasks

scores them based on ROI

logs completed tasks

updates a spreadsheet‑based earnings dashboard

provides daily recommendations

pre‑drafts content using an LLM

stores minimal metadata in a lightweight DB

The system is optimised for speed, low maintenance, and personal use.

2. Core Components

2.1 Task Polling Layer

Python services that run on a schedule (cron or simple loop):

Prolific: RSS feed polling + HTML scrape fallback

Clickworker: HTML scraping

UHRS: browser automation (Playwright) to read task list

UserTesting: email parsing (IMAP) + optional browser automation

Respondent: API polling

Micro‑gigs: search queries (Upwork/Fiverr) via scraping or RSS

Each poller outputs a normalised task object.

2.2 Task Normalisation Schema

Every task is converted into a unified structure:

{
  "platform": "Prolific",
  "task_id": "...",
  "title": "...",
  "pay": 3.20,
  "estimated_minutes": 8,
  "category": "survey",
  "link": "...",
  "timestamp": "...",
  "metadata": {...}
}

2.3 Task Scoring Engine

A Python module that assigns a score from 0–100 based on:

£/hour

your historical speed multiplier

cognitive load

approval rate

time window

automation potential

platform reliability

Formula (Claude‑friendly):

score = (
    (pay / (estimated_minutes / 60)) * 4
    + historical_speed_factor * 2
    + platform_reliability * 1.5
    + automation_potential * 1.5
)

Outputs a ranked list of tasks.

2.4 Automation Layer

Uses Playwright for:

opening tasks

pre‑filling demographic fields

navigating UHRS

capturing task metadata

auto‑opening micro‑gigs

This layer never completes tasks fully — it prepares the environment.

2.5 AI Assistance Layer

LLM‑powered functions:

summarise long instructions

generate short‑answer responses

draft UserTesting commentary

generate regex

generate Python snippets

summarise UHRS guidelines

write Respondent application answers

All outputs are editable before submission.

2.6 Data Storage

Lightweight, minimal:

SQLite for:

tasks

completions

daily earnings

historical speed

scoring metadata

CSV/Excel for:

daily earnings log

weekly/monthly summaries

platform breakdowns

task history

This keeps everything spreadsheet‑friendly.

2.7 Dashboard Layer

Built with Streamlit or FastAPI + HTMX:

Today’s tasks (ranked)

Earnings today

Earnings this week

Earnings this month

Time spent vs money earned

Platform breakdown

Task history

“Start next task” button

3. Daily Workflow (User Experience)

This is the part Claude will use to design flows.

3.1 Morning (5–10 minutes)

System auto‑polls all platforms

You open dashboard

You see:

3–10 available tasks

each with score + estimated minutes

You click Start Best Task

Browser opens with:

task page

pre‑summarised instructions

pre‑drafted answers (if applicable)

You complete the task manually.

3.2 Midday (5–10 minutes)

Quick check for new tasks

Usually 1–2 Prolific studies

1–2 UHRS tasks

Optional micro‑gig surfaced

3.3 Evening (5 minutes)

System logs earnings

Updates spreadsheet

Generates daily summary:

tasks completed

time spent

£ earned

tomorrow’s predicted opportunities

4. Daily Task Breakdown (for Claude to automate)

4.1 Automated Tasks

Poll Prolific every 2 minutes

Poll Clickworker every 10 minutes

Poll UHRS every 15 minutes

Poll Respondent every 30 minutes

Parse UserTesting emails

Score all tasks

Update dashboard

Update earnings spreadsheet

Generate pre‑drafted content

Summarise instructions

Prepare browser automation

4.2 User Tasks (your part)

Total time: 15–35 minutes/day

Complete 1–3 Prolific studies

Complete 1–4 UHRS/Clickworker tasks

Accept 1 micro‑gig every 2–3 days

Review Respondent applications

Approve daily earnings log

Everything else is automated.

5. MVP Feature List

v1 (2–3 weeks)

Prolific + Clickworker polling

Task scoring engine

SQLite storage

Spreadsheet earnings log

Basic dashboard

LLM summarisation + answer drafting

Manual task completion

v2

UHRS automation

Respondent API

Micro‑gig discovery

Historical speed modelling

ROI prediction

v3

Full automation layer

Notifications

Time‑tracking

Personalised earning forecasts

6. Non‑Goals (for Claude to ignore)

Full automation of task completion

Multi‑user support

Heavy UI

Cloud scaling

Payment integration

This keeps the system lean and personal.