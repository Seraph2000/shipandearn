import re
import requests
from meo.pollers.base import BasePoller
import config

# Freecash pays in "coins". Current rate: ~1000 coins = $1 USD.
# We convert to GBP using a fixed approximation (update if rate drifts).
_COINS_PER_USD = 1000
_USD_TO_GBP = 0.79


class FreecashPoller(BasePoller):
    name = "Freecash"

    def is_configured(self) -> bool:
        # No API key required for public offer wall scraping.
        # Returns True so it always runs; sign-up is free at freecash.com.
        return True

    def poll(self):
        # Freecash exposes a public JSON endpoint for their offer wall.
        # If this breaks, inspect network requests at freecash.com/offers.
        headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
        r = requests.get(
            "https://freecash.com/api/offers",
            headers=headers,
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()

        tasks = []
        for offer in data.get("data", data if isinstance(data, list) else []):
            coins = float(offer.get("coins", offer.get("reward", 0)) or 0)
            pay_gbp = round(coins / _COINS_PER_USD * _USD_TO_GBP, 3)
            category = _map_category(offer.get("category", offer.get("type", "")))
            tasks.append({
                "platform": "Freecash",
                "task_id": str(offer.get("id", offer.get("offer_id", ""))),
                "title": offer.get("name", offer.get("title", "Unnamed offer")),
                "pay": pay_gbp,
                "estimated_minutes": float(offer.get("time_to_complete", 10) or 10),
                "category": category,
                "link": offer.get("url", offer.get("link", "https://freecash.com/offers")),
                "timestamp": offer.get("created_at", ""),
                "metadata": {"coins": coins},
            })
        return tasks


def _map_category(raw: str) -> str:
    raw = raw.lower()
    if "survey" in raw:
        return "survey"
    if "video" in raw or "watch" in raw:
        return "video"
    if "game" in raw or "play" in raw:
        return "game"
    if "install" in raw or "app" in raw:
        return "offer"
    return "offer"
