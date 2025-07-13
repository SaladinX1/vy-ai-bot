from core.auto_feedback import autonomous_improve_and_run
from ui.streamlit_app import append_log

class AutonomousAgent:
    def __init__(self, workflow_name):
        self.workflow_name = workflow_name
        self.failure_count = 0
        self.max_failures = 5

    def run_cycle(self):
        append_log("🤖 Agent autonome démarre un cycle.")
        try:
            autonomous_improve_and_run(self.workflow_name)
            self.failure_count = 0
        except Exception as e:
            append_log(f"❌ Agent détecte une erreur: {e}")
            self.failure_count += 1
            if self.failure_count >= self.max_failures:
                append_log("⚠️ Trop d’échecs consécutifs, alerte nécessaire.")
                self.alert_admin()
            else:
                append_log("🔄 Réessayer le workflow au prochain cycle.")

    def alert_admin(self):
        # Pour l’instant on logue, à compléter avec email/webhook etc.
        append_log("🚨 Alerte admin : intervention humaine requise.")
