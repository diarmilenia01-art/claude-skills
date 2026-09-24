# Citation styles quick reference

Generate from the paper's metadata (authors, year, title, journal, volume, issue,
pages, DOI/URL). Ask the user which style if not already known. When a field is
missing, leave a clear `[?]` placeholder rather than inventing it.

## APA (7th)

Author, A. A., & Author, B. B. (Year). Title of the article. *Journal Name,
Volume*(Issue), pages. https://doi.org/xxxx

> Santoso, B., & Pratama, A. (2024). Pengaruh pembelajaran daring terhadap hasil
> belajar. *Jurnal Pendidikan Terapan, 12*(3), 45–58. https://doi.org/10.xxxx

## IEEE

[n] A. A. Author and B. B. Author, "Title of the article," *Journal Name*, vol. X,
no. Y, pp. zz–zz, Year, doi: xxxx.

> [1] B. Santoso and A. Pratama, "Pengaruh pembelajaran daring terhadap hasil
> belajar," *J. Pendidikan Terapan*, vol. 12, no. 3, pp. 45–58, 2024.

## Vancouver

n. Author AA, Author BB. Title of the article. Journal Name. Year;Volume(Issue):
pages.

> 1. Santoso B, Pratama A. Pengaruh pembelajaran daring terhadap hasil belajar.
> J Pendidikan Terapan. 2024;12(3):45–58.

## Rules

- Never fabricate a DOI, page range, or author. Missing field -> `[?]`.
- Match the user's requested style exactly; if none given, default to APA and say so.
- Keep author names and years verifiable against the source; the reader must be able
  to trace every citation back to the original.
