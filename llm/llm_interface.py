import os
import openai
import json
import time
import requests

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "mistralai/mixtral-8x7b")

from llm.selector import select_best_model 
from jsonschema import validate, ValidationError

API_URL = "https://api.mistral.ai/v1/chat/completions"
openai.api_key = os.getenv("OPENAI_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {"https://api.mistral.ai/v1/chat/completions"}",
    "Content-Type": "application/json"
}

PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "action": {"type": "string", "enum": ["click", "type", "open_app", "wait_until"]},
        "target": {"type": ["string", "null"]},
        "value": {"type": ["string", "null"]}
    },
    "required": ["action"],
    "additionalProperties": False
}





def get_command_response(user_input, screen_text, context="", retries=3, delay=2):
    prompt = f"""
Tu es un assistant visuel intelligent.

Voici ce que voit l'utilisateur :
--- CONTEXTE VISUEL ---
{screen_text}

--- CONTEXTE HISTORIQUE ---
{context}

--- DEMANDE ---
{user_input}

Tu dois répondre uniquement en JSON, sous la forme d’une liste d’actions.
Chaque action est un objet avec :
- action: "click" | "type" | "open_app" | "wait_until"
- target: "texte, app ou zone" (si pertinent)
- value: "texte à saisir" (si pertinent)

Exemple :
[
  {{"action": "click", "target": "Paramètres", "value": null}},
  {{"action": "type", "target": null, "value": "admin"}},
  {{"action": "wait_until", "target": "Google", "value": null}},
  {{"action": "click", "target": "Connexion", "value": null}}
]
"""

    for _ in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model=os.getenv("DEFAULT_MODEL"),  # ex: "mistralai/mixtral-8x7b"
                messages=[
                    {"role": "system", "content": "Tu es un assistant pour créer un business automatiquement"},
                    {"role": "user", "content": "Génère une idée rentable"}
                ]
            )
            content = response["choices"][0]["message"]["content"]
            plan_list = json.loads(content)

            if not isinstance(plan_list, list):
                raise ValueError("Réponse du LLM n'est pas une liste.")

            for plan in plan_list:
                validate(instance=plan, schema=PLAN_SCHEMA)

            return json.dumps(plan_list)
        except (json.JSONDecodeError, ValidationError, ValueError) as e:
            print(f"⚠️ Réponse invalide du LLM : {e}")
        except Exception as e:
            print(f"⚠️ Erreur d'appel LLM : {e}")
        time.sleep(delay)

    raise RuntimeError("Échec après plusieurs tentatives")

def query_mistral(prompt, system_prompt=None, model=DEFAULT_MODEL):
    if not model:
        model = select_best_model("generation")
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()
