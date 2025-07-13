import openai
import os

def generate_workflow(prompt):
    try:
        response = openai.ChatCompletion.create(
            model=os.getenv("DEFAULT_MODEL", "gpt-4"),
            messages=[
                {"role": "system", "content": "Tu es un assistant pour créer un business automatiquement."},
                {"role": "user", "content": prompt}
            ]
        )
        workflow_json = response.choices[0].message.content
        return workflow_json
    except Exception as e:
        print(f"❌ Erreur API OpenAI : {e}")
        return None
