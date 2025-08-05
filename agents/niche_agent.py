from llm.llm_interface import get_command_response  # Interface vers LLM

class NicheAgent:
    def __init__(self):
        pass

    def analyze_niche(self, niche_description: str) -> dict:
        prompt = f"""
        Analyse ce marché/niche : {niche_description}
        Donne une synthèse des opportunités, concurrents, tendances.
        """
        response = get_command_response(prompt)
        return {"summary": response}

    def run(self, params: dict) -> dict:
        """
        Point d'entrée standardisé pour exécuter une tâche d'analyse de niche.
        """
        niche_description = params.get("keyword") or params.get("description") or "business en ligne 2025"
        return self.analyze_niche(niche_description)

