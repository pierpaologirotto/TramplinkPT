# 🚆 Tramlink

Sistema di **organizzazione e aggregazione automatica dei dati di misura ruote**.

Il progetto nasce per semplificare la gestione delle cartelle UT (es. UT 7702, UT 7703, …) e automatizzare la raccolta dei dati Excel provenienti dalle varie prove.

---

## 📂 Struttura del progetto

Tramlink/

├── main.py → script principale (menu e logica generale)

├── config/ 

     ── paths.py → definizione dei percorsi base (cartelle sorgente e destinazione)

├── modules/ 
    
    ├── organizer.py → crea la struttura delle cartelle UT e Raccolta
    ├── aggregator.py → aggrega i file Excel e genera i file AR.xlsx
    ├── archiver.py → archivia i file AR.xlsx 
    └── plotter.py → (in sviluppo) generazione di grafici e statistiche

└── README.md → documentazione del progetto


---

## ⚙️ Funzionalità principali

### 1️⃣ **Organizzazione**
Crea automaticamente la struttura delle cartelle UT e le sottocartelle:
costanti di progetto/

    └── UT 7702/
    ├── Raccolta/
    └── Archivio/

### 2️⃣ **Aggregazione**
Legge tutti i file Excel presenti nella cartella `Raccolta` di ogni UT e genera automaticamente il file:

costanti di progetto/UT 77XX/AR_UT77XX.xlsx

Ogni file contiene **6 fogli di lavoro**, ciascuno con intestazione standard e righe compilate con i dati provenienti dai file sorgenti.

### 3️⃣ **Gestione automatica file duplicati**
- Se un file con lo stesso nome è già presente, viene **mantenuto il più vecchio**.  
- Il file più recente viene ignorato per evitare sovrascritture indesiderate.

---

## 🧩 Requisiti

- **Python 3.10+**
- Librerie richieste:

#```bash

#pip install openpyxl xlrd

## ▶️ Come si usa

1) Apri un terminale o prompt dei comandi nella cartella del progetto (Tramlink/)

2) Esegui il programma:

       python main.py
3) Segui le istruzioni del menu:
Seleziona un’operazione:

       1 → Crea struttura UT
       2 → Aggrega file Excel
       3 → (In futuro) Genera grafici
4) I risultati vengono salvati automaticamente nelle relative; i file sovrascritti vengono salvati nella cartelle Archivio.

## 🧠 Note utili

- I file sorgente devono essere in formato .xlsx o .xls.
- I .xls vengono automaticamente convertiti in .xlsx.

- Se nella cartella Raccolta non ci sono file, il programma mostra il messaggio:

        [INFO] Raccolta vuota

- Le celle vuote vengono compilate con "nessun dato" per evitare errori di importazione.

## 🧩 In sviluppo

- Modulo plotter.py: grafici e analisi statistiche automatiche.

- Integrazione con dashboard Python o Excel.

- Esportazione automatica in PDF e report per UT.

## 👨‍💻 Autore

Pierpaolo Girotto
Ingegnere / Data Engineer
📍 Venezia, Italia
📅 Ultimo aggiornamento: ottobre 2025