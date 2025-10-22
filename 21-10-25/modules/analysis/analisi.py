import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# aggiunge la root del progetto al path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import variabili, paths


def predict_limit(km, values, limit_value):
    km = np.array(km).reshape(-1, 1)
    values = np.array(values)
    grado = getattr(variabili, "grado_polinomiale", 1)

    if len(km) < 2:
        return None

    poly = PolynomialFeatures(degree=grado)
    km_poly = poly.fit_transform(km)
    model = LinearRegression()
    model.fit(km_poly, values)

    km_test = np.linspace(min(km), max(km) * 3, 5000).reshape(-1, 1)
    km_test_poly = poly.transform(km_test)
    values_pred = model.predict(km_test_poly)

    if (values_pred[-1] > limit_value and values_pred[0] > limit_value) or \
       (values_pred[-1] < limit_value and values_pred[0] < limit_value):
        return None

    diff = np.abs(values_pred - limit_value)
    idx_min = np.argmin(diff)
    km_limit = km_test[idx_min][0]

    if km_limit <= max(km)[0] or km_limit > 1e6:
        return None

    return float(km_limit)


def interpolate_date(km_series, date_series, target_km):
    km_series = np.array(km_series)
    date_series = pd.to_datetime(date_series, dayfirst=True)

    if len(km_series) < 2:
        return None

    total_days = (date_series - date_series.min()).values / np.timedelta64(1, 'D')
    grado = getattr(variabili, "grado_polinomiale", 1)
    poly = PolynomialFeatures(degree=grado)
    km_poly = poly.fit_transform(km_series.reshape(-1, 1))

    model = LinearRegression().fit(km_poly, total_days)
    target_days = model.predict(poly.transform(np.array([[target_km]])))[0]

    if target_days < 0 or target_days > 50000:
        return None

    target_date = date_series.min() + pd.to_timedelta(target_days, unit="D")
    return target_date


def analyze_single_file(file_path: Path):
    """
    Analizza singolo file AR-UT xxxx.xlsx.
    - Scrive il .txt come prima.
    - Ritorna (alert_summary, out_path)
      where alert_summary è lista di tuple:
        (sheet_number, km_mancanti_min, date_min)
      include solo fogli dove almeno un parametro è sotto soglia.
    """
    print(f"\n--- Analizzando {file_path.name} ---")
    df_excel = pd.ExcelFile(file_path)
    output_lines = [f"FILE: {file_path.name}"]

    mail_alerts = []

    for idx, sheet in enumerate(df_excel.sheet_names, start=1):
        df = pd.read_excel(df_excel, sheet_name=sheet)
        df.columns = df.columns.str.strip()
        #print(f"\nFoglio: {sheet} | Colonne lette: {df.columns.tolist()} | righe totali: {len(df)}")

        col_date = "Measurement date"
        col_km = "Mileage"
        measures = {
            "Altezza": ("Height (sH)  (Left)", "Height (sH)  (Right)", variabili.lim_altezza),
            "Spessore1": ("Thickness (sD)  (Left)", "Thickness (sD) (Right)", variabili.lim_spessore1),
            "Spessore2": ("Thickness (sDF)  (Left)", "Thickness (sDF) (Right)", variabili.lim_spessore2),
            "QR": ("Parameter (sF)  (Left)", "Parameter (sF) (Right)", variabili.lim_qr)
        }

        for cols in measures.values():
            for c in cols[:2]:
                if c in df.columns:
                    df[c] = df[c].astype(str).str.replace(",", ".").astype(float)

        if col_date in df.columns:
            df[col_date] = pd.to_datetime(df[col_date], dayfirst=True, errors='coerce')

        df = df.dropna(subset=[col_km, col_date])
        df = df.sort_values(by=col_km)
        if df.empty:
            print(f"Foglio {sheet} vuoto dopo conversione dati.")
            continue

        output_lines.append(f"\nFoglio: {sheet}\n")

        km_attuali = df[col_km].max()
        sotto_soglia = []

        for name, (col_sx, col_dx, lim) in measures.items():
            for side, col in zip(("SX", "DX"), (col_sx, col_dx)):
                if col not in df.columns:
                    continue

                vals = df[col].dropna().values
                kms = df.loc[df[col].notna(), col_km].values
                dates = df.loc[df[col].notna(), col_date].values

                if len(vals) < 2:
                    output_lines.append(f"{name} {side} -> impossibile stimare (dati insufficienti)")
                    continue

                km_pred = predict_limit(kms, vals, lim)
                date_pred = interpolate_date(kms, dates, km_pred) if km_pred is not None else None
                date_str = date_pred.strftime("%d/%m/%Y") if date_pred is not None else "N/D"

                if km_pred is None or date_pred is None:
                    output_lines.append(f"{name} {side} -> impossibile stimare (dati non coerenti)")
                    continue

                # ✅ Calcolo km mancanti
                km_mancanti = km_pred - km_attuali

                output_lines.append(f"{name} {side} -> Limite previsto a {date_str} | Km mancanti: {km_mancanti:,.0f}")

                # Se km mancanti < soglia, aggiungi alert
                if km_mancanti <= variabili.alert_km_threshold:
                    sotto_soglia.append((float(km_mancanti), pd.to_datetime(date_pred)))
                    output_lines.append(f"⚠️ ALERT: {name} {side} sotto soglia ({km_mancanti:,.0f} km mancanti)")

        # se abbiamo almeno un parametro sotto soglia, segnalo mail
        if sotto_soglia:
            km_min = min(x[0] for x in sotto_soglia)
            date_min = min(x[1] for x in sotto_soglia)
            mail_alerts.append((idx, float(km_min), pd.to_datetime(date_min)))

    # scrivi .txt come prima
    out_path = file_path.with_suffix(".txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    print(f"\nOutput scritto in: {out_path}\n")

    return mail_alerts, out_path


def run_full_analysis():
    root = Path(paths.DEST_BASE_1)
    files = list(root.rglob("AR-UT 77*.xlsx"))
    if not files:
        print("❌ Nessun file AR-UT trovato.")
        return
    for f in files:
        analyze_single_file(f)


if __name__ == "__main__":
    run_full_analysis()
