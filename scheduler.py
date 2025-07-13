
# === 1. PLANIFICATION AUTOMATIQUE (avec schedule) ===
# 📁 Fichier : scheduler.py (à placer à la racine du projet)


import schedule
import time
from workflows.runner import run_workflow

# Définir les workflows à exécuter automatiquement
schedule.every().day.at("09:00").do(run_workflow, "seo_webstarter")
schedule.every().monday.at("10:00").do(run_workflow, "notion_library_builder")

print("✅ Planification active...")

while True:
    schedule.run_pending()
    time.sleep(30)
    