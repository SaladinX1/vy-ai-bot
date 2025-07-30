# 📁 Dossier : core/workflow_generator.py
import openai
import os
import json
from llm.llm_interface import query_mistral

from core import memory

openai.api_key = os.getenv("MISTRAL_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")

# DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "mistralai/mixtral-8x7b")


###########################################################################
###########################################################################"
# "##############################"""#####################################"
# 
# "

def generate_workflow(goal: str):
    past_lessons = memory.get_recent_lessons(limit=3)
    formatted_lessons = "\n".join([f"- {lesson['lesson']}" for lesson in past_lessons]) if past_lessons else "Aucune leçon."

    prompt = f"""
Tu es un agent spécialisé dans la création de workflows métiers.
Objectif : "{goal}"

Voici quelques échecs récents à éviter :
{formatted_lessons}

Génère un plan d'action structuré en 5 à 10 étapes maximum.
Retourne le résultat au format JSON, sous forme d’une liste contenant :
- "task": nom de la tâche à exécuter
- "tool": l’outil à utiliser (ex: 'browser', 'code_executor', 'file_writer', etc.)
- "params": dictionnaire des paramètres nécessaires

Exemple :
[
  {{
    "task": "Faire une recherche Google sur le marché cible",
    "tool": "browser",
    "params": {{"query": "étude de marché dropshipping France 2024"}}
  }},
  ...
]
    """.strip()

    try:
        response = query_mistral(prompt, system_prompt="Tu es un agent générateur de plans d'action automatisés.")
        workflow = json.loads(response)
        return workflow
    except Exception as e:
        print(f"[ERREUR] Échec de génération de workflow : {e}")
        return []

