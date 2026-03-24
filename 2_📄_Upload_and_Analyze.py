"""
pages/2_Upload_and_Analyze.py
------------------------------
Upload syllabus + past papers → extract topics → generate study plan.
All done locally — no internet or API needed.
"""

import streamlit as st
from pdf_processor import read_pdf, read_multiple_pdfs
from engine import (extract_topics_from_syllabus,
                    analyze_past_papers,
                    generate_study_plan)

st.set_page_config(page_title="Upload & Analyze", page_icon="📄")
st.title("📄 Upload & Analyze")

if not st.session_state.get("student_name"):
    st.warning("⚠️ Please go to **⚙️ Settings** and save your profile first.")
    st.stop()

# ── Subject Info ───────────────────────────────────────────
st.markdown("## 📚 Subject Details")
col1, col2 = st.columns(2)
with col1:
    subject = st.text_input("Subject Name", placeholder="e.g. Data Structures")
    level   = st.selectbox("Your Current Level", [
        "Beginner", "Elementary", "Intermediate", "Advanced"
    ])
with col2:
    target    = st.slider("Target Score (%)", 50, 100, 75)
    exam_days = st.slider("Days Until Exam",  7, 60,  30)
    study_hrs = st.slider("Study Hours/Day",  1.0, 10.0, 3.0, 0.5)

st.markdown("---")

# ── Upload Syllabus ────────────────────────────────────────
st.markdown("## 📋 Upload Syllabus PDF")
syllabus_file = st.file_uploader("Choose syllabus PDF", type=["pdf"])

if syllabus_file:
    st.success(f"✅ {syllabus_file.name} uploaded")

    if st.button("🔍 Analyze Syllabus", type="primary"):
        if not subject:
            st.error("Enter subject name first.")
        else:
            with st.spinner("Extracting topics from PDF..."):
                text   = read_pdf(syllabus_file)
                result = extract_topics_from_syllabus(text, subject)
                st.session_state["syllabus_data"] = result
                st.session_state["subject_name"]  = subject

            st.success("✅ Done!")
            st.metric("Units Found",  result["total_units"])
            st.metric("Topics Found", result["total_topics"])

            for unit in result["units"]:
                with st.expander(f"Unit {unit['unit_number']}: {unit['unit_title']} ({unit['difficulty']})"):
                    st.write("**Topics:**", ", ".join(unit["topics"]))
                    st.write("**Estimated Hours:**", unit["estimated_hours"])

st.markdown("---")

# ── Upload Past Papers ─────────────────────────────────────
st.markdown("## 📝 Upload Past Exam Papers (Optional)")
paper_files = st.file_uploader("Choose past paper PDFs",
                                 type=["pdf"],
                                 accept_multiple_files=True)

if paper_files:
    st.success(f"✅ {len(paper_files)} file(s) uploaded")

    if st.button("🔍 Analyze Past Papers", type="primary"):
        if not subject:
            st.error("Enter subject name first.")
        else:
            with st.spinner("Finding patterns in past papers..."):
                text   = read_multiple_pdfs(paper_files)
                result = analyze_past_papers(text, subject)
                st.session_state["paper_analysis"] = result

            st.success("✅ Done!")

            st.markdown("### 🎯 Predicted Topics for Next Exam:")
            for t in result["prediction_for_next_exam"]:
                st.markdown(f"⭐ {t}")

            st.markdown("### 🔥 Most Frequent Topics:")
            for h in result["hot_topics"][:6]:
                icon = {"Very High":"🔴","High":"🟠","Medium":"🟡"}.get(h["importance"],"🟢")
                st.write(f"{icon} **{h['topic']}** — seen {h['frequency']} times")

st.markdown("---")

# ── Weak Topics ────────────────────────────────────────────
st.markdown("## 😰 Your Weak Topics")
weak_input = st.text_area("One topic per line:",
                           placeholder="Binary Trees\nDynamic Programming",
                           height=120)
weak_topics = [t.strip() for t in weak_input.split("\n") if t.strip()]

if weak_topics:
    st.info(f"{len(weak_topics)} weak topics: {', '.join(weak_topics)}")

st.markdown("---")

# ── Generate Plan ──────────────────────────────────────────
st.markdown("## 📅 Generate Study Plan")

if st.button("🚀 Generate My Study Plan", type="primary", use_container_width=True):
    if not subject:
        st.error("Enter subject name.")
    elif not st.session_state.get("syllabus_data"):
        st.error("Analyze your syllabus first.")
    else:
        with st.spinner("Building your personalized plan..."):
            data = st.session_state["syllabus_data"]
            plan = generate_study_plan(
                subject       = subject,
                units         = data.get("units", []),
                weak_topics   = weak_topics,
                target_score  = target,
                available_days= exam_days,
                hours_per_day = study_hrs,
                current_level = level
            )
            st.session_state.update({
                "study_plan":  plan,
                "subject_name":subject,
                "weak_topics": weak_topics,
                "target_score":target,
                "exam_days":   exam_days
            })

        st.success("✅ Study plan created!")
        st.balloons()
        st.markdown("👉 Go to **📅 Study Plan** in the sidebar!")
