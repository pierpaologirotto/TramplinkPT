# modules/mail/mail.py
import win32com.client as win32
import pythoncom
from datetime import datetime

def invia_alert_mail(ruota_id, km_residui, giorni_residui, alert_km_threshold, alert_days_threshold, destinatari):
    """
    Funzione già esistente: invia mail singola per una ruota.
    """
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = "; ".join(destinatari)
    mail.Subject = f"⚠️ Alert Ruota {ruota_id} - Soglia superata"
    mail.Body = (
        f"Buongiorno,\n\n"
        f"È stato rilevato un superamento delle soglie di progetto per le ruote del Tram {ruota_id}.\n\n"
        f"Dati stimati:\n"
        f"- Chilometri residui: {km_residui:.0f} km (soglia {alert_km_threshold} km)\n"
        f"- Giorni residui: {giorni_residui:.0f} giorni (soglia {alert_days_threshold} giorni)\n\n"
        f"Data e ora rilevamento: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        f"Saluti,\n"
        f"Sistema automatico Tramlink"
    )
    mail.Send()
    print(f"[MAIL] Inviata mail di alert per ruota {ruota_id}")


def invia_alert_riassuntiva(file_name, sheet_alerts, alert_km_threshold, alert_days_threshold, destinatari):
    """
    Invia UNA mail riassuntiva per file.
    sheet_alerts: list of tuples -> (sheet_index (int), min_km (float), min_date (pd.Timestamp))
    """
    if not sheet_alerts:
        print(f"[MAIL] Nessun alert per {file_name}, nessuna mail inviata.")
        return

    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)

    # Oggetto: estrai "UT 77XX" se il file si chiama "AR-UT 7702.xlsx"
    ut_name = file_name.replace(".xlsx", "").replace("AR-", "").strip()
    mail.Subject = f"⚠️ Alert usura ruote - Tramlink {ut_name}"

    body_lines = [
        "Buongiorno,",
        "",
        f"È stato rilevato un superamento delle soglie di progetto per le ruote del Tram {ut_name}.",
        "In particolare:\n"
    ]

    for sheet_idx, min_km, min_date in sheet_alerts:
        # format
        date_str = pd_to_str = min_date.strftime("%d/%m/%Y") if hasattr(min_date, "strftime") else str(min_date)
        body_lines.append(
            f"Asse {sheet_idx} - Soglie stimati:\n"
            f"- Chilometri residui: {min_km:,.0f} km (soglia {alert_km_threshold} km)\n"
            f"- Giorni residui: {(min_date - datetime.now()).days:.0f} giorni stimati \n"#(soglia {alert_days_threshold} giorni)\n"
        )

    body_lines.append(f"Data e ora rilevamento: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    body_lines.append("\nSaluti,\nSistema automatico Tramlink")

    mail.Body = "\n".join(body_lines)
    mail.To = "; ".join(destinatari)
    try:
        mail.Send()
        print(f"[MAIL] Inviata mail riassuntiva per {file_name} a {destinatari}")
    except Exception as e:
        print(f"[MAIL] Errore invio mail per {file_name}: {e}")
