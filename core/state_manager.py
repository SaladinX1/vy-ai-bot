import json
import os

STATE_FILE = "db/project_state.json"

def save_state(project_id, state_data):
    os.makedirs("db", exist_ok=True)
    with open(f"db/{project_id}_state.json", "w") as f:
        json.dump(state_data, f)

def load_state(project_id):
    path = f"db/{project_id}_state.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def update_state(project_id, key, value):
    state = load_state(project_id)
    state[key] = value
    save_state(project_id, state)
