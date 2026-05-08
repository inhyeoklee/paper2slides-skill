# paper2slides

**PDF → Journal Club Reveal.js Presentation**

Extract figures from scientific papers, segment them into individual panels, and generate interactive Reveal.js presentations with the paper2slides slate + indigo theme — all in one command.

## Features

- **Automatic figure extraction** — Pulls embedded images from PDF using PyMuPDF
- **Panel segmentation** — Projection profile analysis splits composite figures into individual panels (A, B, C, …)
- **Slate + indigo theme** — Clean, flat academic styling with Inter typography and high-contrast text (WCAG AAA on body copy)
- **Component vocabulary** — Ready-made `aim-flow`, `info-row-3`, `taxonomy-grid`, `compare-grid`, `criteria-grid`, `badge`, `callout`, and `schematic` classes for rich slides
- **16:9 PowerPoint ratio** — Standard widescreen (960×540) matching PowerPoint/Keynote
- **Interactive figure controls** — Zoom, pan, scroll-wheel zoom, drag, double-click lightbox
- **Dark/Light theme** — Toggle via settings panel
- **Per-figure state persistence** — Zoom/pan state saved to localStorage
- **Settings panel** — Font, size, figure scale, transitions, progress bar

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
