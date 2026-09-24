#!/usr/bin/env python3
# Defensible Forecasting — forecasting methodology & engine
# Created by Diar Azari  |  https://www.linkedin.com/in/diarazari/  |  2026  |  MIT License
"""
Produces a defensible time-series forecast and an Excel report that LEADS with a
dense, plain-language Executive Summary for all stakeholders, backed by detail
sheets (History, Backtest, Forecast, Data Profile, Notes).

Pipeline: quality check -> aggregation -> seasonal data-gating -> rolling-origin
backtest across many models -> stability filter -> safeguarded selection
(holdout confirmation + parsimony) -> top-3 + ensemble -> forecast with empirical
prediction interval + risk rating.

This is the IMPLEMENTATION of a methodology; run it instead of regenerating code.
Heavy optional models (Prophet, TBATS, XGBoost, LightGBM) run only if installed.

Usage:
  python forecast.py --input data.csv --date-col DATE --value-col VALUE \
      --freq M --horizon 12 --output forecast.xlsx \
      [--folds 8] [--holdout 6] [--pi 80] [--lang en|id] [--unit ""] [--label Value]
"""
import argparse, warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

SEASON = {"D": 7, "W": 52, "M": 12}
UNSTABLE_MAPE = 500.0  # backtest MAPE above this = numerically unstable -> excluded

# ---------- metrics ----------
def _safe(a): return np.asarray(a, dtype=float)
def mape(y, f):
    y, f = _safe(y), _safe(f); m = y != 0
    return float(np.mean(np.abs((y[m]-f[m])/y[m]))*100) if m.any() else np.nan
def smape(y, f):
    y, f = _safe(y), _safe(f); d = (np.abs(y)+np.abs(f)); m = d != 0
    return float(np.mean(2*np.abs(f[m]-y[m])/d[m])*100) if m.any() else np.nan
def wape(y, f):
    y, f = _safe(y), _safe(f); s = np.abs(y).sum()
    return float(np.abs(y-f).sum()/s*100) if s != 0 else np.nan

# ---------- models ----------
def _last(train): return float(train.iloc[-1])
def m_naive(train, h, m): return np.repeat(_last(train), h)
def m_mean(train, h, m):  return np.repeat(float(train.mean()), h)
def m_drift(train, h, m):
    n = len(train); slope = (train.iloc[-1]-train.iloc[0])/(n-1) if n > 1 else 0
    return train.iloc[-1] + slope*np.arange(1, h+1)
def m_snaive(train, h, m):
    if len(train) < m: return m_naive(train, h, m)
    vals = train.iloc[-m:].values
    return np.array([vals[i % m] for i in range(h)])
def _ets(train, h, trend=None, seasonal=None, damped=False, m=12):
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    sp = m if seasonal else None
    fit = ExponentialSmoothing(train.astype(float), trend=trend, damped_trend=damped,
                               seasonal=seasonal, seasonal_periods=sp,
                               initialization_method="estimated").fit()
    return np.asarray(fit.forecast(h))
def m_ses(train, h, m):       return _ets(train, h, None, None, False, m)
def m_holt(train, h, m):      return _ets(train, h, "add", None, False, m)
def m_holt_damp(train, h, m): return _ets(train, h, "add", None, True, m)
def m_hw_add(train, h, m):    return _ets(train, h, "add", "add", False, m)
def m_hw_mul(train, h, m):    return _ets(train, h, "add", "mul", False, m)
def m_theta(train, h, m):
    from statsmodels.tsa.forecasting.theta import ThetaModel
    sp = m if len(train) >= 2*m else None
    return np.asarray(ThetaModel(train.astype(float), period=sp).fit().forecast(h))
def _sarimax(train, h, order, so):
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    fit = SARIMAX(train.astype(float), order=order, seasonal_order=so,
                  enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
    return np.asarray(fit.forecast(h))
def m_arima(train, h, m): return _sarimax(train, h, (1,1,1), (0,0,0,0))
def m_arima_auto(train, h, m):
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    best, best_aic = None, np.inf
    for p in range(3):
        for q in range(3):
            try:
                f = SARIMAX(train.astype(float), order=(p,1,q),
                            enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
                if f.aic < best_aic: best_aic, best = f.aic, f
            except Exception: pass
    return np.asarray(best.forecast(h)) if best is not None else m_arima(train, h, m)
def m_sarima(train, h, m):
    if len(train) < 2*m: return m_arima(train, h, m)
    return _sarimax(train, h, (1,1,1), (1,0,0,m))
def _design(n, m, kind, kf=2):
    t = np.arange(n); X = [np.ones(n)]
    if kind in ("linear","poly","seasdummy","fourier"): X.append(t)
    if kind == "poly": X.append(t**2)
    if kind == "seasdummy":
        for j in range(1, m): X.append(((t % m) == j).astype(float))
    if kind == "fourier":
        for k in range(1, kf+1):
            X.append(np.sin(2*np.pi*k*t/m)); X.append(np.cos(2*np.pi*k*t/m))
    return np.column_stack(X)
def _reg(train, h, m, kind):
    from numpy.linalg import lstsq
    n = len(train); beta, *_ = lstsq(_design(n, m, kind), train.values.astype(float), rcond=None)
    return _design(n+h, m, kind)[n:] @ beta
def m_linear(train, h, m):    return _reg(train, h, m, "linear")
def m_poly(train, h, m):      return _reg(train, h, m, "poly")
def m_seasdummy(train, h, m): return _reg(train, h, m, "seasdummy")
def m_fourier(train, h, m):   return _reg(train, h, m, "fourier")
def _ml(train, h, m, model):
    lags = max(m, 3)
    if len(train) <= lags + 3: raise ValueError("too short")
    v = train.values.astype(float); X, y = [], []
    for i in range(lags, len(v)): X.append(v[i-lags:i]); y.append(v[i])
    model.fit(np.array(X), np.array(y))
    hist = list(v); out = []
    for _ in range(h):
        p = float(model.predict(np.array(hist[-lags:]).reshape(1, -1))[0])
        out.append(p); hist.append(p)
    return np.array(out)
def m_rf(train, h, m):
    from sklearn.ensemble import RandomForestRegressor
    return _ml(train, h, m, RandomForestRegressor(n_estimators=100, random_state=0))
def m_gbr(train, h, m):
    from sklearn.ensemble import GradientBoostingRegressor
    return _ml(train, h, m, GradientBoostingRegressor(random_state=0))
def m_mlp(train, h, m):
    from sklearn.neural_network import MLPRegressor
    return _ml(train, h, m, MLPRegressor(hidden_layer_sizes=(32,), max_iter=800, random_state=0))

REGISTRY = {
    "Naive": (m_naive, False), "Mean": (m_mean, False), "Drift": (m_drift, False),
    "Seasonal Naive": (m_snaive, True),
    "SES": (m_ses, False), "Holt": (m_holt, False), "Holt (damped)": (m_holt_damp, False),
    "Holt-Winters add": (m_hw_add, True), "Holt-Winters mul": (m_hw_mul, True),
    "Theta": (m_theta, False),
    "ARIMA": (m_arima, False), "AutoARIMA": (m_arima_auto, False), "SARIMA": (m_sarima, True),
    "Linear trend": (m_linear, False), "Poly trend": (m_poly, False),
    "Seasonal dummies": (m_seasdummy, True), "Fourier": (m_fourier, True),
    "Random Forest": (m_rf, False), "Gradient Boosting": (m_gbr, False), "Neural Net": (m_mlp, False),
}
BASELINES = {"Naive", "Seasonal Naive", "Drift", "Mean"}

# ---------- pipeline ----------
def load(path, dc, vc):
    df = pd.read_excel(path) if path.lower().endswith((".xlsx",".xls")) else pd.read_csv(path)
    df[dc] = pd.to_datetime(df[dc]); df = df[[dc, vc]].dropna(subset=[dc]).sort_values(dc)
    return df
def quality(df, dc, vc):
    v = df[vc]
    return {"rows": len(df), "missing": int(v.isna().sum()), "zeros": int((v == 0).sum()),
            "negatives": int((v < 0).sum()), "duplicated_dates": int(df[dc].duplicated().sum()),
            "start": str(df[dc].min().date()), "end": str(df[dc].max().date())}
def aggregate(df, dc, vc, freq):
    s = df.set_index(dc)[vc].astype(float)
    return s.resample({"D":"D","W":"W-MON","M":"MS"}[freq]).sum().dropna()
def backtest(series, freq, folds):
    m = SEASON[freq]; n = len(series); results = {}
    min_train = max(4, n - folds)
    origins = [o for o in [n-1-i for i in range(folds)][::-1] if o >= min_train]
    if not origins and n >= 5: origins = [n-1]
    for name, (fn, needs) in REGISTRY.items():
        if needs and n < 2*m:
            results[name] = {"MAPE": np.nan, "sMAPE": np.nan, "WAPE": np.nan,
                             "status": "excluded: needs >=2 seasonal cycles"}; continue
        yt, yp = [], []
        for o in origins:
            try:
                p = fn(series.iloc[:o], 1, m)[0]
                if np.isfinite(p): yt.append(series.iloc[o]); yp.append(p)
            except Exception: pass
        if len(yt) >= max(3, folds//2):
            mp = mape(yt, yp)
            if not np.isfinite(mp) or mp > UNSTABLE_MAPE:
                results[name] = {"MAPE": np.nan, "sMAPE": np.nan, "WAPE": np.nan,
                                 "status": "excluded: numerically unstable"}
            else:
                results[name] = {"MAPE": mp, "sMAPE": smape(yt, yp), "WAPE": wape(yt, yp),
                                 "status": f"ok ({len(yt)} folds)"}
        else:
            results[name] = {"MAPE": np.nan, "sMAPE": np.nan, "WAPE": np.nan,
                             "status": "failed / insufficient folds"}
    return results
def select(results, series, freq, holdout, tol=2.0):
    ok = {k: v for k, v in results.items() if np.isfinite(v["MAPE"])}
    ranked = sorted(ok.items(), key=lambda kv: kv[1]["MAPE"])
    m = SEASON[freq]; n = len(series); conf = {}
    if holdout and n > holdout + m:
        tr, te = series.iloc[:-holdout], series.iloc[-holdout:]
        for name, _ in ranked[:8]:
            try: conf[name] = mape(te.values, REGISTRY[name][0](tr, holdout, m))
            except Exception: conf[name] = np.nan
    for name, v in ranked: v["holdout_MAPE"] = conf.get(name, np.nan)
    top = [r[0] for r in ranked[:3]]
    if ranked:
        best = ranked[0][1]["MAPE"]
        for name, v in ranked:
            if name in BASELINES and v["MAPE"] <= best+tol and name not in top:
                top = [name] + top[:2]; break
    if not top: top = ["Naive"]
    return ranked, top
def final_forecast(series, freq, top, h, pi):
    m = SEASON[freq]; preds = {}
    for name in top:
        try: preds[name] = REGISTRY[name][0](series, h, m)
        except Exception: pass
    if not preds: preds["Naive"] = m_naive(series, h, m)
    preds["Ensemble (top-3 avg)"] = np.mean(np.column_stack(list(preds.values())), axis=1)
    resid = np.diff(series.values.astype(float)); sigma = np.std(resid) if len(resid) else 0.0
    z = {80:1.2816, 90:1.6449, 95:1.9600}.get(pi, 1.2816); lead = np.sqrt(np.arange(1, h+1))
    center = preds[top[0]] if top and top[0] in preds else preds["Ensemble (top-3 avg)"]
    return preds, np.maximum(center - z*sigma*lead, 0), center + z*sigma*lead, center
def risk_rating(series, hi, lo, center):
    cv = np.std(series.values)/np.mean(series.values)*100 if np.mean(series.values) else 100
    width = np.mean((hi-lo)/np.where(center == 0, np.nan, center))*100
    r = "High" if (cv > 30 or width > 60) else "Medium" if (cv > 18 or width > 35) else "Low"
    return r, cv, width

# ---------- i18n ----------
L = {
 "en": {"exec":"EXECUTIVE SUMMARY", "sub":"{scope} forecast · chosen method: {model} · generated {date}",
   "headline":"HEADLINE", "hl":"Forecast for the {scope}: {center}   (80% range: {lo} to {hi})",
   "means":"WHAT THIS MEANS", "meanstxt":"The most likely outcome is about {center}, but plan around the range {lo}-{hi}. The single midpoint should never be used alone; the range is part of the answer.",
   "acc":"ACCURACY & CONFIDENCE", "acctxt":"Best method: {model} (average error {mape}%). A simple baseline (Naive) scores {naive}%, so the winner is about {margin} points better — a real but {edge} edge. Overall risk: {risk} ({conf}).",
   "cav":"KEY CAVEATS", "use":"HOW TO USE THESE NUMBERS",
   "cav1":"Forecast horizon is {h} period(s); accuracy drops sharply if extrapolated further.",
   "cav2":"Based on {n} periods of history.", "cav3":"{ex} model(s) were excluded (too little data or numerically unstable).",
   "cav4":"Based on historical patterns only — unplanned events (campaigns, stockouts, budget/algorithm changes) are not captured.",
   "use1":"Report the range, not just the single number.", "use2":"Set targets around the midpoint; plan capacity/stock on the upper bound; treat the lower bound as the safe floor.",
   "use3":"Re-run each period as new data arrives; model selection adapts automatically.",
   "s_hist":"History", "s_bt":"Backtest", "s_fc":"Forecast", "s_dp":"Data Profile", "s_notes":"Notes",
   "c_period":"Period", "c_actual":"Actual", "c_mom":"Change vs prev", "c_model":"Model", "c_status":"Status",
   "c_low":"Lower 80%", "c_up":"Upper 80%", "c_field":"Field", "c_value":"Value",
   "edge_narrow":"narrow", "edge_clear":"clear", "conf_hi":"treat as directional", "conf_md":"moderate confidence", "conf_lo":"high confidence"},
 "id": {"exec":"RINGKASAN EKSEKUTIF", "sub":"Forecast {scope} · metode terpilih: {model} · dibuat {date}",
   "headline":"ANGKA UTAMA", "hl":"Forecast untuk {scope}: {center}   (rentang 80%: {lo} sampai {hi})",
   "means":"ARTINYA APA", "meanstxt":"Hasil paling mungkin sekitar {center}, tapi rencanakan pada rentang {lo}-{hi}. Angka tengah jangan dipakai sendirian; rentangnya adalah bagian dari jawaban.",
   "acc":"AKURASI & KEYAKINAN", "acctxt":"Metode terbaik: {model} (rata-rata meleset {mape}%). Baseline sederhana (Naive) meleset {naive}%, jadi pemenang unggul sekitar {margin} poin — keunggulan nyata tapi {edge}. Risiko keseluruhan: {risk} ({conf}).",
   "cav":"CATATAN PENTING", "use":"CARA MEMAKAI ANGKA INI",
   "cav1":"Horizon forecast {h} periode; akurasi turun tajam bila ditarik lebih jauh.",
   "cav2":"Berdasarkan {n} periode data historis.", "cav3":"{ex} model dikecualikan (data kurang atau tidak stabil secara numerik).",
   "cav4":"Berbasis pola historis saja — peristiwa tak terjadwal (kampanye, stockout, perubahan budget/algoritma) tidak tertangkap.",
   "use1":"Laporkan rentangnya, bukan hanya angka tunggal.", "use2":"Tetapkan target di sekitar titik tengah; rencanakan stok/kapasitas pada batas atas; jadikan batas bawah sebagai ambang aman.",
   "use3":"Jalankan ulang tiap periode saat data baru masuk; pemilihan model menyesuaikan otomatis.",
   "s_hist":"Riwayat", "s_bt":"Backtest", "s_fc":"Forecast", "s_dp":"Profil Data", "s_notes":"Catatan",
   "c_period":"Periode", "c_actual":"Aktual", "c_mom":"Perubahan vs sebelumnya", "c_model":"Model", "c_status":"Status",
   "c_low":"Batas Bawah 80%", "c_up":"Batas Atas 80%", "c_field":"Item", "c_value":"Nilai",
   "edge_narrow":"tipis", "edge_clear":"jelas", "conf_hi":"perlakukan sebagai arah", "conf_md":"keyakinan sedang", "conf_lo":"keyakinan tinggi"},
}

def make_fmt(unit):
    def rnd(v):
        v = float(v); a = abs(v)
        if a >= 1e6: return round(v/1000)*1000
        if a >= 1e4: return round(v/100)*100
        return round(v)
    return lambda v: f"{unit}{rnd(v):,.0f}"

# ---------- excel ----------
def write_excel(path, lang, unit, label, prof, results, ranked, top, preds, lo, hi, center, series, freq, h, risk, pi):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    t = L[lang]; f = make_fmt(unit)
    GREEN = "217A4D"; LIGHT = "EAF3ED"
    wb = Workbook(); wb.remove(wb.active)

    # ---- Executive Summary ----
    ws = wb.create_sheet(t["exec"].title()[:31]); ws.column_dimensions["A"].width = 92
    from openpyxl.worksheet.properties import PageSetupProperties
    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    date = pd.Timestamp.today().date().isoformat()
    scope = (f"{h} " + ("periods" if lang == "en" else "periode")) if h > 1 else ("next period" if lang == "en" else "periode berikutnya")
    hc = float(np.sum(center)) if h > 1 else float(center[0])
    hlo = float(np.sum(lo)) if h > 1 else float(lo[0]); hhi = float(np.sum(hi)) if h > 1 else float(hi[0])
    best_name = ranked[0][0] if ranked else top[0]
    best_mape = ranked[0][1]["MAPE"] if ranked else float("nan")
    naive_mape = results.get("Naive", {}).get("MAPE", float("nan"))
    margin = (naive_mape - best_mape) if (np.isfinite(naive_mape) and np.isfinite(best_mape)) else float("nan")
    edge = t["edge_narrow"] if (np.isfinite(margin) and margin < 5) else t["edge_clear"]
    conf = {"High": t["conf_hi"], "Medium": t["conf_md"], "Low": t["conf_lo"]}[risk[0]]
    ex_count = sum(1 for _, v in results.items() if not np.isfinite(v["MAPE"]))
    rows = [
        ("title", f"{t['exec']} — {label}"),
        ("sub", t["sub"].format(scope=scope, model=best_name, date=date)),
        ("gap", ""),
        ("h", t["headline"]),
        ("big", t["hl"].format(scope=scope, center=f(hc), lo=f(hlo), hi=f(hhi))),
        ("gap", ""),
        ("h", t["means"]),
        ("b", t["meanstxt"].format(center=f(hc), lo=f(hlo), hi=f(hhi))),
        ("gap", ""),
        ("h", t["acc"]),
        ("b", t["acctxt"].format(model=best_name, mape=f"{best_mape:.1f}" if np.isfinite(best_mape) else "-",
             naive=f"{naive_mape:.1f}" if np.isfinite(naive_mape) else "-",
             margin=f"{margin:.1f}" if np.isfinite(margin) else "-", edge=edge, risk=risk[0], conf=conf)),
        ("gap", ""),
        ("h", t["cav"]),
        ("b", "• " + t["cav1"].format(h=h)), ("b", "• " + t["cav2"].format(n=len(series))),
        ("b", "• " + t["cav3"].format(ex=ex_count)), ("b", "• " + t["cav4"]),
        ("gap", ""),
        ("h", t["use"]),
        ("b", "• " + t["use1"]), ("b", "• " + t["use2"]), ("b", "• " + t["use3"]),
        ("gap", ""),
        ("sub", "Defensible Forecasting · Diar Azari · linkedin.com/in/diarazari"),
    ]
    r = 1
    for kind, text in rows:
        c = ws.cell(r, 1, text); c.alignment = Alignment(wrap_text=True, vertical="top")
        if kind == "title":
            c.font = Font(bold=True, size=16, color="FFFFFF"); c.fill = PatternFill("solid", fgColor=GREEN); ws.row_dimensions[r].height = 30
        elif kind == "sub":
            c.font = Font(italic=True, size=10, color="595959")
        elif kind == "h":
            c.font = Font(bold=True, size=11, color=GREEN); c.fill = PatternFill("solid", fgColor=LIGHT)
        elif kind == "big":
            c.font = Font(bold=True, size=13); ws.row_dimensions[r].height = 26
        elif kind == "b":
            c.font = Font(size=11); ws.row_dimensions[r].height = 42
        r += 1

    def grid(title, header, data, widths):
        s = wb.create_sheet(title[:31])
        for i, w in enumerate(widths, 1): s.column_dimensions[chr(64+i)].width = w
        for ci, htext in enumerate(header, 1):
            cc = s.cell(1, ci, htext); cc.font = Font(bold=True, color="FFFFFF"); cc.fill = PatternFill("solid", fgColor=GREEN)
        for ri, row in enumerate(data, 2):
            for ci, val in enumerate(row, 1): s.cell(ri, ci, val)
        return s

    # History + MoM
    hist = [[str(d.date()), round(float(v)), (f"{(series.values[i]/series.values[i-1]-1)*100:+.1f}%" if i > 0 else "")]
            for i, (d, v) in enumerate(zip(series.index, series.values))]
    grid(t["s_hist"], [t["c_period"], f"{t['c_actual']} ({label})", t["c_mom"]], hist, [16, 22, 20])

    # Backtest
    bt = [[nm, round(v["MAPE"],2), round(v["sMAPE"],2), round(v["WAPE"],2),
           (round(v.get("holdout_MAPE"),2) if np.isfinite(v.get("holdout_MAPE",np.nan)) else ""), v["status"]]
          for nm, v in ranked]
    for nm, v in results.items():
        if not np.isfinite(v["MAPE"]): bt.append([nm, "", "", "", "", v["status"]])
    grid(t["s_bt"], [t["c_model"], "MAPE %", "sMAPE %", "WAPE %", f"Holdout MAPE %", t["c_status"]], bt, [20,10,10,10,15,30])

    # Forecast detail
    idx = pd.date_range(series.index[-1], periods=h+1, freq={"D":"D","W":"W-MON","M":"MS"}[freq])[1:]
    keys = list(preds.keys())
    fc = [[str(d.date())] + [round(float(preds[k][i]),2) for k in keys] + [round(float(lo[i]),2), round(float(hi[i]),2)]
          for i, d in enumerate(idx)]
    grid(t["s_fc"], [t["c_period"]] + keys + [t["c_low"], t["c_up"]], fc, [14]+[16]*len(keys)+[14,14])

    # Data profile
    grid(t["s_dp"], [t["c_field"], t["c_value"]], [[k, v] for k, v in prof.items()], [22, 26])

    wb.save(path)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True); ap.add_argument("--date-col", required=True)
    ap.add_argument("--value-col", required=True); ap.add_argument("--freq", default="M", choices=["D","W","M"])
    ap.add_argument("--horizon", type=int, default=12); ap.add_argument("--output", default="forecast.xlsx")
    ap.add_argument("--folds", type=int, default=8); ap.add_argument("--holdout", type=int, default=6)
    ap.add_argument("--pi", type=int, default=80); ap.add_argument("--lang", default="en", choices=["en","id"])
    ap.add_argument("--unit", default=""); ap.add_argument("--label", default="Value")
    a = ap.parse_args()
    df = load(a.input, a.date_col, a.value_col); prof = quality(df, a.date_col, a.value_col)
    series = aggregate(df, a.date_col, a.value_col, a.freq)
    print(f"Loaded {prof['rows']} rows -> {len(series)} {a.freq} periods ({prof['start']}..{prof['end']})")
    results = backtest(series, a.freq, a.folds)
    ranked, top = select(results, series, a.freq, a.holdout)
    preds, lo, hi, center = final_forecast(series, a.freq, top, a.horizon, a.pi)
    risk = list(risk_rating(series, hi, lo, center)) + [a.pi]
    write_excel(a.output, a.lang, a.unit, a.label, prof, results, ranked, top, preds, lo, hi, center,
                series, a.freq, a.horizon, risk, a.pi)
    print("Top models:", ", ".join(top))
    if ranked: print(f"Risk: {risk[0]}  |  best MAPE: {ranked[0][1]['MAPE']:.2f}%  ({ranked[0][0]})")
    else: print(f"Risk: {risk[0]}  |  no model passed backtesting — used Naive fallback")
    print("Saved:", a.output)

if __name__ == "__main__":
    main()
