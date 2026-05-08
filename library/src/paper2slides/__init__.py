"""
paper2slides — PDF → Journal Club Reveal.js Presentation

Extract figures from scientific papers, segment them into panels,
and generate interactive Reveal.js presentations with the paper2slides slate + indigo theme.
"""

__version__ = "0.1.0"

from paper2slides.extractor import extract, Paper, FigureImage
from paper2slides.segmenter import segment_figure, segment_all, Panel

__all__ = [
    "__version__",
    "extract",
    "Paper",
    "FigureImage",
    "segment_figure",
    "segment_all",
    "Panel",
]
