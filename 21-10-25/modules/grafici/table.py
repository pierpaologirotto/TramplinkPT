import matplotlib.pyplot as plt
import openpyxl
from config import variabili

def create_summary_table(ax, excel_path):
    """Crea una tabella 4x3 con valori ultimi non vuoti di colonne B, J, L, O,
    tutti formattati con massimo 2 cifre decimali"""
    ax.axis('off')

    def format_value(v):
        """Prova a formattare un numero a 2 decimali, altrimenti ritorna come stringa"""
        try:
            return f"{float(str(v).replace(',', '.')):.2f}"
        except:
            return str(v)

    def last_nonempty_col(path, col_letter):
        """Ritorna l'ultimo valore non vuoto di una colonna"""
        wb = openpyxl.load_workbook(path, data_only=True)
        ws = wb.active
        for r in range(ws.max_row, 1, -1):
            val = ws[f"{col_letter}{r}"].value
            if val not in (None, ""):
                return format_value(val)
        return "—"

    # ottieni valori formattati
    val_b = last_nonempty_col(excel_path, "B")  # intestazione
    val_j = last_nonempty_col(excel_path, "J")  # Altezza
    val_l = last_nonempty_col(excel_path, "L")  # Spessore
    val_o = last_nonempty_col(excel_path, "O")  # qr

    # costruisci tabella
    cell_text = [
        ["\\", "Progetto", val_b],
        ["Altezza", variabili.val_altezza, val_j],
        ["Spessore", variabili.val_spessore1, val_l],
        ["qr", variabili.val_qr, val_o],
    ]

    table = ax.table(cellText=cell_text,
                     colLabels=["", "", ""],  # intestazioni già nella prima riga
                     loc='center',
                     cellLoc='center')
    table.scale(1.2, 2.0)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
