from core.project_manager import create_project
from scripts.task_runner import execute_project
import logging

def run_business(objective: str):
    logging.info(f"Création du projet pour : {objective}")
    project_id, _ = create_project(objective)
    logging.info(f"Projet créé avec ID: {project_id}, lancement de l'exécution...")
    execute_project(project_id)
    logging.info(f"Exécution du projet {project_id} terminée (ou en cours).")
