# from llm.llm_interface import get_command_response

# class CopywritingAgent:
#     def __init__(self):
#         pass

#     def generate_sales_page(self, product_name: str, features: str) -> str:
#         prompt = f"""
#         Écris une page de vente persuasive pour ce produit : {product_name}
#         Détaille ses fonctionnalités : {features}
#         """
#         sales_page = get_command_response(prompt)
#         return sales_page



# FICHIER: agents/copywriting_agent.py

class CopywritingAgent:
    def generate_sales_page(self, product_name: str, features: str):
        return f"Page de vente pour {product_name} avec caractéristiques : {features}"

    def run(self, input: dict):
        return self.generate_sales_page(input.get("product_name", "Produit X"), input.get("features", "Fonctionnalités"))