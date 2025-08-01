from core.workflow_generator import generate_workflow
from core import plan_executor
from core.utils.logger import append_log
from core.memory import save_memory
from evaluator.evaluator import evaluate_workflow_result
from core.monitor import log_kpi
from memory.db import save_lesson

from utils.monitoring import log_metric, notify_failure

from agents.niche_agent import NicheAgent
from agents.copywriting_agent import CopywritingAgent
# TODO: Ajouter ici d'autres agents spécialisés

from core.db_manager import DBManager

# Initialisation de la base (à déplacer dans un entrypoint type main.py)
DBManager.init()

class BusinessOrchestrator:
    def __init__(self, goals=None, plan=None):
        self.goals = goals or []
        self.plan = plan or []
        self.status = {}

        # Initialisation des agents spécialisés
        self.niche_agent = NicheAgent()
        self.copy_agent = CopywritingAgent()
        # TODO: Init autres agents ici

    # === Mode 1 : Lancement automatique à partir d’objectifs ===
    def launch_all(self):
        """Lancer automatiquement tous les business à partir d’objectifs prédéfinis."""
        for goal in self.goals:
            try:
                append_log(f"🚀 Lancement du business : {goal}")

                # Générer le plan
                steps = generate_workflow_from_goal(goal)

                # Enregistrement du projet si nouveau
                DBManager.add_project(goal, steps)

                # Exécution du plan
                result = plan_executor.execute_plan(steps)
                output = result.get("output", "")

                # Évaluation IA
                evaluation = evaluate_workflow_result(output, goal)
                score = evaluation.get("score", 0.0)

                # Mise à jour du statut local
                self.status[goal] = {
                    "result": result,
                    "evaluation": evaluation,
                    "status": "success"
                }

                # Suivi mémoire et apprentissage
                log_kpi(goal, score)
                save_memory({"workflow": steps, "goal": goal, "status": "success"})
                save_lesson(goal, evaluation.get("reason", ""), score)

                # Persistance dans la base
                DBManager.save_state(goal, self.status[goal])
                DBManager.set_last_used(goal)

                # Monitoring
                log_metric("business_success", 1)

            except Exception as e:
                append_log(f"💥 Erreur sur le business '{goal}' : {e}")
                self.status[goal] = {"result": None, "status": "failed"}
                save_memory({"goal": goal, "status": "failed", "error": str(e)})

                # Monitoring
                log_metric("business_failure", 1)
                notify_failure(f"[GOAL: {goal}] {str(e)}")

    # === Mode 2 : Exécution manuelle d’un plan d’action ===
    def run_all(self):
        """Exécute séquentiellement toutes les tâches du plan fourni."""
        if not self.plan:
            append_log("⚠️ Aucun plan de tâches fourni.")
            return

        for task in self.plan:
            self.execute_task(task)

    def execute_task(self, task):
        """Exécute une tâche en fonction de son ID."""
        task_id = task.get("id", "")
        title = task.get("title", "Tâche sans titre")
        append_log(f"🛠️ Exécution de la tâche {task_id} - {title}")

        try:
            result = None

            if task_id == "niche_analysis":
                result = self.niche_agent.run(task.get("input", {}))

            elif task_id == "copywriting":
                result = self.copy_agent.run(task.get("input", {}))

            else:
                result = f"🚫 Tâche non reconnue : {task_id}"

            append_log(f"✅ Résultat de la tâche {task_id} : {result}")
            log_metric("task_success", 1)

            return result

        except Exception as e:
            append_log(f"❌ Erreur lors de la tâche {task_id} : {e}")
            log_metric("task_failure", 1)
            notify_failure(f"[TASK {task_id}] {str(e)}")
            return None
