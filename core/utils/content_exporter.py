import markdown
from weasyprint import HTML
import os

def markdown_to_pdf(md_text, output_path="output.pdf"):
    html_text = markdown.markdown(md_text)
    HTML(string=html_text).write_pdf(output_path)
    print(f"PDF généré: {output_path}")

if __name__ == "__main__":
    sample_md = """
# Titre
Voici un contenu **Markdown** d'exemple.

- Point 1
- Point 2
"""
    markdown_to_pdf(sample_md)
