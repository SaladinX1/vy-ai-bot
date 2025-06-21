from vision.detect_and_click import click_on_text
from execution.keyboard_control import type_text
from execution.app_launcher import open_app

def execute_plan(plan, img_path=None):
    action = plan.get("action")
    target = plan.get("target")
    value = plan.get("value")

    if action == "click" and target:
        if not img_path:
            print("❌ Image requise pour le clic.")
            return
        print(f"🖱️ Clic sur : {target}")
        click_on_text(img_path, target)

    elif action == "type" and value:
        print(f"⌨️ Saisie du texte : {value}")
        type_text(value)

    elif action == "open_app" and target:
        print(f"🚀 Ouverture de l'application : {target}")
        open_app(target)

    else:
        print("❗ Action non reconnue ou incomplète :", plan)
