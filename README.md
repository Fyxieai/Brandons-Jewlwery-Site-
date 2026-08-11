# Zay Jewelers — Shopify Theme

A high-end pre-owned and sourced watch dealer site for Brandon the Jeweler.
Built on Shopify Online Store 2.0 (Dawn foundation), with a custom luxury
design system and a scroll-driven "dissect" hero.

## Brand

Exclusive, trustworthy, modern, quietly expensive — a private concierge, not a
marketplace. Near-black/charcoal base, single warm gold accent, ivory text.
Editorial serif headlines (Cormorant), clean sans body (Montserrat).

## What's here

- `config/settings_data.json` — luxury color schemes (Midnight, Charcoal) and
  brand typography defaults
- `assets/zay-tokens.css` — design tokens: color, type scale, spacing rhythm,
  motion easing, reduced-motion handling
- `sections/hero-dissect.liquid` (+ `.css` / `.js`) — the flagship hero: a gold
  Daytona with a meteorite dial that separates into its component pieces as the
  visitor scrolls, pinned in a tall track. Fully merchant-editable via blocks
  (one block per watch piece, each with its own exploded position/rotation/scale).
  Headline and CTAs are always visible regardless of JS/motion support — the
  dissection is a decorative layer on top of a working hero, not a dependency.
- `sections/path-cards.liquid` — the two primary conversion paths (Request/Reserve,
  Book a Call) plus a secondary Shop In-Stock path
- `sections/trust-strip.liquid` — authentication, discretion, insured shipping
- `sections/dealer-row.liquid` — "Trusted Across the Trade" credibility row
- `sections/brand-line.liquid` — the brand's edge statement (pull-quote style)
- `docs/image-prompts.md` — image-gen prompt kit for the hero's watch pieces
  (gold Daytona, meteorite dial), matched 1:1 to the hero-dissect blocks

## Still needed before launch

- Real (or generated, per `docs/image-prompts.md`) photography for the 8
  hero-dissect piece blocks — currently shows placeholder labels
- Brandon's story for the About page
- Collection page, product detail page, Source a Watch form, Book a Call flow,
  and About page (design brief exists, not yet built)
- Final in-stock vs. sourced piece catalog

## Local development

```bash
shopify theme dev --store <brandons-store>.myshopify.com
```

Requires a Shopify store connection (partner dev store or Brandon's live store)
to preview with real theme editor data — this repo has no store connected yet.
