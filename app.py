"""
app.py  ←  Run this file to start the app:
    streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="ExamSense AI",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
* { font-family: 'Nunito', sans-serif; }
.hero {
    background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
    padding: 3rem 2rem; border-radius: 20px;
    color: white; text-align: center; margin-bottom: 2rem;
}
.hero h1 { font-size: 3rem; font-weight: 800; margin: 0; }
.hero p  { font-size: 1.1rem; opacity: 0.85; margin: 0.6rem 0 0; }
.badge {
    background: #2ecc71; color: white;
    border-radius: 20px; padding: 0.3rem 1rem;
    font-weight: 700; display: inline-block; margin-top: 1rem;
}
.step {
    background: white; border-radius: 12px;
    padding: 1.2rem 1.5rem; margin: 0.5rem 0;
    border-left: 5px solid #0f3460;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.step h4 { margin: 0 0 0.3rem; color: #0f3460; }
.step p  { margin: 0; color: #555; font-size: 0.92rem; }
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🎓 ExamSense AI</h1>
    <p>Personalized Exam Preparation for B.Tech Students</p>
    <p>Analyze Syllabus · Build Study Plans · Take Mock Tests · Track Progress</p>
    <div class="badge">✅ 100% Offline — No API Key Required</div>
</div>
""", unsafe_allow_html=True)

# ── Status ─────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    if st.session_state.get("student_name"):
        st.success(f"✅ Logged in: {st.session_state['student_name']}")
    else:
        st.warning("⚠️ Profile not set")
with col2:
    if st.session_state.get("syllabus_data"):
        st.success("✅ Syllabus analyzed")
    else:
        st.info("📋 No syllabus yet")
with col3:
    if st.session_state.get("study_plan"):
        st.success("✅ Study plan ready")
    else:
        st.info("📅 No study plan yet")

st.markdown("---")

# ── Steps ──────────────────────────────────────────────────
st.markdown("## 📖 How to Use")

steps = [
    ("👤 Step 1 — Profile",
     "Go to Settings and fill in your name, roll number, and branch."),
    ("📄 Step 2 — Upload",
     "Upload your syllabus PDF and past exam papers. The app will extract all topics automatically."),
    ("📅 Step 3 — Study Plan",
     "Enter your weak topics and target score. Get a personalized day-by-day plan."),
    ("📝 Step 4 — Mock Test",
     "Take practice tests generated from your syllabus topics. Get scored instantly."),
    ("📈 Step 5 — Progress",
     "Tick off topics as you complete them. Watch your readiness score grow."),
]

for title, desc in steps:
    st.markdown(f"""
    <div class="step">
        <h4>{title}</h4>
        <p>{desc}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.info("👈 Use the **sidebar** to navigate. Start with **⚙️ Settings**.")
