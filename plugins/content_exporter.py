def send_email(args, context):
    to = args["to"]
    subject = args["subject"]
    attachment = args["attachment"]
    print(f"✉️ Email envoyé à {to} avec l'attachement : {attachment}")
    return f"Email envoyé à {to}"


import os

def save_to_txt(args, context):
    os.makedirs(args["folder"], exist_ok=True)
    content = args["content"]
    for i, item in enumerate(content):
        filename = os.path.join(args["folder"], f"video_{i+1}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Titre : {item['title']}\n\nScript :\n{item['script']}")
    return f"{len(content)} scripts exportés dans {args['folder']}"


from fpdf import FPDF

def export_pdf(args, context):
    content = args["content"]
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for section in content:
        pdf.set_font("Arial", 'B', 14)
        pdf.multi_cell(0, 10, section["title"])
        pdf.ln()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, section["body"])
        pdf.ln()

    filename = args["filename"]
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pdf.output(filename)
    return f"Ebook exporté : {filename}"


def update_product(args, context):
    product = args["product"]
    new_data = args["new_data"]
    path = f"products/{product.replace(' ', '_').lower()}.json"
    os.makedirs("products", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2)
    return f"✅ Produit '{product}' mis à jour dans {path}"
