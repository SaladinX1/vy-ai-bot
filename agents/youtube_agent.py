from llm.llm_interface import get_command_response

class YoutubeAgent:
    def __init__(self):
        pass

    def run(self, input: dict) -> dict:
        """
        input attendu (exemple) :
        {
            "channel_name": "Nom de la chaîne",
            "video_titles": ["Titre vidéo 1", "Titre vidéo 2"],
            "video_descriptions": ["Description 1", "Description 2"],
            "niche": "Description de la niche",
            # autres paramètres possibles
        }
        """
        channel_name = input.get("channel_name", "Chaîne YouTube Générée")
        niche = input.get("niche", "niche inconnue")
        video_titles = input.get("video_titles", [])
        video_descriptions = input.get("video_descriptions", [])

        # Simulation d’une interaction avec le LLM pour créer la chaîne et préparer les vidéos
        prompt = f"""
        Tu es un expert en création et gestion de chaînes YouTube dans la niche : {niche}.
        Propose une stratégie pour créer la chaîne '{channel_name}', ainsi que des idées de vidéos avec titres et descriptions.
        Liste les étapes pour publier les vidéos régulièrement.
        """

        response = get_command_response(prompt)

        # Retour structuré simple
        return {
            "channel_name": channel_name,
            "strategy": response,
            "videos_prepared": len(video_titles),
            "video_titles": video_titles,
            "video_descriptions": video_descriptions
        }
