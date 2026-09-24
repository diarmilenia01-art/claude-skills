# Patterns to flag (objective only)

Each pattern = the trigger to look for + the question to raise + when it is actually fine.
Only flag what you can point to concretely. If you cannot cite a specific trigger, do not
raise it. For anything interpretive (tone, "feels overstated"), raise it as an open
question, never as a flag.

## Truncated / non-zero axis
- Trigger: a bar/area chart whose Y-axis does not start at zero.
- Question: does the visual exaggerate a small real difference?
- When fine: line charts of things that never hit zero (temperature, stock price, pH), or
  when the change is genuinely large. Truncation is not automatically wrong.

## Missing or tiny sample size
- Trigger: a percentage or average with no n stated, or a very small n.
- Question: how many observations is this based on? "80% preferred" from 5 people is noise.
- When fine: well-known large datasets, censuses, or when n is stated and adequate.

## Correlation stated as causation
- Trigger: "X causes / leads to / drives Y" from observational data with no experiment.
- Question: was this a controlled study, or could a third factor explain both?
- When fine: randomized controlled trials, or when the author explicitly claims only
  association ("associated with", "linked to").

## Percentage with no base (relative vs absolute)
- Trigger: "risk doubled", "50% increase" with no absolute numbers.
- Question: doubled from what to what? 0.001% to 0.002% is still tiny.
- When fine: when both relative and absolute figures are given.

## Cherry-picked timeframe / range
- Trigger: a trend shown over a suspiciously specific or short window.
- Question: what does the longer history look like? Was the start point chosen to flatter?
- When fine: when the window is the natural unit (a fiscal year, since a known event) and
  stated as such.

## Misleading scale or dual axes
- Trigger: a log axis without a label, or two different Y-axes forced to "correlate".
- Question: are the scales comparable, or engineered to look aligned?
- When fine: log scales that are labeled and appropriate (data spanning orders of magnitude).

## Average hiding the distribution
- Trigger: a mean reported for skewed data (income, wait time) with no spread.
- Question: what is the median and the range? A few outliers can drag a mean.
- When fine: roughly symmetric data, or when median/spread are also given.

## Survivorship / selection bias
- Trigger: conclusions drawn only from "successes" or a self-selected group.
- Question: what about the cases that dropped out or were not counted?
- When fine: when the sampling frame is representative and described.

## Vague or shifting units
- Trigger: undefined units, changed baselines, or "up to" / "as much as" language.
- Question: measured how, exactly, and compared to what?
- When fine: units clearly defined and consistent.

## Overgeneralization
- Trigger: a broad claim ("students learn better with X") from one narrow study.
- Question: does the sample support a claim this general (one school, one semester)?
- When fine: meta-analyses or explicitly scoped claims.

Reminder: each of these is a question to investigate, not a verdict. Many turn out fine.
