import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "mistralai/mixtral-8x7b")
