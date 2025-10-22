# modules/organizer.py
import os
from config.paths import SOURCE_BASE, DEST_BASE_1, DEST_BASE_2
from modules.utils import is_excel_file, copy_if_newer

def organize_excels():
    """Copia i file Excel in DEST_BASE_1 (nella sottocartella 'Raccolta')
    e crea la struttura vuota anche in DEST_BASE_2."""
    print("🔍 Scansione delle cartelle UT in corso...\n")

    for ut_folder in os.listdir(SOURCE_BASE):
        ut_path = os.path.join(SOURCE_BASE, ut_folder)
        if not os.path.isdir(ut_path):
            continue  # ignora file non-cartella

        # Percorsi di destinazione
        dest_ut_path_1 = os.path.join(DEST_BASE_1, ut_folder)
        dest_ut_path_2 = os.path.join(DEST_BASE_2, ut_folder)
        dest_raccolta_path = os.path.join(dest_ut_path_1, "Raccolta")

        # Crea tutte le cartelle necessarie
        os.makedirs(dest_ut_path_1, exist_ok=True)
        os.makedirs(dest_ut_path_2, exist_ok=True)
        os.makedirs(dest_raccolta_path, exist_ok=True)

        print(f"📁 {ut_folder}")

        # Cerca e copia i file Excel
        for subfolder in os.listdir(ut_path):
            sub_path = os.path.join(ut_path, subfolder)
            if not os.path.isdir(sub_path):
                continue

            for file in os.listdir(sub_path):
                if is_excel_file(file):
                    src_file = os.path.join(sub_path, file)
                    dest_file = os.path.join(dest_raccolta_path, file)
                    copy_if_newer(src_file, dest_file)
