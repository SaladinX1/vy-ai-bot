import time
from ui.streamlit_app import append_log
from data.fallback_plans import get_fallback_plan

from memory.db import save_lesson
from core.monitor import log_kpi
from evaluator.evaluator import evaluate_workflow_result

from core import memory, suggest_alternative_steps
from core.simulator import simulate_workflow
from core.utils.feedback_handler import log_feedback


def run_workflow_with_retry(workflow_name, manager, executor):
    steps = manager.load_workflow(workflow_name)

    # Simulation préalable avant exécution réelle
    sim_result = simulate_workflow(steps, goal=workflow_name)
    if not sim_result.get("success", True):
        append_log(f"🚫 Simulation négative pour '{workflow_name}' : {sim_result['reason']}")
        return

    # Exécution réelle
    result = executor.execute_plan(steps)
    output = result.get("output", "")

    # Évaluation post-exécution
    evaluation = evaluate_workflow_result(output, workflow_name)
    success = evaluation.get("success", False)
    reason = evaluation.get("reason", "")
    score = evaluation.get("score", 0.0)

    log_feedback({
        "workflow": workflow_name,
        "success": success,
        "reason": reason
    })

    # Enregistrement mémoire & apprentissage
    save_memory({
        "workflow": steps,
        "lesson": reason
    })
    save_lesson(workflow_name, reason, score)
    log_kpi(workflow_name, score)

    # Si échec, tentative de correction ou fallback
    if not success:
        corrected = suggest_alternative_steps.suggest_alternative_steps(steps, reason, workflow_name)
        if corrected:
            executor.execute_plan(corrected)
        else:
            fallback = get_fallback_plan(workflow_name)
            if fallback:
                append_log(f"🔁 Déclenchement du plan B pour '{workflow_name}'")
                executor.execute_plan(fallback)
