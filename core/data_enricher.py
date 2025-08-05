# core/data_enricher.py
from core.utils.logger import append_log
import requests

def get_trending_keywords(keyword):
    try:
        response = requests.get("https://trends.google.com/trends/hottrends/visualize/internal/data")
        response.raise_for_status()
        return [t["title"] for t in response.json()]
    except Exception as e:
        append_log(f"[❌ Erreur Google Trends] {e}")
        return []
