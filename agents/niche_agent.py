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
        # Exemple simple de retour structuré (à améliorer)
        return {"summary": response}
