"""
pages/5_Progress_Tracker.py
-----------------------------
Track completed topics + view mock test score history.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from database import save_progress, get_progress, get_results

st.set_page_config(page_title="Progress", page_icon="📈")
st.title("📈 Progress Tracker")

sid      = st.session_state.get("student_id", 1)
subject  = st.session_state.get("subject_name", "")
syllabus = st.session_state.get("syllabus_data", {})

# ── Topic Progress ─────────────────────────────────────────
st.markdown("## ✅ Topics Completed")

all_topics = [t for unit in syllabus.get("units", [])
              for t in unit.get("topics", [])]

if all_topics:
    saved     = get_progress(sid, subject)
    completed = st.multiselect("Tick off topics you've finished:",
                                options=all_topics, default=saved)

    if st.button("💾 Save Progress"):
        save_progress(sid, subject, completed)
        st.success("✅ Saved!")

    total   = len(all_topics)
    done    = len(completed)
    percent = round(done / total * 100, 1) if total > 0 else 0

    st.markdown(f"### {done} / {total} topics done ({percent}%)")
    st.progress(percent / 100)

    fig = go.Figure(go.Pie(
        labels=["Done ✅", "Remaining ⏳"],
        values=[done, total - done],
        marker_colors=["#2ecc71", "#ecf0f1"],
        hole=0.45
    ))
    fig.update_layout(height=260, paper_bgcolor="rgba(0,0,0,0)",
                      margin=dict(t=20,b=20))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("📌 Upload your syllabus in **📄 Upload & Analyze** first.")
    percent = 0

st.markdown("---")

# ── Test History ───────────────────────────────────────────
st.markdown("## 📝 Mock Test Scores")

history = get_results(sid)

if history:
    df = pd.DataFrame(history, columns=["Subject","Score","Total","Percent","Date"])
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%d %b")

    col1, col2, col3 = st.columns(3)
    col1.metric("Tests Taken",   len(df))
    col2.metric("Best Score",    f"{df['Percent'].max():.1f}%")
    col3.metric("Average Score", f"{df['Percent'].mean():.1f}%")

    fig = px.line(df.iloc[::-1], x="Date", y="Percent",
                  title="Score History",
                  markers=True,
                  color_discrete_sequence=["#0f3460"])
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(range=[0,105], title="Score (%)"),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("📌 No tests yet. Go to **📝 Mock Test** to start!")

st.markdown("---")

# ── Readiness Gauge ────────────────────────────────────────
st.markdown("## 🎯 Exam Readiness")

test_avg  = df["Percent"].mean() if history else 0
readiness = round(percent * 0.4 + test_avg * 0.6, 1)

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=readiness,
    gauge={
        "axis": {"range": [0,100]},
        "bar":  {"color": "#0f3460"},
        "steps":[
            {"range":[0,40],  "color":"#ffebee"},
            {"range":[40,70], "color":"#fff3cd"},
            {"range":[70,100],"color":"#d4edda"},
        ]
    },
    title={"text":"Readiness Score (%)"}
))
fig.update_layout(height=280, paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

if   readiness >= 80: st.success("🏆 Well prepared! Keep it up.")
elif readiness >= 60: st.warning("👍 Good — keep following your plan.")
elif readiness >= 40: st.warning("📚 Getting there — study daily!")
else:                 st.error("❌ Start studying now — follow your plan!")
