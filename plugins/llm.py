def generate_product_outline(args, context):
    topic = args["topic"]
    return f"""Plan pour un ebook sur '{topic}':
1. Introduction
2. Pourquoi la {topic} est importante
3. Techniques clés
4. Études de cas
5. Ressources et outils
6. Conclusion"""

def write_infoproduct(args, context):
    outline = args["outline"]
    return f"<html><body><h1>Ebook: {outline.splitlines()[0]}</h1><p>{outline}</p></body></html>"

def generate_keywords(args, context):
    niche = args["niche"]
    return ["productivité personnelle", "outils de productivité", "gagner du temps", "habitudes efficaces"]

def generate_product_idea(args, context):
    niche = args["niche"]
    return {
        "title": "Poster minimaliste abstrait",
        "category": "Art & Décoration",
        "description": f"Un poster dans le style minimaliste inspiré par {niche}",
        "price": 19.99
    }

def generate_product_listing(args, context):
    product = args["input"]
    return {
        "title": f"{product['title']} - Idéal pour votre maison",
        "description": f"{product['description']}. Disponible en plusieurs formats. Impression de qualité.",
        "tags": ["minimaliste", "poster", "déco murale", "scandinave", "art abstrait"],
        "price": product["price"]
    }

def generate_topic(args, context):
    niche = args["niche"]
    return f"10 techniques de {niche} pour doubler votre efficacité en 30 jours"

def generate_outline(args, context):
    topic = args["topic"]
    return [
        "Introduction",
        "Pourquoi la productivité est clé",
        "Technique 1: Gestion du temps",
        "Technique 2: Pomodoro",
        "Technique 3: Eliminer les distractions",
        "Conclusion"
    ]

def write_full_content(args, context):
    outline = args["outline"]
    return "\n\n".join([f"## {section}\nContenu généré par IA..." for section in outline])

def generate_email_topics(args, context):
    niche = args["niche"]
    return [
        f"5 erreurs classiques en {niche}",
        f"Comment doubler votre taux d'ouverture en {niche}",
        f"Stratégie de conversion efficace en {niche}"
    ]

def write_emails(args, context):
    topics = args["topics"]
    emails = []
    for topic in topics:
        content = f"Objet : {topic}\n\nBonjour,\n\nVoici nos conseils sur : {topic}.\n\nÀ très bientôt."
        emails.append({"subject": topic, "body": content})
    return emails


def generate_video_ideas(args, context):
    niche = args["niche"]
    return [
        f"Comment économiser 100€ par mois en {niche}",
        f"Les 3 pires erreurs en {niche}",
        f"{niche.capitalize()} : Mythe ou réalité ?"
    ]

def generate_video_scripts(args, context):
    platform = args.get("platform", "youtube")
    ideas = args["ideas"]
    scripts = []
    for idea in ideas:
        if platform == "tiktok":
            intro = "🎬 En 30 secondes :"
            outro = "🔥 Like & follow pour plus !"
        else:
            intro = "🎬 Bienvenue dans cette vidéo sur :"
            outro = "👍 Abonnez-vous pour plus de conseils."
        scripts.append({
            "title": idea,
            "script": f"{intro} {idea}\n\n[Contenu développé ici]\n\n{outro}"
        })
    return scripts


def generate_outline(args, context):
    topic = args["topic"]
    return [
        f"Introduction au {topic}",
        f"Les fondamentaux du {topic}",
        f"Techniques avancées pour {topic}",
        f"Études de cas en {topic}",
        f"Conclusion et prochaines étapes"
    ]

def write_sections(args, context):
    outline = args["outline"]
    content = []
    for title in outline:
        body = f"{title}\n\nVoici le contenu détaillé de la section sur {title.lower()}.\n\n[Texte généré par IA ici...]"
        content.append({"title": title, "body": body})
    return content


def analyze_offer(args, context):
    product_name = args["product_name"]
    # Placeholder: récupère l'existant depuis une base réelle ou simule
    existing_data = {
        "title": "Coussin relaxant pour bureau",
        "description": "Un coussin ergonomique pour soulager votre dos au travail.",
        "image": "img/coussin_original.jpg"
    }
    return existing_data

def generate_improved_offer(args, context):
    old = args["input"]
    return {
        "title": old["title"] + " - Nouvelle version Premium",
        "description": old["description"] + "\n\nMaintenant avec mousse mémoire de forme et tissu respirant.",
        "image": old["image"].replace("original", "premium")
    }


def generate_blog_post(args, context):
    topic = args["topic"]
    # Appel à l'API GPT pour générer un article SEO-friendly
    return f"Article SEO complet sur le thème {topic}..."

def generate_newsletter(args, context):
    topic = args["topic"]
    # Génère contenu newsletter HTML
    return f"<h1>Newsletter sur {topic}</h1><p>Voici nos astuces ...</p>"

def generate_social_posts(args, context):
    topic = args["topic"]
    # Génère des posts adaptés par plateforme
    return {
        "instagram": {
            "caption": f"Boostez votre productivité avec ces astuces #productivité",
            "image": "images/productivity_ig.jpg"
        },
        "tiktok": {
            "caption": f"Top 5 conseils pour être plus productif ! #productivité",
            "video": "videos/productivity_tiktok.mp4"
        },
        "linkedin": {
            "text": f"Découvrez comment augmenter votre productivité grâce à ces conseils pratiques."
        }
    }
