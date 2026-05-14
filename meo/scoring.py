PLATFORM_RELIABILITY = {
    "Prolific":    0.95,
    "Freecash":    0.82,
    "Clickworker": 0.80,
    "UHRS":        0.85,
    "UserTesting": 0.90,
    "Respondent":  0.88,
}

AUTOMATION_POTENTIAL = {
    "survey":     0.6,
    "clickwork":  0.7,
    "offer":      0.5,
    "video":      0.9,
    "game":       0.3,
    "manual":     0.5,
}


def score_task(task: dict) -> float:
    pay = task.get("pay") or 0
    minutes = task.get("estimated_minutes") or 30
    historical_speed = task.get("historical_speed_factor", 1.0)
    category = task.get("category", "survey")
    platform = task.get("platform", "")

    reliability = PLATFORM_RELIABILITY.get(platform, 0.75)
    automation = AUTOMATION_POTENTIAL.get(category, 0.5)
    hourly_rate = pay / (minutes / 60)

    score = (
        hourly_rate * 4
        + historical_speed * 2
        + reliability * 1.5
        + automation * 1.5
    )
    return min(round(score, 1), 100.0)


def rank_tasks(tasks: list) -> list:
    for task in tasks:
        task["score"] = score_task(task)
    return sorted(tasks, key=lambda t: t["score"], reverse=True)
