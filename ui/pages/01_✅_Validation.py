# Fichier : ui/pages/01_✅_Validation.py

import streamlit as st
from core.db_manager import list_projects, get_project_state, save_project_state

st.title("🧠 Validation humaine")

for pid in list_projects():
    state = get_project_state(pid)
    if state.get("status") == "pending_validation":
        st.subheader(f"Projet : {pid}")
        st.json(state)
        if st.button(f"✅ Valider {pid}"):
            state["status"] = "validated"
            save_project_state(pid, state)
        if st.button(f"❌ Rejeter {pid}"):
            state["status"] = "rejected"
            save_project_state(pid, state)