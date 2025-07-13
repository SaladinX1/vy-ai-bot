import time
from workflows.manager import save_workflow

class Recorder:
    def __init__(self):
        self.recording = False
        self.actions = []

    def is_recording(self):
        return self.recording

    def start(self):
        if self.recording:
            print("⚠️ Enregistrement déjà actif.")
            return
        print("🔴 Mode enregistrement démarré...")
        self.recording = True
        self.actions.clear()

    def stop(self, name):
        if not self.recording:
            print("❌ Aucun enregistrement en cours.")
            return
        if not name:
            print("❌ Nom de workflow invalide.")
            return
        self.recording = False
        if not self.actions:
            print("⚠️ Rien à sauvegarder.")
            return
        print(f"⏹️ Enregistrement arrêté. Sauvegarde sous '{name}'...")
        save_workflow(name, self.actions)

    def record_step(self, step):
        if not self.recording:
            print("⚠️ Enregistrement non démarré, action ignorée.")
            return
        self.actions.append(step)
        # Optionnel : print(f"📝 Action enregistrée : {step}")

    # Méthodes pratiques pour enregistrer rapidement des actions spécifiques
    def record_click(self, target):
        self.record_step({"action": "click", "target": target, "value": None})

    def record_type(self, value):
        self.record_step({"action": "type", "target": None, "value": value})

    def record_open_app(self, target):
        self.record_step({"action": "open_app", "target": target, "value": None})
