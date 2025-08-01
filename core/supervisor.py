# core/supervisor.py

from core.db_manager import DBManager
from core.orchestrator import BusinessOrchestrator
from utils.logger import append_log

class SupervisorAgent:
    """
    Surveille tous les projets enregistrés et relance automatiquement
    ceux qui sont sans état ou dont l'exécution a échoué.
    """

    def __init__(self):
        pass

    def run_check_cycle(self):
        """
        Vérifie tous les projets existants et tente de relancer ceux :
        - sans état (état vide ou absent)
        - avec un statut différent de 'success'
        """
        try:
            projects = DBManager.list_projects()
        except Exception as e:
            append_log(f"❌ Erreur lors de la récupération des projets : {e}")
            return

        for project_id in projects:
            try:
                state = DBManager.get_state(project_id)

                if not state:
                    append_log(f"⚠️ Projet '{project_id}' sans état — relance complète.")
                    orchestrator = BusinessOrchestrator(goals=[project_id])
                    orchestrator.launch_all()
                    continue

                if state.get("status") != "success":
                    append_log(f"🔁 Projet '{project_id}' en échec ou incomplet — tentative de relance.")
                    orchestrator = BusinessOrchestrator(goals=[project_id])
                    orchestrator.launch_all()

            except Exception as err:
                append_log(f"❌ Erreur durant le traitement du projet '{project_id}' : {err}")
