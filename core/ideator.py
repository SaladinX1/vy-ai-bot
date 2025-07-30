

from dotenv import load_dotenv
import openai
import os

load_dotenv()
openai.api_key = os.getenv("MISTRAL_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "mistralai/mixtral-8x7b")




# core/ideator.py



class Ideator:
    def generate_idea(self):
        response = openai.ChatCompletion.create(
             model=DEFAULT_MODEL,
            messages=[{"role": "user", "content": "Donne une idée de produit digital original à vendre."}],
            max_tokens=50
        )
        return response.choices[0].message.content.strip()
