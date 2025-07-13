# evaluator/scoring.py

def score_workflow_result(result: dict, goal: str) -> float:
    """
    Évalue un résultat de workflow avec un score de performance (0-10).
    """
    score = 0
    if not result:
        return 0.0

    # Exemple de critères simples (à adapter par business)
    if result.get("success"):
        score += 5
    if "output" in result:
        score += 2
        if "visibilité" in result["output"].lower():
            score += 1
        if "trafic" in result["output"].lower():
            score += 2

    return min(score, 10.0)
