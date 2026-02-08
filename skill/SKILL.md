---
name: paper2slides
description: Generate a show-ready journal club presentation from a scientific paper PDF using the paper2slides library and agent-driven scientific comprehension.
---

# paper2slides — Agent-Driven Journal Club Presentations

## Overview

This skill transforms a scientific paper PDF into a **show-ready, curated Reveal.js presentation** with speaker notes. It combines two layers:

1. **Mechanical layer** — the `paper2slides` Python library extracts figures, segments panels, and scaffolds a raw Reveal.js deck.
2. **Intelligence layer** — **you, the agent**, read the paper, understand the science, curate the slide deck, write titles/captions, and compose speaker notes.

The mechanical extraction alone produces a figure dump. The agent's job is to turn that into a coherent, PhD-level journal club talk.

---

## Prerequisites

The `paper2slides` library must be installed. It lives at:

```
~/Desktop/Journal_Club_Presentation/paper2slides_lib/
```

If not already installed, run:
```bash
cd ~/Desktop/Journal_Club_Presentation/paper2slides_lib && pip install -e .
```

Required Python packages: `pymupdf`, `pillow`, `numpy`, `jinja2`, `click`

---

## Workflow (5 Phases)

### Phase 1: Extract & Segment (Mechanical)

Run the `paper2slides` CLI to extract figures and segment panels:

```bash
paper2slides "<path/to/paper.pdf>" -o "<output_dir>"
```

This produces:
- `<output_dir>/assets/img/panels/fig1a.png, fig1b.png, ...` — individual panel images
- `<output_dir>/index.html` — a raw, uncurated Reveal.js deck (figure dump)
- `<output_dir>/assets/css/style.css` — Beamer Metropolis-inspired CSS

**Verify:** Check the terminal output for the number of figures and panels extracted. If zero figures found, the PDF may use vector graphics — consider alternatives like screenshots.

### Phase 2: Read & Comprehend the Paper

Use PyMuPDF to extract and read the paper text programmatically:

```python
import fitz
doc = fitz.open("<path/to/paper.pdf>")
for i in range(len(doc)):
    page = doc[i]
    text = page.get_text('text')
    print(f'=== PAGE {i+1} ===')
    print(text)
doc.close()
```

As you read, identify:
- **Title, authors, journal, year** — for the title slide
- **Core hypothesis/question** — what problem does the paper solve?
- **Method/approach** — what's the key technique or innovation?
- **Key results** — which figures tell the most important story?
- **Validation/proof** — structural, functional, or statistical evidence
- **Applications** — practical implications
- **Limitations & future directions** — for the discussion slide

### Phase 3: Inspect Extracted Panels

Open the extracted panel images in the browser to understand what each one contains:

```
file://<output_dir>/assets/img/panels/
```

For each figure number, identify:
- Which panels show **structural data** (protein structures, cryo-EM, etc.)
- Which show **quantitative data** (bar charts, scatter plots, correlations)
- Which show **qualitative data** (gels, blots, microscopy)
- Which panels are **most important** for the narrative

Create a mental mapping: `figNx.png` → "what this panel shows" → "which slide it belongs on"

### Phase 4: Build the Curated Presentation

Create a new `index.html` in a `show_ready/` subdirectory using the reference template structure below. The presentation should follow this structure:

#### Slide Structure (15–25 slides for a typical paper)

| Slide Type | Count | Purpose |
|-----------|-------|---------|
| Title | 1 | Paper title, authors, journal, date |
| Outline | 1 | Numbered list of talk sections |
| Background | 1–3 | Context, prior work, the problem |
| Method | 1–2 | Key innovation / workflow |
| Validation | 3–6 | Core results with figures |
| Application | 2–4 | Deep dive into the primary application |
| Quantitative | 1–2 | Correlations, statistics, benchmarking |
| Takeaways | 1 | Bullet-point summary |
| Discussion | 1 | Limitations, future directions, discussion Qs |
| Thank You | 1 | Close + references/code links |

#### HTML Patterns

**Single figure slide:**
```html
<section>
    <h2>Slide Title</h2>
    <div class="figure-frame" data-fig="fig2a">
        <img src="assets/img/panels/fig2a.png" alt="Description">
    </div>
    <div class="figure-caption">Figure 2A: Brief caption</div>
    <aside class="notes">
        Speaker notes go here. Write 3-6 sentences explaining what the figure shows,
        why it matters, and what to emphasize to the audience.
    </aside>
</section>
```

**Two-figure comparison slide:**
```html
<section>
    <h2>Slide Title</h2>
    <div class="figure-row">
        <div>
            <div class="figure-frame" data-fig="fig3a">
                <img src="assets/img/panels/fig3a.png" alt="Description">
            </div>
            <div class="figure-caption">3A: Sub-caption</div>
        </div>
        <div>
            <div class="figure-frame" data-fig="fig3b">
                <img src="assets/img/panels/fig3b.png" alt="Description">
            </div>
            <div class="figure-caption">3B: Sub-caption</div>
        </div>
    </div>
    <aside class="notes">Speaker notes here.</aside>
</section>
```

**Section break slide:**
```html
<section class="section-slide">
    <h1>Section Title</h1>
    <p>Brief subtitle</p>
    <aside class="notes">Transition notes.</aside>
</section>
```

**Text-only slide (takeaways, discussion):**
```html
<section>
    <h2>Key Takeaways</h2>
    <ul style="font-size: 0.78em; line-height: 1.7;">
        <li><strong>Point 1</strong> — explanation</li>
        <li><strong>Point 2</strong> — explanation</li>
    </ul>
    <aside class="notes">Speaker notes.</aside>
</section>
```

#### Speaker Notes Guidelines

Each `<aside class="notes">` block should contain:

1. **What the figure shows** — describe the data, axes, conditions
2. **Key result** — the punchline of this slide
3. **Context** — why this matters in the paper's narrative
4. **Transition** — optional lead-in to the next slide

Write notes in **natural speech** — as if coaching the presenter. Use concrete numbers and names.

**Good example:**
> "This scatter plot shows CB bias scores on the x-axis versus SAXS-measured percent open conformation on the y-axis. The Spearman correlation is 0.81 — very strong. Open-biased variants cluster in the upper right, while closed-biased cluster lower left. What's remarkable is that CB uses only static backbone structures..."

**Bad example (too vague):**
> "This figure shows the correlation is good."

### Phase 5: Create Standalone Speaker Notes

Write a `speaker_notes.md` file with:
- Per-slide talking points (use `## Slide N — Title` headers)
- Detailed explanations with key numbers and terminology
- 3–5 discussion questions at the end
- An appendix table summarizing all datasets/results

---

## Reference Template

Copy the CSS and JS infrastructure from the existing presentation:

```bash
mkdir -p <output>/show_ready/assets/{css,img/panels}
cp <output>/assets/css/style.css <output>/show_ready/assets/css/
cp <output>/assets/img/panels/*.png <output>/show_ready/assets/img/panels/
```

Use this HTML shell (found in `resources/template_shell.html` in this skill folder):

- Reveal.js 5.0.4 CDN
- 960×540 (16:9 widescreen)
- RevealNotes plugin for speaker view
- Settings panel (theme, font, fig scale)
- Interactive figure controls (zoom, pan, lightbox)

---

## Quality Checklist

Before delivering the final presentation, verify:

- [ ] **Narrative flow** — slides tell a coherent story from background to conclusions
- [ ] **Figure selection** — only the most impactful panels are used (not every panel)
- [ ] **Captions** — every figure has a brief, informative caption
- [ ] **Speaker notes** — every slide has 3+ sentences of notes
- [ ] **Discussion questions** — 3–5 thoughtful questions included
- [ ] **Browser test** — open in browser, navigate all slides, check images load
- [ ] **Speaker view** — press S to verify notes appear correctly
- [ ] **No text overflow** — bullet points and titles fit within the slide
- [ ] **16:9 aspect ratio** — verify slide dimensions are 960×540

---

## Tips

- **Less is more.** A 20-slide curated deck is better than a 50-slide figure dump. Pick the figures that tell the story.
- **One idea per slide.** Don't overload slides with multiple unrelated panels.
- **Use section breaks.** When transitioning between major topics (e.g., "Validation" → "Application"), use a `section-slide` with just a title.
- **Write notes for a nervous presenter.** Include exact numbers, pronunciations of tricky terms, and suggested emphasis points.
- **Pair structure + data.** Whenever possible, show a structural figure alongside quantitative data on the same slide (using `figure-row`).
