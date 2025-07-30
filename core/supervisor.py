# core/supervisor.py

from core.orchestrator import BusinessOrchestrator
from core.db_manager import DBManager
from utils.logger import append_log

class SupervisorAgent:
    """
    Supervise les projets stockés en base de données et relance ceux qui sont bloqués, vides ou incomplets.
    """

    def __init__(self):
        pass

    def run_check_cycle(self):
        """
        Parcourt tous les projets et relance ceux qui ont échoué ou qui sont sans état.
        """
        try:
            projects = DBManager.list_projects()
        except Exception as e:
            append_log(f"❌ Erreur lors du listing des projets : {e}")
            return

        for project in projects:
            try:
                state = DBManager.get_project_state(project)

                # Aucun état trouvé → relance totale
                if not state:
                    append_log(f"⚠️ Projet '{project}' sans état — relance complète.")
                    orchestrator = BusinessOrchestrator(goals=[project])
                    orchestrator.launch_all()
                    continue

                # Statut non succès → tentative de relance
                if state.get("status") != "success":
                    append_log(f"🔁 Projet '{project}' en échec ou incomplet — tentative de relance.")
                    orchestrator = BusinessOrchestrator(goals=[project])
                    orchestrator.launch_all()

            except Exception as err:
                append_log(f"❌ Erreur lors du traitement du projet '{project}' : {err}")



from core.db_manager import DBManager
from orchestrator import BusinessOrchestrator
from utils.logger import append_log

class SupervisorAgent:
    def __init__(self):
        pass

    def run_check_cycle(self):
        projects = DBManager.list_projects()

        for proj in projects:
            state = DBManager.get_project_state(proj)

            if not state:
                append_log(f"⚠️ Projet {proj} sans état — relance plan complète.")
                orchestrator = BusinessOrchestrator(goals=[proj])
                orchestrator.launch_all()
            elif state.get("status") != "success":
                append_log(f"🔁 Projet {proj} incomplet — tentative de relance.")