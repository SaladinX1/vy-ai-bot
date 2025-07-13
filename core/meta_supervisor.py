import json

KPI_FILE = "memory/business_score.json"

def track_kpi(workflow_name, success, revenue=0, traffic=0):
    entry = {
        "workflow": workflow_name,
        "success": success,
        "revenue": revenue,
        "traffic": traffic
    }
    try:
        data = []
        if os.path.exists(KPI_FILE):
            with open(KPI_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        data.append(entry)
        with open(KPI_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Erreur KPI: {e}")

def review_performance():
    if not os.path.exists(KPI_FILE):
        return []
    with open(KPI_FILE, "r", encoding="utf-8") as f:
        return json.load(f)