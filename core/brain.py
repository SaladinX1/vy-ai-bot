import json
from analytics.analytics_watcher import get_gumroad_sales
from workflows import manager
from core import plan_executor
from core.vectorstore import memory
from core.utils.logger import append_log

def improve_product(product_id):
    append_log(f"[BRAIN] IA améliore produit {product_id}")
    plan = manager.generate_improvement_workflow(product_id)
    plan_executor.execute_plan(plan)

def analyze_results():
    sales = get_gumroad_sales()
    for pid, count in sales.items():
        if count < 2:
            append_log(f"[BRAIN] Faibles ventes pour {pid} ({count}), relance IA")
            improve_product(pid)

    try:
        logs = open("logs/execution.log", encoding="utf-8").read()
    except:
        logs = ""
    if "❌" in logs:
        append_log("[BRAIN] Erreurs détectées, ré-execution prévue")
        # à étendre : récupérer last workflow
    mem = memory.retrieve_all()
    for entry in mem:
        if entry.get("status") == "failed":
            append_log(f"[BRAIN] Mémoire signale échec pour {entry['id']}, replanification")
            improve_product(entry["id"])

def improve_or_iterate():
    append_log("[BRAIN] Démarrage de l’analyse IA")
    analyze_results()
    append_log("[BRAIN] Analyse terminée")
