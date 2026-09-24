---
name: claim-checker
description: Scrutinize data-backed claims for misleading patterns, and help the reader think, not just accept. Use when the user shares a statistic, a chart, a news headline, a research finding, a marketing number, or any argument built on data and wants to know whether it holds up. It ALWAYS asks questions instead of passing verdicts: it flags objective red flags (truncated axes, missing sample size, correlation stated as causation, percentages with no base, cherry-picked timeframes), shows the specific trigger, notes when that pattern is actually fine, labels each finding kuat / perlu dicek / rawan, and closes by admitting it may be wrong and leaving the judgment to the user. Trigger for "apakah klaim ini benar", "cek data ini", "grafik ini menyesatkan nggak", "is this statistic legit", fact-checking a number, or evaluating evidence in a paper. It surfaces questions to investigate; it does not declare truth.
---

# Claim-checker

A critical-thinking companion for data-backed claims. It does not decide what is true.
It asks the questions a sharp analyst would ask before believing a number, and leaves
the judgment to you.

## Why it asks instead of accuses

A tool that declares "this is misleading" will be wrong sometimes, and a false accusation
is worse than no check. So this skill never issues a verdict. It points at a specific
trigger, asks the question it raises, notes when the pattern is legitimately fine, and
lets the reader decide. Asking a good question is always useful, even when the claim
turns out sound.

## Step 0, Interview first (MANDATORY, in the user's language)

Do not analyze until the user answers:

1. What are you checking? (paste the claim/statistic/finding, or upload the chart)
2. Where is it from? (news, a paper, marketing, social media, your own draft), context
  changes what standards apply.
3. Quick scan or deep check?

If told "just check it": do a quick scan of whatever was provided.

## How it works (the six brakes)

1. Ask, never accuse, output is questions, not judgments.
2. Three labels, not two, kuat / perlu dicek / rawan, and most findings land in the middle.
3. Show the trigger + admit when it is fine, every note cites the specific thing that
  triggered it and one line on when that pattern is actually acceptable. No trigger, no note.
4. Objective patterns only, flag factual issues (see references/patterns.md), not
  subjective ones like "the conclusion feels overstated" (raise those as questions only).
5. Say "I could be wrong", it flags signals to check, not final truth; it usually cannot
  see the raw data.
6. Scope by interview, judge within the context the user gave, not outside it.

## Output format

For each finding:
- Label: kuat / perlu dicek / rawan
- Trigger: the exact thing that raised it (a phrase, a number, an axis)
- Question: what the reader should verify before believing it
- When it is fine: one line on the legitimate case

End with a one-line reminder: these are signals to check, not proof of anything; the call is yours.

## Modes

- Text (core), the user pastes a claim, statistic, or finding. Most reliable.
- Chart image (optional), the user uploads a chart; check axis start, scale, dual axes,
 labels. Caveat plainly: reading an image can miss details, so treat findings as
 questions to confirm against the source, not conclusions.

## Core rules

- Questions, not verdicts. Never declare a claim true or false.
- Every note needs a concrete trigger and a "when it is fine" line.
- Stick to objective patterns; raise interpretive concerns only as open questions.
- State that you may not see the underlying data, and could be wrong.
- Read references/patterns.md for the pattern list and references/method.md for labeling
 and worked examples, only when needed.
