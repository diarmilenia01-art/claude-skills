# Methodology (detailed reference)

Read when you need the how-to for a mode. Not needed for a simple run.

## Token discipline (default for all modes)

- Convert a PDF once with `scripts/pdf_to_md.py`; the MD is a temporary working copy.
- For check-fit and citations, pull only the relevant lines, then drop the full MD.
- Don't paste the whole paper back to the user; give the targeted answer.
- Suggest Claude Projects for papers revisited often (cached = cheaper).

## Convert a paper

```
pip install pymupdf4llm            # once
python scripts/pdf_to_md.py --input paper.pdf --output paper.md \
  --source "<ORIGINAL open-access URL>"
```
Keeps headings + tables, OCRs scanned PDFs, embeds the source link in the header.
Known limit: complex data tables and figures may convert imperfectly — verify any table
before relying on its numbers.

## Mode how-tos

**(b) Check fit** — the anchor mode.
1. Student pastes their claim/sentence.
2. Convert the paper; scan for evidence for/against that specific claim.
3. Output: `Support / Contradict / Not relevant` + the specific evidence (numbers,
   findings) + a paraphrase of the student's sentence integrating the finding + citation.
4. If the claim is stronger than the evidence supports, flag the overreach and suggest
   softer wording.
5. Close with: "Read the source yourself before citing — this check doesn't replace that."

**(d) Feedback on a draft** — react, don't rewrite.
- Is each claim supported by evidence/citation? Mark unsupported ones.
- Where are the logical gaps or missing counterarguments?
- Which sentences would an examiner challenge, and why?
- Suggest what to add/fix; the student does the rewriting.

**(f) Defense (sidang) prep** — target the biggest fear.
- From the draft, generate likely examiner questions grouped by: background/motivation,
  method choices, results interpretation, limitations, novelty/contribution.
- For each, outline how to think through a strong answer (not a script to memorize).
- Add 2–3 "trap" questions (e.g. "why this method and not X?") with reasoning.

**(g) Polish prose** — `references/anti-slop.md`, academic-tuned. Their sentences only.

## Optional note file (only if the student wants to keep it)

```
# <Paper title>
- Source: <original URL>   - Authors/Year: <...>   - Citation: <formatted>
## Fit with my argument
<support / contradict / not relevant + specific evidence>
## Paraphrase (my wording, woven with the finding + citation)
<sentence>
## To check
- Read the full source before citing.
- Disclose AI assistance per my institution's policy.
```

Keep it short. The point is a usable, honest note — not a copy of the paper.
