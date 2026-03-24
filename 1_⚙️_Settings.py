"""
pages/1_Settings.py
--------------------
Student profile setup. No API key needed!
"""

import streamlit as st
from database import save_student

st.set_page_config(page_title="Settings", page_icon="⚙️")
st.title("⚙️ Settings — Your Profile")
st.success("✅ No API key needed — this app works 100% offline!")

st.markdown("---")
st.markdown("## 👤 Fill In Your Details")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Full Name",
                          value=st.session_state.get("student_name", ""),
                          placeholder="e.g. Ravi Kumar")
    roll = st.text_input("Roll Number",
                          value=st.session_state.get("roll_number", ""),
                          placeholder="e.g. 21BCE0001")
    branch = st.selectbox("Branch", [
        "Computer Science (CSE)",
        "Electronics & Communication (ECE)",
        "Electrical Engineering (EEE)",
        "Mechanical Engineering (ME)",
        "Civil Engineering (CE)",
        "Information Technology (IT)",
        "AI & ML (AIML)",
        "Other"
    ])

with col2:
    semester = st.selectbox("Semester", [1,2,3,4,5,6,7,8], index=3)
    college  = st.text_input("College Name",
                              value=st.session_state.get("college",""),
                              placeholder="e.g. VIT University")

if st.button("💾 Save Profile", type="primary"):
    if name and roll:
        sid = save_student(name, roll, branch, semester)
        st.session_state.update({
            "student_name": name,
            "roll_number":  roll,
            "branch":       branch,
            "semester":     semester,
            "college":      college,
            "student_id":   sid
        })
        st.success(f"✅ Welcome, {name}! Go to 📄 Upload & Analyze next.")
        st.balloons()
    else:
        st.error("Please enter your Name and Roll Number.")

st.markdown("---")
st.markdown("## ✅ Setup Status")

if st.session_state.get("student_name"):
    st.success(f"✅ Name: {st.session_state['student_name']}")
else:
    st.error("❌ Name not set")

if st.session_state.get("roll_number"):
    st.success(f"✅ Roll: {st.session_state['roll_number']}")
else:
    st.error("❌ Roll number not set")
