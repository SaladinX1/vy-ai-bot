

from plugins.google_trends import fetch_trending_keywords
from workflows.runner import run_workflow

def explore_and_launch(niche):
    trends = fetch_trending_keywords(niche)
    for trend in trends:
        print(f"🌱 Nouvelle idée détectée : {trend}")
        run_workflow("seo_webstarter", args={"topic": trend})