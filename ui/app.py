
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import threading
import time
import json

from feedback import save_feedback

from flask import session

from workflows import manager
from core import plan_executor, brain
from ui.json_editor import is_valid_json
from streamlit_elements import elements, mui
from streamlit_autorefresh import st_autorefresh
from utils.logger import read_log, append_log
from llm.generator import suggest_workflow_from_prompt

from flask import Flask, render_template, request, redirect
from workflows.runner import run_workflow
from workflows.manager import list_workflows

import csv

from flask import jsonify


LOG_FILE = "logs/execution.log"

# 🌟 Configuration de la page
st.set_page_config(page_title="Business Autonome", layout="wide")
st.title("🤖 Assistant Business Autonome")

# 🧠 Fonction : exécution d’un workflow avec gestion du stop flag et contexte partagé
def run_workflow(name, stop_flag, context):
    steps = manager.load_workflow(name)
    if not steps:
        append_log(f"❌ Workflow '{name}' introuvable ou vide.")
        return

    append_log(f"▶️ Démarrage workflow '{name}' ({len(steps)} étapes)")
    try:
        for i, step in enumerate(steps):
            if stop_flag["stop"]:
                append_log("🛑 Workflow arrêté.")
                break
            append_log(f"➡️ Étape {i+1}: {step}")
            plan_executor.execute_plan([step], context=context)
            append_log(f"✅ Étape {i+1} terminée.")
    except Exception as e:
        append_log(f"💥 Erreur à l'étape {i+1}: {e}")
    append_log(f"✔️ Fin du workflow '{name}'")

# 🧾 Affichage des logs avec autorefresh
count = st_autorefresh(interval=2000, limit=100, key="log_refresh")
log_area = st.empty()
log_area.text_area("🧾 Logs", value=read_log(), height=300, key=f"log_area_{count}")

# 🎛️ Sélection du workflow
workflows = manager.list_workflows()
selected = st.selectbox("📋 Choisir un workflow", workflows or [])

# Initialisation du stop flag et du contexte
if "stop_flag" not in st.session_state:
    st.session_state.stop_flag = {"stop": False}
if "context" not in st.session_state:
    st.session_state.context = {}

# ▶️ Execution, arrêt et amélioration IA
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    if st.button("🚀 Lancer le workflow"):
        st.session_state.stop_flag["stop"] = False
        threading.Thread(
            target=run_workflow,
            args=(selected, st.session_state.stop_flag, st.session_state.context),
            daemon=True
        ).start()
        st.success(f"Workflow '{selected}' lancé !")
with col2:
    if st.button("🛑 Arrêter le workflow"):
        st.session_state.stop_flag["stop"] = True
        st.warning("Arrêt demandé...")
with col3:
    if st.button("🧠 IA : Améliorer"):
        threading.Thread(target=brain.improve_or_iterate, daemon=True).start()
        st.success("Amélioration IA déclenchée")

# 📝 Éditeur JSON du workflow
st.markdown("### 🛠️ Modifier le workflow JSON")
workflow_path = os.path.join("workflows", f"{selected}.json")
if os.path.exists(workflow_path):
    with open(workflow_path, "r", encoding="utf-8") as f:
        content = f.read()
    edited = st.text_area("✏️ Éditer le JSON", value=content, height=400)
    with elements("modifier_workflow"):
        mui.Typography("Créer ou modifier visuellement le JSON")
    if st.button("💾 Enregistrer les modifications"):
        try:
            data = json.loads(edited)
            schema = {"type": "array", "items": {"type": "object"}}
            valid, message = is_valid_json(schema, data)
            if valid:
                with open(workflow_path, "w", encoding="utf-8") as f:
                    f.write(edited)
                st.success("✅ Modifications enregistrées.")
            else:
                st.error(f"❌ JSON invalide : {message}")
        except Exception as e:
            st.error(f"💥 Erreur JSON : {e}")

# 💡 Génération de workflow via prompt IA
st.markdown("### 💡 Générer un workflow depuis un prompt")
prompt = st.text_area("Décris ce que tu veux automatiser", height=100)
if st.button("✨ Générer le workflow depuis le prompt"):
    try:
        generated = suggest_workflow_from_prompt(prompt)
        st.text_area("📋 Résultat généré", value=generated, height=300)
        with open(workflow_path, "w", encoding="utf-8") as f:
            f.write(generated)
        st.success("🎉 Workflow généré et enregistré.")
    except Exception as e:
        st.error(f"💥 Erreur IA : {e}")

# ⏱️ Sidebar : démarrage du scheduler
with st.sidebar:
    st.markdown("### ⚙️ Tâches programmées")
    if st.button("🔄 Démarrer le scheduler"):
        threading.Thread(
            target=lambda: os.system("python3 core/scheduler.py &"),
            daemon=True
        ).start()
        st.success("✅ Scheduler lancé en arrière-plan")



app = Flask(__name__)



@app.route("/")
def index():
    workflows = list_workflows()
    return render_template("index.html", workflows=workflows)

@app.route("/run/<name>")
def launch(name):
    run_workflow(name)
    return redirect("/")

@app.route("/feedback", methods=["POST"])
def feedback():
    workflow = request.form["workflow"]
    score = request.form["score"]
    note = request.form["note"]
    save_feedback(workflow, score, note)
    return redirect("/")




# @app.route("/")
# def index():
#     if "user" not in session:
#         return redirect("/login")
#     workflows = list_workflows()
#     return render_template("index.html", workflows=workflows, user=session["user"])

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# @app.route("/dashboard")
# def dashboard():
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM feedback ORDER BY created_at DESC")
#     feedback = cursor.fetchall()
#     conn.close()

#     return render_template("dashboard.html", feedback=feedback)



# @app.route("/")
# def index():
#     workflows = list_workflows()
#     return render_template("index.html", workflows=workflows)

@app.route("/run/<name>")
def launch(name):
    run_workflow(name)
    return redirect("/")



app.secret_key = "votre_cle_secrete"



from db.db import get_connection

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/")
        return "❌ Mauvais identifiants"

    return '''
      <form method="post">
        <input name="username" placeholder="Nom d'utilisateur">
        <input name="password" type="password" placeholder="Mot de passe">
        <button type="submit">Connexion</button>
      </form>
    '''



# === API: GET /api/workflows ===
@app.route("/api/workflows")
def api_workflows():
    workflows = list_workflows()
    return jsonify({"workflows": workflows})

# === API: POST /api/run/<workflow> ===
@app.route("/api/run/<workflow>", methods=["POST"])
def api_run_workflow(workflow):
    try:
        run_workflow(workflow)
        return jsonify({"status": "success", "message": f"{workflow} lancé"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# === API: POST /api/feedback ===
@app.route("/api/feedback", methods=["POST"])
def api_feedback():
    data = request.json
    workflow = data.get("workflow")
    score = data.get("score")
    note = data.get("note", "")
    save_feedback(workflow, score, note)
    return jsonify({"status": "success", "message": "Feedback reçu"})


