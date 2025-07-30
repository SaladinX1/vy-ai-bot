

from core.db_manager import save_project_state, get_project_state

def run_task(project_id):
    # Lire l’état précédent
    state = get_project_state(project_id)

    if state.get("status") == "en cours":
        print(f"Reprise du projet {project_id} à l'étape {state.get('current_task')}...")

    # Simule une tâche
    for step in range(1, 6):
        state = {
            "current_task": f"step_{step}",
            "progress": round(step / 5, 2),
            "status": "en cours"
        }
        save_project_state(project_id, state)

    # Tâche complétée
    save_project_state(project_id, {
        "current_task": "terminé",
        "progress": 1.0,
        "status": "terminé"
    })


def run_project(project_id, resume=False):
    from core.project_manager import get_project_state
    state = get_project_state(project_id) if resume else {}

    current_task = state.get("current_task", "start")
    
    # Logique de gestion du projet selon la tâche en cours
    if current_task == "start":
        launch_project(project_id)
    elif current_task == "rédaction emails":
        generate_emails(project_id)
    elif current_task == "analyse marché":
        analyze_market(project_id)
    else:
        print(f"⚠️ Tâche inconnue ou terminée : {current_task}")
