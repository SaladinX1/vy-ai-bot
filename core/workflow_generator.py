# 📁 Dossier : core/workflow_generator.py
# 📁 core/workflow_generator.py
import openai
import os
import json
from llm.llm_interface import query_mistral

from core import memory

openai.api_key = os.getenv("MISTRAL_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")


def map_llm_output_to_internal_tasks(llm_tasks):
    mapped = []
    for t in llm_tasks:
        label = t.get("task", "").lower()

        if "niche" in label or "marché" in label:
            mapped.append({"task": "niche_analysis", "input": {"query": t["params"].get("query", "")}})
        elif "copy" in label or "texte" in label:
            mapped.append({"task": "copywriting", "input": {"content": t["params"].get("content", "")}})
        elif "youtube" in label:
            mapped.append({"task": "youtube", "input": t["params"]})
        elif "tiktok" in label:
            mapped.append({"task": "tiktok", "input": t["params"]})
        else:
            print(f"[IGNORÉ] Tâche non mappée : {label}")
            continue

    # Ajoute la tâche "lesson" à la fin pour le suivi
    mapped.append({
        "task": "lesson",
        "input": {
            "goal": "auto",
            "score": 0.0,
            "result": "pending"
        }
    })

    return mapped


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
        mapped_workflow = map_llm_output_to_internal_tasks(workflow)
        return mapped_workflow
    except Exception as e:
        print(f"[ERREUR] Échec de génération de workflow : {e}")
        return []
