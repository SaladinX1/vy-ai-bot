# memory/db.py

import json
import os
from core.utils.logger import append_log  # ✅ Ajout de l'import

MEMORY_PATH = "logs/memory.json"

def save_lesson(workflow_name, reason, score):
    append_log(f"📚 Enregistrement de la leçon pour le goal '{workflow_name}'")  # ✅ Ajout ici

    entry = {"workflow": workflow_name, "reason": reason, "score": score}
    memory = []
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r", encoding="utf-8") as f:
            memory = json.load(f)
    memory.append(entry)
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)
