import json
from core import plan_executor
from plugins import email_reader

FEEDBACK_FILE = "data/feedback.json"

def collect_feedback():
    feedbacks = email_reader.handle_action("get_feedback", {})
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(feedbacks, f, indent=2)
    print("[Feedback] Sauvegardé feedback utilisateur")

def analyze_feedback():
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    for fdbk in data:
        plan_executor.execute_plan([{"plugin": "llm", "action": "improve_based_on_feedback", "args": {"feedback": fdbk}}])

if __name__ == "__main__":
    collect_feedback()
    analyze_feedback()


    import json
import os
from utils.logger import append_log

FEEDBACK_FILE = "data/feedback.json"

def collect_feedback():
    # Simuler la collecte automatique (ex: API emails, réseaux sociaux)
    # Ici on simule l'ajout de feedback
    feedback = {
        "user": "client1@example.com",
        "comment": "Le produit est bien, mais j’aimerais un module supplémentaire."
    }

    if not os.path.exists("data"):
        os.makedirs("data")
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(feedback)
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    append_log("[FeedbackCollector] Feedback ajouté.")

def get_all_feedback():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

if __name__ == "__main__":
    collect_feedback()
