# # 📁 Dossier : core/improver.py
# class Improver:
#     def analyze_and_improve(self, analytics):
#         # analytics = { 'views': 100, 'clicks': 5, 'sales': 0 }
#         if analytics['sales'] == 0:
#             return "Résultats faibles. Tenter un autre angle marketing ou changer le produit."
#         elif analytics['sales'] < 5:
#             return "Produit prometteur. Améliorer la landing page ou tester une promo."
#         else:
#             return "Succès détecté. Dupliquer ou faire un upsell."


# core/improver.py

from core.memory_store import MemoryStore

class Improver:
    def __init__(self):
        self.memory = MemoryStore()

    def analyze_and_improve(self):
        print("Analyse des performances...")
        result = "Produit X a eu peu d'interactions"
        self.memory.add(result)
