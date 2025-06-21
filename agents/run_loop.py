import time
from vision.screen_capture import take_screenshot
from vision.ocr import extract_text
from llm.llm_interface import get_command_response
from vision.detect_and_click import click_on_text
from execution.keyboard_control import type_text
from execution.app_launcher import open_app
import json

from agents.executor import execute_plan
from workflows.manager import save_workflow, load_workflow, list_workflows

def run_agent():
    history = []

    while True:
        print("\n💬 Que veux-tu faire ? (ou 'exit', 'list workflows', 'run <nom>', 'save <nom>')")
        user_input = input(">>> ").strip()

        if user_input.lower() == "exit":
            break
        elif user_input.startswith("run "):
            name = user_input[4:].strip()
            steps = load_workflow(name)
            for step in steps:
                execute_plan(step, "screenshot.png")
            continue
        elif user_input == "list workflows":
            print("📁 Workflows existants :", list_workflows())
            continue
        elif user_input.startswith("save "):
            name = user_input[5:].strip()
            save_workflow(name, history)
            continue

        print("📸 Capture de l'écran...")
        img_path = take_screenshot()

        print("🔍 Extraction du texte...")
        screen_text = extract_text(img_path)

        print("🧠 Analyse de l'IA...")
        ai_response = get_command_response(user_input, screen_text)

        try:
            plan = json.loads(ai_response)
            print("✅ Action comprise :", plan)

            execute_plan(plan, img_path)
            history.append(plan)

            # 💾 Proposer d'enregistrer le workflow après chaque action
            if input("💾 Sauvegarder ce workflow ? (y/n): ").lower() == 'y':
                name = input("📝 Nom du workflow : ").strip()
                save_workflow(name, history)
                history.clear()

        except Exception as e:
            print("❌ Erreur de parsing JSON ou d'exécution :", e)

        time.sleep(1)
