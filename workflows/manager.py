import json
import os
from datetime import datetime

WORKFLOWS_DIR = "workflows"
os.makedirs(WORKFLOWS_DIR, exist_ok=True)

def save_workflow(name, steps):
    path = os.path.join(WORKFLOWS_DIR, f"{name}.json")
    data = {
        "created": datetime.now().isoformat(),
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
        data = json.load(f)
    return data.get("steps", [])

def list_workflows():
    files = os.listdir(WORKFLOWS_DIR)
    return [f[:-5] for f in files if f.endswith(".json")]

def validate_workflow(steps):
    for step in steps:
        if "action" not in step:
            raise ValueError("Chaque étape doit avoir une clé 'action'")
    return True

def generate_improvement_workflow(product_name):
    return [
        {
            "plugin": "llm",
            "action": "llm_generate",
            "args": {
                "input": f"Analyse pourquoi le produit '{product_name}' ne vend pas et propose une amélioration (titre, visuel, contenu)"
            }
        },
        {
            "plugin": "content_exporter",
            "action": "update_product",
            "args": {
                "product": product_name,
                "new_data": "{{last_output}}"
            }
        }
    ]
