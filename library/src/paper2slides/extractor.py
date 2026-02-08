#!/usr/bin/env python3
"""
PDF figure/text extraction using PyMuPDF.

Extracts embedded images (figures) and text blocks from a scientific paper PDF.
Returns a Paper dataclass containing metadata, text content, and raw figure images.
"""

from __future__ import annotations

import io
import re
from dataclasses import dataclass, field
from typing import Dict, List

import fitz  # PyMuPDF
from PIL import Image


@dataclass
class FigureImage:
    """A single embedded image extracted from the PDF."""

    page_index: int
    xref: int
    native_width: int
    native_height: int
    image_bytes: bytes
    page_area_ratio: float  # fraction of page area covered by image

    def to_pil(self) -> Image.Image:
        """Convert raw bytes to a PIL Image."""
        return Image.open(io.BytesIO(self.image_bytes))


@dataclass
class Paper:
    """Parsed scientific paper."""

    title: str = ""
    authors: str = ""
    journal: str = ""
    year: str = ""
    doi: str = ""
    text_by_page: Dict[int, str] = field(default_factory=dict)
    figures: List[FigureImage] = field(default_factory=list)


def extract(pdf_path: str, min_figure_ratio: float = 0.30) -> Paper:
    """
    Extract text, metadata, and figure images from a PDF.

    Args:
        pdf_path: Path to the PDF file.
        min_figure_ratio: Minimum fraction of page area an image must cover
            to be considered a figure (default: 0.30).

    Returns:
        A Paper dataclass with extracted content.
    """
    doc = fitz.open(pdf_path)
    paper = Paper()

    # --- Extract metadata from first page ---
    first_page_text = doc[0].get_text("text")
    lines = [line.strip() for line in first_page_text.split("\n") if line.strip()]

    # Title heuristic: first non-empty line that's long enough
    for line in lines:
        if len(line) > 20 and not line.startswith("http"):
            paper.title = line
            break

    # Try to find DOI
    doi_match = re.search(r"(10\.\d{4,}/[^\s]+)", first_page_text)
    if doi_match:
        paper.doi = doi_match.group(1)

    # --- Extract text from all pages ---
    for page_idx in range(len(doc)):
        page = doc[page_idx]
        paper.text_by_page[page_idx] = page.get_text("text")

    # --- Extract figures ---
    for page_idx in range(len(doc)):
        page = doc[page_idx]
        page_area = page.rect.width * page.rect.height
        
        # Get all image placements on the page
        img_info_list = page.get_image_info(hashes=False)
        if not img_info_list:
            continue

        # Cluster rectangles that are close to each other
        # (This captures multi-part figures as a single unit)
        rects = [fitz.Rect(info["bbox"]) for info in img_info_list]
        clusters: List[fitz.Rect] = []
        
        for r in rects:
            merged = False
            for i, c in enumerate(clusters):
                # If rect is close to an existing cluster, merge it
                # 48pt is about 2/3 inch, typical gap between distant figures
                if r.distance_to(c) < 60:
                    clusters[i] = c | r # Union
                    merged = True
                    break
            if not merged:
                clusters.append(r)

        # Process each cluster as a potential figure
        for i, rect in enumerate(clusters):
            # Expand rect slightly to capture nearby labels/legends
            margin = 12
            rect = rect + (-margin, -margin, margin, margin)
            rect = rect & page.rect # Keep in bounds
            
            img_area = rect.width * rect.height
            ratio = img_area / page_area
            
            # Filter out very small artifacts or tiny icons
            if ratio < 0.05: # Stricter lower bound for clusters
                # But allow if it's broad enough (e.g. a wide but short figure)
                if rect.width < 100 and rect.height < 100:
                    continue

            # Render cluster at high DPI
            try:
                matrix = fitz.Matrix(4.0, 4.0)
                pix = page.get_pixmap(clip=rect, matrix=matrix, alpha=False)
                
                # Filter out "skinny" artifacts
                if pix.width < 100 or pix.height < 100:
                    if pix.width < 60 or pix.height < 60: 
                        continue
                    if pix.width / pix.height > 15 or pix.height / pix.width > 15:
                        continue 

                image_bytes = pix.tobytes("png")
                item_w, item_h = pix.width, pix.height
            except Exception:
                continue

            paper.figures.append(
                FigureImage(
                    page_index=page_idx,
                    xref=i, # Use cluster index as a placeholder xref
                    native_width=item_w,
                    native_height=item_h,
                    image_bytes=image_bytes,
                    page_area_ratio=ratio,
                )
            )

    doc.close()
    return paper


def save_figure_images(paper: Paper, output_dir: str) -> List[str]:
    """Save extracted figure images to disk. Returns list of saved paths."""
    from pathlib import Path

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    paths: List[str] = []

    for i, fig in enumerate(paper.figures, 1):
        path = out / f"figure_{i}_page{fig.page_index + 1}.png"
        img = fig.to_pil()
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(str(path), "PNG")
        paths.append(str(path))

    return paths
