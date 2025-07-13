import pyautogui
import time
from vision.logger_config import setup_logger

logger = setup_logger()

class BaseAction:
    def __init__(self, target=None, value=None):
        self.target = target
        self.value = value

    def execute(self):
        raise NotImplementedError("Méthode execute doit être implémentée.")

    def undo(self):
        # Optionnel, à implémenter si besoin
        pass

class ClickAction(BaseAction):
    def execute(self):
        logger.info(f"🚀 ClickAction | Target: {self.target}")
        if self.target:
            location = pyautogui.locateCenterOnScreen(f"images/{self.target}.png", confidence=0.8)
            if location:
                pyautogui.click(location)
                logger.info(f"✅ Click sur {self.target}")
            else:
                logger.warning(f"🔍 Élément {self.target} non trouvé à l'écran.")
                raise RuntimeError(f"Élément {self.target} non trouvé pour click.")
        else:
            pyautogui.click()
            logger.info("✅ Click générique effectué.")

class TypeAction(BaseAction):
    def execute(self):
        logger.info(f"🚀 TypeAction | Value: {self.value}")
        if self.value:
            pyautogui.write(self.value, interval=0.05)
            logger.info(f"⌨️ Saisie: {self.value}")
        else:
            logger.warning("⛔ Aucune valeur fournie pour saisie.")
            raise ValueError("Valeur manquante pour TypeAction.")

class OpenAppAction(BaseAction):
    def execute(self):
        logger.info(f"🚀 OpenAppAction | Target: {self.target}")
        if self.target:
            pyautogui.press('win')
            time.sleep(0.5)
            pyautogui.write(self.target)
            pyautogui.press('enter')
            logger.info(f"📂 Application lancée: {self.target}")
        else:
            logger.warning("⛔ Aucun nom d'application fourni pour OpenApp.")
            raise ValueError("Target manquant pour OpenAppAction.")

class WaitUntilAction(BaseAction):
    def execute(self, timeout=20):
        logger.info(f"⏳ WaitUntilAction | Target: {self.target} (timeout {timeout}s)")
        if self.target:
            start = time.time()
            while time.time() - start < timeout:
                location = pyautogui.locateOnScreen(f"images/{self.target}.png", confidence=0.8)
                if location:
                    logger.info(f"🟢 Élément détecté: {self.target}")
                    return
                time.sleep(1)
            logger.warning(f"⛔ Élément {self.target} non détecté après délai.")
            raise TimeoutError(f"Élément {self.target} non détecté dans le temps imparti.")
        else:
            logger.warning("⛔ Aucun target fourni pour WaitUntil.")
            raise ValueError("Target manquant pour WaitUntilAction.")

# Registre dynamique
actions_registry = {
    "click": ClickAction,
    "type": TypeAction,
    "open_app": OpenAppAction,
    "wait_until": WaitUntilAction,
}

def get_action_instance(action_type, target=None, value=None):
    cls = actions_registry.get(action_type)
    if not cls:
        raise ValueError(f"Action inconnue: {action_type}")
    return cls(target, value)
