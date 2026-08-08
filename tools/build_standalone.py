#!/usr/bin/env python3
"""
Packages the homepage into a single self-contained HTML file.

Inlines the stylesheet, the script, every SVG (as a URL-encoded data URI) and
the two webfonts (as base64 @font-face rules) so the page renders identically
with no network access at all — needed for hosts that block external requests.

    python3 tools/build_standalone.py            # uses cached fonts if present
    python3 tools/build_standalone.py --fonts    # re-download the font subsets

Outputs:
    dist/index.html      complete standalone page
    dist/artifact.html   same page as a head+body fragment for embedding
"""

import base64
import os
import re
import subprocess
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
FONT_CACHE = os.path.join(ROOT, "tools", ".fontcache")

GF_URL = ("https://fonts.googleapis.com/css2"
          "?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400"
          "&family=Jost:wght@300;400;500;600&display=swap")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120.0.0.0 Safari/537.36")


def fetch(url, binary=False):
    out = subprocess.run(["curl", "-sS", "-m", "40", "-A", UA, url],
                         capture_output=True, check=True)
    return out.stdout if binary else out.stdout.decode("utf-8")


def build_fonts(refresh=False):
    """Return @font-face CSS with the latin subsets embedded as data URIs."""
    os.makedirs(FONT_CACHE, exist_ok=True)
    cached = os.path.join(FONT_CACHE, "faces.css")
    if os.path.exists(cached) and not refresh:
        return open(cached, encoding="utf-8").read()

    css = fetch(GF_URL)
    faces = []
    # each @font-face is preceded by a /* subset */ comment; keep latin only
    for subset, block in re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{[^}]+\})", css):
        if subset != "latin":
            continue
        url = re.search(r"url\((https://[^)]+\.woff2)\)", block)
        if not url:
            continue
        name = url.group(1).rsplit("/", 1)[-1]
        path = os.path.join(FONT_CACHE, name)
        if not os.path.exists(path):
            with open(path, "wb") as f:
                f.write(fetch(url.group(1), binary=True))
        b64 = base64.b64encode(open(path, "rb").read()).decode("ascii")
        block = block.replace(url.group(1), "data:font/woff2;base64," + b64)
        block = re.sub(r"\s*unicode-range:[^;]+;", "", block)
        faces.append(block)

    out = "/* fonts embedded so the page needs no network */\n" + "\n".join(faces) + "\n"
    with open(cached, "w", encoding="utf-8") as f:
        f.write(out)
    return out


def svg_data_uri(path):
    """URL-encoded data URI — smaller than base64 for SVG text."""
    svg = open(path, encoding="utf-8").read()
    svg = re.sub(r">\s+<", "><", svg).strip()
    return "data:image/svg+xml," + urllib.parse.quote(svg, safe="")


def main():
    fonts = build_fonts(refresh="--fonts" in sys.argv)
    css = open(os.path.join(ROOT, "assets/css/styles.css"), encoding="utf-8").read()
    js = open(os.path.join(ROOT, "assets/js/main.js"), encoding="utf-8").read()
    html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

    # every image reference becomes an inline data URI
    images = {}
    for name in sorted(os.listdir(os.path.join(ROOT, "assets/img"))):
        if name.endswith(".svg"):
            images["assets/img/" + name] = svg_data_uri(os.path.join(ROOT, "assets/img", name))
    for ref, uri in sorted(images.items(), key=lambda kv: -len(kv[0])):
        html = html.replace(ref, uri)

    # drop the external font links and the linked css/js, inline everything
    html = re.sub(r'\s*<link rel="preconnect"[^>]*>', "", html)
    html = re.sub(r'\s*<link href="https://fonts\.googleapis[^>]*>', "", html)
    html = re.sub(r'\s*<link rel="stylesheet" href="assets/css/styles\.css">',
                  "\n<style>\n" + fonts + "\n" + css + "\n</style>", html)
    html = re.sub(r'\s*<script src="assets/js/main\.js" defer></script>',
                  "\n<script>\n" + js + "\n</script>", html)

    os.makedirs(DIST, exist_ok=True)
    full = os.path.join(DIST, "index.html")
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)

    # fragment form: <title> + <style> from head, then the body contents
    head = re.search(r"<head>(.*?)</head>", html, re.S).group(1)
    body = re.search(r"<body>(.*?)</body>", html, re.S).group(1)
    title = re.search(r"<title>.*?</title>", head, re.S).group(0)
    style = re.search(r"<style>.*?</style>", head, re.S).group(0)
    frag = os.path.join(DIST, "artifact.html")
    with open(frag, "w", encoding="utf-8") as f:
        f.write(title + "\n" + style + "\n" + body)

    for p in (full, frag):
        print("%-22s %6.0f KB" % (os.path.relpath(p, ROOT), os.path.getsize(p) / 1024))
    print("%d images inlined, %d font faces embedded" % (len(images), fonts.count("@font-face")))


if __name__ == "__main__":
    main()
