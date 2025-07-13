import json
import os

MEMORY_PATH = "data/memory.json"

def store(plan, result):
    if not os.path.exists("data"):
        os.makedirs("data")
    data = []
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                data = []
    entry = {
        "plan": plan,
        "result": result,
        "status": "failed" if result.get("error") else "success",
        "sales": result.get("sales", 0),
        "id": result.get("product_id", "unknown")
    }
    data.append(entry)
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def retrieve_all():
    if not os.path.exists(MEMORY_PATH):
        return []
    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
