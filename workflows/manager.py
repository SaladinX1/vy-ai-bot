import json
import os
from datetime import datetime

WORKFLOWS_DIR = "workflows"
os.makedirs(WORKFLOWS_DIR, exist_ok=True)

def save_workflow(name, steps):
    path = os.path.join(WORKFLOWS_DIR, f"{name}.json")
    data = {
        "created": str(datetime.now()),
        "steps": steps
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Workflow '{name}' sauvegardé ({len(steps)} étapes)")

def load_workflow(name):
    path = os.path.join(WORKFLOWS_DIR, f"{name}.json")
    if not os.path.exists(path):
        print(f"❌ Workflow '{name}' introuvable.")
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)["steps"]

def list_workflows():
    files = os.listdir(WORKFLOWS_DIR)
    return [f[:-5] for f in files if f.endswith(".json")]
