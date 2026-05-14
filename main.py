import argparse
import sys
import threading
import time

import config
from meo import storage
from meo.pollers import ALL_POLLERS
from meo.scoring import rank_tasks


def poll_all() -> list:
    storage.init_db()
    all_tasks = []
    for poller in ALL_POLLERS:
        if not poller.is_configured():
            print(f"[{poller.name}] skipped — not configured")
            continue
        print(f"[{poller.name}] polling...")
        tasks = poller.safe_poll()
        print(f"[{poller.name}] {len(tasks)} tasks found")
        all_tasks.extend(tasks)

    ranked = rank_tasks(all_tasks)
    for task in ranked:
        storage.upsert_task(task)

    if ranked:
        print(f"\nTotal: {len(ranked)} tasks | top score: {ranked[0]['score']} ({ranked[0]['title']})")
    else:
        print("No tasks found.")
    return ranked


def run_scheduler():
    storage.init_db()

    def poll_loop(poller, interval):
        while True:
            tasks = poller.safe_poll()
            from meo.scoring import score_task
            for task in tasks:
                task["score"] = score_task(task)
                storage.upsert_task(task)
            time.sleep(interval)

    for poller in ALL_POLLERS:
        interval = config.POLL_INTERVALS.get(poller.name.lower(), 300)
        t = threading.Thread(target=poll_loop, args=(poller, interval), daemon=True)
        t.start()
        status = f"every {interval}s" if poller.is_configured() else "skipped (not configured)"
        print(f"[{poller.name}] {status}")

    print("\nScheduler running. Start the dashboard in another terminal:")
    print("  streamlit run dashboard.py\n")
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("Stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Earnstack")
    parser.add_argument(
        "command", nargs="?", default="run",
        choices=["run", "poll"],
        help="run: start background scheduler | poll: one-shot fetch",
    )
    args = parser.parse_args()

    if args.command == "poll":
        poll_all()
    else:
        run_scheduler()
