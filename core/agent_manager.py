from core.ideator import generate_idea
from core.workflow_generator import generate_workflow
from core.executor import execute_workflow
from bots.publisher import publish_product, post_to_twitter
from core.analytics_watcher import analyze_performance, decide_next_action
from core.memory_store import save_memory

def run_autonomous_loop():
    print("🚀 Début de la boucle autonome")
    idea = generate_idea()
    print(f"💡 Idée générée : {idea}")

    workflow = generate_workflow(idea)
    print(f"📝 Plan généré : {workflow}")

    results = execute_workflow(workflow)
    print(f"✅ Workflow exécuté : {results}")

    product_data = {
        "name": idea,
        "description": "Produit créé automatiquement par l'IA.",
        "price_cents": 1500
    }
    published = publish_product(product_data)
    if published:
        print("📢 Produit publié avec succès.")

    analytics = analyze_performance()
    action = decide_next_action(analytics)
    print(f"🎯 Décision prise : {action}")

    memory_entry = {
        "idea": idea,
        "workflow": workflow,
        "results": results,
        "analytics": analytics,
        "action": action
    }
    save_memory(memory_entry)
    print("💾 Mémoire sauvegardée.")
    print("🔄 Boucle terminée, en attente pour redémarrer.")
