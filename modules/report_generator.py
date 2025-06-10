from fpdf import FPDF
from datetime import datetime
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 10, 'CyberToolbox - Rapport d\'Audit', ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def add_section_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, title, ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def add_scan_table(self, scan_history):
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(220, 220, 220)
        self.cell(40, 8, 'IP', border=1, fill=True)
        self.cell(40, 8, 'Ports ouverts', border=1, fill=True)
        self.cell(40, 8, 'Statut', border=1, fill=True)
        self.cell(40, 8, 'Date', border=1, ln=True, fill=True)
        self.set_font('Helvetica', '', 10)

        for scan in scan_history:
            self.cell(40, 8, scan['ip'], border=1)
            self.cell(40, 8, scan['ports'], border=1)
            self.cell(40, 8, scan['statut'], border=1)
            self.cell(40, 8, scan['date'], border=1, ln=True)

        self.ln(10)

    def add_summary(self, scan_history):
        stats = {'Sain': 0, 'Vulnérable': 0}
        for scan in scan_history:
            stats[scan['statut']] += 1

        self.set_font('Helvetica', '', 11)
        self.cell(0, 10, f"Nombre de scans : {len(scan_history)}", ln=True)
        self.cell(0, 10, f"Sains : {stats['Sain']}", ln=True)
        self.cell(0, 10, f"Vulnérables : {stats['Vulnérable']}", ln=True)
        self.ln(5)


def generate_report(scan_history):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_section_title('Résumé des Scans')
    pdf.add_summary(scan_history)

    pdf.add_section_title('Détails des Scans')
    pdf.add_scan_table(scan_history)

    folder = "reports"
    os.makedirs(folder, exist_ok=True)
    filename = f"rapport_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(folder, filename)

    pdf.output(filepath, 'F')
    return filepath
