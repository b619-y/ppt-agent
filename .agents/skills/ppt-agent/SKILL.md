---
name: ppt-agent
description: Create or revise scientific PowerPoint presentations using the user's evidence-first slide workflow, citation rules, and Microsoft YaHei style.
---

# PPT Agent

Use this skill when the user asks to create, revise, or continue a scientific PPT using this workflow. Read the repository's [`风格规范.md`](../../../风格规范.md) before drafting. Follow [`AGENTS.md`](../../../AGENTS.md) for project boundaries.

## Workflow

1. Review the supplied papers, reports, data, existing deck, and any reference slide. Identify the audience, purpose, main claim, and evidence available. Do not assume a missing local reference file is accessible; use the written style parameters when it is absent.
2. Outline the presentation's argument before designing slides. Write conclusion-style titles, then 2–3 concise evidence-linked bullets per slide. Keep observed results separate from hypotheses and planned work.
3. Use primary papers or official reports for evidence. Verify year, figure/table number, physical PDF page, and printed page against the source. Never estimate values from plotted pixels or invent missing data. For a redrawn chart, document every value's source and sampling basis.
4. Create the standard two-image conclusion slide with `模板/make_slide.py`; crop original figures with `模板/crop_pdf_figure.py`; redraw simple charts from verified tabular data with `模板/make_bar_chart.py`. Copy and edit the JSON templates in `模板/`. The standard slide script supports two images; use a custom layout for a genuine three-panel evidence page.
5. Save work under `output/<topic>/`: editable `.pptx`, rendered preview images, source notes (`图片来源.md`), configuration JSON, and figure assets. Keep supplied PDFs and raw data under `input/`.
6. Produce one sample slide and show it to the user for style and wording approval before generating the full deck. After approval, finish the deck and visually inspect every slide preview for clipping, overlap, unreadable evidence, citation accuracy, and page numbering.
7. Deliver the PPTX together with previews and source notes. Clearly identify any unsupported claim or source limitation.

## House style

Use a white 16:9 slide with a one-line conclusion title, full-width red rule, 2–3 short bullets, evidence figures, blue Chinese captions, black parenthetical citations, and a gray page number. Mark only key phrases in red. All newly written text—including English and numerals—uses Microsoft YaHei; source-image text retains its original appearance. See `风格规范.md` for exact dimensions, colors, captions, and the full review checklist.
