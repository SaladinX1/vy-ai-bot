import streamlit as st
from workflows import manager
from streamlit_elements import elements, mui, html

def app():
    st.title("✍️ Éditeur de workflows")

    workflows = manager.list_workflows()
    selected = st.selectbox("Modifier workflow existant", [""] + workflows)

    steps = []
    if selected:
        steps = manager.load_workflow(selected)

    new_step = st.text_input("Nouvelle étape (JSON dict)", "{}")

    if st.button("Ajouter étape"):
        try:
            step = eval(new_step)
            if isinstance(step, dict):
                steps.append(step)
                st.success("Étape ajoutée !")
            else:
                st.error("Entrée invalide, attendue un dict JSON.")
        except Exception as e:
            st.error(f"Erreur: {e}")

    if st.button("Sauvegarder workflow"):
        name = selected or st.text_input("Nom du workflow")
        if name and steps:
            manager.save_workflow(name, steps)
            st.success(f"Workflow '{name}' sauvegardé.")

    st.markdown("### Étapes actuelles")
    for i, step in enumerate(steps):
        st.json(step)


def workflow_editor(steps):
    with elements("workflow_editor"):
        mui.Typography("Éditeur visuel de workflow")
        for i, step in enumerate(steps):
            with mui.Paper(key=i, style={"padding": 8, "margin": "8px 0"}):
                mui.Typography(f"Étape {i+1}: {step['action']} cible: {step.get('target', 'N/A')}")
                # Boutons de modification/suppression pourraient être ajoutés ici

if __name__ == "__main__":
    app()
