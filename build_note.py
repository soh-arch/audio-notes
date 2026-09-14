#!/usr/bin/env python3
"""Convert a Markdown audio-note script into the static HTML page format
verified to work with Edge's Immersive Reader on iPhone.

Reads the Markdown source from, and writes the generated HTML into,
the notes/ directory. The page title comes from the source's opening
"# " heading, so a note carries exactly one title.

Usage:
    python3 build_note.py <slug>.md
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOTES_DIR = ROOT / "notes"
TEMPLATE_PATH = ROOT / "note-template.html"


def read_title(markdown):
    for line in markdown.splitlines():
        if not line.strip():
            continue
        heading = re.match(r"#\s+(\S.*)", line)
        return heading.group(1).strip() if heading else None
    return None


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python3 build_note.py <slug>.md")

    md_path = NOTES_DIR / sys.argv[1]

    if not md_path.exists():
        sys.exit(f"not found: {md_path}")

    title = read_title(md_path.read_text(encoding="utf-8"))
    if title is None:
        sys.exit(f"no title: {md_path} must open with a '# ' heading")

    slug = md_path.stem
    html_path = NOTES_DIR / f"{slug}.html"

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
