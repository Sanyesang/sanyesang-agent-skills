---
name: chinese-mobile-pdf-qa
description: Create or inspect Chinese PDFs intended for phone reading, especially text extracted from ordered screenshots, essays, resumes or booklets. Check semantic order, readable typography, font embedding, Unicode extraction and rendered pages. 中文手机阅读 PDF 验收。
---

# Chinese mobile PDF QA

## Establish the text

Confirm the intended source order before extraction. User-specified numbering wins over attachment arrival order; if numbering is unavailable or contradictory, ask for the first page rather than guess. Extract actual text, not a montage of screenshots unless that is requested.

Separate transcription from editorial rewriting. Preserve author's attribution, dates, headings, quotations and meaningful color distinctions. Correct OCR errors against the image; uncertain characters remain flagged. Assertions in the article stay attributed to its author, not converted to your verified claims.

## Design for the target

Choose a narrow, single-column page proportion for phone reading. Start with a generous body size and line spacing, short lines, clear paragraph breaks and consistent running navigation. A point-size number alone cannot guarantee phone readability: inspect the page at an approximate phone viewport with realistic fit-to-width.

Avoid tiny footnotes, long unbroken URLs and cramped justified spacing. Split at semantic boundaries; do not squeeze a paragraph to force a page count. If the user wants a PDF, do not substitute a PPT.

## Structural and visual checks

Use `scripts/check_pdf.py` for a read-only structural report. It requires `pypdf`. Treat font and ToUnicode warnings as investigation leads, not automatic proof of failure.

Render the actual final PDF with an available renderer. Inspect the first page, representative middle pages, final page and every layout variation. For short documents inspect all pages. Verify:

- source order, complete paragraphs and no duplicated/omitted blocks;
- no clipped content, collisions or lonely headings;
- CJK glyphs present, appropriate font embedding and usable text extraction;
- readable body at phone width, not merely at desktop zoom;
- title, attribution, page count and output file match the request.

An image-only PDF will have no selectable text; acknowledge that limitation rather than saying the extraction test passed. Missing ToUnicode may be valid for some encodings, so test actual extracted Chinese.

## Delivery

Provide the actual PDF file and a concise description of what was checked. Keep editable source when requested. If a renderer or reliable OCR is unavailable, preserve the draft and state the unverified part.

Acceptance example: four numbered long screenshots become readable text pages in that exact semantic order, with a title reflecting the contents and verified Chinese copy/search behavior.
