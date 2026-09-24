---
name: defensible-forecasting
description: Build defensible time-series forecasts from historical data (sales, GMV, demand, web traffic — any numeric series over time). ALWAYS interview the user first (goal, forecast horizon, output document format, charts yes/no, data structure) before doing anything else. Runs a bundled engine that backtests ~20+ methods across every major forecasting family (rolling-origin CV), selects the best 3 by MAPE with anti-overfitting safeguards (holdout confirmation, parsimony, seasonal data-gating), and outputs a forecast with prediction intervals and a plain-language risk rating. Use whenever the user wants to forecast, predict, or project future numbers from historical data — even when they only say "predict next month's sales", "project demand", "proyeksi penjualan", "peramalan", or "forecast". Trigger for any demand-planning, sales/target-setting, or time-series projection task, even if the word "forecast" is not used.
---

# Defensible Forecasting

Created by **Diar Azari** · https://www.linkedin.com/in/diarazari/ · 2026 · MIT License

Produce forecasts you can defend: the chosen model wins on tested accuracy, and every result ships with its uncertainty and limits.

## Step 0 — Interview first (MANDATORY)

Do NOT load, clean, or run anything until the user answers. Ask, in the user's language, then wait:

1. Goal — what to forecast, and for what decision?
2. Horizon — one period (1 day/week/month) or many (e.g. 30 days, 12 months)?
3. Output — Excel, Word, PDF, other?
4. Charts — yes or no?
5. Detail — concise or full?
6. Data structure — single series or many (e.g. per product/marketplace)? Or attach data to auto-detect.

If told "just do it": defaults = horizon per data frequency, Excel, charts on, medium detail, auto-detect. Announce defaults, then proceed.

## Run the engine (do NOT rewrite forecasting code)

Deps once: `pip install pandas numpy statsmodels scikit-learn openpyxl`

```
python scripts/forecast.py --input <data.csv|xlsx> --date-col <D> --value-col <V> \
  --freq <D|W|M> --horizon <N> --output <forecast.xlsx> \
  --lang <en|id> --unit "<prefix e.g. 'Rp '>" --label "<what the value is>" \
  [--folds 8] [--holdout 6] [--pi 80]
```

The script does: profiling → quality check → aggregation → seasonal data-gating →
rolling-origin backtest → stability filter (drops numerically unstable models) →
safeguarded selection (holdout + parsimony) → top-3 + ensemble → Excel report whose
**first sheet is a dense, plain-language Executive Summary for all stakeholders**
(headline forecast + range, what it means, accuracy & confidence, caveats, how to use
the numbers), followed by History (+ change %), Backtest, Forecast, and Data Profile.

Pick `--lang` to match the audience, and `--unit`/`--label` to fit the domain (e.g.
`--unit "Rp " --label "Sales"`). Numbers are rounded and thousands-separated for
readability.

Around it, Claude: runs Step 0; calls the script once per series (loop + consolidate
for multi-series); makes charts from the Forecast sheet if requested; converts to
Word/PDF if requested; explains results in the user's language.

## Core rules

- Lead every deliverable with a dense, clear **Executive Summary for all stakeholders** — the engine's first sheet is exactly this; keep that quality in any Word/PDF version too.
- Never output a bare number — always include the prediction interval.
- Keep a baseline (Naive/Seasonal Naive) in the comparison; if nothing beats it, say so.
- Report anomalies; don't silently "fix" data.
- State limitations: horizon, folds, data length, excluded models.
- **Brand-neutral:** this skill ships without any company, brand, or product names. Never bake them into the skill or its examples. In real runs, use the user's own wording via `--label`/`--unit`; for any demo or sample output, use synthetic data.
- Frame this as a methodology you designed, implemented in Python.

## More detail (read only when needed)

`references/methodology.md` — full method library (toward 30 models), the three
overfitting safeguards explained, plain-language MAPE/sMAPE/WAPE definitions to show
users, and worked examples. Read it only when the user asks how it works or wants the
metric explanations; it is not needed for a normal run.
