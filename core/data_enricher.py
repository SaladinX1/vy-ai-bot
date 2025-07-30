# core/data_enricher.py

import requests

def get_trending_keywords(query="startups"):
    """Interroge Google Trends via une API ou source proxy."""
    try:
        url = f"https://trends.google.com/trends/api/widgetdata/multiline?hl=fr&q={query}"
        response = requests.get(url)
        data = response.json()
        # Adaptation ici selon la vraie structure (à ajuster selon l’API que tu choisis)
        trends = [row["title"] for row in data.get("trends", [])]
        return trends[:5]
    except Exception as e:
        print(f"[❌ Erreur Google Trends] {e}")
        return []
