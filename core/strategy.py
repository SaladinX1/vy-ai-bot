import random
from utils.logger import load_logs_summary
from core.business_templates import load_available_templates

def decide_next_action():
    """Détermine le prochain objectif stratégique automatiquement."""
    logs = load_logs_summary()
    templates = load_available_templates()

    # Ex : éviter les échecs fréquents ou réessayer si succès
    last_failures = [log['workflow'] for log in logs[-10:] if log['status'] == 'fail']
    last_successes = [log['workflow'] for log in logs[-10:] if log['status'] == 'success']

    if len(last_failures) > 5:
        return "Analyser et corriger workflow échoués"
    elif len(last_successes) > 3:
        return random.choice([t['goal'] for t in templates])
    else:
        return "Lancer un business modèle simple"