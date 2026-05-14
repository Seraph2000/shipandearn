import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# v1 platforms
PROLIFIC_SESSION_COOKIE = os.getenv("PROLIFIC_SESSION_COOKIE", "")
CLICKWORKER_EMAIL       = os.getenv("CLICKWORKER_EMAIL", "")
CLICKWORKER_PASSWORD    = os.getenv("CLICKWORKER_PASSWORD", "")

# v2 — Phase 0
SWAGBUCKS_EMAIL       = os.getenv("SWAGBUCKS_EMAIL", "")
SWAGBUCKS_PASSWORD    = os.getenv("SWAGBUCKS_PASSWORD", "")
PRIZEREBEL_EMAIL      = os.getenv("PRIZEREBEL_EMAIL", "")
PRIZEREBEL_PASSWORD   = os.getenv("PRIZEREBEL_PASSWORD", "")
INBOXDOLLARS_EMAIL    = os.getenv("INBOXDOLLARS_EMAIL", "")
INBOXDOLLARS_PASSWORD = os.getenv("INBOXDOLLARS_PASSWORD", "")

# v2 — Phase 1
USERTESTING_IMAP_HOST     = os.getenv("USERTESTING_IMAP_HOST", "imap.gmail.com")
USERTESTING_IMAP_EMAIL    = os.getenv("USERTESTING_IMAP_EMAIL", "")
USERTESTING_IMAP_PASSWORD = os.getenv("USERTESTING_IMAP_PASSWORD", "")

# v2 — Phase 2
OUTLIER_EMAIL              = os.getenv("OUTLIER_EMAIL", "")
OUTLIER_PASSWORD           = os.getenv("OUTLIER_PASSWORD", "")
DATAANNOTATION_EMAIL       = os.getenv("DATAANNOTATION_EMAIL", "")
DATAANNOTATION_PASSWORD    = os.getenv("DATAANNOTATION_PASSWORD", "")
APPEN_EMAIL                = os.getenv("APPEN_EMAIL", "")
APPEN_PASSWORD             = os.getenv("APPEN_PASSWORD", "")
RESPONDENT_SESSION_COOKIE  = os.getenv("RESPONDENT_SESSION_COOKIE", "")

DB_PATH      = os.getenv("DB_PATH", "meo.db")
EARNINGS_CSV = os.getenv("EARNINGS_CSV", "earnings.csv")

POLL_INTERVALS = {
    "prolific":        int(os.getenv("POLL_PROLIFIC_SECS",        "120")),
    "clickworker":     int(os.getenv("POLL_CLICKWORKER_SECS",     "600")),
    "freecash":        int(os.getenv("POLL_FREECASH_SECS",        "300")),
    "swagbucks":       int(os.getenv("POLL_SWAGBUCKS_SECS",       "600")),
    "prizerebel":      int(os.getenv("POLL_PRIZEREBEL_SECS",      "600")),
    "inboxdollars":    int(os.getenv("POLL_INBOXDOLLARS_SECS",    "600")),
    "outlier":         int(os.getenv("POLL_OUTLIER_SECS",         "300")),
    "dataannotation":  int(os.getenv("POLL_DATAANNOTATION_SECS",  "300")),
    "appen":           int(os.getenv("POLL_APPEN_SECS",           "1800")),
    "respondent":      int(os.getenv("POLL_RESPONDENT_SECS",      "1800")),
}
