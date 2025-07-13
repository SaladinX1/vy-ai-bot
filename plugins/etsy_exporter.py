def export_listing(args, context):
    data = args["data"]
    
    # Simule l'export (fichier JSON pour Etsy manual upload ou future API)
    import json, os
    os.makedirs("exports", exist_ok=True)
    with open("exports/listing.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("📦 Produit exporté dans 'exports/listing.json'")
    return "Listing prêt pour Etsy"
