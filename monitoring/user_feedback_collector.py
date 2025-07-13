# monitoring/user_feedback_collector.py

import json
from core import brain

FEEDBACK_FILE = "data/user_feedback.json"

def load_feedback():
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def analyze_feedback():
    feedbacks = load_feedback()
    for entry in feedbacks:
        if "bug" in entry["comment"].lower() or "nul" in entry["comment"].lower():
            print(f"[FEEDBACK] Suggestion d'amélioration : {entry}")
            brain.react_to_feedback(entry)
