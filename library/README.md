# paper2slides

**PDF → Journal Club Reveal.js Presentation**

Extract figures from scientific papers, segment them into individual panels, and generate interactive Reveal.js presentations with the paper2slides slate + indigo theme — all in one command.

## Features

- **Automatic figure extraction** — Pulls embedded images from PDF using PyMuPDF
- **Panel segmentation** — Projection profile analysis splits composite figures into individual panels (A, B, C, …)
- **Slate + accented theme** — Clean academic styling with high-contrast text, Montserrat/Source Sans defaults, and blue/fuchsia/emerald aim accents
- **Component vocabulary** — Ready-made `aim-flow`, `info-row-3`, `why-strip`, `method-menu`, `taxonomy-grid`, `compare-grid`, `criteria-grid`, `badge`, `callout`, `schematic`, `feature-family-step`, and `expected-outcomes-table` classes for rich slides
- **16:9 PowerPoint ratio** — Standard widescreen (1280×720) matching PowerPoint/Keynote
- **Interactive figure controls** — Toolbar zoom/pan/reset, scroll-wheel zoom, drag, and single-click centered lightbox; click outside the enlarged figure or press `Escape` to close
- **Dark/Light theme** — Toggle via settings panel
- **Per-figure state persistence** — Zoom/pan state saved to localStorage
- **Presenter and overview views** — Custom overview for main/backup slides; presenter window with current notes and next-click preview
- **Editable slides** — Browser autosave, reset, and downloadable edited HTML
- **MathJax support** — Display and inline equations in the deck and presenter view
- **Settings panel** — Theme, font, size, figure scale, transitions, progress bar, controls
- **Expanded font set** — Montserrat, Source Sans 3, Inter, Fira Sans, Lato, Open Sans, Roboto, Nunito Sans, Work Sans, IBM Plex Sans, Noto Sans, Crimson Pro, and system UI fonts
- **Reusable color utilities** — Per-aim section gradients, wrapped feature-family badges, and colored expected-outcomes rows

## Installation

```bash
pip install .
```

Or in editable/development mode:

```bash
pip install -e .
```

## Quick Start

```bash
# Generate presentation from a paper PDF
paper2slides paper.pdf -o ./my_presentation

# Generate and serve locally
paper2slides paper.pdf -o ./my_presentation --serve

# Custom options
paper2slides paper.pdf -o ./slides --upscale 2 --min-gap 12 --port 3000
```

Or via Python module:

```bash
python -m paper2slides paper.pdf -o ./my_presentation
```

## CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--output, -o` | `./presentation` | Output directory |
| `--title, -t` | Auto-detected | Presentation title |
| `--upscale, -u` | `4` | Panel upscale factor (Lanczos) |
| `--min-gap` | `8` | Min whitespace gap for panel detection (px) |
| `--serve` | Off | Start local dev server after generation |
| `--port` | `8000` | Dev server port |
| `--version` | — | Show version |

## Output Structure

```
my_presentation/
├── index.html              # Reveal.js presentation (16:9)
├── assets/
│   ├── css/style.css       # paper2slides slate + indigo theme
│   └── img/panels/         # Extracted panel images
│       ├── fig1a.png
│       ├── fig1b.png
│       └── ...
```

## Deck Template Details

Generated decks inherit the shared Reveal.js shell in `src/paper2slides/templates/base.html` and theme CSS in `src/paper2slides/templates/slides.css`.

- The settings panel exposes the full font set and defaults to Montserrat.
- Any `.figure-frame[data-fig]` opens an enlarged centered lightbox on single click. The toolbar still supports zoom, pan, reset, and explicit expand controls.
- Long badges inside `.pipeline-step` wrap safely. Add `.feature-family-step` to a pipeline card to apply the multi-accent feature-family treatment.
- Add `class="expected-outcomes-table"` to a table and `aim1-row`, `aim2-row`, or `aim3-row` to body rows for colored expected-outcome summaries.

## Python API

```python
from paper2slides import extract, segment_all

# Extract figures from PDF
paper = extract("paper.pdf")
print(f"Found {len(paper.figures)} figures")

# Segment into panels
panels = segment_all(paper.figures, "./output/panels", upscale=4)
print(f"Extracted {len(panels)} panels")
```

## Architecture

```
src/paper2slides/
├── __init__.py         # Public API
├── __main__.py         # python -m paper2slides
├── cli.py              # Click CLI entry point
├── extractor.py        # PDF text + image extraction (PyMuPDF)
├── segmenter.py        # Projection profile panel splitting
├── generator.py        # Jinja2 template → HTML
├── server.py           # Local dev server
└── templates/
    ├── base.html        # Jinja2 Reveal.js template
    └── slides.css       # paper2slides theme CSS
```

## Dependencies

- Python ≥ 3.8
- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF parsing
- [Pillow](https://pillow.readthedocs.io/) — Image manipulation
- [NumPy](https://numpy.org/) — Projection profile computation
- [Jinja2](https://jinja.palletsprojects.com/) — Template rendering
- [Click](https://click.palletsprojects.com/) — CLI framework

## License

MIT
