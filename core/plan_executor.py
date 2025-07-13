# ✅ plan_executor.py modifié avec gestion des variables dynamiques

import pyautogui
import time
import logging
import json
import re
from vision.guards import detect_blockers
from vision.recognizer import extract_text_from_image
from core.utils.logger import log_info, log_error, append_log, read_log


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)

import os
from datetime import datetime

MEMORY_PATH = "memory.json"

def execute_plan(plan, context=None):
    if detect_blockers():  # ✅ détection CAPTCHA
        append_log("🛑 Captcha détecté. Passage en mode attente.")
        return

def resolve_variables(obj, context):
    """
    Remplace toutes les occurrences {{var}} dans un string ou dict avec leur valeur dans context.
    """
    if isinstance(obj, str):
        matches = re.findall(r"\{\{(.*?)\}\}", obj)
        for m in matches:
            if m in context:
                obj = obj.replace(f"{{{{{m}}}}}", str(context[m]))
        return obj
    elif isinstance(obj, dict):
        return {k: resolve_variables(v, context) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [resolve_variables(item, context) for item in obj]
    else:
        return obj

class Action:
    def __init__(self, action_type, target=None, value=None, context=None):
        self.action = action_type
        self.target = target
        self.value = value
        self.context = context or {}

    def execute(self):
        try:
            # Résolution variables dans target et value
            self.target = resolve_variables(self.target, self.context)
            self.value = resolve_variables(self.value, self.context)

            logging.info(f"🚀 Exécution: {self.action} | Target: {self.target} | Value: {self.value}")
            method = getattr(self, f"_{self.action}", None)
            if method:
                method()
            else:
                logging.error(f"❌ Action inconnue: {self.action}")
                raise ValueError(f"Action inconnue: {self.action}")
        except Exception as e:
            logging.error(f"💥 Erreur pendant l'exécution de l'action {self.action}: {e}")
            raise

    def _click(self):
        if self.target:
            location = pyautogui.locateCenterOnScreen(f"images/{self.target}.png", confidence=0.8)
            if location:
                pyautogui.click(location)
                logging.info(f"✅ Click sur {self.target}")
            else:
                logging.warning(f"🔍 Élément {self.target} non trouvé à l'écran.")
                raise RuntimeError(f"Élément {self.target} non trouvé pour click.")
        else:
            pyautogui.click()
            logging.info("✅ Click générique effectué.")

    def _type(self):
        if self.value:
            pyautogui.write(self.value, interval=0.05)
            logging.info(f"⌨️ Saisie: {self.value}")
        else:
            logging.warning("⛔ Aucune valeur fournie pour l'action de saisie.")
            raise ValueError("Valeur manquante pour l'action type.")

    def _open_app(self):
        if self.target:
            pyautogui.press('win')
            time.sleep(0.5)
            pyautogui.write(self.target)
            pyautogui.press('enter')
            logging.info(f"📂 Application lancée: {self.target}")
        else:
            logging.warning("⛔ Aucun nom d'application fourni pour open_app.")
            raise ValueError("Target manquant pour open_app.")

    def _wait_until(self, timeout=20):
        if self.target:
            logging.info(f"⏳ Attente de l'apparition de {self.target} (timeout {timeout}s)...")
            start = time.time()
            while time.time() - start < timeout:
                location = pyautogui.locateOnScreen(f"images/{self.target}.png", confidence=0.8)
                if location:
                    logging.info(f"🟢 Élément détecté: {self.target}")
                    return
                time.sleep(1)
            logging.warning(f"⛔ Élément {self.target} non détecté après délai de {timeout}s.")
            raise TimeoutError(f"Élément {self.target} non détecté dans le temps imparti.")
        else:
            logging.warning("⛔ Aucun target fourni pour wait_until.")
            raise ValueError("Target manquant pour wait_until.")

    def _if_element_found(self):
        if not self.target or not isinstance(self.value, list):
            raise ValueError("Action if_element_found requiert un 'target' et une liste d'actions dans 'value'")
        location = pyautogui.locateOnScreen(f"images/{self.target}.png", confidence=0.8)
        if location:
            logging.info(f"🟡 Élément trouvé : {self.target} — exécution conditionnelle")
            for substep in self.value:
                subaction = Action(substep["action"], substep.get("target"), substep.get("value"), self.context)
                subaction.execute()
        else:
            logging.info(f"❌ Élément non trouvé : {self.target} — aucune action exécutée")

    def _repeat_until_found(self):
        if not self.target or not isinstance(self.value, list):
            raise ValueError("Action repeat_until_found requiert un 'target' et une liste d'actions dans 'value'")
        
        timeout = 15
        start_time = time.time()

        logging.info(f"🔁 Répétition jusqu'à détection de {self.target} (timeout {timeout}s)")
        while time.time() - start_time < timeout:
            location = pyautogui.locateOnScreen(f"images/{self.target}.png", confidence=0.8)
            if location:
                logging.info(f"✅ Élément détecté : {self.target}")
                return
            for step in self.value:
                subaction = Action(step["action"], step.get("target"), step.get("value"), self.context)
                subaction.execute()
            time.sleep(1)

        logging.warning(f"⛔ Élément {self.target} non trouvé après {timeout}s")
        raise TimeoutError(f"Élément {self.target} non détecté après répétition.")

    def _wait_for_text(self):
        expected = self.value.lower() if self.value else ""
        timeout = 15
        start = time.time()

        while time.time() - start < timeout:
            pyautogui.screenshot("screenshot.png")
            text = extract_text_from_image("screenshot.png")
            if expected in text:
                logging.info(f"🟢 Texte détecté: {expected}")
                return
            time.sleep(1)

        logging.warning(f"⛔ Texte '{expected}' non détecté dans le délai imparti")
        raise TimeoutError(f"Texte '{expected}' non détecté dans les logs.")

    def _set_variable(self):
        if self.target and self.value is not None:
            self.context[self.target] = self.value
            logging.info(f"📌 Variable définie : {self.target} = {self.value}")
        else:
            raise ValueError("Action set_variable nécessite un 'target' et une 'value'")
        
    def log_event(event_type, content):
        memory = load_memory()
        memory.append({
            "timestamp": datetime.utcnow().isoformat(),
            "type": event_type,
            "content": content
        })
        with open(MEMORY_PATH, "w") as f:
            json.dump(memory, f, indent=2)

    def load_memory():
        if not os.path.exists(MEMORY_PATH):
            return []
        with open(MEMORY_PATH, "r") as f:
            return json.load(f)
        
def execute_plan(plan, context=None):
    if isinstance(plan, str):
        plan = json.loads(plan)
    if context is None:
        context = {}
    for step in plan:
        step_resolved = resolve_variables(step, context)
        action = Action(step_resolved["action"], step_resolved.get("target"), step_resolved.get("value"), context)
        action.execute()

