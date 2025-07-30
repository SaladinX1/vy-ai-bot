# core/goal_generator.py

import random
from core.data_enricher import get_trending_keywords

# ─────────────────────────────────────────────
# Templates statiques (fallback)
# ─────────────────────────────────────────────

GOAL_TEMPLATES = [
    "Créer un business sur {niche} pour {audience}",
    "Monétiser une compétence en {niche} via un produit numérique",
    "Lancer un service d'abonnement autour de {niche}"
]

NICHES = ["fitness", "crypto", "éducation", "AI", "écologie"]
AUDIENCES = ["étudiants", "parents", "freelances", "PME"]


# ─────────────────────────────────────────────
# Générateur principal de goal
# ─────────────────────────────────────────────

def generate_goal():
    """Génère un objectif de business basé sur une tendance si possible, sinon fallback."""
    try:
        trends = get_trending_keywords("startups")
        if trends:
            return f"Lancer un business autour de : {trends[0]}"
    except Exception as e:
        print(f"[⚠️ Trends indisponible] {e}")

    # Fallback : génération statique
    template = random.choice(GOAL_TEMPLATES)
    niche = random.choice(NICHES)
    audience = random.choice(AUDIENCES)
    return template.format(niche=niche, audience=audience)
