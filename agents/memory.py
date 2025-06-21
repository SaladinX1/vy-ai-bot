class Memory:
    def __init__(self):
        self.history = []

    def update(self, plan, user_input):
        """Ajoute la commande et le plan d’action à l’historique."""
        self.history.append({
            "input": user_input,
            "plan": plan
        })

    def get_context(self, limit=5):
        """Retourne les dernières interactions pour enrichir le prompt."""
        context_items = self.history[-limit:]
        context_str = ""
        for item in context_items:
            context_str += f"Utilisateur: {item['input']}\nPlan: {item['plan']}\n"
        return context_str.strip()
