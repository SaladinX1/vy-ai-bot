import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_command_response(user_input, screen_text, context=""):
    prompt = f"""
Tu es un assistant visuel sur ordinateur.
Voici ce que voit l'utilisateur :

--- CONTEXTE VISUEL ---
{screen_text}

--- CONTEXTE HISTORIQUE ---
{context}

--- DEMANDE ---
{user_input}

Réponds uniquement avec un JSON comme :
{{
  "action": "click" | "type" | "open_app",
  "target": "texte, app ou zone",
  "value": "texte à saisir s’il y a lieu"
}}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]
