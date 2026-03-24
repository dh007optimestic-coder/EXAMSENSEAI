"""
pages/4_Mock_Test.py
---------------------
Generates and runs a mock test from your syllabus topics.
No AI needed — uses smart templates to create questions.
"""

import streamlit as st
from engine import generate_mock_test
from database import save_result

st.set_page_config(page_title="Mock Test", page_icon="📝")
st.title("📝 Mock Test")

syllabus = st.session_state.get("syllabus_data", {})
subject  = st.session_state.get("subject_name", "")

# ── Config ─────────────────────────────────────────────────
st.markdown("## ⚙️ Test Settings")
col1, col2 = st.columns(2)
with col1:
    test_subject = st.text_input("Subject", value=subject, placeholder="e.g. Data Structures")
    difficulty   = st.selectbox("Difficulty", ["Easy","Medium","Hard","Mixed"])
with col2:
    num_q = st.slider("Number of Questions", 5, 15, 8)

# Topic selection
all_topics = []
for unit in syllabus.get("units", []):
    all_topics.extend(unit.get("topics", []))

if all_topics:
    selected = st.multiselect("Select Topics",
                               options=all_topics,
                               default=all_topics[:4] if len(all_topics) >= 4 else all_topics)
else:
    typed = st.text_area("Type topics (one per line):", height=90,
                          placeholder="Arrays\nLinked Lists\nTrees")
    selected = [t.strip() for t in typed.split("\n") if t.strip()]

# ── Generate ───────────────────────────────────────────────
if st.button("🚀 Generate Test", type="primary", use_container_width=True):
    if not test_subject:
        st.error("Enter a subject name.")
    elif not selected:
        st.error("Select at least one topic.")
    else:
        with st.spinner("Generating questions..."):
            test = generate_mock_test(test_subject, selected, difficulty, num_q)
            st.session_state["current_test"]    = test
            st.session_state["test_submitted"]  = False
            st.session_state["test_answers"]    = {}
        st.success("✅ Test ready!")

st.markdown("---")

# ── Show Questions ─────────────────────────────────────────
test = st.session_state.get("current_test")

if test and not st.session_state.get("test_submitted", False):
    st.markdown(f"## 📋 {test['title']}")
    st.markdown(f"**Total Marks:** {test['total_marks']}  |  **Questions:** {len(test['questions'])}")
    st.markdown("---")

    answers = {}
    for q in test["questions"]:
        n       = q["number"]
        options = q.get("options", [])

        st.markdown(f"**Q{n}. {q['question']}**")
        st.caption(f"Topic: {q['topic']}  |  Type: {q['type']}  |  Marks: {q['marks']}")

        if q["type"] == "MCQ" and options:
            ans = st.radio("Your answer:", options, key=f"q{n}",
                           index=None, label_visibility="collapsed")
        else:
            ans = st.text_area("Your answer:", key=f"q{n}", height=80,
                               label_visibility="collapsed",
                               placeholder="Write your answer here...")

        answers[n] = {"answer": ans, "question": q}
        st.markdown("---")

    if st.button("📤 Submit Test", type="primary", use_container_width=True):
        st.session_state["test_answers"]   = answers
        st.session_state["test_submitted"] = True
        st.rerun()

# ── Results ────────────────────────────────────────────────
if st.session_state.get("test_submitted") and test:
    st.markdown("## 🏆 Your Results")

    answers     = st.session_state.get("test_answers", {})
    total_marks = test["total_marks"]
    scored      = 0

    for n, data in answers.items():
        q       = data["question"]
        ans     = data.get("answer", "")
        correct = q.get("correct_answer", "")
        marks   = q.get("marks", 2)

        if q["type"] == "MCQ" and ans and ans[0] == correct:
            scored += marks
        elif q["type"] != "MCQ" and ans and len(ans.strip()) > 10:
            scored += marks // 2   # partial marks for attempted short/long answers

    pct   = round(scored / total_marks * 100, 1) if total_marks > 0 else 0
    grade = ("🏆 Excellent" if pct >= 85 else
             "👍 Good"      if pct >= 65 else
             "📚 Average"   if pct >= 50 else "❌ Need More Practice")

    col1, col2, col3 = st.columns(3)
    col1.metric("Your Score",   f"{scored}/{total_marks}")
    col2.metric("Percentage",   f"{pct}%")
    col3.metric("Grade",        grade)

    st.progress(pct / 100)

    # Save to DB
    sid = st.session_state.get("student_id", 1)
    save_result(sid, test_subject, scored, total_marks)

    st.markdown("---")
    st.markdown("### 📋 Answer Review")
    for n, data in answers.items():
        q       = data["question"]
        ans     = data.get("answer", "Not answered")
        correct = q.get("correct_answer", "")
        ok      = q["type"] == "MCQ" and ans and ans[0] == correct
        icon    = "✅" if ok else "❌"

        with st.expander(f"{icon} Q{n}: {q['question'][:55]}..."):
            st.write(f"**Your answer:** {ans}")
            st.write(f"**Correct answer:** {correct}")
            st.info(f"💡 {q.get('explanation','')}")

    if st.button("🔄 Try Another Test"):
        st.session_state["current_test"]   = None
        st.session_state["test_submitted"] = False
        st.rerun()
