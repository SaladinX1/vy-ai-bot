def resume_business(name, config, path):
    # Exemple : relancer une campagne marketing ou régénérer visuels
    print(f"[▶️] Reprise de génération pour {name}")
    print(f"Statut précédent : {config['status']}")
    # Ici, tu peux appeler à nouveau tes modules GPT, DALL·E, etc.
    # Et ensuite mettre à jour le config.json
    config['status'] = 'resumed'
    update_project(name, config)
