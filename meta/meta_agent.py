import json
from core.utils.logger import append_log

def rank_and_select_workflows(score_file="data/business_score.json", top_n=3):
    try:
        with open(score_file, encoding="utf-8") as f:
            scores = json.load(f)
        sorted_workflows = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)
        selected = [item[0] for item in sorted_workflows[:top_n]]
        append_log(f"🏆 Meta-agent a sélectionné les workflows les plus performants: {selected}")
        return selected
    except Exception as e:
        append_log(f"❌ Meta-agent erreur: {e}")
        return []