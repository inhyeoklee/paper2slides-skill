#!/usr/bin/env python3
"""
Slide generator: renders a Reveal.js presentation from extracted paper data.

Uses Jinja2 to fill a template with extracted figures, panels, and metadata.
Copies all required assets (CSS, JS, images) into the output directory.
"""

from __future__ import annotations

import shutil
from importlib import resources
from pathlib import Path
from typing import List, Optional

import click
from jinja2 import Environment, FileSystemLoader

from paper2slides.extractor import Paper
from paper2slides.segmenter import Panel


def _template_dir() -> Path:
    """Resolve the path to the bundled templates directory."""
    # Python 3.9+ files(); fallback for 3.8
    try:
        ref = resources.files("paper2slides") / "templates"
        return Path(str(ref))
    except AttributeError:
        # Python 3.8 compat
        with resources.path("paper2slides", "templates") as p:
            return p


def render(
    paper: Paper,
    panels: List[Panel],
    output_dir: str,
    *,
    title: Optional[str] = None,
) -> str:
    """
    Generate a complete Reveal.js presentation.

    Args:
        paper: Paper dataclass from extractor.
        panels: List of Panel dataclass from segmenter.
        output_dir: Output directory for the presentation.
        title: Override title (auto-detected from paper if None).

    Returns:
        Path to the generated index.html.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    tmpl_dir = _template_dir()
    if not tmpl_dir.exists():
        raise FileNotFoundError(f"Template directory not found: {tmpl_dir}")

    # Group panels by figure number
    panels_by_fig: dict = {}
    for p in panels:
        panels_by_fig.setdefault(p.figure_num, []).append(p)

    # Build template context
    ctx = {
        "title": title or paper.title or "Journal Club Presentation",
        "authors": paper.authors,
        "journal": paper.journal,
        "year": paper.year,
        "doi": paper.doi,
        "figures": panels_by_fig,
        "num_figures": len(panels_by_fig),
        "num_panels": len(panels),
    }

    # Render HTML
    env = Environment(
        loader=FileSystemLoader(str(tmpl_dir)),
        autoescape=False,
    )
    template = env.get_template("base.html")
    html = template.render(**ctx)

    # Write HTML
    index_path = out / "index.html"
    index_path.write_text(html, encoding="utf-8")

    # Copy CSS
    css_dir = out / "assets" / "css"
    css_dir.mkdir(parents=True, exist_ok=True)
    css_src = tmpl_dir / "slides.css"
    if css_src.exists():
        shutil.copy2(str(css_src), str(css_dir / "style.css"))

    # Panel images are already in the right place (output_dir/assets/img/panels/)
    panels_dir = out / "assets" / "img" / "panels"
    if panels_dir.exists():
        count = len(list(panels_dir.glob("*.png")))
        click.echo(f"  {count} panel images in output")
    else:
        click.echo("  Warning: no panel images found in output")

    click.echo(f"  Presentation written to: {index_path}")
    return str(index_path)
