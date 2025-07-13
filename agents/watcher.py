import time
import threading
from vision.screen_capture import take_screenshot
from vision.ocr import extract_text
from agents.executor import execute_plan
from agents.memory import Memory
from llm.llm_interface import get_command_response
import json
import jsonschema

import os
from datetime import datetime
from workflows.manager import save_workflow

from agents.planner import AgentPlanner

agent = AgentPlanner()

# Liste des règles (déclencheurs)
rules = [
    {
        "trigger": "Erreur 404",
        "plan": {"action": "click", "target": "Réessayer", "value": None}
    },
    {
        "trigger": "Connexion",
        "plan": [
            {"action": "type", "value": "monemail@mail.com"},
            {"action": "type", "value": "motdepasse123"},
            {"action": "click", "target": "Se connecter"}
        ]
    }
]

agent.watch_triggers(rules)



PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "enum": ["click", "type", "open_app", "wait_until"]
        },
        "target": {"type": ["string", "null"]},
        "value": {"type": ["string", "null"]}
    },
    "required": ["action"],
    "additionalProperties": False
}


class AgentPlanner:
    def __init__(self):
        self.memory = Memory()

    def watch_triggers(self, rules, interval=3):
        print("🚫 Mode surveillance activé. Ctrl+C pour quitter.")
        import time

        triggered_history = []

        try:
            while True:
                img_path = take_screenshot()
                screen_text = extract_text(img_path)

                for rule in rules:
                    if rule["trigger"].lower() in screen_text.lower():
                        plan = rule["plan"]
                        print(f"🔍 Déclencheur détecté: {rule['trigger']} -> exécution du plan")

                        plans = plan if isinstance(plan, list) else [plan]
                        for p in plans:
                            execute_plan(p, img_path)
                            triggered_history.append(p)

                        # 🔖 Sauvegarder le workflow automatiquement sous un nom horodaté
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        save_workflow(f"auto_trigger_{rule['trigger']}_{timestamp}", triggered_history)
                        triggered_history.clear()

                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n🔚 Surveillance stoppée par l'utilisateur.")
