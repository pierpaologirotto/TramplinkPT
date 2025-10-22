import os
from config import paths
from modules import organizer, aggregator, archiver


def main():
    """
    Main entry point del progetto Tramlink.
    Puoi scegliere quale parte del processo eseguire:
    1) organizzazione file
    2) aggregazione dati
    3) tutto
    """

    print("=== TRAMLINK AUTOMATION ===")
    print("1 - Organizzare i file (copiati da 'Ruote Milano')")
    print("2 - Aggregare i file Excel (creare AR-UT)")
    print("3 - Tutto (1 + 2)")
    scelta = input("Seleziona un'operazione (1, 2 o 3): ").strip()

    if scelta == "1":
        print("\n🔹 Avvio organizzazione file...")
        organizer.organize_excels()
        print("✅ Organizzazione completata.")

    elif scelta == "2":
        print("\n🔹 Avvio aggregazione file...")
        base_path = paths.DEST_BASE_1

        # ancora non implementata
        #archiver.archive_all_ut(paths.DEST_BASE_1)

        for ut_folder in os.listdir(base_path):
            full_path = os.path.join(base_path, ut_folder)
            if os.path.isdir(full_path) and ut_folder.startswith("UT "):
                # archivia tutti i file AR presenti nelle UT
                print("✅ Aggregazione completata.")

    elif scelta == "3":
        print("\n🔹 Avvio organizzazione + aggregazione...")
        organizer.organize_excels()

        # archivia tutti i file AR presenti nelle UT
        #archiver.archive_all_ut(paths.DEST_BASE_1)

        base_path = paths.DEST_BASE_1
        for ut_folder in os.listdir(base_path):
            full_path = os.path.join(base_path, ut_folder)
            if os.path.isdir(full_path) and ut_folder.startswith("UT "):

                aggregator.collect_data_for_ut(full_path)
        print("✅ Tutto completato.")

    else:
        print("❌ Scelta non valida. Riprova.")


if __name__ == "__main__":
    main()
