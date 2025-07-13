import openai
import time
import os

class LLMClient:
    def __init__(self, api_key, model="gpt-4o-mini"):
        openai.api_key = api_key
        self.model = model

    def generate_plan(self, prompt, retries=3, delay=2):
        for attempt in range(retries):
            try:
                response = openai.ChatCompletion.create(
                    model=os.getenv("DEFAULT_MODEL"),  # ex: "mistralai/mixtral-8x7b"
                    messages=[
                        {"role": "system", "content": "Tu es un assistant pour créer un business automatiquement"},
                        {"role": "user", "content": "Génère une idée rentable"}
                    ]
                )
                return response['choices'][0]['message']['content']
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    raise e

    def enrich_prompt(self, context, workflow_desc):
        # Ajoute contexte + instructions claires dans le prompt
        prompt = f"""
        Contexte : {context}
        Description du workflow à générer : {workflow_desc}

        Génère un plan détaillé d’actions automatisées, avec étapes et cibles.
        """
        return prompt
