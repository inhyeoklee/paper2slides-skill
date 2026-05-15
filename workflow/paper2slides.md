---
description: Generate a show-ready journal club presentation from a scientific paper PDF
---

# paper2slides Workflow

This workflow uses the `paper2slides` skill. Read the full skill instructions first by viewing `SKILL.md` in the skill directory.

## Steps

### 1. Ensure paper2slides is installed

// turbo
```bash
python -c "import paper2slides; print(f'paper2slides v{paper2slides.__version__} OK')" 2>&1 || pip install paper2slides 2>&1 | tail -5
```

### 2. Run mechanical extraction

```bash
paper2slides "<path/to/paper.pdf>" -o "<output_dir>"
```

Replace `<path/to/paper.pdf>` with the actual PDF path.

### 3. Read and comprehend the paper

Use PyMuPDF to extract text from the PDF. Read all pages. Identify: title, authors, core hypothesis, key figures, validation, applications, and limitations.

### 4. Inspect extracted panels

Open `<output_dir>/index.html` in the browser. Map panel filenames to their scientific content.

### 5. Build the curated presentation

Create `<output_dir>/show_ready/index.html` using the template from `resources/template_shell.html` in the skill directory.

Copy CSS:
// turbo
```bash
mkdir -p <output_dir>/show_ready/assets/{css,img/panels}
cp <output_dir>/assets/css/style.css <output_dir>/show_ready/assets/css/
cp <output_dir>/assets/img/panels/*.png <output_dir>/show_ready/assets/img/panels/
```

Write 15-25 curated slides with embedded `<aside class="notes">` speaker notes.

The show-ready deck should preserve the full runtime shell from `resources/template_shell.html`, including:
- Reveal.js 5.0.4 with RevealNotes and MathJax3.
- The custom two-row overview (`O` or `Esc`) with main slides and hidden backup slides.
- Hidden backup slides marked with `data-visibility="hidden"` and preserved as uncounted overview slides.
- Presenter window launched from **Fullscreen**, showing current notes plus the next click/slide preview.
- Settings panel with theme, font, font scale, figure scale, transition, progress, and controls.
- Editable slide text with browser autosave plus **Download edited deck** and reset controls.
- Interactive figure controls: zoom, pan, reset, and centered lightbox.
- Figure lightbox behavior: single-click opens a centered/enlarged figure; click outside the figure, click the close button, or press `Escape` to return to the slide.
- Expanded font choices in the settings panel: Montserrat, Source Sans 3, Inter, Fira Sans, Lato, Open Sans, Roboto, Nunito Sans, Work Sans, IBM Plex Sans, Noto Sans, Crimson Pro, and system UI fonts.
- Reusable color components: per-aim accents, `feature-family-step` for wrapped multi-color badges, `intentional-workflow` badges, aim-section gradients, and `expected-outcomes-table` row colors.
- MathJax formatting for all equations and inline notation using `\(...\)` and `$$...$$`; avoid raw Unicode math in slide-facing text.

Use shared components from `assets/css/style.css` rather than ad hoc inline styles where possible:
- `.why-strip`, `.why-card`, `.why-kicker` for section-level "why / hypothesis / enables / limitation" cards.
- `.plain-hypothesis` for a single high-signal framing sentence.
- `.method-menu`, `.method-card` for method choices, tradeoffs, or interpretation panels.
- Existing figure, table, badge, taxonomy, compare, criteria, and pipeline classes.
- `.feature-family-step` on pipeline cards that contain long feature-family badges; badges wrap inside the card.
- `.expected-outcomes-table` with `aim1-row`, `aim2-row`, and `aim3-row` for colored expected-outcome summaries.

### 6. Create speaker notes

Write `<output_dir>/show_ready/speaker_notes.html` following the template from `resources/speaker_notes_template.html` in the skill directory. The notes page should include a standalone talk script, collapsible slide cards, backup-slide notes, quick reference table, anticipated Q&A, and pronunciation guide.

The speaker notes page should also preserve:
- MathJax support for equations and inline notation.
- Editable notes mode with browser autosave, **Download edited HTML**, and reset controls.
- Sidebar links that match every main slide and backup slide.
- Exact `CLICK` markers aligned with deck fragments.

### 7. Verify in browser

Open the final presentation and navigate through all slides. Press S to check embedded Reveal speaker notes, then open `speaker_notes.html` separately and verify the sidebar links, collapsible slide cards, click markers, and Q&A sections.

Also verify:
- `O` or `Esc` opens the overview and backup slides are separated from main slides.
- The **Fullscreen** button opens the custom presenter window and shows the next-click preview.
- Slide edit mode can modify text, autosave, download `index_edited.html`, and reset.
- Speaker notes edit mode can modify notes, autosave, download `speaker_notes_edited.html`, and reset.
- MathJax renders in the main deck, speaker notes page, and presenter window.
