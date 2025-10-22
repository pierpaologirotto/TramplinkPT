# modules/archiver.py
import os
import shutil
from datetime import datetime


def archive_ar_file(ar_path, archive_base=None):
    """
    Archivia il file AR-UT esistente.

    Parametri:
    - ar_path: percorso completo del file AR-UT.xlsx da archiviare
    - archive_base: percorso base della cartella Archivio (default: stessa cartella del progetto)

    Il file viene copiato in:
    Archivio/UT XXXX/AR-UT XXXX_YYYY-MM.xlsx
    """
    if not os.path.exists(ar_path):
        # nessun file da archiviare
        return None

    ut_folder = os.path.dirname(ar_path)
    ut_name = os.path.basename(ut_folder)  # es. UT 7702

    # cartella Archivio base
    if archive_base is None:
        archive_base = os.path.join(os.path.dirname(ut_folder), "Archivio")
    archive_folder = os.path.join(archive_base, ut_name)
    os.makedirs(archive_folder, exist_ok=True)

    # suffisso anno-mese
    date_suffix = datetime.now().strftime("%Y-%m")
    filename = f"{os.path.splitext(os.path.basename(ar_path))[0]}_{date_suffix}.xlsx"
    archive_path = os.path.join(archive_folder, filename)

    # copia del file
    shutil.copy2(ar_path, archive_path)
    print(f"[ARCHIVIATO] {os.path.basename(ar_path)} → {archive_path}")
    return archive_path


def archive_all_ut(base_ut_folder, archive_base=None):
    """
    Archivia tutti i file AR-UT presenti nelle sottocartelle UT.
    """
    if not os.path.isdir(base_ut_folder):
        print(f"[ERROR] Cartella UT non trovata: {base_ut_folder}")
        return

    ut_folders = [os.path.join(base_ut_folder, d) for d in os.listdir(base_ut_folder)
                  if os.path.isdir(os.path.join(base_ut_folder, d)) and d.startswith("UT ")]

    if not ut_folders:
        print("[INFO] Nessuna cartella UT trovata.")
        return

    for ut in ut_folders:
        ar_files = [f for f in os.listdir(ut)
                    if f.lower().startswith("ar-") and f.lower().endswith(".xlsx")]
        for ar_file in ar_files:
            ar_path = os.path.join(ut, ar_file)
            archive_ar_file(ar_path, archive_base)
    print("✅ Archiviazione completata.")
