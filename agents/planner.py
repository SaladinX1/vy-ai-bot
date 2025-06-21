from vision.screen_capture import take_screenshot
from vision.ocr import extract_text
from llm.llm_interface import get_command_response
from agents.executor import execute_plan
from agents.memory import Memory
import json

class AgentPlanner:
    def __init__(self):
        self.memory = Memory()

    def run(self, user_input):
        print("📸 Capture de l'écran...")
        img_path = take_screenshot()

        print("🔍 Extraction du texte...")
        screen_text = extract_text(img_path)

        print("🧠 Envoi au LLM...")

        # 👀 Ajout de contexte mémoire dans le prompt (bonus)
        context = self.memory.get_context()
        ai_response = get_command_response(user_input, screen_text, context)

        try:
            plan = json.loads(ai_response)
            print("✅ Plan d'action :", plan)

            self.memory.update(plan, user_input)
            execute_plan(plan, img_path)

        except Exception as e:
            print("❌ Erreur de parsing ou exécution :", e)
