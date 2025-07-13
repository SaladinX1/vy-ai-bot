# utils/feedback_handler.py (à créer si besoin)

import json
import os

# FEEDBACK_PATH = "data/feedback.json"

# def log_feedback(entry):
#     if not os.path.exists(FEEDBACK_PATH):
#         with open(FEEDBACK_PATH, "w", encoding="utf-8") as f:
#             json.dump([], f)
#     with open(FEEDBACK_PATH, "r+", encoding="utf-8") as f:
#         data = json.load(f)
#         data.append(entry)
#         f.seek(0)
#         json.dump(data, f, indent=2, ensure_ascii=False)



# utils/feedback_handler.py

from datetime import datetime

FEEDBACK_FILE = "data/feedback.json"

def log_feedback(feedback: dict):
    feedback["timestamp"] = datetime.utcnow().isoformat()
    os.makedirs("data", exist_ok=True)
    try:
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                all_feedback = json.load(f)
        else:
            all_feedback = []

        all_feedback.append(feedback)

        with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
            json.dump(all_feedback, f, indent=2, ensure_ascii=False)

    except Exception as e:
        print(f"[Erreur feedback] {e}")
