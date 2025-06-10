# report_generator.py
from fpdf import FPDF
import os
from datetime import datetime

def generate_report(data, filename="rapport_scan.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Rapport de Scan - CyberToolbox", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Généré le {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(10)

    for item in data:
        pdf.multi_cell(0, 10, f"IP : {item['ip']}\nPorts : {item['ports']}\nStatut : {item['statut']}\nDate : {item['date']}")
        pdf.ln(5)

    os.makedirs("static", exist_ok=True)
    path = os.path.join("static", filename)
    pdf.output(path)
    return path
