# Methodology (detailed reference)

Read this when you need the full workflow, the legal/source rules, or the
anti-plagiarism policy. Not required for a simple run.

## Workflow

1. Interview (Step 0 in SKILL.md) — settle mode, topic, depth, citation style,
   synthesis, and language before doing anything.
2. Obtain the paper:
   - Mode A (auto): search and fetch from OPEN-ACCESS sources only.
   - Mode B (manual): the user supplies a link or uploads the PDF.
3. Convert once: `scripts/pdf_to_md.py` -> clean Markdown with a metadata header
   holding the original source link. Discuss from the MD, not the PDF.
4. Extract structured content from the MD: research problem, method, key findings,
   limitations. Summarize; quote sparingly and exactly.
5. Polish prose through `references/anti-slop.md` (academic-tuned). Prose only —
   never quotations, citations, tables, or metadata.
6. Save a note file (see below) with summary + key quotes (marked) + source link +
   citation. This is the deliverable, not "memory".

## Legal & source rules (non-negotiable)

- Open-access only: Google Scholar / Semantic Scholar to discover, then download
  from arXiv, DOAJ, PubMed Central, institutional repositories, or the publisher's
  own open-access page.
- Never bypass paywalls; never use pirate mirrors (e.g. Sci-Hub). If a paper is not
  legally accessible, say so and ask the user for a legal copy.
- If web access is unavailable in the environment, do not fake a search or invent
  papers — switch to Mode B and ask for the link/file.
- Always record the original source URL in the note and the MD header.

## Anti-plagiarism policy (non-negotiable)

- Paraphrase in the user's own words; never present copied text as original.
- Mark any direct quotation clearly and keep it exact, with a page/section locator.
- Attach a citation to every substantive claim.
- This skill supports understanding sources and writing clearly and honestly. It is
  NOT for disguising AI-generated text to evade academic AI/plagiarism detection.
  Keep that framing in every output; remind the user to cite and paraphrase.

## Note file format (the deliverable)

Save as Markdown, e.g. `catatan-<slug>.md`:

```
# <Paper title>

- Source: <original URL>       - Authors/Year: <...>
- Citation (<style>): <formatted citation>

## Summary
<3–6 sentences, polished via anti-slop>

## Structured extraction
- Research problem: ...
- Method: ...
- Key findings: ...
- Limitations: ...

## Key quotes (exact, cite the locator)
> "<short exact quote>" (p. X)

## Notes for my writing
<paraphrase-ready points, in the user's own words>
```

## Multi-paper synthesis (for a literature review)

When several papers are processed, add a comparison table:

| Author (Year) | Method | Sample | Key finding | Limitation |
|---|---|---|---|---|

This is the backbone of a literature review. Keep each cell factual and cited.
