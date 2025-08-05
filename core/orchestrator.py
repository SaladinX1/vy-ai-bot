from core.workflow_generator import generate_workflow
from core import plan_executor
from core.utils.logger import append_log
from core.memory import save_memory
from evaluator.evaluator import evaluate_workflow_result
from core.monitor import log_kpi
from memory.db import save_lesson
from agents.lesson_agent import LessonAgent
from utils.monitoring import log_metric, notify_failure

from agents.niche_agent import NicheAgent
from agents.copywriting_agent import CopywritingAgent
from agents.youtube_agent import YoutubeAgent
from agents.tiktok_agent import TikTokAgent
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
        self.youtube_agent = YoutubeAgent()
        self.tiktok_agent = TikTokAgent()
        self.lesson_agent = LessonAgent()
        # TODO: Init autres agents ici

        # Table de correspondance des tâches supportées
        self.supported_tasks = {
            "niche_analysis": self.niche_agent.run,
            "copywriting": self.copy_agent.run,
            "lesson": self.lesson_agent.run,
            # "video_editing": self.video_agent.run,  # Exemple futur
        }

    # === Mode 1 : Lancement automatique à partir d’objectifs ===
    def launch_all(self):
        for goal in self.goals:
            try:
                append_log(f"🚀 Lancement du business : {goal}")

                steps = generate_workflow(goal)
                append_log(f"🔍 Étapes générées pour le goal '{goal}' : {steps}")
                steps = [s for s in steps if s.get("task") in self.supported_tasks]  # filtrage

                if not steps:
                    raise ValueError("Aucune étape valide générée.")

                DBManager.add_project(goal, steps)

                result = plan_executor.execute_plan(steps)
                output = result.get("output", "")

                evaluation = evaluate_workflow_result(output, goal)
                score = evaluation.get("score", 0.0)

                self.status[goal] = {
                    "result": result,
                    "evaluation": evaluation,
                    "status": "success"
                }

                log_kpi(goal, score)
                save_memory({"workflow": steps, "goal": goal, "status": "success"})
                
                append_log(f"📚 Enregistrement de la leçon pour le goal '{goal}'")

                save_lesson(goal, evaluation.get("reason", ""), score)

                DBManager.save_state(goal, self.status[goal])
                DBManager.set_last_used(goal)

                log_metric("business_success", 1)

            except Exception as e:
                append_log(f"💥 Erreur sur le business '{goal}' : {e}")
                self.status[goal] = {"result": None, "status": "failed"}
                save_memory({"goal": goal, "status": "failed", "error": str(e)})

                log_metric("business_failure", 1)
                notify_failure(f"[GOAL: {goal}] {str(e)}")

    # === Mode 2 : Exécution manuelle d’un plan d’action ===
    def run_all(self):
        if not self.plan:
            append_log("⚠️ Aucun plan de tâches fourni.")
            return

        for task in self.plan:
            self.execute_task(task)

    def execute_task(self, task):
        task_id = task.get("id") or task.get("task")  # supporte les deux formats
        title = task.get("title", task_id or "Tâche sans titre")
        append_log(f"🛠️ Exécution de la tâche {task_id} - {title}")

        try:
            if task_id in self.supported_tasks:
                result = self.supported_tasks[task_id](task.get("input", {}))
            elif task_id == "youtube":
                result = self.youtube_agent.run(task.get("input", {}))
            elif task_id == "tiktok":
                result = self.tiktok_agent.run(task.get("input", {}))
            else:
                append_log(f"⚠️ Tâche non supportée ignorée : {task_id}")
                log_metric("task_skipped", 1)
                return None

            append_log(f"✅ Résultat de la tâche {task_id} : {result}")
            log_metric("task_success", 1)
            return result

        except Exception as e:
            append_log(f"❌ Erreur lors de la tâche {task_id} : {e}")
            log_metric("task_failure", 1)
            notify_failure(f"[TASK {task_id}] {str(e)}")
            return None
