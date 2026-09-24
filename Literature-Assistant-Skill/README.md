# Literature Assistant

A token-efficient Claude skill for students working through research papers for a
thesis, dissertation, or literature review. Part of
[Claude Skills by Diar Azari](../). Connect:
[linkedin.com/in/diarazari](https://www.linkedin.com/in/diarazari/)

## What it does

1. **Interviews you first** — find-for-me vs you-give-link/file, topic, depth, citation
   style, synthesis, language — so the output fits what you actually need.
2. **Finds open-access papers** (legal sources only) or takes your link/PDF.
3. **Converts each PDF to Markdown once** so the conversation runs on compact clean text
   instead of re-reading the PDF — with the original source link kept in the file header.
4. **Extracts structured content** — research problem, method, key findings, limitations.
5. **Polishes prose** with academic-tuned anti-slop rules (clarity and precision, without
   stripping the passive voice and hedging that scholarly writing needs).
6. **Cites and saves** — formats APA/IEEE/Vancouver and writes a note file with summary,
   exact quotes, source link, and citation. For multiple papers, a comparison table for
   your literature review.

## Why token-efficient

Convert each PDF once, then discuss from the compact Markdown; the short note file
replaces re-reading the whole paper later. For real multi-page journals this is a large
saving over reading the PDF each turn.

## Structure

```
literature-assistant/
├── SKILL.md                     # entry point: interview + pipeline + rules
├── scripts/pdf_to_md.py         # PDF -> Markdown (pymupdf4llm), keeps source link
└── references/
    ├── methodology.md           # workflow, open-access & anti-plagiarism rules, note format
    ├── anti-slop.md             # academic-tuned prose rules (adapted from stop-slop)
    └── citation-styles.md       # APA / IEEE / Vancouver
```

## Requirements

```
pip install pymupdf4llm
```

## Academic honesty

This skill helps you **understand sources and write clearly and honestly** — it is not
for disguising AI-generated text to evade academic detection. Every substantive claim
should be cited; paraphrase in your own words; keep quotations exact and marked.

## Credits

The prose-polishing layer adapts **[stop-slop](https://github.com/hardikpandya/stop-slop)**
by Hardik Pandya (MIT License), re-scoped for academic writing. See
`references/anti-slop.md` for what was kept, softened, and dropped, and why.

## License

MIT License · Created by **Diar Azari** ·
[linkedin.com/in/diarazari](https://www.linkedin.com/in/diarazari/) · 2026
