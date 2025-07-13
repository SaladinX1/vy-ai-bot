import json
import jsonschema
from vision.screen_capture import take_screenshot
from vision.ocr import extract_text
from llm.llm_interface import get_command_response
from agents.executor import execute_plan
from agents.memory import Memory

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

    def run(self, user_input):
        print("📸 Capture de l'écran...")
        img_path = take_screenshot()

        print("🔍 Extraction du texte...")
        screen_text = extract_text(img_path)

        print("🧠 Envoi au LLM...")
        context = self.memory.get_context()
        ai_response = get_command_response(user_input, screen_text, context)

        try:
            plans = json.loads(ai_response)
            jsonschema.validate(instance=plans, schema=PLAN_SCHEMA)
            print(f"✅ {len(plans)} action(s) planifiée(s)")

            for i, plan in enumerate(plans, 1):
                try:
                    print(f"\n⚙️  [{i}/{len(plans)}] Exécution : {plan}")
                    execute_plan(plan, img_path)
                    self.memory.update(plan, user_input)
                except Exception as e:
                    print(f"❌ Erreur pendant l'action {i} : {e}")
                    # 🛠️ Option : journaliser l'erreur ou proposer une reprise

        except json.JSONDecodeError:
            print("❌ Réponse JSON invalide :", ai_response)
        except jsonschema.ValidationError as ve:
            print(f"❌ JSON non conforme au schéma: {ve.message}")
        except Exception as e:
            print("❌ Erreur générale :", e)
