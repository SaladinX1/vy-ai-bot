import json
from llm.llm_interface import query_mistral
from core.utils.logger import append_log

from evaluator.scoring import score_workflow_result

def evaluate_workflow_result(output_text: str, goal: str) -> dict:
    prompt = f"""
Voici un résultat de workflow :
---
{output_text}
---

Objectif initial :
"{goal}"

L'objectif a-t-il été atteint ? Donne une réponse sous la forme :
{{
  "success": true/false,
  "reason": "explication brève"
}}
"""
    try:
        result = query_mistral(prompt, system_prompt="Tu es un évaluateur de performances de workflows.")
        parsed = json.loads(result)
        score = score_workflow_result(parsed, goal)
        parsed["score"] = score  # enrichissement
        append_log(f"🧠 Évaluation: {parsed}")
        return parsed
    except Exception as e:
        append_log(f"⚠️ Erreur lors de l'évaluation : {e}")
        return {"success": False, "reason": f"Erreur d'analyse : {e}"}

