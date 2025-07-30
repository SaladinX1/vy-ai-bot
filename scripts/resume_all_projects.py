from core.project_manager import list_projects, get_project_state
from scripts.task_runner import execute_project
import logging

def resume_all_projects():
    projects = list_projects()
    if not projects:
        logging.info("Aucun projet à reprendre.")
        return

    logging.info(f"{len(projects)} projet(s) détecté(s) pour reprise.")
    for project_id in projects:
        state = get_project_state(project_id)
        if state and state.get("status") != "completed":
            logging.info(f"Reprise du projet : {project_id}")
            execute_project(project_id)
        else:
            logging.info(f"Projet {project_id} déjà terminé ou sans état, saut.")
