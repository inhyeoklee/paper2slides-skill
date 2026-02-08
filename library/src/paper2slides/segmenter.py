#!/usr/bin/env python3
"""
Panel segmentation via projection profile analysis.

Takes raw figure images and splits them into individual panels (A, B, C, ...)
by detecting white-space gaps in row/column projections.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import numpy as np
from PIL import Image

from paper2slides.extractor import FigureImage


@dataclass
class Panel:
    """A single panel extracted from a figure."""

    figure_num: int
    panel_label: str  # e.g. "a", "b", "c"
    path: str
    width: int
    height: int


# ---------------------------------------------------------------------------
# Projection profile helpers
# ---------------------------------------------------------------------------


def _to_grayscale_array(img: Image.Image) -> np.ndarray:
    """Convert PIL image to grayscale numpy array."""
    return np.array(img.convert("L"))


def _row_projection(gray: np.ndarray, threshold: int = 240) -> np.ndarray:
    """Count non-white pixels per row."""
    return np.sum(gray < threshold, axis=1)


def _col_projection(gray: np.ndarray, threshold: int = 240) -> np.ndarray:
    """Count non-white pixels per column."""
    return np.sum(gray < threshold, axis=0)


def _find_gaps(
    projection: np.ndarray, min_gap: int = 8, max_content: int = 10
) -> List[Tuple[int, int]]:
    """
    Find contiguous runs where projection[i] <= max_content.

    Returns list of (start, end) tuples for gaps >= min_gap pixels.
    """
    gaps: List[Tuple[int, int]] = []
    in_gap = False
    gap_start = 0

    for i, val in enumerate(projection):
        if val <= max_content:
            if not in_gap:
                in_gap = True
                gap_start = i
        else:
            if in_gap:
                if i - gap_start >= min_gap:
                    gaps.append((gap_start, i))
                in_gap = False

    # Handle trailing gap
    if in_gap and len(projection) - gap_start >= min_gap:
        gaps.append((gap_start, len(projection)))

    return gaps


def _gaps_to_bands(
    gaps: List[Tuple[int, int]], total_size: int, margin: int = 2
) -> List[Tuple[int, int]]:
    """
    Convert gap positions to band (content region) positions.

    Returns list of (start, end) tuples.
    """
    bands: List[Tuple[int, int]] = []
    prev_end = 0

    for gap_start, gap_end in gaps:
        band_start = max(0, prev_end + margin)
        band_end = min(total_size, gap_start - margin)
        if band_end > band_start + 10:  # minimum band size
            bands.append((band_start, band_end))
        prev_end = gap_end

    # Trailing band
    band_start = max(0, prev_end + margin)
    if total_size > band_start + 10:
        bands.append((band_start, total_size))

    return bands


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

_LABELS = "abcdefghijklmnopqrstuvwxyz"


def segment_figure(
    img: Image.Image,
    figure_num: int,
    output_dir: str,
    *,
    upscale: int = 1,
    min_gap: int = 10,
    threshold: int = 245,
    pad: int = 2,
) -> List[Panel]:
    """
    Segment a single figure image into panels using projection profiling.

    Args:
        img: PIL Image of the full figure.
        figure_num: Figure number (1-indexed).
        output_dir: Directory to save panel images.
        upscale: Upscale factor for output images (default 4×).
        min_gap: Minimum gap width in pixels to count as panel separator.
        threshold: Grayscale threshold for "white" pixels (0-255).
        pad: Padding around each crop in native pixels.

    Returns:
        List of Panel instances.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    gray = _to_grayscale_array(img)
    h, w = gray.shape

    # Find horizontal bands (rows of panels)
    row_proj = _row_projection(gray, threshold)
    h_gaps = _find_gaps(row_proj, min_gap=min_gap)
    h_bands = _gaps_to_bands(h_gaps, h)

    if not h_bands:
        h_bands = [(0, h)]

    panels: List[Panel] = []
    label_idx = 0

    for band_y0, band_y1 in h_bands:
        # Extract band and find vertical gaps within it
        band_gray = gray[band_y0:band_y1, :]
        col_proj = _col_projection(band_gray, threshold)
        v_gaps = _find_gaps(col_proj, min_gap=min_gap)
        v_bands = _gaps_to_bands(v_gaps, w)

        if not v_bands:
            v_bands = [(0, w)]

        for band_x0, band_x1 in v_bands:
            # Apply padding
            x0 = max(0, band_x0 - pad)
            y0 = max(0, band_y0 - pad)
            x1 = min(w, band_x1 + pad)
            y1 = min(h, band_y1 + pad)

            # Crop from original image
            panel_img = img.crop((x0, y0, x1, y1))

            # Skip artifacts (too small or narrow strips like Fig 1A error)
            if panel_img.width < 100 or panel_img.height < 100:
                # If it's a very skinny strip, ignore it.
                if panel_img.width < 50 or panel_img.height < 50:
                    continue

            # Upscale with Lanczos
            if upscale > 1:
                new_w = panel_img.width * upscale
                new_h = panel_img.height * upscale
                panel_img = panel_img.resize((new_w, new_h), Image.LANCZOS)

            # Save
            label = _LABELS[label_idx] if label_idx < len(_LABELS) else str(label_idx)
            filename = f"fig{figure_num}{label}.png"
            filepath = out / filename
            panel_img.save(str(filepath), "PNG")

            panels.append(
                Panel(
                    figure_num=figure_num,
                    panel_label=label,
                    path=str(filepath),
                    width=panel_img.width,
                    height=panel_img.height,
                )
            )
            label_idx += 1

    return panels


def segment_all(
    figure_images: List[FigureImage],
    output_dir: str,
    *,
    upscale: int = 4,
    min_gap: int = 8,
) -> List[Panel]:
    """
    Segment all extracted figure images into panels.

    Args:
        figure_images: List of FigureImage objects from extractor.
        output_dir: Directory to save panel images.
        upscale: Upscale factor.
        min_gap: Minimum gap width for panel detection.

    Returns:
        Flat list of all Panel objects across all figures.
    """
    import click

    all_panels: List[Panel] = []

    for i, fig in enumerate(figure_images, 1):
        img = fig.to_pil()
        if img.mode != "RGB":
            img = img.convert("RGB")

        panels = segment_figure(img, i, output_dir, upscale=upscale, min_gap=min_gap)
        all_panels.extend(panels)
        click.echo(f"  Figure {i}: {len(panels)} panels extracted")

    return all_panels
