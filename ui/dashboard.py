# ui/dashboard.py

import streamlit as st
import json
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from core.db_manager import DBManager

# ───────────────────────────────────────────────────────────────
# SECTION STREAMLIT - INTERFACE LOCALE
# ───────────────────────────────────────────────────────────────

LOGS_PATH = "logs.json"
FEEDBACK_PATH = "feedback.json"
MEMORY_PATH = "memory_store.json"

def load_json(path, default=[]):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def streamlit_ui():
    st.set_page_config(page_title="Business Dashboard", layout="wide")
    st.title("📊 Dashboard – Business Autonome")

    # Logs
    logs = load_json(LOGS_PATH)
    st.subheader("🧠 Logs Récents")
    for log in reversed(logs[-10:]):
        st.code(log)

    # Feedbacks
    feedback = load_json(FEEDBACK_PATH)
    if feedback:
        st.subheader("📈 Feedbacks des Workflows")
        for f in reversed(feedback[-5:]):
            st.write(f)

    # Mémoire de cycle
    memory = load_json(MEMORY_PATH)
    st.subheader("📂 Dernier cycle mémoire")
    if memory:
        st.json(memory[-1])
    else:
        st.info("Aucune exécution mémoire enregistrée.")

    # Bouton exécution
    if st.button("🚀 Lancer un nouveau cycle"):
        from core.agent_manager import run_autonomous_loop
        run_autonomous_loop()
        st.success("✅ Cycle lancé. Rechargez la page pour voir les nouveaux résultats.")

# ───────────────────────────────────────────────────────────────
# SECTION FASTAPI - API REST POUR INTERFACES EXTERNES
# ───────────────────────────────────────────────────────────────

app = FastAPI()

@app.get("/api/projects")
def list_projects():
    return DBManager.list_projects()

@app.get("/api/projects/{project_id}")
def get_project_state(project_id: str):
    return DBManager.get_project_state(project_id)

@app.get("/api/dashboard")
def get_dashboard_data():
    return JSONResponse(content={
        "total_sales": 25,
        "revenue": 1250.50,
        "active_customers": 18,
        "products_sold": {
            "Ebook": 15,
            "Templates": 10
        }
    })

# ───────────────────────────────────────────────────────────────
# POINT D'ENTRÉE STREAMLIT
# ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    streamlit_ui()

# Pour exécuter FastAPI : uvicorn ui.dashboard:app --reload --port 8000
# Pour exécuter Streamlit : streamlit run ui/dashboard.py
