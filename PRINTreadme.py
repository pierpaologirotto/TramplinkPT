# PRINTreadme.py
import pdfkit
import markdown
import os

# -------------------------------
# Configura percorsi
# -------------------------------
md_file = r"C:\Users\piegir\Desktop\Treni\AttAp\TramLink\TramlinkPT\Tramilink\ReadMe.md"
pdf_file = r"C:\Users\piegir\Desktop\Ruote Milano PY\README.pdf"
css_file = r"C:\Users\piegir\Desktop\Treni\AttAp\TramLink\TramlinkPT\Tramilink\grafics\style.css"
wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

# -------------------------------
# Controllo che i file esistano
# -------------------------------
for fpath, desc in [(md_file, "Markdown"), (css_file, "CSS"), (wkhtmltopdf_path, "wkhtmltopdf.exe")]:
    if not os.path.isfile(fpath):
        raise FileNotFoundError(f"{desc} non trovato: {fpath}")

# -------------------------------
# Leggi Markdown con sicurezza
# -------------------------------
with open(md_file, "r", encoding="utf-8", errors="replace") as f:
    text = f.read()
print("[INFO] File Markdown letto correttamente.")

# -------------------------------
# Converti Markdown in HTML
# -------------------------------
html = markdown.markdown(text, extensions=['fenced_code', 'tables'])

# -------------------------------
# Configura pdfkit
# -------------------------------
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

# -------------------------------
# Genera PDF
# -------------------------------
pdfkit.from_string(html, pdf_file, configuration=config, css=css_file)

print(f"✅ PDF generato correttamente in: {pdf_file}")
