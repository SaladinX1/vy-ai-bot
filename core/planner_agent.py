import openai
import os
import httpx
from core.config import OPENAI_API_KEY, MISTRAL_API_KEY
from utils.logger import append_log
from utils.json_utils import fix_json
from core.validators import validate_plan_schema

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")

class AgentPlanner:
    def __init__(self, model_name=DEFAULT_MODEL):
        self.model_name = model_name

    def generate_plan(self, objective: str) -> list:
        append_log(f"🔍 Génération du plan pour : {objective}")
        
        try:
            if "gpt" in self.model_name:
                # Appel OpenAI
                openai.api_key = OPENAI_API_KEY
                response = openai.ChatCompletion.create(
                    model=self.model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": "Tu es un assistant qui génère un plan JSON structuré pour créer un business.",
                        },
                        {
                            "role": "user",
                            "content": f"Génère un plan JSON pour : {objective}",
                        },
                    ],
                    temperature=0.7,
                )
                raw_output = response["choices"][0]["message"]["content"]

            elif "mistral" in self.model_name:
                # Appel Mistral API
                headers = {
                    "Authorization": f"Bearer {MISTRAL_API_KEY}",
                    "Content-Type": "application/json",
                }

                body = {
                    "model": self.model_name,
                    "messages": [
                        {
                            "role": "system",
                            "content": "Tu es un assistant qui génère un plan JSON structuré pour créer un business.",
                        },
                        {
                            "role": "user",
                            "content": f"Génère un plan JSON pour : {objective}",
                        },
                    ],
                    "temperature": 0.7,
                }

                mistral_url = "https://api.mistral.ai/v1/chat/completions"
                with httpx.Client() as client:
                    response = client.post(mistral_url, headers=headers, json=body)
                    response.raise_for_status()
                    raw_output = response.json()["choices"][0]["message"]["content"]

            else:
                append_log(f"❌ Modèle non pris en charge : {self.model_name}")
                return []

            plan = fix_json(raw_output)
            if plan is None or not validate_plan_schema(plan):
                append_log("⚠️ Erreur plan: JSON invalide ou non conforme.")
                return []

            append_log("✅ Plan généré avec succès.")
            return plan

        except Exception as e:
            append_log(f"💥 Erreur durant la génération du plan : {e}")
            return []
