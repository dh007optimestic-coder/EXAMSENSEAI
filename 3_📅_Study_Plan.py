"""
pages/3_Study_Plan.py
----------------------
Shows the generated study plan with charts and day-by-day schedule.
"""

import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Study Plan", page_icon="📅")
st.title("📅 Your Study Plan")

plan    = st.session_state.get("study_plan")
subject = st.session_state.get("subject_name", "Your Subject")
weak    = st.session_state.get("weak_topics", [])
target  = st.session_state.get("target_score", 75)
days    = st.session_state.get("exam_days", 30)

if not plan:
    st.warning("⚠️ No plan yet. Go to **📄 Upload & Analyze** first.")
    st.stop()

# ── Summary ────────────────────────────────────────────────
st.markdown(f"### Subject: **{subject}** | Target: **{target}%** | Days: **{days}**")
st.info(f"🧠 Strategy: {plan.get('strategy','')}")
st.markdown("---")

# ── Weekly Goals ───────────────────────────────────────────
st.markdown("## 📆 Weekly Goals")
for week in plan.get("weekly_goals", []):
    with st.expander(f"Week {week['week']} — {week.get('focus','')}"):
        for t in week.get("topics", []):
            is_weak = any(w.lower() in t.lower() for w in weak)
            st.markdown(f"- {t}" + (" ⚠️ *(weak topic)*" if is_weak else ""))

st.markdown("---")

# ── Daily Plan ─────────────────────────────────────────────
st.markdown("## 🗓️ Day-by-Day Schedule")
daily = plan.get("daily_plan", [])

if daily:
    # Hours bar chart
    fig = go.Figure(go.Bar(
        x=[f"Day {d['day']}" for d in daily[:14]],   # show first 14 days
        y=[d.get("hours", 3) for d in daily[:14]],
        marker_color="#0f3460",
        text=[d.get("hours", 3) for d in daily[:14]],
        textposition="auto"
    ))
    fig.update_layout(
        title="Study Hours — First 2 Weeks",
        xaxis_title="Day", yaxis_title="Hours",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=280
    )
    st.plotly_chart(fig, use_container_width=True)

    # Day cards
    for d in daily:
        priority  = d.get("priority","Medium")
        icon      = {"High":"🔴","Medium":"🟡","Low":"🟢"}.get(priority,"⚪")
        is_weak   = any(w.lower() in d.get("topic","").lower() for w in weak)
        label     = f"**Day {d['day']}** — {d.get('topic','?')} {icon}" + (" ⚠️" if is_weak else "")

        with st.expander(label):
            st.markdown(f"**Unit:** {d.get('unit','')}")
            st.markdown(f"**Hours:** {d.get('hours',3)}")
            st.markdown("**Tasks:**")
            for task in d.get("tasks", []):
                st.markdown(f"  ✅ {task}")

st.markdown("---")

# ── Tips ───────────────────────────────────────────────────
st.markdown("## 💡 Study Tips")
for tip in plan.get("study_tips", []):
    st.markdown(f"- 💡 {tip}")

st.markdown("---")
st.markdown("## 🔄 Final Week Strategy")
if plan.get("last_week_plan"):
    st.success(plan["last_week_plan"])
