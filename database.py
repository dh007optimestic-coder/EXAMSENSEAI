"""
database.py
-----------
Saves all data using SQLite — a file-based database built into Python.
No installation, no MySQL, no setup needed. Just runs automatically.

Creates a file called 'examSense.db' in your project folder.
"""

import sqlite3
import json
from datetime import datetime

DB = "examSense.db"


def connect():
    return sqlite3.connect(DB)


def setup():
    """Create all tables when app starts."""
    conn = connect()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS students (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT NOT NULL,
        roll        TEXT UNIQUE,
        branch      TEXT,
        semester    INTEGER,
        created_at  TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS test_results (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id  INTEGER,
        subject     TEXT,
        score       INTEGER,
        total       INTEGER,
        percent     REAL,
        taken_at    TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS progress (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id  INTEGER,
        subject     TEXT UNIQUE,
        completed   TEXT,
        updated_at  TEXT
    )""")

    conn.commit()
    conn.close()


def save_student(name, roll, branch, semester):
    conn = connect()
    c = conn.cursor()
    c.execute("""INSERT OR REPLACE INTO students
        (name, roll, branch, semester, created_at)
        VALUES (?,?,?,?,?)""",
        (name, roll, branch, semester, datetime.now().isoformat()))
    sid = c.lastrowid
    conn.commit()
    conn.close()
    return sid


def save_result(student_id, subject, score, total):
    conn = connect()
    c = conn.cursor()
    pct = round(score / total * 100, 1) if total > 0 else 0
    c.execute("""INSERT INTO test_results
        (student_id, subject, score, total, percent, taken_at)
        VALUES (?,?,?,?,?,?)""",
        (student_id, subject, score, total, pct, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_results(student_id):
    conn = connect()
    c = conn.cursor()
    c.execute("""SELECT subject, score, total, percent, taken_at
        FROM test_results WHERE student_id=? ORDER BY taken_at DESC""",
        (student_id,))
    rows = c.fetchall()
    conn.close()
    return rows


def save_progress(student_id, subject, completed: list):
    conn = connect()
    c = conn.cursor()
    c.execute("""INSERT OR REPLACE INTO progress
        (student_id, subject, completed, updated_at)
        VALUES (?,?,?,?)""",
        (student_id, subject, json.dumps(completed), datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_progress(student_id, subject):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT completed FROM progress WHERE student_id=? AND subject=?",
              (student_id, subject))
    row = c.fetchone()
    conn.close()
    return json.loads(row[0]) if row else []


setup()  # Auto-run when imported
