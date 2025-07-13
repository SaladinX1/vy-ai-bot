# core/publisher.py

import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

logging.basicConfig(level=logging.INFO)

class Publisher:
    def __init__(self):
        self.gumroad_key = GUMROAD_API_KEY
        self.twitter_token = TWITTER_BEARER_TOKEN

    def publish_product_gumroad(self, product_data: dict):
        url = "https://api.gumroad.com/v2/products"
        headers = {"Authorization": f"Bearer {self.gumroad_key}"}
        try:
            response = requests.post(url, json=product_data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            logging.error(f"Erreur Gumroad: {e.response.text}")
            return None

    def tweet(self, message: str):
        url = "https://api.twitter.com/2/tweets"
        headers = {
            "Authorization": f"Bearer {self.twitter_token}",
            "Content-Type": "application/json"
        }
        data = {"text": message}
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            logging.error(f"Erreur Twitter: {e.response.text}")
            return None
