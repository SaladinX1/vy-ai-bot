from openai import OpenAI
import json

def suggest_alternative_steps(failed_workflow):
    prompt = f"""
    Voici un plan ayant échoué :\n{json.dumps(failed_workflow, indent=2)}\n
    Propose une nouvelle version corrigée de ce workflow avec explication.
    """
    response = OpenAI().chat_completion(prompt)
    return response['content']