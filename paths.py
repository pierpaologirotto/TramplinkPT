# config/paths.py
import os


#PERCORSI SU DATABASE MILANO
#SOURCE_BASE = r"C:\Users\piegir\OneDrive - Stadlerrail AG\Quiroz Carlos STAV's files - ATM TL MILANO"
#DEST_BASE_1 = r"C:\Users\piegir\Desktop\Treni\AttAp\TramLink\Analisi-risultati-PYTHON\costanti di progetto"
#DEST_BASE_2 = r"C:\Users\piegir\Desktop\Treni\AttAp\TramLink\Analisi-risultati-PYTHON\Profilo"

#PERCORSI PROVA PER TEST PROGRAMMA
SOURCE_BASE = r"C:\Users\piegir\Desktop\Ruote Milano"
DEST_BASE_1 = r"C:\Users\piegir\Desktop\Ruote Milano PY\costanti di progetto"
DEST_BASE_2 = r"C:\Users\piegir\Desktop\Ruote Milano PY\Profilo"

#elimina
#SOURCE_BASE = r"C:\Users\piegir\Desktop\Ruote Milano"
#DEST_BASE_1 = r"C:\Users\piegir\Desktop\Ruote Milano Clous PY\costanti di progetto"
#EST_BASE_2 = r"C:\Users\piegir\Desktop\Ruote Milano Clous PY\Profilo"


def ensure_paths():
    """Crea le cartelle di destinazione principali se non esistono."""
    os.makedirs(DEST_BASE_1, exist_ok=True)
    os.makedirs(DEST_BASE_2, exist_ok=True)
