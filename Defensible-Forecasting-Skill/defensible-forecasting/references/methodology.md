# Defensible Forecasting — Methodology (detailed reference)

Read this only when the user asks how the method works, wants the metric
explanations, or needs the full model list. Not required for a normal run.

## Workflow (as implemented by scripts/forecast.py)

1. Load & profile — frequency, date range, history length, number of series.
2. Data quality check — missing, duplicates, negatives/zeros, date gaps, anomalies (reported, not silently fixed).
3. Aggregate — to analysis frequency (weekly/monthly), complete periods only.
4. Seasonal data-gating — seasonal models need >=2 full cycles; ineligible ones are excluded and the reason recorded.
5. Backtest — rolling-origin cross-validation (1-step-ahead, several folds); compute MAPE (primary) + sMAPE + WAPE.
6. Safeguarded selection — best MAPE candidates -> holdout confirmation -> parsimony rule -> top 3 + ensemble.
7. Output — forecast + prediction interval + risk rating + short "why this model won" summary.

## Method library (by family)

Implemented & tested:
- Baseline: Naive, Seasonal Naive, Drift, Mean
- Exponential smoothing / ETS: SES, Holt, Holt (damped), Holt-Winters additive, Holt-Winters multiplicative
- ARIMA family: ARIMA, AutoARIMA (grid), SARIMA
- Decomposition & other: Theta
- Regression-based: Linear trend, Polynomial trend, Seasonal dummies, Fourier terms
- ML / advanced: Random Forest, Gradient Boosting, simple Neural Net (lag features)

Extension points (activate when the library is installed), toward 30 methods:
Prophet, TBATS, XGBoost, LightGBM, ARIMAX with external regressors.

On short business series, the ML family often does NOT beat classical models
(a consistent M4/M5 competition finding) — that is a true result, not a failure.

## The three overfitting safeguards (why it's "defensible")

Testing many models and cherry-picking the best MAPE invites selection bias — a
winner that fits noise. Guardrails:

1. Holdout confirmation — selection by rolling-origin CV, then re-checked on a final untouched window.
2. Parsimony rule — if a complex model beats a simple baseline only marginally, prefer the simple one.
3. Seasonal data-gating — seasonal models excluded automatically when history is too short, and the exclusion is reported.

Never adjust an anomaly just because a chart looks odd. Report it; if warranted,
test raw vs adjusted and keep raw unless backtesting consistently favors adjustment.

## Accuracy metrics (plain language — show these to users)

- MAPE — "on average, how many percent the forecast is off." (primary) Smaller is better.
- sMAPE — "a fairer MAPE": treats too-high and too-low guesses more evenly.
- WAPE — "MAPE that cares about the big numbers": weights high-value items more.

Analogy: MAPE = average report-card grade, sMAPE = a fairer grading scheme,
WAPE = a report card where important subjects count more. When all three agree a
model is good, confidence it is not a fluke is much higher.

## Worked examples

- Minimal: user attaches daily sales, wants next month. After Step 0 (1 month, Excel,
  chart, concise, single series): run with --freq D --horizon 30; deliver .xlsx with
  forecast, 80% interval, risk rating, one-line rationale — explained in the user's language.
- Multi-series: "project 12 months of GMV per marketplace." Confirm 12 monthly periods
  and multiple series; run the engine per marketplace (--freq M --horizon 12), apply
  safeguards per series, consolidate.

---
Created by Diar Azari · https://www.linkedin.com/in/diarazari/ · 2026 · MIT License
