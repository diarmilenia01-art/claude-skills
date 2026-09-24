# Defensible Forecasting

A Claude skill that produces time-series forecasts you can **defend** — the chosen model wins on tested accuracy, not luck, and every result ships with its uncertainty and limits stated openly.

Part of [Claude Skills by Diar Azari](../). Connect: [linkedin.com/in/diarazari](https://www.linkedin.com/in/diarazari/)

---

## What it does

Given historical data (sales, GMV, demand, traffic — any numeric series over time), the skill:

1. **Interviews the user first** — goal, forecast horizon, output format (Excel/Word/PDF), charts yes/no, and data structure — so the output matches what's actually needed.
2. **Backtests broadly** — rolling-origin cross-validation across models from every major family:
   - Baselines: Naive, Seasonal Naive, Drift, Mean
   - Exponential smoothing / ETS: SES, Holt, Holt (damped), Holt-Winters (add/mul)
   - ARIMA family: ARIMA, AutoARIMA, SARIMA
   - Decomposition & other: Theta
   - Regression: linear trend, polynomial trend, seasonal dummies, Fourier terms
   - ML: Random Forest, Gradient Boosting, simple Neural Net
   - Extension points (auto-enabled if installed): Prophet, TBATS, XGBoost, LightGBM, ARIMAX
3. **Selects with safeguards** — top 3 by MAPE, then holdout confirmation + a parsimony rule + seasonal data-gating to avoid overfitting.
4. **Reports clearly** — forecast + prediction interval + plain-language risk rating, plus simple MAPE / sMAPE / WAPE explanations.

## Structure

```
defensible-forecasting/
├── SKILL.md                    # entry point: interview + run instructions + core rules
├── scripts/forecast.py         # the engine (run, not loaded into context)
└── references/methodology.md   # full method list, safeguards, metric definitions
```

## Requirements

```
pip install pandas numpy statsmodels scikit-learn openpyxl
```

## Run directly (outside Claude)

```
python scripts/forecast.py --input data.csv --date-col DATE --value-col VALUE \
  --freq M --horizon 12 --output forecast.xlsx [--folds 8] [--holdout 6] [--pi 80]
```

`--freq`: D (daily), W (weekly), M (monthly). Output is an Excel report with four sheets: Summary, Data Profile, Backtest, and Forecast (with interval + risk rating).

## Note on authorship

This skill packages a forecasting **methodology I designed** — the model set, the metric choices, and the anti-overfitting safeguards — implemented in Python. The methodology and its rationale are documented in `references/methodology.md`.

---

MIT License · Created by **Diar Azari** · [linkedin.com/in/diarazari](https://www.linkedin.com/in/diarazari/) · 2026
