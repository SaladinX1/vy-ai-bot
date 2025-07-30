import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")
TWITTER_BEARER = os.getenv("TWITTER_BEARER")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")