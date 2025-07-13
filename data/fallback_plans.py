import json

def get_fallback_plan(workflow_name):
    try:
        with open("data/fallback_plans.json", encoding="utf-8") as f:
            plans = json.load(f)
        for p in plans:
            if workflow_name in p["trigger"]:
                return p["workflow"]
    except:
        pass
    return None