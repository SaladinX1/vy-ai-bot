# main.py

from vision.screen_capture import take_screenshot
from vision.ocr import extract_text
from llm.llm_interface import get_command_response
import json
from vision.detect_and_click import click_on_text
from execution.keyboard_control import type_text
from execution.app_launcher import open_app
from agents.run_loop import run_agent
from agents.planner import AgentPlanner

import threading
import time
from core.scheduler import start_scheduler
from core.orchestrator import BusinessOrchestrator
from ui.streamlit_app import run_streamlit_ui


def start_ui():
    """Démarre l’interface utilisateur Streamlit (optionnelle mais utile pour surveillance)."""
    threading.Thread(target=run_streamlit_ui, daemon=True).start()


def start_scheduler_thread():
    """Démarre le scheduler (workflow planifiés dans workflow_schedule.json)."""
    threading.Thread(target=start_scheduler, daemon=True).start()


def launch_autonomous_business_goals():
    """Définir ici les idées de business à lancer automatiquement."""
    business_goals = [
        "Créer un blog SEO sur les IA en 2025",
        "Développer une micro-solution SaaS pour freelances",
        "Automatiser un tunnel de vente pour e-book",
        "Créer une chaîne TikTok automatisée",
    ]
    orchestrator = BusinessOrchestrator(goals=business_goals)
    orchestrator.launch_all()


def interactive_console():
    """Console CLI agent : exécution manuelle."""
    agent = AgentPlanner()
    while True:
        user_input = input("\n💬 Que veux-tu faire ? (exit pour quitter) >>> ")
        if user_input.lower() == "exit":
            break
        agent.run(user_input)


if __name__ == "__main__":
    print("🚀 Initialisation de l’agent générateur de business autonome...")

    # Lancement des modules parallèles
    start_ui()
    start_scheduler_thread()
    launch_autonomous_business_goals()

    # Console CLI interactive (optionnelle)
    interactive_console()

    # Boucle de maintien principale
    while True:
        time.sleep(60)
