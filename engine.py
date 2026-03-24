"""
engine.py
----------
This file does everything the AI used to do — but WITHOUT any API key.
It uses simple Python logic + text analysis to:
  1. Extract topics from syllabus text
  2. Find frequently asked topics from past papers
  3. Build a study plan based on student info
  4. Generate mock test questions from topics

"""

import re
import random
from collections import Counter


# ── STOP WORDS ─────────────────────────────────────────────
# These are common English words we ignore when extracting topics
STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "has", "have", "had", "do", "does", "did", "will", "would", "can",
    "could", "should", "may", "might", "shall", "this", "that", "these",
    "those", "it", "its", "as", "if", "then", "than", "so", "yet", "both",
    "each", "few", "more", "most", "other", "some", "such", "no", "not",
    "only", "same", "also", "just", "because", "while", "although", "after",
    "before", "since", "until", "about", "above", "below", "between",
    "into", "through", "during", "including", "based", "using", "used",
    "given", "following", "understand", "study", "learn", "unit", "chapter",
    "introduction", "overview", "explain", "describe", "define", "list"
}


# ─────────────────────────────────────────────────────────────
# FUNCTION 1: Extract topics from syllabus text
# ─────────────────────────────────────────────────────────────
def extract_topics_from_syllabus(text: str, subject: str) -> dict:
    """
    Reads the syllabus text and breaks it into units and topics.
    
    How it works:
    - Splits text by unit/chapter headings
    - Extracts important phrases (2-4 word combinations)
    - Filters out common/irrelevant words
    - Groups them under units
    
    Returns a dictionary with units and topics.
    """

    lines = text.split("\n")
    units = []
    current_unit = None
    current_topics = []

    # Patterns that usually indicate a unit/chapter heading
    unit_patterns = [
        r"(?i)unit\s*[-:]?\s*(\d+|[ivxlcdm]+)",
        r"(?i)module\s*[-:]?\s*(\d+|[ivxlcdm]+)",
        r"(?i)chapter\s*[-:]?\s*(\d+|[ivxlcdm]+)",
        r"(?i)section\s*[-:]?\s*(\d+|[ivxlcdm]+)",
    ]

    difficulty_levels = ["Easy", "Medium", "Hard"]

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if this line is a unit heading
        is_unit_heading = any(re.search(p, line) for p in unit_patterns)

        if is_unit_heading and len(line) < 100:
            # Save the previous unit if it exists
            if current_unit and current_topics:
                units.append({
                    "unit_number": len(units) + 1,
                    "unit_title": current_unit,
                    "topics": list(set(current_topics[:8])),  # max 8 topics per unit
                    "difficulty": difficulty_levels[len(units) % 3],
                    "estimated_hours": random.randint(3, 6)
                })
            current_unit = line
            current_topics = []
        else:
            # Extract topic phrases from this line
            phrases = extract_phrases(line)
            current_topics.extend(phrases)

    # Don't forget the last unit
    if current_unit and current_topics:
        units.append({
            "unit_number": len(units) + 1,
            "unit_title": current_unit,
            "topics": list(set(current_topics[:8])),
            "difficulty": difficulty_levels[len(units) % 3],
            "estimated_hours": random.randint(3, 6)
        })

    # If no units found (poorly formatted PDF), create generic ones
    if not units:
        units = create_generic_units(text, subject)

    # Count total topics
    total_topics = sum(len(u["topics"]) for u in units)

    return {
        "subject": subject,
        "total_units": len(units),
        "units": units,
        "total_topics": total_topics,
    }


def extract_phrases(line: str) -> list:
    """
    Extract meaningful 1-3 word phrases from a line of text.
    Filters out stop words and very short/long words.
    """
    # Remove special characters, keep letters and spaces
    clean = re.sub(r"[^a-zA-Z\s]", " ", line)
    words = clean.split()

    # Filter words: not a stop word, length 3-20 characters
    filtered = [w for w in words
                if w.lower() not in STOP_WORDS
                and 3 <= len(w) <= 20
                and not w.isdigit()]

    phrases = []

    # Single important words
    for w in filtered:
        if len(w) > 5:
            phrases.append(w.title())

    # Two-word combinations (bigrams)
    for i in range(len(filtered) - 1):
        bigram = f"{filtered[i].title()} {filtered[i+1].title()}"
        if len(bigram) > 8:
            phrases.append(bigram)

    return phrases[:5]  # Return max 5 phrases per line


def create_generic_units(text: str, subject: str) -> list:
    """
    If the syllabus is badly formatted, we still extract keywords
    and group them into 5 generic units.
    """
    # Get all important words from the text
    clean = re.sub(r"[^a-zA-Z\s]", " ", text)
    words = clean.split()
    
    important = [w.title() for w in words
                 if w.lower() not in STOP_WORDS
                 and len(w) > 5
                 and not w.isdigit()]

    # Count frequency
    freq = Counter(important)
    top_words = [w for w, _ in freq.most_common(40)]

    # Split into 5 units of ~8 topics each
    units = []
    chunk = 8
    unit_names = [
        f"Introduction to {subject}",
        f"Core Concepts of {subject}",
        f"Advanced Topics in {subject}",
        f"Applications of {subject}",
        f"Review and Problem Solving"
    ]
    for i in range(5):
        start = i * chunk
        end   = start + chunk
        units.append({
            "unit_number": i + 1,
            "unit_title":  unit_names[i],
            "topics":      top_words[start:end] if top_words[start:end] else [f"Topic {j+1}" for j in range(4)],
            "difficulty":  ["Easy", "Easy", "Medium", "Hard", "Medium"][i],
            "estimated_hours": [3, 4, 5, 5, 4][i]
        })
    return units


# ─────────────────────────────────────────────────────────────
# FUNCTION 2: Analyze past papers
# ─────────────────────────────────────────────────────────────
def analyze_past_papers(text: str, subject: str) -> dict:
    """
    Finds which topics appear most often in past exam papers.
    
    How it works:
    - Extracts all important words/phrases from paper text
    - Counts how many times each appears
    - Ranks them by frequency
    - Predicts top 5 likely topics for next exam
    """

    clean = re.sub(r"[^a-zA-Z\s]", " ", text)
    words = clean.split()

    # Count word frequency
    important = [w.lower() for w in words
                 if w.lower() not in STOP_WORDS
                 and len(w) > 4]

    freq = Counter(important)
    top_words = freq.most_common(20)

    # Build hot topics list
    hot_topics = []
    importance_levels = ["Very High", "Very High", "High", "High",
                         "High", "Medium", "Medium", "Medium",
                         "Low", "Low"]

    for i, (word, count) in enumerate(top_words[:10]):
        hot_topics.append({
            "topic": word.title(),
            "frequency": count,
            "importance": importance_levels[i] if i < len(importance_levels) else "Low"
        })

    # Top 5 predictions for next exam = most frequent topics
    predictions = [t["topic"] for t in hot_topics[:5]]

    return {
        "hot_topics": hot_topics,
        "prediction_for_next_exam": predictions,
        "exam_pattern": {
            "total_marks": 100,
            "duration_hours": 3
        }
    }


# ─────────────────────────────────────────────────────────────
# FUNCTION 3: Generate personalized study plan
# ─────────────────────────────────────────────────────────────
def generate_study_plan(subject: str, units: list, weak_topics: list,
                         target_score: int, available_days: int,
                         hours_per_day: float, current_level: str) -> dict:
    """
    Builds a day-by-day study plan based on the student's situation.
    
    Logic:
    - Weak topics get assigned more days
    - Hard units get more time than Easy ones
    - Last 3 days are always kept for revision
    - Tips are generated based on target score and level
    """

    # Strategy message based on target and level
    strategy = build_strategy(target_score, current_level, available_days)

    # Build weekly goals
    study_days   = available_days - 3  # Last 3 days = revision
    days_per_unit = max(1, study_days // max(len(units), 1))
    weekly_goals = build_weekly_goals(units, available_days)

    # Build daily plan
    daily_plan = build_daily_plan(
        units, weak_topics, study_days, hours_per_day, available_days
    )

    # Study tips
    tips = build_tips(target_score, current_level, weak_topics)

    # Last week advice
    last_week = build_last_week_plan(target_score)

    return {
        "strategy": strategy,
        "weekly_goals": weekly_goals,
        "daily_plan": daily_plan,
        "study_tips": tips,
        "last_week_plan": last_week
    }


def build_strategy(target: int, level: str, days: int) -> str:
    if target >= 85:
        return f"High target plan: Deep understanding + lots of practice. Every day counts across {days} days."
    elif target >= 70:
        return f"Balanced plan: Cover all topics with focus on important ones. {days} days of consistent effort."
    else:
        return f"Foundation plan: Focus on core concepts and high-weightage topics. {days} days to build confidence."


def build_weekly_goals(units: list, total_days: int) -> list:
    weeks = []
    total_weeks = max(1, total_days // 7)

    for i in range(min(total_weeks, len(units))):
        unit = units[i] if i < len(units) else units[-1]
        weeks.append({
            "week": i + 1,
            "focus": f"Complete {unit['unit_title']}",
            "topics": unit.get("topics", [])[:4]
        })

    # Add revision week at end
    weeks.append({
        "week": total_weeks + 1,
        "focus": "Full Revision + Mock Tests",
        "topics": ["Revise all units", "Solve past papers", "Focus on weak topics"]
    })

    return weeks


def build_daily_plan(units, weak_topics, study_days, hours, total_days):
    daily = []
    day   = 1

    # Assign topics to days
    topic_queue = []
    for unit in units:
        for topic in unit.get("topics", []):
            # Weak topics get 2 days, others get 1
            is_weak = any(w.lower() in topic.lower() for w in weak_topics)
            repeats = 2 if is_weak else 1
            for _ in range(repeats):
                topic_queue.append({
                    "topic": topic,
                    "unit":  unit["unit_title"],
                    "priority": "High" if is_weak else (
                        "High" if unit["difficulty"] == "Hard" else "Medium"
                    )
                })

    # Fill days with topics
    for i, item in enumerate(topic_queue):
        if day > study_days:
            break

        tasks = build_daily_tasks(item["topic"], item["priority"])
        daily.append({
            "day":      day,
            "topic":    item["topic"],
            "unit":     item["unit"],
            "hours":    hours,
            "tasks":    tasks,
            "priority": item["priority"]
        })
        day += 1

    # Add revision days at end
    for i in range(3):
        daily.append({
            "day":      total_days - 2 + i,
            "topic":    f"Revision Day {i+1}",
            "unit":     "Full Revision",
            "hours":    hours,
            "tasks":    ["Revise all notes", "Solve 10 practice questions",
                         "Focus on weak topics", "Review formulas and definitions"],
            "priority": "High"
        })

    return daily


def build_daily_tasks(topic: str, priority: str) -> list:
    base_tasks = [
        f"Read about {topic} from textbook/notes",
        f"Write a 1-page summary of {topic}",
        f"Solve 5 practice problems on {topic}",
    ]
    if priority == "High":
        base_tasks.append(f"Watch a YouTube video on {topic}")
        base_tasks.append(f"Create flashcards for {topic} key points")
    return base_tasks


def build_tips(target: int, level: str, weak_topics: list) -> list:
    tips = [
        "Study in 45-minute sessions with 10-minute breaks (Pomodoro technique).",
        "Rewrite your notes in your own words — it improves memory retention.",
        "Solve at least one past year question per topic you complete.",
        "Don't skip sleep — 7-8 hours of sleep helps memory consolidation.",
        "Review what you studied yesterday for 10 minutes before starting today.",
    ]
    if weak_topics:
        tips.append(f"Spend extra 30 mins daily on your weak topics: {', '.join(weak_topics[:3])}.")
    if target >= 85:
        tips.append("For high scores: always explain concepts out loud to yourself as if teaching someone.")
    return tips


def build_last_week_plan(target: int) -> str:
    if target >= 85:
        return ("Last week: Day 1-2 revise all units. Day 3-4 solve full mock tests. "
                "Day 5 focus only on weak topics. Day 6 light revision. Day 7 rest + formulas only.")
    elif target >= 70:
        return ("Last week: Revise unit-wise. Solve 2 mock tests. "
                "Focus on frequently asked topics. Keep last day for rest and light review.")
    else:
        return ("Last week: Cover all important topics once. "
                "Solve 10 likely questions per unit. Keep last day light — no new topics.")


# ─────────────────────────────────────────────────────────────
# FUNCTION 4: Generate mock test questions
# ─────────────────────────────────────────────────────────────
def generate_mock_test(subject: str, topics: list,
                        difficulty: str, num_questions: int) -> dict:
    """
    Generates mock test questions from topics using question templates.
    No AI needed — uses pre-defined question patterns.
    """

    questions = []

    # Question templates for different types
    mcq_templates = [
        ("Which of the following best describes {topic}?",
         ["A definition", "A process", "An algorithm", "A data structure"]),
        ("What is the main purpose of {topic}?",
         ["To store data", "To process information", "To improve efficiency", "To reduce complexity"]),
        ("Which property is associated with {topic}?",
         ["Sequential access", "Random access", "Both A and B", "Neither A nor B"]),
        ("In the context of {topic}, what does efficiency refer to?",
         ["Time complexity", "Space complexity", "Both time and space", "Neither"]),
    ]

    short_templates = [
        "Define {topic} with an example.",
        "Explain the working of {topic} in brief.",
        "What are the advantages of {topic}?",
        "List the key characteristics of {topic}.",
        "Compare {topic} with a related concept.",
    ]

    long_templates = [
        "Explain {topic} in detail with a suitable example.",
        "Describe the algorithm/procedure for {topic} step by step.",
        "What are the applications of {topic}? Explain with examples.",
    ]

    difficulty_marks = {"Easy": 2, "Medium": 4, "Hard": 6, "Mixed": None}
    marks_val = difficulty_marks.get(difficulty, 2)

    for i in range(num_questions):
        topic = topics[i % len(topics)]

        # Alternate between MCQ, Short, and Long
        if i % 3 == 0 or difficulty == "Easy":
            q_type = "MCQ"
            template, opts = random.choice(mcq_templates)
            question_text  = template.format(topic=topic)
            options        = opts
            correct        = "A"
            explanation    = f"{topic} is best understood by reviewing its core definition and use cases."
            marks          = 2
        elif i % 3 == 1:
            q_type         = "Short Answer"
            question_text  = random.choice(short_templates).format(topic=topic)
            options        = []
            correct        = f"Answer should include: definition of {topic}, key characteristics, and a simple example."
            explanation    = f"Focus on defining {topic} clearly, then give a real-world example."
            marks          = marks_val if marks_val else 4
        else:
            q_type         = "Long Answer"
            question_text  = random.choice(long_templates).format(topic=topic)
            options        = []
            correct        = (f"A complete answer should include: introduction to {topic}, "
                              f"detailed explanation, step-by-step process if applicable, "
                              f"advantages/disadvantages, and examples.")
            explanation    = f"Structure your answer: Introduction → Main Content → Example → Conclusion"
            marks          = marks_val if marks_val else 6

        questions.append({
            "number":      i + 1,
            "question":    question_text,
            "type":        q_type,
            "topic":       topic,
            "marks":       marks,
            "options":     options,
            "correct_answer": correct,
            "explanation": explanation
        })

    total_marks = sum(q["marks"] for q in questions)

    return {
        "title":       f"Mock Test — {subject}",
        "total_marks": total_marks,
        "questions":   questions
    }
