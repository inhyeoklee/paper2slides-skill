#!/usr/bin/env python3
"""
paper2slides CLI — PDF → Journal Club Reveal.js Presentation

Single-command pipeline that extracts figures from a scientific paper PDF,
segments them into individual panels, and generates a complete Reveal.js
presentation with Beamer Metropolis styling and interactive figure controls.

Usage:
    paper2slides paper.pdf --output ./presentation
    paper2slides paper.pdf -o ./presentation --serve
"""

import os

import click

from paper2slides import __version__
from paper2slides.extractor import extract
from paper2slides.segmenter import segment_all
from paper2slides.generator import render
from paper2slides.server import serve as start_server


@click.command()
@click.argument("pdf_path", type=click.Path(exists=True))
@click.option(
    "--output", "-o",
    default="./presentation",
    help="Output directory (default: ./presentation)",
)
@click.option("--title", "-t", default=None, help="Presentation title (auto-detected from PDF if omitted)")
@click.option("--upscale", "-u", default=1, type=int, help="Panel upscale factor (default: 1, extraction is already 4x)")
@click.option("--min-gap", default=10, type=int, help="Minimum whitespace gap for panel detection (default: 10px)")
@click.option("--serve", is_flag=True, help="Start local dev server after generation")
@click.option("--port", default=8000, type=int, help="Dev server port (default: 8000)")
@click.version_option(version=__version__, prog_name="paper2slides")
def main(pdf_path: str, output: str, title: str, upscale: int, min_gap: int, serve: bool, port: int) -> None:
    """Generate a journal club presentation from a scientific paper PDF."""
    click.echo(f"\n{'=' * 60}")
    click.echo("  paper2slides — PDF → Presentation Pipeline")
    click.echo(f"{'=' * 60}\n")

    # Step 1: Extract
    click.echo(f"[1/3] Extracting from: {pdf_path}")
    paper = extract(pdf_path)
    display_title = (paper.title[:60] + "...") if len(paper.title) > 60 else paper.title
    click.echo(f"  Title: {display_title}")
    click.echo(f"  Pages: {len(paper.text_by_page)}")
    click.echo(f"  Figures found: {len(paper.figures)}")

    if not paper.figures:
        click.echo("\n  Warning: No figure images found in the PDF.")
        click.echo("  The PDF may use vector graphics or the figures may be too small.")
        click.echo("  Try adjusting extraction parameters.\n")

    # Step 2: Segment panels
    click.echo("\n[2/3] Segmenting panels...")
    panels_dir = os.path.join(output, "assets", "img", "panels")
    panels = segment_all(paper.figures, panels_dir, upscale=upscale, min_gap=min_gap)
    click.echo(f"  Total panels: {len(panels)}")

    # Step 3: Generate presentation
    click.echo("\n[3/3] Generating presentation...")
    index_path = render(paper, panels, output, title=title)

    click.echo(f"\n{'=' * 60}")
    click.echo(f"  Done! Presentation generated at: {output}/")
    click.echo(f"  Open: {index_path}")
    click.echo(f"{'=' * 60}\n")

    # Optionally serve
    if serve:
        start_server(output, port)
