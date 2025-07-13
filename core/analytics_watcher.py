import random

def analyze_performance():
    # Simuler récupération de données analytics
    data = {
        "views": random.randint(100, 1000),
        "sales": random.randint(0, 50),
        "conversion_rate": round(random.uniform(0, 0.1), 3),
    }
    print(f"📊 Analyse des performances : {data}")
    return data

def decide_next_action(analytics_data):
    if analytics_data["conversion_rate"] < 0.02:
        return "pivot"
    else:
        return "iterate"
