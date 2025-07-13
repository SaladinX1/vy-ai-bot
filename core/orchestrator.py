# core/orchestrator.py

from core.workflow_generator import generate_workflow_from_goal
from core import plan_executor
from utils.logger import append_log
from core.memory import save_memory

from evaluator.evaluator import evaluate_workflow_result  # ✅
from core.monitor import log_kpi  # ✅
from memory.db import save_lesson  # ✅

class BusinessOrchestrator:
    def __init__(self, goals):
        self.goals = goals
        self.status = {}

    def launch_all(self):
        for goal in self.goals:
            try:
                append_log(f"🚀 Lancement business : {goal}")
                steps = generate_workflow_from_goal(goal)
                result = plan_executor.execute_plan(steps)

                evaluation = evaluate_workflow_result(result.get("output", ""), goal)  # ✅
                score = evaluation.get("score", 0.0)

                self.status[goal] = {"result": result, "evaluation": evaluation, "status": "success"}
                
                log_kpi(goal, score)  # ✅ suivi KPI
                save_memory({"workflow": steps, "goal": goal, "status": "success"})  # existant
                save_lesson(goal, evaluation.get("reason", ""), score)  # ✅ apprentissage
               
            except Exception as e:
                append_log(f"💥 Erreur sur {goal} : {e}")
                self.status[goal] = {"result": None, "status": "failed"}
                save_memory({"goal": goal, "status": "failed", "error": str(e)})
