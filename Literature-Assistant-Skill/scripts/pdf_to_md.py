#!/usr/bin/env python3
# Literature Assistant — PDF to Markdown converter
# Created by Diar Azari | https://www.linkedin.com/in/diarazari/ | 2026 | MIT License
"""
Convert a journal PDF to clean Markdown ONCE, so the rest of the conversation
works from compact text instead of re-reading the PDF (token-efficient). The
output MD keeps a metadata header with the ORIGINAL source link, so the citation
trail is never lost.

Headings and tables are preserved (via pymupdf4llm); scanned PDFs fall back to
OCR automatically. This script only converts a local PDF — finding/downloading
the paper (open-access only) is done by Claude around it.

Usage:
  python pdf_to_md.py --input paper.pdf --output paper.md \
      --source "https://open-access.example/paper.pdf" [--title "Paper title"]
"""
import argparse, datetime, os, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="path to a local PDF")
    ap.add_argument("--output", required=True, help="path to write the .md")
    ap.add_argument("--source", default="", help="ORIGINAL source URL (for the citation trail)")
    ap.add_argument("--title", default="", help="paper title (optional; detected if omitted)")
    a = ap.parse_args()

    if not os.path.exists(a.input):
        sys.exit(f"Input not found: {a.input}")
    try:
        import pymupdf4llm
    except ImportError:
        sys.exit("Missing dependency. Run: pip install pymupdf4llm")

    md = pymupdf4llm.to_markdown(a.input)

    title = a.title
    if not title:  # first ATX heading, if any
        for line in md.splitlines():
            if line.startswith("# "):
                title = line[2:].strip(); break
        title = title or os.path.splitext(os.path.basename(a.input))[0]

    header = (
        "---\n"
        f'title: "{title.replace(chr(34), chr(39))}"\n'
        f'source_url: "{a.source}"\n'
        f"converted: {datetime.date.today().isoformat()}\n"
        "note: Converted from PDF for token-efficient reading. Cite the original source_url.\n"
        "---\n\n"
    )
    with open(a.output, "w", encoding="utf-8") as f:
        f.write(header + md)

    chars = len(md)
    print(f"Converted -> {a.output}")
    print(f"Markdown length: {chars:,} chars (~{round(chars/4):,} tokens)")
    if not a.source:
        print("WARNING: no --source given. Add the original link so the citation trail is kept.")

if __name__ == "__main__":
    main()
