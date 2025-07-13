# plugins/shopify_api.py

import requests

SHOPIFY_API_KEY = "your_api_key"
SHOPIFY_PASSWORD = "your_password"
SHOPIFY_STORE_NAME = "yourstore.myshopify.com"

def create_product(args):
    title = args.get("title", "Produit Sans Titre")
    body_html = args.get("description", "")
    price = args.get("price", "9.99")

    product_data = {
        "product": {
            "title": title,
            "body_html": body_html,
            "variants": [
                {
                    "price": price
                }
            ]
        }
    }

    url = f"https://{SHOPIFY_API_KEY}:{SHOPIFY_PASSWORD}@{SHOPIFY_STORE_NAME}/admin/api/2023-10/products.json"
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=product_data, headers=headers)

    if response.status_code == 201:
        return {
            "status": "success",
            "product_id": response.json()["product"]["id"]
        }
    else:
        return {
            "status": "error",
            "message": response.text
        }

def handle_action(action, args):
    if action == "create_product":
        return create_product(args)
    else:
        raise ValueError(f"[SHOPIFY] Action inconnue: {action}")
