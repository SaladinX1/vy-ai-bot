from core import brain
from core.auto_executor import run_workflow_with_retry
from workflows import manager
from core import plan_executor
from ui.streamlit_app import append_log

def autonomous_improve_and_run(workflow_name):
    append_log(f"🧠 Début cycle auto-amélioration et exécution pour '{workflow_name}'")

    success = run_workflow_with_retry(workflow_name, manager, plan_executor)

    if not success:
        append_log("⚙️ Workflow échoué, déclenchement de l'amélioration automatique...")
        try:
            brain.improve_or_iterate()
            append_log("✅ Amélioration automatique effectuée, relance du workflow.")
            run_workflow_with_retry(workflow_name, manager, plan_executor)
        except Exception as e:
            append_log(f"❌ Échec de l'amélioration automatique : {e}")
    else:
        append_log(f"✔️ Workflow '{workflow_name}' terminé avec succès sans amélioration.")

