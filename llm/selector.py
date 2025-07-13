# llm/selector.py

def select_best_model(task_type: str = "generation") -> str:
    """
    Sélectionne dynamiquement le modèle LLM selon la tâche.
    """
    if task_type in ["correction", "résumé"]:
        return "mistral-tiny"
    elif task_type in ["idée business", "planification"]:
        return "mistral-medium"
    else:
        return "mistral-tiny"  # Par défaut
