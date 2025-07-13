# import streamlit as st
# import threading
# import time
# import os

# from fastapi import APIRouter
# from fastapi.responses import JSONResponse

# router = APIRouter()

# # Dummy data (à remplacer par vraie base de données / suivi)
# sales_data = {
#     "total_sales": 25,
#     "revenue": 1250.50,
#     "active_customers": 18,
#     "products_sold": {
#         "Ebook": 15,
#         "Templates": 10
#     }
# }

# @router.get("/api/dashboard")
# async def get_dashboard_data():
#     return JSONResponse(content=sales_data)


# LOG_FILE = "execution.log"

# def append_log(text):
#     with open(LOG_FILE, "a", encoding="utf-8") as f:
#         f.write(text + "\n")

# def read_log():
#     if not os.path.exists(LOG_FILE):
#         return ""
#     with open(LOG_FILE, "r", encoding="utf-8") as f:
#         return f.read()

# def run_workflow_thread(name, manager, plan_executor):
#     steps = manager.load_workflow(name)
#     if not steps:
#         append_log(f"❌ Workflow '{name}' introuvable ou vide.")
#         return

#     append_log(f"▶️ Démarrage workflow '{name}' - {len(steps)} étapes")

#     for i, step in enumerate(steps):
#         append_log(f"➡️ Étape {i+1}: {step}")
#         try:
#             plan_executor.execute_plan([step])
#             append_log(f"✅ Étape {i+1} terminée.")
#         except Exception as e:
#             append_log(f"❌ Erreur étape {i+1}: {e}")
#             break

#     append_log(f"✔️ Fin du workflow '{name}'")

# def app():
#     from workflows import manager
#     from core import plan_executor

#     st.title("🛠️ Dashboard Workflows")

#     workflows = manager.list_workflows()
#     selected = st.selectbox("Choisir un workflow", workflows)

#     if st.button("Lancer le workflow"):
#         thread = threading.Thread(target=run_workflow_thread, args=(selected, manager, plan_executor))
#         thread.start()
#         st.success(f"Workflow '{selected}' lancé !")

#     st.markdown("### Logs d'exécution")
#     log_text = read_log()
#     st.text_area("Logs", value=log_text, height=300)

# if __name__ == "__main__":
#     app()


import streamlit as st
import json
import os


st.set_page_config(page_title="Business Dashboard", layout="wide")
st.title("📊 Business Autonome – Dashboard")

if os.path.exists("logs.json"):
    with open("logs.json", "r", encoding="utf-8") as f:
        logs = json.load(f)
else:
    logs = []

st.subheader("🧠 Logs Récents")
for log in reversed(logs[-10:]):
    st.code(log)

if os.path.exists("feedback.json"):
    with open("feedback.json", "r", encoding="utf-8") as f:
        feedback = json.load(f)
        st.subheader("📈 Feedbacks des Workflows")
        for f in reversed(feedback[-5:]):
            st.write(f)

            

MEMORY_PATH = "memory_store.json"

def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return []
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)

def main():
    st.title("🧠 Générateur de Business Autonome - Supervision")
    memory = load_memory()
    if not memory:
        st.info("Aucune mémoire enregistrée pour l'instant.")
    else:
        last_run = memory[-1]
        st.subheader("Dernier cycle exécuté")
        st.json(last_run)

    if st.button("Lancer un nouveau cycle"):
        from core.agent_manager import run_autonomous_loop
        run_autonomous_loop()
        st.success("Cycle exécuté, actualisez la page pour voir les résultats.")

if __name__ == "__main__":
    main()




