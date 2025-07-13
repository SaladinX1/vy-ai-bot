import os
import requests

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

def publish_product(product_data):
    # Exemple publication Gumroad
    url = "https://api.gumroad.com/v2/products"
    headers = {"Authorization": f"Bearer {GUMROAD_API_KEY}"}
    payload = {
        "name": product_data["name"],
        "description": product_data.get("description", ""),
        "price_cents": product_data.get("price_cents", 1000),
        "currency": "USD"
    }
    resp = requests.post(url, headers=headers, json=payload)
    return resp.status_code == 200

def post_to_twitter(message: str):
    url = "https://api.twitter.com/2/tweets"
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    payload = {"text": message}
    resp = requests.post(url, headers=headers, json=payload)
    return resp.status_code == 201
