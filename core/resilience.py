# Objectif : Ajouter la gestion des erreurs critiques, le retry intelligent et un fallback

import time
import traceback
from utils.logger import append_log


class ResilienceManager:
    def __init__(self, max_retries=3, retry_delay=5):
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def execute_with_resilience(self, func, *args, **kwargs):
        for attempt in range(1, self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                append_log(f"⚠️ Tentative {attempt}/{self.max_retries} échouée : {e}")
                traceback.print_exc()
                time.sleep(self.retry_delay)
        append_log("🚫 Toutes les tentatives ont échoué. Passage en mode fallback.")
        return self.fallback(func.__name__, *args, **kwargs)

    def fallback(self, func_name, *args, **kwargs):
        # Implémentation simple de secours
        append_log(f"🔁 Fallback actif pour : {func_name}. Aucun plan d’urgence n’est défini.")
        return None