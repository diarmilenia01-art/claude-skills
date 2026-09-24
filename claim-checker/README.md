# Claim-checker

A critical-thinking companion for data-backed claims. It does not tell you what is true. It asks the questions a sharp analyst would ask before believing a statistic, a chart, or a finding, and leaves the judgment to you. Part of [Claude Skills by Diar Azari](../). Connect: [linkedin.com/in/diarazari](https://www.linkedin.com/in/diarazari/)

## What it does

Paste a statistic, a news claim, a research finding, a marketing number, or upload a chart. The skill:

- Flags objective red flags only: truncated axes, missing sample size, correlation stated as causation, percentages with no base, cherry-picked timeframes, misleading scales, and more.
- Shows the exact trigger for each note, and one line on when that pattern is actually fine.
- Labels each finding kuat / perlu dicek / rawan, with most landing in the middle.
- Closes by admitting it may be missing context and leaving the decision to you.

## What it will NOT do

It never declares a claim true, false, or "a lie". A false accusation is worse than no check, so it asks questions instead of passing verdicts. Interpretive concerns are raised as open questions, not flags. It usually cannot see the underlying data, and it says so.

## Why this design

Most "bias detectors" fail by over-accusing: calling a legitimate chart misleading. This skill is built to avoid that. By pointing at concrete triggers, always noting the legitimate case, and phrasing everything as a question, a good question stays useful even when the claim turns out sound.

## Structure

```
claim-checker/
├── SKILL.md                 # entry point: interview + six brakes + output format
└── references/
    ├── patterns.md          # objective patterns: trigger + question + when it is fine
    └── method.md            # labels, stance, worked example, chart-image caveat
```

No script and no dependencies. This is a reasoning skill, so it stays light on context.

## License

MIT License · Created by **Diar Azari** · [linkedin.com/in/diarazari](https://www.linkedin.com/in/diarazari/) · 2026
