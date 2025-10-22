# modules/utils.py
import os
import shutil

def is_excel_file(filename: str) -> bool:
    """Verifica se un file è un Excel valido (.xlsx o .xls)."""
    return filename.lower().endswith((".xlsx", ".xls"))

def copy_if_newer(src_file: str, dest_file: str):
    """Copia un file se nella destinazione non esiste o se il file sorgente è più vecchio."""
    if not os.path.exists(dest_file):
        shutil.copy2(src_file, dest_file)
        print(f"[COPIATO] {os.path.basename(src_file)}")
    else:
        # Confronta date di modifica
        src_time = os.path.getmtime(src_file)
        dest_time = os.path.getmtime(dest_file)
        if src_time < dest_time:
            print(f"[MANTENUTO] File più vecchio già presente: {os.path.basename(dest_file)}")
        else:
            print(f"[SALTATO] File più recente già presente: {os.path.basename(dest_file)}")
