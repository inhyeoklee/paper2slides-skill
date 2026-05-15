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

The `paper2slides` library must be installed. If the library source is available locally:

```bash
cd <path_to_paper2slides_library> && pip install -e .
```

Otherwise install from the packaged distribution:
```bash
pip install paper2slides
```

Required Python packages (auto-installed): `pymupdf`, `pillow`, `numpy`, `jinja2`, `click`

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
- `<output_dir>/assets/css/style.css` — slate + accented theme with expanded font choices, high-contrast body text, per-aim color tokens, feature-family badge colors, and ready-made component classes for aim-flow / info-row-3 / taxonomy-grid / compare-grid / criteria-grid / badges / schematics

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

**Two-column text + figure slide (most common layout):**
```html
<section>
    <h2>Slide Title</h2>
    <div class="two-col-layout">
        <div class="col-text" style="font-size: 0.8em;">
            <ul>
                <li><strong>Point 1:</strong> Explanation</li>
                <li><strong>Point 2:</strong> Explanation</li>
            </ul>
        </div>
        <div class="col-img">
            <div class="figure-frame" data-fig="fig2a">
                <img src="assets/img/panels/fig2a.png" alt="Description">
            </div>
            <div class="figure-caption">Figure 2A: Caption</div>
        </div>
    </div>
    <aside class="notes">Speaker notes.</aside>
</section>
```

**Math/equation slide (uses MathJax3 plugin):**
```html
<section>
    <h2>Slide Title</h2>
    <div class="math-block">
        $$
        \Delta G = -RT \ln K
        $$
    </div>
    <ul style="font-size: 0.78em; line-height: 1.7;">
        <li><strong>\(\Delta G\):</strong> Free energy change</li>
    </ul>
    <aside class="notes">Walk through the equation step by step.</aside>
</section>
```

**Plain-English framing cards** — for section openers and proposal-style aims. Use these to lead with the "why", then state hypothesis, what the section enables, and limitations.
```html
<section class="section-slide aim-1-section">
    <h1><span class="aim-number aim1-text">Aim 1:</span> Short aim title</h1>
    <p>Goal: plain-English reason this aim matters.</p>
    <div class="why-strip">
        <div class="why-card fragment fade-in"><div class="why-kicker">Why it matters</div><p>Clinical or scientific motivation.</p></div>
        <div class="why-card fragment fade-in"><div class="why-kicker">Hypothesis</div><p>Plain-English hypothesis.</p></div>
        <div class="why-card fragment fade-in"><div class="why-kicker">Enables</div><p>What the result unlocks.</p></div>
        <div class="why-card fragment fade-in"><div class="why-kicker">Limitation</div><p>Scope boundary.</p></div>
    </div>
    <aside class="notes">Lead with the goal; click through why, hypothesis, enables, and limitation.</aside>
</section>
```

**Method/tradeoff cards** — for algorithm menus, interpretation panels, or hypothesis-generation versus validation distinctions.
```html
<div class="method-menu">
    <div class="method-card fragment fade-in">
        <h3>Hypotheses</h3>
        <p>Use interpretation tools to nominate candidate features.</p>
    </div>
    <div class="method-card fragment fade-in">
        <h3>Validation</h3>
        <p>Test candidates against held-out data and prespecified controls.</p>
    </div>
</div>
```

**Feature-family pipeline card** — use `.feature-family-step` when a pipeline step contains long badges. Badges wrap inside the card and inherit distinct feature-family colors.
```html
<div class="pipeline-step step-1 feature-family-step">
    <div class="pipe-num">Step 1</div>
    <div class="pipe-title">Four feature families</div>
    <div class="pipe-body">
        <span class="badge physiology">Routine physiology</span>
        <span class="badge process">Routine workflow</span>
        <span class="badge mixed">Intentional measurements/interventions</span>
        <span class="badge intentional-workflow">Intentional workflow</span>
    </div>
</div>
```

**Expected outcomes table** — add `expected-outcomes-table` to the table and aim row classes for colored summaries.
```html
<table class="expected-outcomes-table">
    <tbody>
        <tr class="aim1-row"><td><strong>1.</strong> Input representation</td><td>Outcome text.</td></tr>
        <tr class="aim2-row"><td><strong>2.</strong> Signal source</td><td>Outcome text.</td></tr>
        <tr class="aim3-row"><td><strong>3.</strong> Latent interventions</td><td>Outcome text.</td></tr>
    </tbody>
</table>
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

**Hidden/backup slide (for Q&A appendix):**
```html
<section data-visibility="hidden">
    <h2>Backup: Detail Slide</h2>
    <p>This slide is hidden from navigation but can be jumped to during Q&amp;A.</p>
    <aside class="notes">Backup content for anticipated questions.</aside>
</section>
```

#### Component Classes (Already Styled in style.css)

The theme ships with ready-made component classes. Use them instead of inventing inline-styled `<div>`s, so the deck stays visually coherent and accessible.

**Aim flow card row** — for outline / expected-outcomes overviews. Three colored cards (`aim-1`, `aim-2`, `aim-3`) with optional `aim-arrow` separators.
```html
<div class="aim-flow">
    <div class="aim-card aim-1">
        <div class="aim-num">Aim 1</div>
        <div class="aim-title">Short headline</div>
        <div class="aim-status">Status / one-liner</div>
    </div>
    <div class="aim-arrow">→</div>
    <div class="aim-card aim-2">…</div>
    <div class="aim-arrow">→</div>
    <div class="aim-card aim-3">…</div>
</div>
```

**Three-column info row** — three side-by-side colored cards for "use cases", "options", "tradeoffs". Each `info-card` has a colored left border.
```html
<div class="info-row-3">
    <div class="info-card"><div class="info-title">Title</div>Body text…</div>
    <div class="info-card">…</div>
    <div class="info-card">…</div>
</div>
```

**Critique vs counter-evidence compare grid** — two opposing panels with a center arrow. `compare-panel.before` is amber, `compare-panel.after` is indigo.
```html
<div class="compare-grid">
    <div class="compare-panel before">
        <div class="cmp-title">Critique</div>
        <ul>…</ul>
    </div>
    <div class="compare-arrow">⇋</div>
    <div class="compare-panel after">
        <div class="cmp-title">Counter-evidence</div>
        <ul>…</ul>
    </div>
</div>
```

**Taxonomy grid** — three categorical columns with distinct colors. Pre-defined modifiers `physiology` (emerald), `process` (amber), `mixed` (slate).
```html
<div class="taxonomy-grid">
    <div class="taxonomy-card physiology"><div class="tax-title">Physiology</div><div class="tax-body">…</div></div>
    <div class="taxonomy-card process"><div class="tax-title">Process</div><div class="tax-body">…</div></div>
    <div class="taxonomy-card mixed"><div class="tax-title">Mixed</div><div class="tax-body">…</div></div>
</div>
```

**Decision-criteria grid** — numbered acceptance criteria as 2×2 cards with circular numbers.
```html
<div class="criteria-grid">
    <div class="criterion">
        <span class="cri-num">1</span><span class="cri-title">Threshold</span><br>
        Body text describing the criterion.
    </div>
    <!-- repeat for criteria 2–4 -->
</div>
```

**Inline badges** — pill labels for inline aim/category tags. Modifiers: `aim1`/`aim2`/`aim3`, `physiology`/`process`/`mixed`.
```html
<span class="badge aim2">Aim 2</span>
<span class="badge physiology">Physiology</span>
```

**Callout** — light indigo block with an accent left bar; use for the headline framing on a slide.
```html
<div class="callout">The single thing the audience should remember from this slide.</div>
```

**Schematic** — bordered container that holds an inline `<svg>` diagram (pipeline, study-design flow). The CSS auto-fits the SVG to slide width.
```html
<div class="schematic">
    <svg viewBox="0 0 1100 320" xmlns="http://www.w3.org/2000/svg">…</svg>
</div>
```

**Per-aim color tokens** — when you need a custom inline element, reach for the CSS variables instead of hex codes: `var(--aim1)`, `var(--aim2)`, `var(--aim3)`, `var(--physiology)`, `var(--process)`, `var(--mixed)`, `var(--accent)`, `var(--muted)`.

#### Click-by-click reveal cadence

Every bullet that the presenter wants to reveal on its own click should carry `class="fragment fade-in"`. The matching `<aside class="notes">` (and the slide's block in `speaker_notes.html`) should use explicit `CLICK` markers between segments so the speaker view tells the presenter exactly what to say between clicks:

```html
<ul>
    <li class="fragment fade-in">First point.</li>
    <li class="fragment fade-in">Second point.</li>
    <li class="fragment fade-in">Third point.</li>
</ul>
<aside class="notes">
    Open with the framing sentence.<br>
    (Click) item 1 — read the headline number.<br>
    (Click) item 2 — extend with the specific finding.<br>
    (Click) item 3 — link back to the aim.<br>
    Transition: "this is exactly what comes next."
</aside>
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

### Phase 5: Create Speaker Notes

Write a `speaker_notes.html` file using the template in `resources/speaker_notes_template.html`. The HTML notes page should be the primary rehearsal artifact, not a dumping ground. It should include:
- **Top navigation and sidebar** — direct links to the talk script, slide cards, backup slides, quick reference, Q&A, and pronunciation guide.
- **Standalone talk script** — complete, natural spoken prose for every slide. The presenter should be able to rehearse from this section without looking at the slides.
- **Click markers** — use `<span class="click">CLICK</span>` exactly where the matching deck fragment appears.
- **Slide cards** — collapsible per-slide reference cards containing what's on screen, why it matters, what to say, and deeper technical or citation details.
- **Backup-slide section** — Q&A-only hidden-slide material, using the same slide-card pattern.
- **Quick reference card** — consolidated table of key results/statistics.
- **Anticipated Q&A** — question blocks with direct answers and slide references.
- **Pronunciation guide** — names, terms, symbols, and acronyms.

Write notes in **natural speech** — as if coaching a nervous presenter.

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
- 1280×720 (16:9 widescreen)
- RevealNotes plugin for speaker view
- MathJax3 for display and inline equations (`$$...$$` and `\(...\)`)
- Settings panel (theme, font, font scale, fig scale, transition, progress, controls)
- Custom overview (`O` / `Esc`) with main slides and hidden backup slides
- Presenter window from the Fullscreen button with current notes and next-click preview
- Editable slide text with browser autosave, reset, and "Download edited deck"
- Interactive figure controls (zoom, pan, reset, and centered lightbox)

Figure behavior in the shell:
- Single-click a figure to open a centered, enlarged lightbox.
- Click outside the enlarged figure, click the close button, or press `Escape` to return to the slide.
- The toolbar still supports explicit zoom, pan, reset, and expand controls.

Available font choices in the settings panel:
Montserrat, Source Sans 3, Inter, Fira Sans, Lato, Open Sans, Roboto, Nunito Sans, Work Sans, IBM Plex Sans, Noto Sans, Crimson Pro, and system UI fonts.

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
- [ ] **Presenter view** — use Fullscreen button; verify next-click preview and notes update
- [ ] **Overview** — press `O` or `Esc`; verify hidden backup slides are separated from main slides
- [ ] **Edit/download** — test slide edit mode, autosave, reset, and `index_edited.html` download
- [ ] **MathJax** — all equations render in the deck, presenter window, and speaker notes page
- [ ] **No text overflow** — bullet points and titles fit within the slide
- [ ] **16:9 aspect ratio** — verify slide dimensions are 1280×720

---

## Tips

- **Less is more.** A 20-slide curated deck is better than a 50-slide figure dump. Pick the figures that tell the story.
- **One idea per slide.** Don't overload slides with multiple unrelated panels.
- **Two-column layout is your friend.** The `two-col-layout` pattern (text left, figure right) is the most used layout in practice.
- **Use section breaks.** When transitioning between major topics (e.g., "Validation" → "Application"), use a `section-slide` with just a title.
- **Use hidden slides for backup.** Add `data-visibility="hidden"` to slides with extra detail — they won't show during the talk but can be jumped to during Q&A.
- **Write notes for a nervous presenter.** Include exact numbers, pronunciations of tricky terms, and suggested emphasis points.
- **Pair structure + data.** Whenever possible, show a structural figure alongside quantitative data on the same slide (using `figure-row` or `two-col-layout`).
