from llm.llm_interface import query_mistral
import json


# def simulate_workflow(steps, goal):
#     """
#     Simule les effets probables d’un plan avant de l’exécuter réellement.
#     Renvoie : dict {"success": bool, "reason": str}
#     """
#     plan_description = "\n".join(
#         [f"{i+1}. {step['task']} via {step['tool']} (params: {step['params']})" for i, step in enumerate(steps)]
#     )

#     prompt = f"""
# Tu es un simulateur d'efficacité pour des agents autonomes.
# L'objectif est : "{goal}"

# Voici le plan proposé :
# {plan_description}

# Analyse la faisabilité et la probabilité de succès de ce plan.
# Réponds au format JSON :
# {{
#   "success": true/false,
#   "reason": "raison pour laquelle cela peut échouer ou réussir"
# }}
#     """.strip()

#     try:
#         response = query_mistral(prompt, system_prompt="Tu es un expert en simulation de workflows automatisés.")
#         result = json.loads(response)
#         return {
#             "success": bool(result.get("success", False)),
#             "reason": result.get("reason", "Aucune raison fournie")
#         }
#     except Exception as e:
#         return {
#             "success": False,
#             "reason": f"Erreur de simulation : {e}"
#         }





def simulate_workflow(steps):
    try:
        plan_description = "\n".join([f"- {step['task']} via {step['tool']}" for step in steps])
        prompt = f"""
Tu es un simulateur de workflows. Analyse ce plan pour détecter les incohérences, erreurs ou risques.
Plan :
{plan_description}

Réponds en JSON :
{{
  "feasible": true/false,
  "reason": "explication si non faisable"
}}
        """
        response = query_mistral(prompt, system_prompt="Tu es un simulateur expert de plan d'action.")
        return eval(response)  # Assure-toi que Mistral renvoie un JSON valide
    except Exception as e:
        return {"feasible": False, "reason": f"Erreur simulation : {str(e)}"}