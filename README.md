# EXAMSENSEAI
Smart Exam Preparation & Performance Analyzer

A personalized exam preparation and performance analysis system that helps college students prepare efficiently for semester exams by analyzing syllabus, past exam papers, and individual performance to generate a structured study plan and performance insights.

📌 Project Overview

Smart Exam Preparation & Performance Analyzer is a Streamlit-based academic support system designed to assist students in preparing for semester exams within a limited time frame (such as 30 days).

The system reads syllabus and previous year question papers in PDF format, analyzes important topics, evaluates student preparation level, and generates a personalized study plan and performance insights.

The core AI logic is implemented in engine.py, which processes data and produces analysis using Python-based algorithms.

🚀 Features
📄 Upload syllabus PDF
📑 Upload previous year question papers
🧠 AI-based topic importance analysis
📊 Subject-wise performance insights
📅 30-day personalized study planner
🎯 Target-based preparation strategy
📈 Visual performance graphs
🖥️ Simple and interactive Streamlit interface
🔍 Automated PDF content extraction
🛠️ Tech Stack
Frontend
Streamlit
Backend
Python
Libraries
pdfplumber (PDF data extraction)
pandas (data processing and analysis)
plotly (interactive graphs and visualization)
Core Logic
engine.py (AI analysis and study plan generation)
🧩 System Workflow
Student uploads syllabus PDF
Student uploads previous year papers
System extracts text using pdfplumber
Data is processed using pandas
engine.py analyzes topics and frequency
AI logic identifies important units and weak areas
System generates personalized study plan
Installation & Setup
Step 1: Clone Repository
git clone https://github.com/your-username/exam-prep-analyzer.git
cd exam-prep-analyzer
Step 2: Create Virtual Environment
python -m venv venv

Activate:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
Step 3: Install Dependencies
pip install -r requirements.txt
Step 4: Run Application
streamlit run app.py

Then open in browser:

http://localhost:8501
Plotly displays visual performance graphs
Streamlit shows final analysis and recommendations
📂 Project Structure
