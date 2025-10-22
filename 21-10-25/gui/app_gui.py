import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import subprocess
import sys
from pathlib import Path

# Aggiunge la root del progetto per i moduli interni
sys.path.append(str(Path(__file__).resolve().parents[1]))

from modules import organizer, aggregator
from modules.analysis import analisi   # ✅ percorso corretto
from config import paths, variabili
from modules.mail import mail, indirizzi
from modules.mail.mail import invia_alert_riassuntiva


class TramlinkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚆 Tramlink - Analisi automatica")
        self.root.geometry("650x400")
        self.root.resizable(False, False)

        # intestazione
        tk.Label(
            root,
            text="Tramlink - Analisi automatica dei dati UT",
            font=("Segoe UI", 14, "bold"),
            fg="#1E90FF"
        ).pack(pady=10)

        # frame pulsanti
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        # --- Pulsante 1: Analisi completa ---
        self.btn_full_analysis = tk.Button(
            btn_frame, text="📊 Analisi completa", width=25,
            command=lambda: self.run_in_thread(self.run_full_analysis)
        )
        self.btn_full_analysis.grid(row=0, column=0, padx=20, pady=5)

        # --- Pulsante 2: Invia alert ---
        self.btn_alert = tk.Button(
            btn_frame, text="✉️ Invia alert", width=25,
            command=lambda: self.run_in_thread(self.run_send_alerts)
        )
        self.btn_alert.grid(row=0, column=1, padx=20, pady=5)

        # area log
        tk.Label(root, text="Log di esecuzione:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20, pady=(10, 0))
        self.log_box = scrolledtext.ScrolledText(root, width=80, height=15, state="disabled", bg="#f4f4f4")
        self.log_box.pack(padx=20, pady=5, fill="both", expand=True)

        # inizializza percorsi
        paths.ensure_paths()

    # ================== FUNZIONI ==================
    def log(self, text):
        """Scrive un messaggio nel box log."""
        self.log_box.configure(state="normal")
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.configure(state="disabled")
        self.log_box.see(tk.END)

    def run_in_thread(self, func):
        """Esegue un'operazione in thread separato per non bloccare l'interfaccia."""
        threading.Thread(target=func, daemon=True).start()

    # --- Analisi completa ---
    def run_full_analysis(self):
        """
        Esegue l'intera catena:
        1. organizer.organize_excels()
        2. aggregator.aggregate_all_ut()
        3. avvia il plotter grafico
        4. lancia analisi.py per generare i file .txt
        """
        self.log("🔹 Avvio ANALISI COMPLETA (org. + agg. + grafico + analisi.py)...")
        try:
            # 1️⃣ Organizzazione
            organizer.organize_excels()
            self.log("✅ Organizzazione completata.")

            # 2️⃣ Aggregazione
            aggregator.aggregate_all_ut()
            self.log("✅ Aggregazione completata.")

            # 3️⃣ Avvio modulo grafico
            plotter_path = Path(__file__).resolve().parents[1] / "modules" / "grafici" / "plotter.py"
            if not plotter_path.exists():
                raise FileNotFoundError(f"plotter.py non trovato in {plotter_path}")

            self.log("📈 Avvio modulo grafico...")
            subprocess.Popen(["python", str(plotter_path)], shell=True)
            self.log("✅ Grafico generato.")

            # 4️⃣ Avvio analisi.py per generare i .txt
            analisi_path = Path(__file__).resolve().parents[1] / "modules" / "analysis" / "analisi.py"
            if not analisi_path.exists():
                raise FileNotFoundError(f"analisi.py non trovato in {analisi_path}")

            self.log("🔍 Avvio analisi (analisi.py)...")
            subprocess.run(["python", str(analisi_path)], check=True, shell=True)
            self.log("🏁 Analisi completa terminata con successo.\n")

        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'analisi completa:\n{e}")
            self.log(f"❌ Errore in analisi completa: {e}\n")

    # --- Invia alert ---
    def run_send_alerts(self):
        self.log("📬 Generazione alert ed invio tramite Outlook...")

        try:
            root = Path(paths.DEST_BASE_1)
            files = list(root.rglob("AR-UT 77*.xlsx"))
            if not files:
                self.log("❌ Nessun file AR-UT trovato per l'invio alert.")
                return

            for f in files:
                self.log(f"🔎 Analizzo (per alert) {f.name} ...")
                sheet_alerts, out_path = analisi.analyze_single_file(f)
                if sheet_alerts:
                    self.log(f"⚠️ Alert trovati in {f.name}: {len(sheet_alerts)} foglio(i).")
                    if indirizzi.email_alerts_enabled:
                        try:
                            invia_alert_riassuntiva(
                                f.name,
                                sheet_alerts,
                                variabili.alert_km_threshold,
                                variabili.alert_days_threshold,
                                indirizzi.email_recipients
                            )
                            self.log(f"📧 Mail inviata per {f.name}")
                        except Exception as e:
                            self.log(f"❌ Errore invio mail per {f.name}: {e}")
                    else:
                        self.log("⚠️ Invio email disattivato in indirizzi.py.")
                else:
                    self.log(f"✅ Nessun alert critico in {f.name}. Nessuna mail inviata.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'invio mail:\n{e}")
            self.log(f"❌ Errore invio mail: {e}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = TramlinkGUI(root)
    root.mainloop()
