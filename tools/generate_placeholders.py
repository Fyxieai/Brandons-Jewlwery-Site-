#!/usr/bin/env python3
"""
Generates the studio-style placeholder imagery used across the homepage.

Every image is a self-contained SVG built from the same three "sets" a real
shoot would use: black velvet, white studio sweep, warm neutral linen — each
lit with a single soft key light, a reflection under the piece, and a light
film grain. Subjects are drawn geometrically (Art Deco construction) so the
placeholders read as deliberate art direction rather than broken images.

Swap any file in assets/img/ for real photography of the same aspect ratio
and nothing in the CSS needs to change.

    python3 tools/generate_placeholders.py
"""

import math
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img")

# --- palette ---------------------------------------------------------------
GOLD_HI = "#F0E0B4"
GOLD = "#C6A15B"
GOLD_MID = "#A8843F"
GOLD_DEEP = "#6E5626"

SETS = {
    "black":   {"a": "#141416", "b": "#08080A", "key": "#3A3226", "floor": "#0B0B0D", "ink": "#F7F5F1"},
    "white":   {"a": "#FFFFFF", "b": "#E8E4DC", "key": "#FFFFFF", "floor": "#DED8CD", "ink": "#12120F"},
    "neutral": {"a": "#E9E0D2", "b": "#CBBCA5", "key": "#F6EEE0", "floor": "#BFAF97", "ink": "#1A1712"},
}


def defs(w, h, set_name, key=(0.5, 0.34), key_r=0.78):
    s = SETS[set_name]
    metal_dark = GOLD_DEEP if set_name == "black" else "#8A6C2F"
    return f"""<defs>
  <radialGradient id="bg" cx="{key[0] * 100:.1f}%" cy="{key[1] * 100:.1f}%" r="{key_r * 100:.0f}%">
    <stop offset="0%" stop-color="{s['key']}" stop-opacity="{0.55 if set_name == 'black' else 1}"/>
    <stop offset="42%" stop-color="{s['a']}"/>
    <stop offset="100%" stop-color="{s['b']}"/>
  </radialGradient>
  <linearGradient id="metal" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{metal_dark}"/>
    <stop offset="18%" stop-color="{GOLD}"/>
    <stop offset="38%" stop-color="{GOLD_HI}"/>
    <stop offset="55%" stop-color="{GOLD}"/>
    <stop offset="74%" stop-color="{metal_dark}"/>
    <stop offset="90%" stop-color="{GOLD_MID}"/>
    <stop offset="100%" stop-color="{metal_dark}"/>
  </linearGradient>
  <linearGradient id="metalV" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="{GOLD_HI}"/>
    <stop offset="30%" stop-color="{GOLD}"/>
    <stop offset="62%" stop-color="{metal_dark}"/>
    <stop offset="100%" stop-color="{GOLD_MID}"/>
  </linearGradient>
  <linearGradient id="stone" x1="20%" y1="0%" x2="80%" y2="100%">
    <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
    <stop offset="45%" stop-color="#D8E3EA" stop-opacity="0.75"/>
    <stop offset="100%" stop-color="#8FA3B0" stop-opacity="0.65"/>
  </linearGradient>
  <linearGradient id="fade" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="{s['floor']}" stop-opacity="0.55"/>
    <stop offset="100%" stop-color="{s['floor']}" stop-opacity="0"/>
  </linearGradient>
  <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="{max(w, h) * 0.012:.1f}"/>
  </filter>
  <filter id="cast" x="-40%" y="-40%" width="180%" height="180%">
    <feDropShadow dx="0" dy="{h * 0.012:.1f}" stdDeviation="{max(w, h) * 0.014:.1f}"
      flood-color="#000000" flood-opacity="{0.55 if set_name == 'black' else 0.32}"/>
  </filter>
  <filter id="grain" x="0%" y="0%" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
  <radialGradient id="vig" cx="50%" cy="46%" r="72%">
    <stop offset="55%" stop-color="#000000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000000" stop-opacity="{0.62 if set_name == 'black' else 0.2}"/>
  </radialGradient>
</defs>"""


def backdrop(w, h, set_name):
    return f'<rect width="{w}" height="{h}" fill="url(#bg)"/>'


def finish(w, h, set_name):
    op = 0.055 if set_name == "black" else 0.04
    return (f'<rect width="{w}" height="{h}" fill="url(#vig)"/>'
            f'<rect width="{w}" height="{h}" filter="url(#grain)" opacity="{op}"/>')


def reflection(cx, cy, rw, rh, set_name):
    """Soft pooled reflection beneath the piece."""
    return (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rw:.1f}" ry="{rh:.1f}" '
            f'fill="url(#fade)" filter="url(#soft)" opacity="0.9"/>')


# --- subject drawing -------------------------------------------------------
def link(cx, cy, ang, w, h, t, squash=1.0, op=1.0):
    rx = h * 0.46
    return (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({ang:.1f}) scale({squash:.2f},1)">'
            f'<rect x="{-w / 2:.1f}" y="{-h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" '
            f'fill="none" stroke="url(#metal)" stroke-width="{t:.1f}" opacity="{op}"/>'
            f'<rect x="{-w / 2 + t * 0.28:.1f}" y="{-h / 2 + t * 0.28:.1f}" width="{w - t * 0.56:.1f}" '
            f'height="{h - t * 0.56:.1f}" rx="{rx:.1f}" fill="none" stroke="{GOLD_HI}" '
            f'stroke-width="{t * 0.16:.1f}" opacity="{0.5 * op}"/></g>')


def quad(p0, p1, p2, t):
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])


def chain_along_quad(p0, p1, p2, n, lw, lh, t, start=0.0, end=1.0):
    out = []
    for i in range(n):
        u = start + (end - start) * (i / (n - 1))
        x, y = quad(p0, p1, p2, u)
        x2, y2 = quad(p0, p1, p2, min(1.0, u + 0.01))
        ang = math.degrees(math.atan2(y2 - y, x2 - x)) + 90
        out.append(link(x, y, ang, lw, lh, t, 1.0 if i % 2 == 0 else 0.42))
    return "".join(out)


def deco_rays(cx, cy, r0, r1, n, color, width, op=0.5):
    out = []
    for i in range(n):
        a = math.radians(i * 360 / n)
        out.append(f'<line x1="{cx + r0 * math.cos(a):.1f}" y1="{cy + r0 * math.sin(a):.1f}" '
                   f'x2="{cx + r1 * math.cos(a):.1f}" y2="{cy + r1 * math.sin(a):.1f}" '
                   f'stroke="{color}" stroke-width="{width}" opacity="{op}"/>')
    return "".join(out)


def subject_chain(w, h, s):
    cx, cy = w * 0.5, h * 0.5
    span = min(w, h)
    body = chain_along_quad((cx - span * 0.42, cy - span * 0.22),
                            (cx, cy + span * 0.36), (cx + span * 0.42, cy - span * 0.22),
                            26, span * 0.115, span * 0.085, span * 0.023)
    clasp = (f'<rect x="{cx - span * 0.045:.1f}" y="{cy - span * 0.30:.1f}" width="{span * 0.09:.1f}" '
             f'height="{span * 0.055:.1f}" rx="{span * 0.012:.1f}" fill="url(#metalV)" opacity="0"/>')
    return f'<g filter="url(#cast)">{body}{clasp}</g>' + reflection(cx, cy + span * 0.30, span * 0.34, span * 0.05, s)


def subject_pendant(w, h, s):
    cx, cy = w * 0.5, h * 0.44
    span = min(w, h)
    r = span * 0.15
    left = chain_along_quad((cx - span * 0.36, cy - span * 0.30), (cx - span * 0.24, cy + span * 0.02),
                            (cx - span * 0.012, cy + span * 0.10), 14, span * 0.062, span * 0.05, span * 0.014)
    right = chain_along_quad((cx + span * 0.36, cy - span * 0.30), (cx + span * 0.24, cy + span * 0.02),
                             (cx + span * 0.012, cy + span * 0.10), 14, span * 0.062, span * 0.05, span * 0.014)
    bail = (f'<rect x="{cx - span * 0.028:.1f}" y="{cy + span * 0.085:.1f}" width="{span * 0.056:.1f}" '
            f'height="{span * 0.062:.1f}" rx="{span * 0.026:.1f}" fill="none" stroke="url(#metal)" '
            f'stroke-width="{span * 0.016:.1f}"/>')
    disc = (f'<circle cx="{cx:.1f}" cy="{cy + span * 0.135 + r:.1f}" r="{r:.1f}" fill="url(#metal)"/>'
            f'<circle cx="{cx:.1f}" cy="{cy + span * 0.135 + r:.1f}" r="{r * 0.82:.1f}" fill="none" '
            f'stroke="{GOLD_DEEP}" stroke-width="{r * 0.05:.1f}" opacity="0.7"/>'
            + deco_rays(cx, cy + span * 0.135 + r, r * 0.24, r * 0.74, 24, GOLD_DEEP, r * 0.035, 0.55) +
            f'<circle cx="{cx:.1f}" cy="{cy + span * 0.135 + r:.1f}" r="{r * 0.20:.1f}" fill="url(#stone)"/>')
    return (f'<g filter="url(#cast)">{left}{right}{bail}{disc}</g>'
            + reflection(cx, cy + span * 0.135 + r * 2.2, span * 0.22, span * 0.035, s))


def subject_bracelet(w, h, s):
    cx, cy = w * 0.5, h * 0.5
    span = min(w, h)
    rx, ry = span * 0.33, span * 0.20
    out = []
    n = 30
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        ang = math.degrees(math.atan2(ry * math.cos(a), -rx * math.sin(a))) + 90
        out.append(link(x, y, ang, span * 0.085, span * 0.065, span * 0.018,
                        1.0 if i % 2 == 0 else 0.45, 1.0 if math.sin(a) > -0.55 else 0.85))
    return f'<g filter="url(#cast)">{"".join(out)}</g>' + reflection(cx, cy + ry * 1.35, span * 0.30, span * 0.045, s)


def subject_ring(w, h, s):
    cx, cy = w * 0.5, h * 0.54
    span = min(w, h)
    r = span * 0.20
    band = (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{r:.1f}" ry="{r * 1.02:.1f}" fill="none" '
            f'stroke="url(#metal)" stroke-width="{r * 0.30:.1f}"/>'
            f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{r * 1.06:.1f}" ry="{r * 1.08:.1f}" fill="none" '
            f'stroke="{GOLD_HI}" stroke-width="{r * 0.02:.1f}" opacity="0.45"/>')
    top = cy - r * 1.15
    st = span * 0.115
    stone = (f'<g transform="translate({cx:.1f},{top:.1f})">'
             f'<polygon points="{-st:.1f},{-st * 0.28:.1f} {-st * 0.62:.1f},{-st * 0.86:.1f} '
             f'{st * 0.62:.1f},{-st * 0.86:.1f} {st:.1f},{-st * 0.28:.1f} 0,{st * 0.62:.1f}" '
             f'fill="url(#stone)" stroke="{GOLD_HI}" stroke-width="{st * 0.03:.1f}"/>'
             f'<polyline points="{-st * 0.6:.1f},{-st * 0.28:.1f} {st * 0.6:.1f},{-st * 0.28:.1f}" '
             f'fill="none" stroke="#FFFFFF" stroke-width="{st * 0.03:.1f}" opacity="0.8"/>'
             f'<polyline points="{-st * 0.6:.1f},{-st * 0.28:.1f} 0,{st * 0.62:.1f} {st * 0.6:.1f},{-st * 0.28:.1f}" '
             f'fill="none" stroke="#FFFFFF" stroke-width="{st * 0.025:.1f}" opacity="0.55"/>'
             f'<polyline points="0,{-st * 0.86:.1f} 0,{st * 0.62:.1f}" fill="none" stroke="#FFFFFF" '
             f'stroke-width="{st * 0.02:.1f}" opacity="0.4"/></g>')
    prongs = "".join(
        f'<line x1="{cx + dx * st * 0.9:.1f}" y1="{top + st * 0.1:.1f}" x2="{cx + dx * st * 0.55:.1f}" '
        f'y2="{top + st * 0.95:.1f}" stroke="url(#metalV)" stroke-width="{st * 0.11:.1f}" stroke-linecap="round"/>'
        for dx in (-1, 1))
    return f'<g filter="url(#cast)">{prongs}{stone}{band}</g>' + reflection(cx, cy + r * 1.25, r * 1.5, r * 0.22, s)


def subject_watch(w, h, s):
    cx, cy = w * 0.5, h * 0.48
    span = min(w, h)
    r = span * 0.215
    ink = SETS[s]["ink"]
    strap = (f'<path d="M{cx - r * 0.62:.1f},{cy - r * 0.92:.1f} L{cx - r * 0.48:.1f},{cy - r * 2.5:.1f} '
             f'Q{cx:.1f},{cy - r * 2.72:.1f} {cx + r * 0.48:.1f},{cy - r * 2.5:.1f} '
             f'L{cx + r * 0.62:.1f},{cy - r * 0.92:.1f} Z" fill="url(#metalV)" opacity="0.92"/>'
             f'<path d="M{cx - r * 0.62:.1f},{cy + r * 0.92:.1f} L{cx - r * 0.48:.1f},{cy + r * 2.5:.1f} '
             f'Q{cx:.1f},{cy + r * 2.72:.1f} {cx + r * 0.48:.1f},{cy + r * 2.5:.1f} '
             f'L{cx + r * 0.62:.1f},{cy + r * 0.92:.1f} Z" fill="url(#metalV)" opacity="0.92"/>')
    strap_lines = "".join(
        f'<line x1="{cx - r * (0.5 + 0.06 * i):.1f}" y1="{cy + sgn * r * (1.1 + 0.34 * i):.1f}" '
        f'x2="{cx + r * (0.5 + 0.06 * i):.1f}" y2="{cy + sgn * r * (1.1 + 0.34 * i):.1f}" '
        f'stroke="{GOLD_DEEP}" stroke-width="{r * 0.035:.1f}" opacity="0.5"/>'
        for sgn in (-1, 1) for i in range(4))
    crown = (f'<rect x="{cx + r * 0.98:.1f}" y="{cy - r * 0.10:.1f}" width="{r * 0.13:.1f}" '
             f'height="{r * 0.20:.1f}" rx="{r * 0.04:.1f}" fill="url(#metalV)"/>')
    case = (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="url(#metal)"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * 0.86:.1f}" fill="{"#0C0C0E" if s == "black" else "#141416"}"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * 0.86:.1f}" fill="none" stroke="{GOLD_DEEP}" '
            f'stroke-width="{r * 0.02:.1f}"/>')
    idx = []
    for i in range(12):
        a = math.radians(i * 30 - 90)
        r0, r1 = r * 0.70, r * 0.80
        wdt = r * 0.05 if i % 3 == 0 else r * 0.028
        idx.append(f'<line x1="{cx + r0 * math.cos(a):.1f}" y1="{cy + r0 * math.sin(a):.1f}" '
                   f'x2="{cx + r1 * math.cos(a):.1f}" y2="{cy + r1 * math.sin(a):.1f}" '
                   f'stroke="{GOLD_HI}" stroke-width="{wdt:.1f}" stroke-linecap="round"/>')
    hands = (f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx + r * 0.34:.1f}" y2="{cy - r * 0.30:.1f}" '
             f'stroke="{GOLD_HI}" stroke-width="{r * 0.045:.1f}" stroke-linecap="round"/>'
             f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx - r * 0.30:.1f}" y2="{cy - r * 0.52:.1f}" '
             f'stroke="{GOLD_HI}" stroke-width="{r * 0.032:.1f}" stroke-linecap="round"/>'
             f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * 0.045:.1f}" fill="{GOLD_HI}"/>'
             f'<circle cx="{cx:.1f}" cy="{cy + r * 0.42:.1f}" r="{r * 0.16:.1f}" fill="none" '
             f'stroke="{GOLD_DEEP}" stroke-width="{r * 0.018:.1f}" opacity="0.8"/>')
    glare = (f'<path d="M{cx - r * 0.8:.1f},{cy - r * 0.3:.1f} A{r * 0.86:.1f},{r * 0.86:.1f} 0 0 1 '
             f'{cx - r * 0.1:.1f},{cy - r * 0.85:.1f} L{cx - r * 0.55:.1f},{cy - r * 0.1:.1f} Z" '
             f'fill="#FFFFFF" opacity="0.07"/>')
    return (f'<g filter="url(#cast)">{strap}{strap_lines}{crown}{case}{"".join(idx)}{hands}{glare}</g>'
            + reflection(cx, cy + r * 2.9, r * 1.2, r * 0.22, s))


def subject_earrings(w, h, s):
    span = min(w, h)
    cy = h * 0.40
    edge = GOLD_HI if s == "black" else GOLD_MID
    out = []
    for sgn in (-1, 1):
        cx = w * 0.5 + sgn * span * 0.155
        r = span * 0.085
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="url(#metal)" '
                   f'stroke-width="{r * 0.26:.1f}"/>')
        # bail links the hoop to the drop with no visible gap
        top = cy + r * 0.92
        out.append(f'<rect x="{cx - span * 0.014:.1f}" y="{top:.1f}" width="{span * 0.028:.1f}" '
                   f'height="{span * 0.042:.1f}" rx="{span * 0.013:.1f}" fill="none" stroke="url(#metalV)" '
                   f'stroke-width="{span * 0.009:.1f}"/>')
        # tapered baguette drop
        dy = top + span * 0.036
        dw, dh = span * 0.048, span * 0.185
        pts = (f'{cx - dw * 0.72:.1f},{dy:.1f} {cx - dw:.1f},{dy + dh * 0.22:.1f} '
               f'{cx:.1f},{dy + dh:.1f} {cx + dw:.1f},{dy + dh * 0.22:.1f} {cx + dw * 0.72:.1f},{dy:.1f}')
        out.append(f'<polygon points="{pts}" fill="url(#stone)" stroke="{edge}" '
                   f'stroke-width="{span * 0.005:.1f}"/>')
        out.append(f'<polyline points="{cx - dw:.1f},{dy + dh * 0.22:.1f} {cx:.1f},{dy + dh * 0.36:.1f} '
                   f'{cx + dw:.1f},{dy + dh * 0.22:.1f}" fill="none" stroke="{edge}" opacity="0.5" '
                   f'stroke-width="{span * 0.0035:.1f}"/>')
        out.append(f'<line x1="{cx:.1f}" y1="{dy + dh * 0.36:.1f}" x2="{cx:.1f}" y2="{dy + dh:.1f}" '
                   f'stroke="{edge}" opacity="0.45" stroke-width="{span * 0.003:.1f}"/>')
    return f'<g filter="url(#cast)">{"".join(out)}</g>' + reflection(w * 0.5, cy + span * 0.33, span * 0.24, span * 0.035, s)


def subject_custom(w, h, s):
    """Bench sketch: Art Deco construction lines, dividers and a ring in progress."""
    span = min(w, h)
    cx, cy = w * 0.5, h * 0.5
    line = GOLD if s == "black" else GOLD_MID
    grid = []
    step = span * 0.075
    for i in range(-7, 8):
        grid.append(f'<line x1="{cx + i * step:.1f}" y1="{cy - span * 0.5:.1f}" x2="{cx + i * step:.1f}" '
                    f'y2="{cy + span * 0.5:.1f}" stroke="{line}" stroke-width="0.6" opacity="0.10"/>')
        grid.append(f'<line x1="{cx - span * 0.55:.1f}" y1="{cy + i * step:.1f}" x2="{cx + span * 0.55:.1f}" '
                    f'y2="{cy + i * step:.1f}" stroke="{line}" stroke-width="0.6" opacity="0.10"/>')
    arcs = "".join(
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{span * rr:.2f}" fill="none" stroke="{line}" '
        f'stroke-width="{span * 0.0035:.1f}" opacity="{op}" stroke-dasharray="{span * 0.012:.1f} {span * 0.012:.1f}"/>'
        for rr, op in ((0.30, 0.35), (0.235, 0.5), (0.36, 0.22)))
    ring = (f'<ellipse cx="{cx:.1f}" cy="{cy + span * 0.02:.1f}" rx="{span * 0.155:.1f}" ry="{span * 0.16:.1f}" '
            f'fill="none" stroke="url(#metal)" stroke-width="{span * 0.045:.1f}"/>')
    st = span * 0.075
    stone = (f'<g transform="translate({cx:.1f},{cy - span * 0.155:.1f})">'
             f'<polygon points="{-st:.1f},{-st * 0.3:.1f} {-st * 0.6:.1f},{-st * 0.9:.1f} {st * 0.6:.1f},'
             f'{-st * 0.9:.1f} {st:.1f},{-st * 0.3:.1f} 0,{st * 0.65:.1f}" fill="url(#stone)" '
             f'stroke="{GOLD_HI}" stroke-width="{st * 0.04:.1f}"/></g>')
    divider = (f'<g transform="translate({cx + span * 0.30:.1f},{cy - span * 0.30:.1f}) rotate(24)">'
               f'<line x1="0" y1="0" x2="{-span * 0.06:.1f}" y2="{span * 0.34:.1f}" stroke="url(#metalV)" '
               f'stroke-width="{span * 0.014:.1f}" stroke-linecap="round"/>'
               f'<line x1="0" y1="0" x2="{span * 0.06:.1f}" y2="{span * 0.34:.1f}" stroke="url(#metalV)" '
               f'stroke-width="{span * 0.014:.1f}" stroke-linecap="round"/>'
               f'<circle cx="0" cy="0" r="{span * 0.018:.1f}" fill="url(#metal)"/></g>')
    ticks = deco_rays(cx, cy, span * 0.40, span * 0.435, 36, line, span * 0.0035, 0.28)
    return "".join(grid) + arcs + ticks + divider + f'<g filter="url(#cast)">{ring}{stone}</g>' + \
        reflection(cx, cy + span * 0.23, span * 0.22, span * 0.03, s)


def subject_hero(w, h, s):
    """Layered composition: draped chain, ring on the light, watch just off-key."""
    span = min(w, h)
    cx, cy = w * 0.52, h * 0.52
    back = chain_along_quad((cx - w * 0.46, cy - h * 0.34), (cx - w * 0.05, cy + h * 0.30),
                            (cx + w * 0.34, cy - h * 0.30), 30, span * 0.075, span * 0.056, span * 0.015)
    back = f'<g opacity="0.42" filter="url(#soft)">{back}</g>'
    front = chain_along_quad((cx - w * 0.40, cy - h * 0.16), (cx - w * 0.02, cy + h * 0.40),
                             (cx + w * 0.30, cy - h * 0.10), 24, span * 0.125, span * 0.092, span * 0.026)
    r = span * 0.115
    rx, ry = cx + w * 0.24, cy + h * 0.12
    ring = (f'<g filter="url(#cast)"><ellipse cx="{rx:.1f}" cy="{ry:.1f}" rx="{r:.1f}" ry="{r * 1.02:.1f}" '
            f'fill="none" stroke="url(#metal)" stroke-width="{r * 0.28:.1f}"/>'
            f'<polygon points="{rx - r * 0.5:.1f},{ry - r * 1.28:.1f} {rx - r * 0.3:.1f},{ry - r * 1.62:.1f} '
            f'{rx + r * 0.3:.1f},{ry - r * 1.62:.1f} {rx + r * 0.5:.1f},{ry - r * 1.28:.1f} '
            f'{rx:.1f},{ry - r * 0.78:.1f}" fill="url(#stone)" stroke="{GOLD_HI}" stroke-width="{r * 0.02:.1f}"/></g>')
    beam = (f'<path d="M{w * 0.16:.1f},0 L{w * 0.44:.1f},0 L{w * 0.72:.1f},{h:.1f} L{w * 0.30:.1f},{h:.1f} Z" '
            f'fill="#FFFFFF" opacity="{0.045 if s == "black" else 0.10}" filter="url(#soft)"/>')
    return (beam + back + f'<g filter="url(#cast)">{front}</g>' + ring
            + reflection(cx, cy + h * 0.34, w * 0.34, h * 0.045, s))


def subject_bench(w, h, s):
    """Editorial: loupe, tweezers and an Art Deco fan of light over the bench."""
    span = min(w, h)
    cx, cy = w * 0.5, h * 0.52
    line = GOLD if s == "black" else GOLD_MID
    fan = "".join(
        f'<path d="M{cx:.1f},{cy - span * 0.46:.1f} L{cx + math.cos(math.radians(a)) * span * 0.5:.1f},'
        f'{cy - span * 0.46 + math.sin(math.radians(a)) * span * 0.5:.1f}" stroke="{line}" '
        f'stroke-width="{span * 0.003:.1f}" opacity="0.18"/>' for a in range(20, 165, 12))
    r = span * 0.155
    loupe = (f'<circle cx="{cx - span * 0.06:.1f}" cy="{cy - span * 0.02:.1f}" r="{r:.1f}" fill="none" '
             f'stroke="url(#metal)" stroke-width="{r * 0.17:.1f}"/>'
             f'<circle cx="{cx - span * 0.06:.1f}" cy="{cy - span * 0.02:.1f}" r="{r * 0.9:.1f}" '
             f'fill="#FFFFFF" opacity="0.05"/>'
             f'<path d="M{cx - span * 0.06 + r * 0.72:.1f},{cy - span * 0.02 + r * 0.72:.1f} '
             f'L{cx + span * 0.20:.1f},{cy + span * 0.24:.1f}" stroke="url(#metalV)" '
             f'stroke-width="{r * 0.15:.1f}" stroke-linecap="round"/>')
    tweez = (f'<g transform="translate({cx + span * 0.30:.1f},{cy - span * 0.34:.1f}) rotate(28)">'
             f'<path d="M0,0 L{span * 0.012:.1f},{span * 0.34:.1f}" stroke="url(#metalV)" '
             f'stroke-width="{span * 0.011:.1f}" stroke-linecap="round"/>'
             f'<path d="M{span * 0.026:.1f},0 L{span * 0.02:.1f},{span * 0.34:.1f}" stroke="url(#metalV)" '
             f'stroke-width="{span * 0.011:.1f}" stroke-linecap="round"/></g>')
    # a single set stone waiting on the bench, held under the loupe's reach
    grit = (f'<polygon points="{cx + span * 0.185:.1f},{cy + span * 0.300:.1f} '
            f'{cx + span * 0.215:.1f},{cy + span * 0.253:.1f} {cx + span * 0.255:.1f},{cy + span * 0.273:.1f} '
            f'{cx + span * 0.230:.1f},{cy + span * 0.320:.1f}" fill="url(#stone)" stroke="{GOLD_HI}" '
            f'stroke-width="{span * 0.003:.1f}" opacity="0.9"/>')
    return fan + f'<g filter="url(#cast)">{loupe}{tweez}{grit}</g>' + reflection(cx, cy + span * 0.36, span * 0.30, span * 0.035, s)


SUBJECTS = {
    "chain": subject_chain, "pendant": subject_pendant, "bracelet": subject_bracelet,
    "ring": subject_ring, "watch": subject_watch, "earrings": subject_earrings,
    "custom": subject_custom, "hero": subject_hero, "bench": subject_bench,
}


def build(name, w, h, subject, set_name, key=(0.5, 0.34), scale=1.0, shift=(0.0, 0.0)):
    inner = SUBJECTS[subject](w, h, set_name)
    tx, ty = w * shift[0], h * shift[1]
    body = (f'<g transform="translate({w / 2 + tx:.1f},{h / 2 + ty:.1f}) scale({scale}) '
            f'translate({-w / 2:.1f},{-h / 2:.1f})">{inner}</g>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
           f'role="img" preserveAspectRatio="xMidYMid slice">'
           f'{defs(w, h, set_name, key)}{backdrop(w, h, set_name)}{body}{finish(w, h, set_name)}</svg>')
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    return path


# name, w, h, subject, set, key light, scale, shift
PLAN = [
    ("hero.svg", 1800, 1200, "hero", "black", (0.42, 0.30), 0.82, (0.02, 0)),
    ("hero-detail.svg", 1000, 1250, "watch", "black", (0.5, 0.30), 1.15, (0, 0.02)),

    ("cat-chains.svg", 900, 1200, "chain", "black", (0.5, 0.32), 1.25, (0, 0)),
    ("cat-pendants.svg", 900, 1200, "pendant", "neutral", (0.5, 0.28), 1.05, (0, 0)),
    ("cat-bracelets.svg", 900, 1200, "bracelet", "white", (0.5, 0.30), 1.20, (0, 0)),
    ("cat-rings.svg", 900, 1200, "ring", "black", (0.5, 0.34), 1.20, (0, 0)),
    ("cat-watches.svg", 900, 1200, "watch", "neutral", (0.5, 0.30), 1.00, (0, 0)),
    ("cat-custom.svg", 900, 1200, "custom", "black", (0.5, 0.34), 1.10, (0, 0)),

    ("p-1.svg", 1000, 1000, "chain", "black", (0.5, 0.34), 1.0, (0, 0)),
    ("p-2.svg", 1000, 1000, "watch", "white", (0.5, 0.30), 1.0, (0, 0)),
    ("p-3.svg", 1000, 1000, "ring", "black", (0.5, 0.34), 1.05, (0, 0)),
    ("p-4.svg", 1000, 1000, "pendant", "neutral", (0.5, 0.30), 1.0, (0, 0)),
    ("p-5.svg", 1000, 1000, "bracelet", "black", (0.5, 0.34), 1.05, (0, 0)),
    ("p-6.svg", 1000, 1000, "earrings", "white", (0.5, 0.30), 1.05, (0, 0)),
    ("p-7.svg", 1000, 1000, "watch", "black", (0.46, 0.32), 1.05, (0, 0)),
    ("p-8.svg", 1000, 1000, "custom", "neutral", (0.5, 0.32), 1.0, (0, 0)),

    ("ed-craft.svg", 1200, 1500, "bench", "black", (0.44, 0.30), 1.0, (0, 0)),
    ("ed-custom.svg", 1200, 1500, "custom", "neutral", (0.5, 0.32), 1.15, (0, 0)),
    ("watch-feature.svg", 1600, 1000, "watch", "black", (0.38, 0.34), 0.70, (0.12, 0)),

    ("g-1.svg", 800, 800, "chain", "neutral", (0.5, 0.32), 1.3, (0.04, 0)),
    ("g-2.svg", 800, 800, "watch", "black", (0.5, 0.32), 1.25, (0, 0)),
    ("g-3.svg", 800, 800, "ring", "white", (0.5, 0.30), 1.35, (0, 0)),
    ("g-4.svg", 800, 800, "bench", "black", (0.42, 0.30), 1.2, (0, 0)),
    ("g-5.svg", 800, 800, "earrings", "neutral", (0.5, 0.30), 1.3, (0, 0.02)),
    ("g-6.svg", 800, 800, "bracelet", "black", (0.5, 0.34), 1.3, (0, 0)),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for row in PLAN:
        p = build(*row)
        print("wrote", os.path.relpath(p, os.path.dirname(OUT)))
    print(f"{len(PLAN)} images generated")
