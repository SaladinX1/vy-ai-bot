# ui/streamlit_app.py

import streamlit as st
import threading


from core.db_manager import DBManager



import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Forcer l'ajout du dossier racine (C:/vy-clone) au PYTHONPATH
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


from workflows import manager
from core import plan_executor
from core import brain
from streamlit_autorefresh import st_autorefresh



LOG_FILE = "execution.log"

def append_log(text):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def read_log():
    if not os.path.exists(LOG_FILE):
        return ""
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return f.read()

def run_workflow_thread(name, manager, plan_executor):
    steps = manager.load_workflow(name)
    if not steps:
        append_log(f"❌ Workflow '{name}' introuvable ou vide.")
        return

    append_log(f"▶️ Démarrage workflow '{name}' - {len(steps)} étapes")

    for i, step in enumerate(steps):
        append_log(f"➡️ Étape {i+1}: {step}")
        try:
            plan_executor.execute_plan([step])
            append_log(f"✅ Étape {i+1} terminée.")
        except Exception as e:
            append_log(f"❌ Erreur étape {i+1}: {e}")
            break

    append_log(f"✔️ Fin du workflow '{name}'")

def run_streamlit_ui():
    st.title("Vy-AI-Bot - Projets en cours")

    projects = DBManager.list_projects() 
    # list_projects()
    for p in projects:
        st.write(f"**Objectif:** {p.objective}")
        st.write(f"Statut: {p.status}")
        st.write("---")

    if st.button("Recharger"):
        st.experimental_rerun()

def app():

    st.set_page_config(page_title="Assistant Business Autonome", layout="wide")
    st.title("🧠 Assistant Business Autonome")

    workflows = manager.list_workflows()
    selected = st.selectbox("Choisir un workflow", workflows)

    col1, col2, col3 = st.columns([2, 1, 1])

    if col1.button("▶️ Lancer le workflow"):
        thread = threading.Thread(target=run_workflow_thread, args=(selected, manager, plan_executor), daemon=True)
        thread.start()
        st.success(f"Workflow '{selected}' lancé !")

    if col2.button("🔁 Analyse IA (amélioration automatique)"):
        brain.improve_or_iterate()
        st.success("Amélioration automatique déclenchée !")

    if col3.button("📊 Mettre à jour le dashboard"):
        st.rerun()

    # Auto-refresh des logs toutes les 5 secondes
    st_autorefresh(interval=5000, limit=None, key="log_refresh")

    st.markdown("### 📄 Logs d'exécution")
    log_text = read_log()
    st.text_area("Logs", value=log_text, height=300)

if __name__ == "__main__":
    from core.scheduler import start_scheduler  # ✅ décalé ici, pour éviter l'import circulaire

# Démarrage scheduler sur le workflow sélectionné, intervalle 24h (86400 sec)
   
    workflows = manager.list_workflows()
    if workflows:
        start_scheduler(workflows[0], interval_seconds=86400)

    app()



    