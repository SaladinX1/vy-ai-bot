# main_loop.py

import time
from core.goal_generator import generate_goal
from core.orchestrator import BusinessOrchestrator
from core.supervisor import SupervisorAgent
from utils.logger import append_log

def main_loop(polling_interval_minutes=10):
    supervisor = SupervisorAgent()

    while True:
        append_log("🔄 Lancement du cycle principal")

        try:
            # 🧠 Génération d’un nouveau goal
            new_goal = generate_goal()
            append_log(f"🎯 Nouveau goal généré : {new_goal}")

            orchestrator = BusinessOrchestrator(goals=[new_goal])
            orchestrator.launch_all()

        except Exception as e:
            append_log(f"❌ Erreur pendant la génération/exécution du goal : {e}")

        try:
            # 🛠️ Supervision des projets existants
            supervisor.run_check_cycle()

        except Exception as e:
            append_log(f"❌ Erreur dans la supervision : {e}")

        append_log(f"⏳ Attente {polling_interval_minutes} min avant prochain cycle.\n")
        time.sleep(polling_interval_minutes * 60)

if __name__ == "__main__":
    main_loop()



# ☑️ Prochaine étape :

# Pour l’exécuter en permanence :

# Avec pm2 :


# pm2 start main_loop.py --interpreter=python3 --name=bizloop

########################################

# Ou avec cron (si tu veux un déclenchement périodique sans boucle) :


# */10 * * * * /usr/bin/python3 /path/to/main_loop.py >> /path/to/logs/bizloop.log 2>&1