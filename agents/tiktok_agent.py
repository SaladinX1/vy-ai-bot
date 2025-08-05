from llm.llm_interface import get_command_response

class TikTokAgent:
    def __init__(self):
        pass

    def run(self, input: dict) -> dict:
        """
        input attendu (exemple) :
        {
            "account_name": "Nom du compte TikTok",
            "video_ideas": ["Idée vidéo 1", "Idée vidéo 2"],
            "niche": "Description de la niche",
            # autres paramètres possibles
        }
        """
        account_name = input.get("account_name", "Compte TikTok Généré")
        niche = input.get("niche", "niche inconnue")
        video_ideas = input.get("video_ideas", [])

        prompt = f"""
        Tu es un expert en création et gestion de comptes TikTok dans la niche : {niche}.
        Propose une stratégie pour créer le compte '{account_name}', ainsi que des idées de vidéos courtes virales.
        Donne aussi des conseils pour la publication régulière et l’engagement.
        """

        response = get_command_response(prompt)

        return {
            "account_name": account_name,
            "strategy": response,
            "video_ideas_count": len(video_ideas),
            "video_ideas": video_ideas
        }
