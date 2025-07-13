import os

def build_site(args, context):
    content = args["content"]
    folder = "dist"
    os.makedirs(folder, exist_ok=True)
    
    for i, article in enumerate(content):
        with open(os.path.join(folder, f"article_{i+1}.html"), "w", encoding="utf-8") as f:
            f.write(f"<html><body><h1>{article['title']}</h1>{article['content']}</body></html>")
    
    return f"{len(content)} articles créés dans {folder}"

def deploy(args, context):
    folder = args["folder"]
    print(f"🚀 Site déployé à partir de : {folder} (mock déploiement)")
    return "Site en ligne !"

def build_landing_page(args, context):
    offer = args["offer"]
    html = f"""
    <html>
    <head><title>Formation IA</title></head>
    <body>
        <h1>{offer[:60]}...</h1>
        <p>{offer}</p>
        <a href="/download/infoproduit.pdf">Télécharger</a>
    </body>
    </html>
    """
    with open("exports/landing.html", "w", encoding="utf-8") as f:
        f.write(html)
    return "Landing page générée dans exports/landing.html"



def publish_article(args, context):
    content = args["content"]
    # Simulation d’enregistrement dans un CMS ou fichier local
    with open("site/content/blog_post.html", "w", encoding="utf-8") as f:
        f.write(content)
    return "Article publié sur le site."
