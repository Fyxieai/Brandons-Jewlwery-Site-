# Brandon &amp; Co. — homepage

A premium, ecommerce-ready homepage for a luxury jewelry and watch house: chains,
pendants, bracelets, rings, earrings, custom commissions and authenticated
pre-owned watches.

Static HTML, CSS and vanilla JavaScript — no build step, no dependencies, no
framework. Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000   # → http://localhost:8000
```

## Design direction

Luxury Minimal · Metropolitan · Editorial · restrained Art Deco — the atmosphere
of a private Manhattan showroom rather than a storefront.

| Role | Token | Value |
| --- | --- | --- |
| Exclusivity, depth | `--black` / `--black-2` | `#08080A` / `#0E0E11` |
| Clean, readable ground | `--white` / `--bone` | `#FFFFFF` / `#F5F2EC` |
| Accent only — type, hairlines, icons, buttons | `--gold` | `#C6A15B` |

Gold is a **hairline**, never a surface: 1px rules, lozenge dividers, stepped
corner brackets, eyebrows, icon strokes, and the primary button. No bright
yellow, no metallic gradients on chrome, no gradient backgrounds.

**Type** — `Cormorant Garamond` (high-fashion serif) for headlines, `Jost`
(geometric sans, Art Deco lineage) for navigation, prices, specs and buttons.
Both load from Google Fonts with a system fallback stack, so the page still sets
correctly offline.

**Motion** — slow and editorial: a 24s hero drift, clip-path image reveals,
gold underlines that draw in, 1.2s card easing. Everything collapses under
`prefers-reduced-motion: reduce`.

## Sections

Announcement bar (rotating) → header (logo, nav with mega panel, search,
account, wishlist, cart) → cinematic hero → trust marquee → six category cards →
featured grid with filters, wishlist and quick view → craftsmanship editorial →
custom commission process → watch desk (buy / sell / trade + offer form) →
authenticity guarantee → client stories slider → private consultation booking →
Instagram-style gallery → VIP signup → footer (contact, hours, policies, social,
financing).

Plus: cart drawer, wishlist drawer, search overlay, quick-view modal, mobile nav
drawer, sticky mobile cart dock, back-to-top.

## Behaviour

`assets/js/main.js` (~380 lines, no dependencies) handles the announcement
rotator, sticky header, mega menu, overlay manager (focus trap, `Esc`, scroll
lock, focus restore), cart and wishlist with `localStorage` persistence,
category filtering, product search, the testimonial slider with touch swipe,
form validation, and `IntersectionObserver` scroll reveals.

Progressive enhancement: reveal start-states are scoped to a `.js` class set by
the script itself, so if JavaScript fails the page renders complete and readable
rather than blank.

## Imagery — placeholders to replace

`assets/img/*.svg` are **generated placeholders**, not photography. Each is a
self-contained SVG built from the three sets a real shoot would use — black
velvet, white studio sweep, warm neutral linen — with one soft key light, a
pooled reflection and light film grain, so the page reads as art-directed while
the real photos are shot.

Regenerate them with:

```bash
python3 tools/generate_placeholders.py
```

To go live, replace each file with real photography **at the same aspect ratio**
and nothing in the CSS needs to change:

| File | Ratio | Shot |
| --- | --- | --- |
| `hero.svg` | 3:2 | Hero — draped chain and ring, black velvet |
| `cat-*.svg` (6) | 3:4 | Category cards, portrait |
| `p-1…p-8.svg` | 1:1 | Product grid, square, mixed backgrounds |
| `ed-craft.svg`, `ed-custom.svg` | 4:5 | Editorial, portrait |
| `watch-feature.svg` | 8:5 | Watch desk feature |
| `g-1…g-6.svg` | 1:1 | Lifestyle gallery |

Keep the mix the brief calls for: crisp studio close-ups on black, white or warm
neutral, alternating with editorial lifestyle frames.

## Wiring it to a store

The page is front-end only. Connect these to a backend or a headless commerce
API when it goes live:

- `data-*` attributes on `.card` elements are the product source of truth
  (`data-id`, `data-name`, `data-price`, `data-img`, `data-s1…s4`) — swap for
  rendered product data.
- Cart and wishlist live in `localStorage` under `bandco.v1`.
- The three forms (watch offer, consultation, VIP) validate and confirm on the
  client; point them at your endpoint or CRM.
- `#checkout` and `#account` are placeholder targets.

## Content placeholders

Brand name, address, phone, email, hours, financing partners, review counts and
testimonials are all illustrative and should be replaced before launch.

## Browser support

Evergreen Chrome, Safari, Firefox and Edge. Uses CSS grid, `aspect-ratio`,
`clamp()`, custom properties, `backdrop-filter` and `IntersectionObserver` —
all baseline-available.

## Files

```
index.html                     the page
assets/css/styles.css          design system + all sections
assets/js/main.js              behaviour
assets/img/                    generated placeholder imagery
tools/generate_placeholders.py regenerates assets/img
tools/shots.py, tools/states.py screenshot + interaction checks (dev only)
```
