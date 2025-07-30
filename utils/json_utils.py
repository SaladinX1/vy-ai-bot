import json
import re

def fix_json(bad_json_str):
    # Exemples simples de corrections possibles
    # 1. Remplacer les apostrophes simples par doubles quotes
    fixed = re.sub(r"'", '"', bad_json_str)

    # 2. Supprimer les virgules finales avant fermetures
    fixed = re.sub(r",(\s*[\]}])", r"\1", fixed)

    try:
        return json.loads(fixed)
    except json.JSONDecodeError:
        return None
