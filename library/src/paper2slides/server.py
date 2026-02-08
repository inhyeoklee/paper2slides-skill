#!/usr/bin/env python3
"""Local development server for the generated presentation."""

from __future__ import annotations

import functools
import http.server
from pathlib import Path

import click


def serve(directory: str, port: int = 8000) -> None:
    """Serve a directory on localhost."""
    directory = str(Path(directory).resolve())
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=directory
    )
    with http.server.HTTPServer(("", port), handler) as httpd:
        click.echo(f"\n  Serving presentation at: http://localhost:{port}")
        click.echo("  Press Ctrl+C to stop.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            click.echo("\n  Server stopped.")
