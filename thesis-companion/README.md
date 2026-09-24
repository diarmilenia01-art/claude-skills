# Teman Skripsi — Thesis Companion

A token-efficient Claude skill for students writing a skripsi, thesis, or journal article. It cuts the mechanical work and eases the fear, while keeping you the author of your own work. Part of [Claude Skills by Diar Azari](../). Connect: [linkedin.com/in/diarazari](https://www.linkedin.com/in/diarazari/)

Built by someone who wrote a thesis by hand, start to finish, and remembers exactly where it hurt.

## What it helps with

- **Find sources** — open-access papers on your topic (legal sources only).
- **Check fit** — paste your own claim; find whether a paper supports, contradicts, or doesn't touch it, with the specific evidence, plus a cited paraphrase of your sentence.
- **Understand** — plain-language explanation of a hard paper so you actually learn it.
- **Feedback** — reactions to your own draft: weak arguments, gaps, and what an examiner might question.
- **Citations** — APA / IEEE / Vancouver, with fields verified (no fabricated references).
- **Defense (sidang) prep** — likely examiner questions from your draft, plus how to think through the answers.
- **Polish** — tighten your own sentences (academic-tuned anti-slop), keeping the formal register.

## What it will NOT do

It won't write your literature review, synthesis, or arguments, and it won't let you cite a paper you haven't read. Those cross into academic misconduct. This is a companion, not a ghost-writer. See [`references/integrity.md`](./references/integrity.md).

## Why token-efficient

Free-tier students have a small, session-based allowance that attachments and long context drain fast. The skill converts a PDF once, works from compact text, extracts only what's needed, and gives short targeted answers instead of dumping the paper back.

## Structure

```
thesis-companion/
├── SKILL.md                     # entry point: interview + modes + rules
├── scripts/pdf_to_md.py         # PDF -> Markdown (pymupdf4llm), keeps source link
└── references/
    ├── integrity.md             # the green/red line, disclosure (2025 guidance)
    ├── methodology.md           # mode how-tos, defense prep, note format, token discipline
    ├── anti-slop.md             # academic-tuned prose rules (adapted from stop-slop)
    └── citation-styles.md       # APA / IEEE / Vancouver
```

## Requirements

```
pip install pymupdf4llm
```

## Academic honesty

This skill helps you do honest work faster and with less fear. Every substantive claim should be cited; read your sources; keep quotations exact; and disclose AI assistance if your institution requires it. Rules differ by program and journal — check yours.

## Credits

The prose-polishing layer adapts **[stop-slop](https://github.com/hardikpandya/stop-slop)** by Hardik Pandya (MIT License), re-scoped for academic writing.

## License

MIT License · Created by **Diar Azari** · [linkedin.com/in/diarazari](https://www.linkedin.com/in/diarazari/) · 2026
