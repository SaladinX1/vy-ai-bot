import streamlit as st
from core.db_manager import list_projects, get_project_state

st.title("📁 Projets enregistrés")

projects = list_projects()
for pid in projects:
    state = get_project_state(pid)
    with st.expander(f"📌 Projet : {pid}"):
        st.json(state)
