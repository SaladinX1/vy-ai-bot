# # FICHIER: core/validators.py

# def validate_plan_schema(plan: list) -> bool:
#     required_keys = {"id", "title", "description", "depends_on"}
#     if not isinstance(plan, list):
#         return False
#     for step in plan:
#         if not isinstance(step, dict):
#             return False
#         if not required_keys.issubset(step):
#             return False
#     return True


# core/validators.py
def validate_plan_schema(plan: list) -> bool:
    if not isinstance(plan, list):
        return False
    for task in plan:
        if not all(k in task for k in ("id", "title", "description", "depends_on")):
            return False
    return True