class LessonAgent:
    def __init__(self):
        pass

    def run(self, input_data):
        goal = input_data.get("goal", "inconnu")
        result = input_data.get("result", "")
        score = input_data.get("score", 0.0)

        lesson = f"🎓 Leçon apprise du projet '{goal}': Résultat = {result}, Score = {score}"

        # Simule une persistance mémoire ou traitement IA si besoin
        return {
            "lesson": lesson,
            "success": True
        }
