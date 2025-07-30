# Fichier : core/utils/json_fixer.py

import json
import re

def fix_json(raw_output):
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        # Correction simple
        fixed = re.sub(r"(\w+):", r'"\1":', raw_output)
        fixed = fixed.replace("'", '"')
        try:
            return json.loads(fixed)
        except:
            return {"error": "Could not fix JSON"}
