def generate_articles(args, context):
    keywords = args["keywords"]
    articles = []
    for kw in keywords:
        articles.append({
            "title": f"Comment améliorer votre {kw} ?",
            "content": f"<h1>{kw.title()}</h1><p>Voici des astuces pour améliorer votre {kw}...</p>"
        })
    return articles
