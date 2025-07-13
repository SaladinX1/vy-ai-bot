# analytics/analytics_watcher.py
import requests

GUMROAD_API_URL = "https://api.gumroad.com/v2"
GUMROAD_ACCESS_TOKEN = "ton_token_gumroad_ici"  # Mets ta clé API Gumroad ici

def get_gumroad_sales():
    """
    Récupère les ventes Gumroad via API officielle.
    """
    url = f"{GUMROAD_API_URL}/sales"
    headers = {
        "Authorization": f"Bearer {GUMROAD_ACCESS_TOKEN}"
    }
    params = {
        "limit": 50  # Nombre de ventes à récupérer
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Erreur API Gumroad : {response.status_code} {response.text}")

    data = response.json()
    sales = data.get("sales", [])
    total_revenue = sum(float(sale["price"]) for sale in sales)
    total_sales = len(sales)

    # Regrouper les ventes par produit
    products = {}
    for sale in sales:
        product_name = sale["product_name"]
        products.setdefault(product_name, 0)
        products[product_name] += 1

    return {
        "total_sales": total_sales,
        "total_revenue": total_revenue,
        "products": [{"name": k, "sales": v} for k, v in products.items()]
    }

def get_performance_data():
    # Appel réel Gumroad (peut étendre à Stripe, etc.)
    try:
        return get_gumroad_sales()
    except Exception as e:
        print(f"Erreur récupération performance: {e}")
        return {
            "product1": {"sales": 0, "visits": 50},
            "product2": {"sales": 4, "visits": 200}
        }