#!/usr/bin/env python3
"""Convert a Markdown audio-note script into the static HTML page format
verified to work with Edge's Immersive Reader on iPhone.

Usage:
    python3 build_note.py <slug>.md "<記事タイトル>"
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE_PATH = ROOT / "note-template.html"


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: python3 build_note.py <slug>.md \"<title>\"")

    md_path = ROOT / sys.argv[1]
    title = sys.argv[2]

    if not md_path.exists():
        sys.exit(f"not found: {md_path}")

    slug = md_path.stem
    html_path = ROOT / f"{slug}.html"

    body_html = subprocess.run(
        ["pandoc", "--from=markdown", "--to=html", str(md_path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout

    # The top-level "# タイトル" heading is rendered separately via h1.title,
    # so drop the corresponding <h1>...</h1> from the converted body.
    body_html = re.sub(r"^\s*<h1[^>]*>.*?</h1>\s*", "", body_html, count=1, flags=re.S)

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    page = (
        template
        .replace("__TITLE__", title)
        .replace("__SLUG__", slug)
        .replace("__BODY__", body_html.strip())
    )

    html_path.write_text(page, encoding="utf-8")
    print(f"wrote {html_path}")


if __name__ == "__main__":
    main()
