# core/continuous_self_improvement.py

import json
from llm.llm_interface import query_mistral
from core import manager

FEEDBACK_FILE = "data/feedback_log.json"

def improve_failed_workflows():
    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            feedbacks = json.load(f)
    except:
        return []

    improvements = []

    for fb in feedbacks:
        if fb.get("success") is False:
            old_steps = manager.load_workflow(fb["workflow"])
            reason = fb.get("reason", "non précisé")

            prompt = f"""
Le workflow suivant a échoué :
Tâches :
{old_steps}

Raison de l'échec :
{reason}

Corrige-le et retourne un nouveau plan JSON.
            """
            try:
                new_plan_json = query_mistral(prompt, system_prompt="Tu es un agent d'amélioration continue.")
                new_plan = json.loads(new_plan_json)
                manager.save_workflow(fb["workflow"], new_plan)
                improvements.append(fb["workflow"])
            except:
                continue

    return improvements
