from plugins.google_trends import fetch_trending_keywords
from ai.workflow_generator import generate_workflow_from_niche
from workflows.manager import save_workflow

def auto_create_workflow():
    niches = fetch_trending_keywords()
    for niche in niches:
        wf = generate_workflow_from_niche(niche)
        save_workflow(wf)