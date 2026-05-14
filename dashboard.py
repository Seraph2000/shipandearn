import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime
import streamlit as st
import pandas as pd
from meo import storage, ai
from meo.scoring import score_task

st.set_page_config(page_title="Earnstack", layout="wide")
storage.init_db()

st.title("Earnstack")

# ── Earnings summary ──────────────────────────────────────────────────────────
today = storage.get_earnings_today()
month = storage.get_earnings_this_month()
target = 1000.0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Today",        f"£{today['total_pay']:.2f}", f"{today['tasks_completed']} tasks")
col2.metric("This month",   f"£{month['total_pay']:.2f}", f"{month['tasks_completed']} tasks")
col3.metric("Monthly target", f"£{target:.0f}")
progress = min(month["total_pay"] / target, 1.0)
col4.metric("Progress", f"{progress*100:.0f}%")
st.progress(progress)

st.divider()

# ── Available tasks ───────────────────────────────────────────────────────────
tasks = storage.get_available_tasks()
st.subheader(f"Available tasks ({len(tasks)})")

if not tasks:
    st.info("No tasks yet. Run `python main.py poll` or add one manually below.")
else:
    for i, task in enumerate(tasks):
        mins = task["estimated_minutes"] or 30
        hourly = task["pay"] / (mins / 60) if mins else 0
        label = (
            f"**[{task['score']:.0f}]** {task['platform']} — {task['title']} "
            f"| £{task['pay']:.2f} · {mins:.0f}min · £{hourly:.0f}/hr"
        )
        with st.expander(label):
            left, right = st.columns([3, 1])
            with left:
                if task["link"]:
                    st.markdown(f"[Open task]({task['link']})")
                if st.button("Summarise instructions", key=f"sum_{i}"):
                    with st.spinner("Summarising..."):
                        text = ai.summarise_instructions(
                            task["title"], task.get("metadata") or ""
                        )
                    st.text(text)
            with right:
                with st.form(key=f"complete_{i}"):
                    actual_mins = st.number_input(
                        "Actual minutes", min_value=1,
                        value=int(task["estimated_minutes"] or 15),
                        key=f"mins_{i}",
                    )
                    actual_pay = st.number_input(
                        "Actual pay (£)", min_value=0.0,
                        value=float(task["pay"] or 0), step=0.01,
                        key=f"pay_{i}",
                    )
                    if st.form_submit_button("Mark complete"):
                        storage.mark_completed(
                            task["platform"], task["task_id"],
                            actual_mins, actual_pay, task["title"],
                        )
                        st.rerun()

st.divider()

# ── Manual task entry ─────────────────────────────────────────────────────────
with st.expander("Add task manually"):
    with st.form("manual_task"):
        m_platform = st.selectbox(
            "Platform", ["Prolific", "Freecash", "Clickworker", "UHRS", "UserTesting", "Respondent", "Other"]
        )
        m_title   = st.text_input("Title")
        m_pay     = st.number_input("Pay (£)", min_value=0.0, step=0.01)
        m_minutes = st.number_input("Estimated minutes", min_value=1, value=15)
        m_link    = st.text_input("Link (optional)")
        if st.form_submit_button("Add"):
            if m_title:
                task = {
                    "platform": m_platform,
                    "task_id": f"manual_{datetime.now().timestamp()}",
                    "title": m_title,
                    "pay": m_pay,
                    "estimated_minutes": m_minutes,
                    "category": "manual",
                    "link": m_link,
                    "timestamp": datetime.now().isoformat(),
                    "metadata": {},
                }
                task["score"] = score_task(task)
                storage.upsert_task(task)
                st.success("Task added!")
                st.rerun()

st.divider()

# ── Completion history ────────────────────────────────────────────────────────
st.subheader("Recent completions")
completions = storage.get_recent_completions(30)
if completions:
    df = pd.DataFrame(completions)[["completed_at", "platform", "title", "pay", "actual_minutes"]]
    df["£/hr"] = (df["pay"] / df["actual_minutes"] * 60).round(2)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No completions yet.")
