from fpdf import FPDF
import os

def html_to_pdf(args, context):
    html = args["html_content"]
    output_path = args["output_path"]
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    
    for line in html.split('\n'):
        pdf.multi_cell(0, 10, line)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    return output_path


def create_pdf(args, context):
    content = args["content"]
    filename = args.get("filename", "infoproduit.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in content.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(f"exports/{filename}")

    return f"exports/{filename}"
