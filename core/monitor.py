# core/monitor.py

import json
import datetime
from utils.logger import append_log

def log_kpi(workflow_name: str, score: float):
    now = datetime.datetime.utcnow().isoformat()
    with open("logs/kpi_history.json", "a", encoding="utf-8") as f:
        json.dump({"date": now, "workflow": workflow_name, "score": score}, f)
        f.write("\n")
    append_log(f"📊 KPI enregistré : {workflow_name} → {score}/10")
