def generate_workflow_from_niche(niche):
    # Génère dynamiquement un nouveau workflow en JSON
    return {
        "name": f"{niche}_autogen",
        "steps": [
            {"plugin": "google_trends", "args": {"niche": niche}},
            {"plugin": "content_creator", "args": {"topic": niche}},
            {"plugin": "mailchimp_api", "args": {"list_id": "123", "subject": f"Actu {niche}"}},
        ]
    }
