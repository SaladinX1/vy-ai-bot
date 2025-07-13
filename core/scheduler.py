import schedule
import time
import threading
import json
from core.agent import AutonomousAgent
from workflows import manager
from core.auto_executor import run_workflow_with_retry  # à créer si pas encore fait

from core import plan_executor
from utils.logger import append_log

from core.agent_manager import run_autonomous_loop

def run_workflow(name):
    append_log(f"▶️ Programmation exécutée: {name}")
    try:
        run_workflow_with_retry(name, manager, plan_executor)
    except Exception as e:
        append_log(f"💥 Échec irrécupérable du workflow planifié '{name}': {e}")

def schedule_loop(interval_minutes=60):
    agent = AutonomousAgent("default")  # ou choisir dynamiquement selon ton use case
    while True:
        agent.run_cycle()
        time.sleep(interval_minutes * 60)

def start_scheduler():
    try:
        data = json.load(open("workflow_schedule.json", encoding="utf-8"))
    except Exception as e:
        append_log(f"❌ Impossible de lire workflow_schedule.json: {e}")
        return

    for item in data:
        cron = item.get("cron", "")
        w = item.get("workflow")
        try:
            h, m = cron.split()[1], cron.split()[0]
            job = schedule.every().day.at(f"{int(h):02d}:{int(m):02d}").do(run_workflow, name=w)
            append_log(f"⏰ Planifié '{w}' chaque jour à {h}:{m}")
        except Exception as e:
            append_log(f"⚠️ Cron invalide '{cron}' pour '{w}': {e}")

    def loop():
        while True:
            schedule.run_pending()
            time.sleep(10)
    threading.Thread(target=loop, daemon=True).start()
    append_log("✅ Scheduler démarré en tâche de fond")

if __name__ == "__main__":
    start_scheduler()
    while True:
        time.sleep(86400)

