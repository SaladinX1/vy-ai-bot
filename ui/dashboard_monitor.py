import streamlit as st
from core.memory_store import load_memory

def dashboard_monitor():
    st.title("📈 Monitoring Automatisé")

    logs = load_memory()

    error_logs = [log for log in logs if "❌" in log.get("content", "")]
    success_logs = [log for log in logs if "✅" in log.get("content", "")]

    st.markdown(f"### 📊 Statistiques d’exécution")
    st.write(f"✔️ Succès : {len(success_logs)}")
    st.write(f"❌ Erreurs : {len(error_logs)}")

    if error_logs:
        st.markdown("### ❗ Dernières erreurs")
        for log in error_logs[-5:]:
            st.write(f"{log['timestamp']} - {log['content']}")

    # Alerting basique : afficher alerte dans le dashboard
    if len(error_logs) > 10:
        st.error("🚨 Trop d’erreurs détectées, intervention requise.")

if __name__ == "__main__":
    dashboard_monitor()
