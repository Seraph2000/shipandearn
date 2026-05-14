import re
import requests
from bs4 import BeautifulSoup
from meo.pollers.base import BasePoller
import config


class ClickworkerPoller(BasePoller):
    name = "Clickworker"

    def is_configured(self) -> bool:
        return bool(config.CLICKWORKER_EMAIL and config.CLICKWORKER_PASSWORD)

    def _get_session(self) -> requests.Session:
        s = requests.Session()
        s.headers.update({"User-Agent": "Mozilla/5.0"})
        login_page = s.get("https://workplace.clickworker.com/en/login", timeout=10)
        soup = BeautifulSoup(login_page.text, "html.parser")
        csrf_input = soup.find("input", {"name": "csrfmiddlewaretoken"})
        token = csrf_input["value"] if csrf_input else ""
        s.post(
            "https://workplace.clickworker.com/en/login",
            data={
                "username": config.CLICKWORKER_EMAIL,
                "password": config.CLICKWORKER_PASSWORD,
                "csrfmiddlewaretoken": token,
            },
            timeout=10,
        )
        return s

    def poll(self):
        s = self._get_session()
        r = s.get("https://workplace.clickworker.com/en/jobs", timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        tasks = []
        for row in soup.select(".job-list-item, .task-item, [data-job-id]"):
            title_el = row.select_one(".job-title, h3, .title")
            pay_el   = row.select_one(".reward, .pay, .price")
            time_el  = row.select_one(".duration, .time, .estimated-time")
            link_el  = row.select_one("a[href]")

            if not title_el:
                continue

            title   = title_el.get_text(strip=True)
            pay     = _parse_amount(pay_el.get_text(strip=True) if pay_el else "0")
            minutes = _parse_minutes(time_el.get_text(strip=True) if time_el else "15")
            link    = link_el["href"] if link_el else ""
            if link and not link.startswith("http"):
                link = "https://workplace.clickworker.com" + link

            tasks.append({
                "platform": "Clickworker",
                "task_id": link or title,
                "title": title,
                "pay": pay,
                "estimated_minutes": minutes,
                "category": "clickwork",
                "link": link,
                "timestamp": "",
                "metadata": {},
            })
        return tasks


def _parse_amount(text: str) -> float:
    m = re.search(r"[\d.]+", text.replace(",", "."))
    return float(m.group()) if m else 0.0


def _parse_minutes(text: str) -> float:
    hours = re.search(r"(\d+)\s*h", text)
    mins  = re.search(r"(\d+)\s*m", text)
    total = 0.0
    if hours:
        total += float(hours.group(1)) * 60
    if mins:
        total += float(mins.group(1))
    if not total:
        m = re.search(r"[\d.]+", text)
        total = float(m.group()) if m else 15.0
    return total
