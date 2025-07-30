import os
import json
import uuid
from datetime import datetime

from core.db_manager import get_connection

PROJECTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'projects')
DB_DIR = "db"

# =========================
# 🎯 GESTION DES PROJETS EN FICHIERS LOCAUX
# =========================

def create_project(name):
    project_id = str(uuid.uuid4())
    folder_name = name.replace(" ", "_").lower()
    project_path = os.path.join(PROJECTS_DIR, folder_name)
    os.makedirs(project_path, exist_ok=True)

    config = {
        "project_id": project_id,
        "name": name,
        "created_at": datetime.utcnow().isoformat(),
        "status": "created",
        "generated_files": [],
        "logs": []
    }

    with open(os.path.join(project_path, 'config.json'), 'w') as f:
        json.dump(config, f, indent=4)

    return project_id, project_path

def load_all_projects():
    if not os.path.exists(PROJECTS_DIR):
        return []
    return [
        f for f in os.listdir(PROJECTS_DIR)
        if os.path.exists(os.path.join(PROJECTS_DIR, f, 'config.json'))
    ]

def load_project(name):
    folder_name = name.replace(" ", "_").lower()
    config_path = os.path.join(PROJECTS_DIR, folder_name, 'config.json')
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Project '{name}' not found.")
    with open(config_path, 'r') as f:
        return json.load(f), os.path.join(PROJECTS_DIR, folder_name)

def update_project(name, updates: dict):
    config, path = load_project(name)
    config.update(updates)
    with open(os.path.join(path, 'config.json'), 'w') as f:
        json.dump(config, f, indent=4)

def log_action(name, action_text):
    config, path = load_project(name)
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action_text
    }
    config["logs"].append(log_entry)
    update_project(name, config)

# =========================
# 💾 GESTION DES ÉTATS (FICHIERS)
# =========================

def list_projects():
    projects_path = os.path.join(DB_DIR, "projects.json")
    if not os.path.exists(projects_path):
        return []
    with open(projects_path, "r") as f:
        return json.load(f)

def register_project(project_id):
    projects = list_projects()
    if project_id not in projects:
        projects.append(project_id)
        with open(os.path.join(DB_DIR, "projects.json"), "w") as f:
            json.dump(projects, f, indent=4)

def get_project_state_file(project_id):
    state_file = os.path.join(DB_DIR, project_id, "state.json")
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            return json.load(f)
    return {}

def save_project_state(project_id, state_data):
    os.makedirs(os.path.join(DB_DIR, project_id), exist_ok=True)
    with open(os.path.join(DB_DIR, project_id, "state.json"), "w") as f:
        json.dump(state_data, f, indent=4)

# =========================
# 🗃️ GESTION DES PROJETS VIA MySQL
# =========================

def get_all_projects():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, name FROM projects")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows

def get_project_state(project_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT state_json FROM project_states WHERE project_id = %s", (project_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row and row["state_json"]:
        return json.loads(row["state_json"])
    return {}

def get_all_projects_states():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT project_id, state_json FROM project_states")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    all_states = {}
    for row in rows:
        try:
            all_states[row["project_id"]] = json.loads(row["state_json"])
        except Exception:
            continue

    return all_states

# =========================
# ▶️ LANCEMENT D'UN PROJET
# =========================

def run_project(project_id, resume=False):
    print(f"▶️ Lancement du projet {project_id} {'(reprise)' if resume else ''}")
    try:
        from scripts.task_runner import execute_project  # à remplacer si autre nom
        execute_project(project_id, resume=resume)
    except ImportError:
        print("⚠️ 'execute_project' introuvable. Assure-toi que 'task_runner.py' existe et contient la fonction.")



def get_project_config(project_id):
    # Recherche du projet par ID
    for folder in os.listdir(PROJECTS_DIR):
        config_path = os.path.join(PROJECTS_DIR, folder, 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                data = json.load(f)
                if data.get("project_id") == project_id:
                    return data
    raise FileNotFoundError(f"Config introuvable pour le projet {project_id}")
