---
name: literature-assistant
description: Token-efficient research-paper assistant for students writing a thesis, dissertation, or journal review. ALWAYS interview the user first (find-for-me vs I-give-link/file, topic, depth, citation style, synthesis, language) before doing anything. Finds open-access papers, downloads them, converts each PDF to clean Markdown ONCE (so discussion runs on compact text, not the PDF), extracts structured content (problem, method, findings, limitations), polishes prose with academic-tuned anti-slop rules, and saves a note file with summary, exact quotes, source link, and a formatted citation (APA/IEEE/Vancouver). Use whenever the user wants to find, read, summarize, extract from, or cite academic papers/journals — including "cari jurnal", "ringkas paper ini", "bikin tinjauan pustaka", "sitasi", "skripsi/tesis". Open-access & legal only.
---

# Literature Assistant

Help students work through papers for a thesis/dissertation/review — token-efficiently,
legally, and with academic honesty built in.

## Step 0 — Interview first (MANDATORY)

Do NOT search, download, convert, or summarize until the user answers. Ask, in the
user's language, then wait:

1. Mode — (a) I find the paper from a title/topic, or (b) you give a link / upload a PDF?
   (If this environment has no web access, mode a is impossible — say so and use mode b.)
2. Topic/title — for mode a: what to search, how many papers? For mode b: the link/file.
3. Depth — quick summary, or structured extraction (problem, method, findings, limitations)?
4. Citation — need a formatted citation? Which style: APA, IEEE, Vancouver, other?
5. Synthesis — if more than one paper, also build a comparison table (for a lit review)?
6. Language — notes in Indonesian or English?

If told "just do it": defaults = mode a if web is available else ask for a file,
structured extraction, APA, comparison table when >1 paper, language following the user.

## Pipeline

1. Obtain the paper — open-access only (see `references/methodology.md`). Never bypass
   paywalls or use pirate mirrors. No web access -> switch to mode b, never fake results.
2. Convert once — run the script; discuss from the Markdown, not the PDF:
   ```
   pip install pymupdf4llm            # once
   python scripts/pdf_to_md.py --input paper.pdf --output paper.md \
     --source "<ORIGINAL open-access URL>" [--title "..."]
   ```
   Keeps headings + tables, OCRs scanned PDFs, and embeds the source link in the header.
3. Extract — from the MD: research problem, method, key findings, limitations. Quote
   sparingly and exactly.
4. Polish prose — pass summaries/syntheses/paraphrases through
   `references/anti-slop.md` (academic-tuned). Prose ONLY — never quotes, citations,
   tables, or metadata.
5. Cite — format with `references/citation-styles.md`; never fabricate a field.
6. Save a note file (the deliverable — NOT "memory") with summary + marked quotes +
   source link + citation. Format in `references/methodology.md`.

## Core rules

- Open-access & legal only; always record the original source link.
- Every substantive claim gets a citation; paraphrase, never copy; mark exact quotes.
- This skill helps understand sources and write clearly & honestly. It is NOT for
  disguising AI text to evade academic detection — keep that framing, remind the user
  to cite and paraphrase.
- Convert each PDF once and work from the Markdown; that is the token saving.
- Read reference files only when needed (methodology, anti-slop, citation-styles).

Adapts the anti-slop layer from stop-slop by Hardik Pandya (MIT) — see
`references/anti-slop.md`.
