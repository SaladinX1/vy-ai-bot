from workflows import manager
from core import plan_executor


def execute_workflow(steps):
    for step in steps:
        if step["action"] == "if":
            condition = step["condition"]
            substeps = step["then"] if evaluate_condition(condition) else step.get("else", [])
            execute_workflow(substeps)
        elif step["action"] == "call_subworkflow":
            sub_name = step["target"]
            sub_steps = manager.load_workflow(sub_name)
            execute_workflow(sub_steps)
        else:
            plan_executor.execute_plan([step])


def evaluate_condition(condition):
    # Ex. {"type": "element_exists", "target": "Connexion"}
    if condition["type"] == "element_exists":
        from vision import recognizer
        return recognizer.detect_element("screenshot.png", condition["target"])
    return False