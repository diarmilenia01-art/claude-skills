# Claude Skills — by Diar Azari

A growing collection of **effective, token-efficient skills for Claude**, built for two kinds of people I know well: **students** (thesis, dissertation, coursework) and **data analysts** (forecasting, reporting, analysis).

Every skill here follows the same principle: carry a well-designed *methodology*, run reliably, and stay light on context. New skills are added over time.

> Connect: [linkedin.com/in/diarazari](https://www.linkedin.com/in/diarazari/)

---

## For students

Skills that help with research, writing, and coursework.

| Skill | What it does | Status |
|---|---|---|
| [thesis-companion](./thesis-companion) | A companion for skripsi/thesis/journal work: finds open-access sources, checks whether a paper fits your argument, explains hard papers, reviews your draft, formats citations, and preps you for the defense — token-efficient, and it keeps you the author | ✅ Tested |

## For data analysts

Skills for forecasting, analysis, and turning data into decisions.

| Skill | What it does | Status |
|---|---|---|
| [defensible-forecasting](./defensible-forecasting) | Interviews the user, backtests 20+ forecasting models across every major family, and selects the best 3 by MAPE with anti-overfitting safeguards (holdout confirmation, parsimony, seasonal data-gating) | ✅ Tested |

*More skills for both groups are on the way — this collection grows over time.*

---

## Design principles

- **Methodology first.** The value is in the analytical and editorial decisions, not just code.
- **Token-efficient.** `SKILL.md` stays lean; heavy logic lives in bundled scripts that are *run*, not loaded into context; long explanations sit in `references/` and load only when needed.
- **Tested, not just written.** Each skill is verified to run end-to-end before it ships.
- **Honest by design.** Skills state their limits, cite their sources, and never fake results.

---

## How to use a skill

Each skill folder contains a `SKILL.md` (the entry point) plus any `scripts/` and `references/`. Point Claude at the skill folder, or clone the repo and use the skill in a Claude environment that supports skills. Python-based skills list their dependencies at the top of the run instructions.

---

## License

Released under the **MIT License** — free to use, modify, and share, including commercially, as long as attribution is kept. See [`LICENSE`](./LICENSE).

Created by **Diar Azari** · [linkedin.com/in/diarazari](https://www.linkedin.com/in/diarazari/)
