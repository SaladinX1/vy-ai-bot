# scripts/task_runner.py
import importlib
from core.project_manager import save_project_state, get_project_state

def execute_project(project_id, resume=False):
    from core.planner_agent import generate_plan
    from core.project_manager import get_project_config

    config = get_project_config(project_id)
    objective = config["name"]

    if resume:
        state = get_project_state(project_id)
        current_step = state.get("current_step", 0)
        plan = state.get("plan", [])
    else:
        plan = generate_plan(objective)
        current_step = 0

    for step in plan[current_step:]:
        print(f"🚀 Étape {step['step_id']} : {step['name']}")
        agent_module = importlib.import_module(f"scripts.agents.{step['agent']}")
        result = agent_module.run(step["input"])

        save_project_state(project_id, {
            "current_step": step["step_id"],
            "status": "en cours",
            "plan": plan,
            "last_output": result
        })

    print("✅ Projet terminé !")
    save_project_state(project_id, {"status": "terminé"})

