# FILE: main.py

import argparse
import threading
import time
import logging

from core.db_manager import DBManager
from core.supervisor import SupervisorAgent
from core.goal_generator import generate_goal

# --- Core modules ---
from core.orchestrator import BusinessOrchestrator
from core.scheduler import start_scheduler

# --- Scripts ---
from scripts.resume_all_projects import resume_all_projects
from scripts.task_runner import execute_project

# --- UI ---
from ui.streamlit_app import run_streamlit_ui

# --- Configure logs ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

# === UI Thread ===
def start_ui():
    threading.Thread(target=run_streamlit_ui, daemon=True).start()

# === Supervisor Thread ===
def start_supervisor():
    supervisor = SupervisorAgent()
    def loop():
        while True:
            logging.info("[Supervisor] Vérification des projets en cours...")
            supervisor.run_check_cycle()
            time.sleep(600)  # Toutes les 10 minutes

    threading.Thread(target=loop, daemon=True).start()

# === Scheduler Thread ===
def start_scheduler_thread():
    threading.Thread(target=start_scheduler, daemon=True).start()

# === Autonomous Loop ===
def autonomous_loop():
    while True:
        try:
            goal = generate_goal()
            orchestrator = BusinessOrchestrator(goals=[goal])
            orchestrator.launch_all()
        except Exception as e:
            logging.error(f"[AutonomousLoop] Erreur : {e}")
        time.sleep(3600)  # 1h d'attente entre cycles

# === Autonomous Loop Thread ===
def start_autonomous_loop():
    threading.Thread(target=autonomous_loop, daemon=True).start()

# === MAIN ENTRY ===
def main():
    parser = argparse.ArgumentParser(description="🤖 Vy-AI-Bot – Générateur de business IA")
    parser.add_argument("--objective", type=str, help="🎯 Objectif business à exécuter")
    parser.add_argument("--console", action='store_true', help="🧠 Lancer console interactive manuelle")
    parser.add_argument("--autopilot", action='store_true', help="🚀 Lancer les business automatiquement")
    args = parser.parse_args()

    logging.info("🔄 Démarrage du système Vy-AI-Bot")

    try:
        resume_all_projects()
        logging.info("✅ Projets précédents restaurés.")
    except Exception as e:
        logging.warning(f"⚠️ Erreur lors de la reprise : {e}")

    start_ui()
    start_scheduler_thread()
    start_supervisor()
    start_autonomous_loop()

    if args.objective:
        logging.info(f"🎯 Objectif unique : {args.objective}")
        plan = BusinessOrchestrator(goals=[args.objective])
        plan.launch_all()
    elif args.console:
        while True:
            cmd = input("\n🧠 Entrez un objectif ou 'exit' : ")
            if cmd.lower() == "exit":
                break
            try:
                orchestrator = BusinessOrchestrator(goals=[cmd])
                orchestrator.launch_all()
            except Exception as e:
                logging.error(f"Erreur : {e}")
    elif args.autopilot:
        logging.info("🚀 Mode autopilot activé. Les objectifs seront générés en boucle.")
        while True:
            time.sleep(60)  # laisse le thread tourner
    else:
        logging.info("⏳ Aucun mode choisi. Système en veille...")
        print("💡 Utilisez --objective, --autopilot ou --console pour démarrer.")
        while True:
            time.sleep(60)

if __name__ == "__main__":
    main()
    DBManager.init()