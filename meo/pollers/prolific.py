import requests
from meo.pollers.base import BasePoller
import config

# Prolific internal API — verify endpoints via browser devtools (F12 > Network tab)
# after logging in at app.prolific.com
_BASE = "https://app.prolific.com"


class ProlificPoller(BasePoller):
    name = "Prolific"

    def is_configured(self) -> bool:
        return bool(config.PROLIFIC_SESSION_COOKIE)

    def _session(self) -> requests.Session:
        s = requests.Session()
        # Grab the exact cookie name from devtools: Application > Cookies > prolific.com
        s.cookies.set("sessionid", config.PROLIFIC_SESSION_COOKIE, domain=".prolific.com")
        s.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        })
        return s

    def poll(self):
        s = self._session()
        r = s.get(f"{_BASE}/api/v1/studies/?status=active", timeout=10)
        r.raise_for_status()
        data = r.json()

        tasks = []
        for study in data.get("results", []):
            pay_pence = study.get("reward", 0) or 0
            tasks.append({
                "platform": "Prolific",
                "task_id": study.get("id", ""),
                "title": study.get("name", "Unnamed study"),
                "pay": round(pay_pence / 100, 2),           # pence -> pounds
                "estimated_minutes": float(study.get("estimated_completion_time", 15) or 15),
                "category": "survey",
                "link": f"{_BASE}/studies/{study.get('id', '')}",
                "timestamp": study.get("date_created", ""),
                "metadata": {"places_available": study.get("places_available", 0)},
            })
        return tasks
