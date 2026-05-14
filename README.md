# Earnstack

**Your income stack, optimised.**

Earnstack polls micro-earning platforms, scores every available task by £/hour, and surfaces the best opportunity in a single dashboard. Stop tab-switching. Open Earnstack, start the top task.

---

## What it does

- Polls Prolific, Clickworker, and Freecash automatically
- Scores tasks by hourly rate, platform reliability, and historical speed
- Ranks everything in one dashboard — best task always at the top
- Logs completions and tracks daily/monthly earnings
- Uses Claude AI to summarise task instructions so you can decide in seconds

---

## Platforms supported

| Platform | Type | Status |
|---|---|---|
| Prolific | Academic surveys | v0.1.0 |
| Clickworker | Micro-tasks | v0.1.0 |
| Freecash | Offers & surveys | v0.1.0 |
| Swagbucks, PrizeRebel, InboxDollars | Offer walls | v0.2.0 |
| UserTesting | Usability tests | v0.2.0 |
| Outlier.ai, DataAnnotation, Appen | AI training work | v0.2.0 |
| Respondent.io | Research interviews | v0.2.0 |

---

## Setup

**Requirements:** Python 3.10+

```bash
git clone https://github.com/YOUR_USERNAME/earnstack.git
cd earnstack
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and add your platform credentials. See `.env.example` for instructions on where to find each value.

---

## Running

```bash
# One-shot poll — fetch tasks now and exit
python main.py poll

# Background scheduler — polls on a continuous loop
python main.py run

# Dashboard — open in browser at localhost:8501
streamlit run dashboard.py
```

Run `main.py run` and `dashboard.py` in separate terminals for the full experience.

---

## Roadmap

See [roadmap.md](roadmap.md).

---

## Licence

Proprietary. See [LICENSE](LICENSE).
