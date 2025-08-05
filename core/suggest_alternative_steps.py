# core/suggest_alternative_steps.py

import json
from llm.llm_interface import query_mistral
from core.utils.logger import append_log

def suggest_alternative_steps(workflow, error_reason, goal):
    prompt = f"""
Le plan suivant a échoué :
{json.dumps(workflow, indent=2, ensure_ascii=False)}

Raison de l’échec :
"{error_reason}"

Objectif initial :
"{goal}"

Propose une version corrigée du plan, toujours au format JSON listé :
[
  {{
    "task": "titre tâche",
    "tool": "nom outil",
    "params": {{}}
  }},
  ...
]
"""
    try:
        corrected = query_mistral(prompt, system_prompt="Tu es un agent de correction de workflows.")
        return json.loads(corrected)
    except Exception as e:
        append_log(f"💥 Échec génération alternative : {e}")
        return []
