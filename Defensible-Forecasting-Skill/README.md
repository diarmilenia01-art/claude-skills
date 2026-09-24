# Claude Skills — by Diar Azari

A growing collection of **effective, token-efficient skills for Claude**, built around a simple principle: a skill should carry a well-designed *methodology*, run reliably, and stay light on context.

I'm a Data Analyst (Mathematics, minor in Statistics) focused on turning raw data into systems and decisions. These skills package methodologies I've designed for real analytical work into reusable tools.

> Connect: [linkedin.com/in/diarazari](https://www.linkedin.com/in/diarazari/)

---

## Skills

| Skill | What it does | Status |
|---|---|---|
| [defensible-forecasting](./defensible-forecasting) | Interviews the user, backtests 20+ forecasting models across every major family, and selects the best with anti-overfitting safeguards | ✅ Tested |

*(More skills coming — this collection grows over time.)*

---

## Featured: Defensible Forecasting

A methodology for forecasts you can **defend** — where the chosen model wins on tested accuracy, not luck, and every result ships with its uncertainty and limits.

- **Interviews first** — asks goal, horizon, output format, charts, and data structure before doing anything, so the result is what the user actually needs.
- **Tests broadly** — backtests models from every family (baselines, exponential smoothing/ETS, ARIMA/SARIMA, Theta, regression, and ML) using rolling-origin cross-validation.
- **Selects honestly** — picks the top 3 by MAPE, then applies three anti-overfitting safeguards: holdout confirmation, a parsimony rule, and seasonal data-gating.
- **Communicates clearly** — outputs a forecast with a prediction interval, a plain-language risk rating, and simple explanations of MAPE / sMAPE / WAPE.

See [`defensible-forecasting/`](./defensible-forecasting) for the full skill.

---

## Design principles

- **Methodology first.** The value is in the analytical decisions (which models, which metric, which safeguards), not just code.
- **Token-efficient.** `SKILL.md` stays lean; heavy logic lives in bundled scripts that are *run*, not loaded into context; long explanations sit in `references/` and load only when needed.
- **Tested, not just written.** Each skill is verified to run end-to-end before it ships.

---

## How to use a skill

Each skill folder contains a `SKILL.md` (the entry point) plus any `scripts/` and `references/`. Point Claude at the skill folder, or clone the repo and use the skill in a Claude environment that supports skills. Python-based skills list their dependencies at the top of the run instructions.

---

## License

Released under the **MIT License** — free to use, modify, and share, including commercially, as long as attribution is kept. See [`LICENSE`](./LICENSE).

Created by **Diar Azari** · [linkedin.com/in/diarazari](https://www.linkedin.com/in/diarazari/)
