#!/usr/bin/env python3
"""Build the complete, offline CARDIA v8 review HTML from an immutable v7 base.

The original cardiac engine, clock, interactive source nodes, and gated content
are not rewritten. v8 adds only an isolated CSS and JS presentation adapter.
"""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
work = root / "prototypes" / "cardia-v8"
base = (work / "base-v7.html").read_text(encoding="utf-8")
css = (work / "cardia-v8.css").read_text(encoding="utf-8")
js = (work / "cardia-v8.js").read_text(encoding="utf-8")
if base.count("</head>") != 1 or base.count("</body>") != 1:
    raise RuntimeError("Unexpected baseline document structure")
if "CardiaV7" not in base or "CardiacCourseV113" not in base:
    raise RuntimeError("v7 native engine adapter is missing")
if "<style data-cardia-v8" in base or "<script data-cardia-v8" in base:
    raise RuntimeError("v8 has already been injected into the source baseline")
html = base.replace(
    "</head>", '<style data-cardia-v8="true">' + css + "</style>\n</head>"
).replace(
    "</body>", '<script data-cardia-v8="true">' + js.replace("</script", "<\\/script") + "</script>\n</body>"
)
out = work / "index.html"
out.write_text(html, encoding="utf-8")
print(f"CARDIA v8 standalone built: {out.relative_to(root)} | {len(html)} characters")
