import json
import jsonschema
from jsonschema import validate

def is_valid_json(schema, data):
    try:
        validate(instance=data, schema=schema)
        return True, "JSON valide."
    except jsonschema.exceptions.ValidationError as e:
        return False, f"Erreur de validation: {e.message}"