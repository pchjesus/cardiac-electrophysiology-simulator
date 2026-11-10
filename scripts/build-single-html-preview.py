#!/usr/bin/env python3
"""Bundle the current review branch into a single offline, click-through HTML.

Do not modify original app source, physiology logic, course/case or release gates.
Source CSS/JS order is preserved exactly as declared in index.html.
"""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
page = (root / "index.html").read_text(encoding="utf-8")
css_count = 0
js_count = 0

def embed_css(match):
    global css_count
    rel = match.group(1)
    source = root / rel
    if not source.is_file() or source.suffix != ".css":
        raise ValueError(f"Unexpected stylesheet reference: {rel}")
    css_count += 1
    content = source.read_text(encoding="utf-8").replace("</style", "<\\/style")
    return f'<style data-bundled-from="{rel}">\n{content}\n</style>'

def embed_js(match):
    global js_count
    rel = match.group(1)
    source = root / rel
    if not source.is_file() or source.suffix != ".js":
        raise ValueError(f"Unexpected script reference: {rel}")
    js_count += 1
    # Avoid HTML parser interpreting a JavaScript literal as script closure.
    content = source.read_text(encoding="utf-8").replace("</script", "<\\/script")
    return f'<script data-bundled-from="{rel}">\n{content}\n</script>'

page = re.sub(
    r'<link rel="stylesheet" href="([^"]+\.css)">',
    embed_css, page
)
page = re.sub(
    r'<script src="([^"]+\.js)"></script>',
    embed_js, page
)

if css_count != 2 or js_count != 17:
    raise RuntimeError(f"Missing CSS or JS source: {css_count} styles / {js_count} scripts")
if re.search(r'<(?:script|link)[^>]+(?:src|href)="[^"]+\.(?:js|css)"', page):
    raise RuntimeError("Unbundled style or script dependency remains")

out = root / "preview-build" / "Cardiac_Lab_v2_Interactive_Preview.html"
out.parent.mkdir(exist_ok=True)
out.write_text(page, encoding="utf-8")
print(f"OFFLINE PREVIEW READY: {out.relative_to(root)} ({out.stat().st_size:,} bytes; {css_count} CSS, {js_count} JS)")
