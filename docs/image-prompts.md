# Zaeed Jewelers — Hero Watch Image Prompt Kit

Gold Rolex Daytona, meteorite dial. These 8 piece shots + 1 assembled shot feed the
`hero-dissect` section blocks directly (same order as `templates/index.json`).
Generate the assembled shot first, then generate every piece prompt **in the same
chat/session** with it as reference so lighting, gold tone, and camera angle stay
identical across all 9 images — that consistency is what sells the "one watch,
taken apart" illusion on scroll.

## Style anchor — prepend to every prompt below

```
Ultra-realistic luxury product photography of a solid gold Rolex Daytona with a
meteorite dial. Studio lighting: single soft key light from upper-left, warm
3200K tone, subtle rim light to separate the gold from the background. Background:
pure near-black (#0b0a08), seamless, no gradient banding. Shot on a macro lens,
shallow depth of field, tack-sharp focus on the piece itself. No text, no
watermark, no hands, no wrist. Cinematic, editorial, restrained — the kind of
photo you'd see in Hodinkee or A Collected Man, not a catalog listing.
```

## 1. Assembled hero shot

```
[style anchor] Full 3/4 angle shot of the complete watch, case and bracelet both
visible, meteorite dial catching the key light so its crystalline Widmanstätten
pattern is legible. Composed with generous negative space on all sides so it can
sit centered in a hero layout. Square 1:1 crop.
```

## 2. Case (block: `case`)

```
[style anchor] Isolated gold Daytona case only — no dial, no bracelet, no crystal,
as if lifted mid-assembly. Cut out on a transparent background (PNG, alpha
channel, clean edges, no drop shadow baked in — shadow will be added in CSS).
Show the case's screw-down pushers and fluted crown guards in sharp detail.
```

## 3. Dial — meteorite (block: `dial`)

```
[style anchor] Macro shot of the meteorite dial alone, removed from the case,
floating flat toward camera. The Widmanstätten crystalline pattern must be the
hero of the frame — that's the point of this piece. Sub-dials visible. Cut out on
transparent background, clean edges, no baked-in shadow.
```

## 4. Bezel (block: `bezel`)

```
[style anchor] The tachymeter bezel ring alone, removed from the case, shot
face-on so its full circle reads clearly. Gold with black ceramic tachymeter
scale. Cut out on transparent background, clean edges, no baked-in shadow.
```

## 5. Crystal (block: `crystal`)

```
[style anchor] The sapphire crystal alone — near-invisible glass disc, only
visible through its edge highlight and a faint specular reflection of the key
light. This should read as "barely there" in the final composite. Cut out on
transparent background, clean edges, no baked-in shadow.
```

## 6. Crown (block: `crown`)

```
[style anchor] The fluted gold winding crown alone, macro detail on the fluting
and the Rolex coronet. Cut out on transparent background, clean edges, no
baked-in shadow.
```

## 7. Hands (block: `hands`)

```
[style anchor] The dial hands (hour, minute, chronograph seconds) alone,
arranged as if lifted together off the dial, gold with a faint luminous
edge. Cut out on transparent background, clean edges, no baked-in shadow.
```

## 8 & 9. Bracelet links (blocks: `link1`, `link2`)

```
[style anchor] Two to three links of the gold Oyster bracelet, disconnected from
the rest of the bracelet, shown at a slight angle to reveal the link profile and
the polished/brushed finish contrast. Cut out on transparent background, clean
edges, no baked-in shadow.
```

*(Generate this one twice, or generate once and use it for both `link1` and
`link2` blocks — the CSS gives them different explode positions so identical
source art still reads as two distinct moments.)*

---

## Hero video slot (optional, sits below the scroll piece)

For the commercial-style video slot in the hero section, direct it as:

```
5-8 second cinematic product video of a gold Rolex Daytona with a meteorite
dial. Slow orbital camera move around the watch on a near-black seamless
background, single warm key light sweeping across the meteorite dial to reveal
its crystalline pattern as the camera passes. No music sting, no text overlay —
this is a background-loop asset, captions/CTA are handled by the page around it.
Shot in the same lighting style as the product stills (warm 3200K key, near-black
#0b0a08 background) so it feels like one continuous shoot with the photography.
```

## Notes

- All 8 piece images upload as `image_picker` fields on the `hero-dissect`
  section's blocks in the Shopify theme editor — no code changes needed once
  they exist.
- Transparent PNG is required for the pieces (not the assembled shot) — anything
  with a baked-in background or shadow will show a visible box when it explodes
  outward on scroll.
- If real photography of Brandon's actual piece becomes available before AI
  generation, use it instead — real photography of the actual watch being sold
  will always outperform generated imagery for a page whose whole pitch is
  authentication and trust.
