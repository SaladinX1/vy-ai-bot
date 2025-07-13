from vision.detect_and_click import click_on_text
from execution.keyboard_control import type_text
from execution.app_launcher import open_app
import time
from vision.ocr import extract_text
from vision.screen_capture import take_screenshot

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

    elif action == "wait_until" and target:
        print(f"⏳ Attente jusqu'à voir : {target}")
        max_wait = 20  # secondes
        delay = 2
        waited = 0
        while waited < max_wait:
            img_path = take_screenshot()
            screen_text = extract_text(img_path)
            if target.lower() in screen_text.lower():
                print("✅ Condition remplie.")
                return
            print(f"🔄 Toujours pas trouvé ({waited}s)...")
            time.sleep(delay)
            waited += delay
        print("❌ Timeout : élément non trouvé.")

    else:
        print("❗ Action non reconnue ou incomplète :", plan)
