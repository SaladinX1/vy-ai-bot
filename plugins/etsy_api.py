
import requests

ETSY_API_KEY = "<your_etsy_api_key>"
ETSY_SHOP_ID = "<your_shop_id>"


def create_listing(title, description, price, quantity, image_url):
    url = f"https://openapi.etsy.com/v3/application/shops/{ETSY_SHOP_ID}/listings"
    headers = {
        "x-api-key": ETSY_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "title": title,
        "description": description,
        "price": price,
        "quantity": quantity,
        "who_made": "i_did",
        "is_supply": False,
        "when_made": "made_to_order",
        "taxonomy_id": 123,
        "shipping_profile_id": 123456,
        "image_urls": [image_url]
    }
    r = requests.post(url, headers=headers, json=data)
    if r.status_code == 201:
        print("✅ Produit Etsy créé")
    else:
        print("❌ Erreur Etsy", r.text)


def publish_product_to_etsy(api_key, shop_id, product_data):
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    endpoint = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/listings"
    response = requests.post(endpoint, headers=headers, json=product_data)
    if response.status_code == 201:
        print("✅ Produit publié sur Etsy")
    else:
        print(f"❌ Erreur Etsy: {response.text}")