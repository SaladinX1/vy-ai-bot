import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_llm_response(prompt, model="gpt-4"):
    try:
        response = openai.ChatCompletion.create(
            model=os.getenv("DEFAULT_MODEL"),  # ex: "mistralai/mixtral-8x7b"
            messages=[
                {"role": "system", "content": "Tu es un assistant pour créer un business automatiquement"},
                {"role": "user", "content": "Génère une idée rentable"}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Erreur LLM {model}: {e}")
        return None

def get_workflow_from_prompt(prompt):
    for model in ["gpt-4", "gpt-3.5-turbo"]:
        result = get_llm_response(prompt, model)
        if result:
            return result
    raise RuntimeError("Aucun modèle LLM disponible.")



def suggest_workflow_from_prompt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu génères un JSON de workflow."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content.strip()