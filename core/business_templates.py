import json

def load_available_templates():
    with open("data/business_templates.json", encoding="utf-8") as f:
        return json.load(f)
