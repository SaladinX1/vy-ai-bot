# monitoring/analytics_watcher.py

import requests
from core import brain

GUMROAD_API_KEY = "your_api_key"

def fetch_sales():
    url = f"https://api.gumroad.com/v2/sales?access_token={GUMROAD_API_KEY}"
    r = requests.get(url)
    data = r.json()
    return data.get("sales", [])

def detect_weak_products(sales):
    counts = {}
    for sale in sales:
        product_id = sale["product_id"]
        counts[product_id] = counts.get(product_id, 0) + 1
    return [pid for pid, count in counts.items() if count < 3]

def feedback_loop():
    sales = fetch_sales()
    weak_products = detect_weak_products(sales)
    for pid in weak_products:
        print(f"[MONITOR] Produit faible : {pid}, itération...")
        brain.improve_product(pid)
