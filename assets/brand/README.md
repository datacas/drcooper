# DrCooper brand assets

Vector proposal for the DrCooper identity. Every deliverable is generated from
the sources in this directory; the SVG files are readable and editable, and the
PNGs are exports, never sources.

## Hierarchy

The mascot is the identity. The symbol is the reduction.

| Level | Asset | Use |
|---|---|---|
| Primary | `logo.svg`, `logo-dark.svg`, `logo-mono.svg`, `logo-mono-inverse.svg` | Mascot plus wordmark. Website header, README, decks, store listings |
| Secondary | `mascot.svg` | GitHub organisation avatar and social profiles |
| Secondary | `lockup-symbol.svg`, `lockup-symbol-dark.svg` | Horizontal lockups for widths where the mascot stops working |
| Reduction | `symbol.svg` | Favicon, CLI, app icon, 16–32 px |
| Illustration | `mascot-transparent.svg`, `mascot-full.svg` | Documentation, empty states, diagrams, swag |

This ordering is a decision, not an accident: see
[`docs/brand/DECISION_PRIMARY_IDENTITY.md`](../../docs/brand/DECISION_PRIMARY_IDENTITY.md).
`brief_identidad.md` is unchanged.

## Files

| File | Notes |
|---|---|
| `logo.svg` | Primary lockup, dark ink, transparent background, 1015 × 320 |
| `logo-dark.svg` | Primary lockup for dark backgrounds, white wordmark |
| `logo-mono.svg` | One ink, transparent, for terminals and one-colour print |
| `logo-mono-inverse.svg` | One white ink, transparent, for dark one-colour surfaces |
| `mascot.svg` | Bust in a navy disc with the knowledge graph, 512 × 512 |
| `mascot-transparent.svg` | Bust, no disc, no background, 512 × 512 |
| `mascot-mono.svg`, `mascot-mono-inverse.svg` | Bust as one-colour line art |
| `mascot-full.svg` | Full body, transparent, 512 × 780 |
| `mascot-full-mono.svg` | Full body as one-colour line art |
| `symbol.svg` | Spark in a rounded navy tile, 128 × 128 |
| `symbol-mono.svg`, `symbol-mono-inverse.svg` | Spark alone, no tile |
| `lockup-symbol.svg`, `lockup-symbol-dark.svg` | Tile or spark plus wordmark |
| `src/` | Illustration sources; the only hand-drawn files |
| `fonts/` | Space Grotesk 2.000 variable font and its SIL OFL 1.1 licence |
| `tools/build.py` | Composes every SVG above and exports the PNGs |
| `png/` | Exports: logos 1600 (light, dark, mono, mono inverse), lockup 1200, mascots 512 (bust, transparent, mono, mono inverse, full body, full body mono), symbols 512 (tile, mono, mono inverse), avatar 128/64, favicon 32/16 |

## One spark

The spark is a single rounded stroke with three straight segments and two
rounded terminals, drawn inside a 128-unit box:

```
M 34 24 L 80 56 L 56 68 L 94 104
stroke-width 15, round caps and joins
```

That path is defined once, in `tools/build.py`, and injected into the symbol,
both lockups and the chest of both illustrations. The chest emblem is the same
`d` and the same stroke, transformed by position and scale, plus the navy
outline the illustration uses on every shape so the yellow survives on the red
shirt. No second interpretation of the mark exists in the repository:
`python3 assets/brand/tools/build.py --check` fails if any file drifts.

## Wordmark

Space Grotesk, weight 500, converted to outlines at build time with fontTools.
Version 2.000, SIL Open Font License 1.1, vendored in `fonts/` together with
`OFL.txt`. Outlining a font does not remove its licence: the outlines remain
derived from the Font Software and the OFL terms apply to them. Do not
redistribute the font on its own, do not sell it, and keep `OFL.txt` next to it.

The knock-on effect is that the wordmark can be rebuilt exactly: change
`WORDMARK` or `WORDMARK_WEIGHT` in `tools/build.py` and rerun the build.

## Palette

| Role | Colour | Contrast |
|---|---|---|
| Ground and ink | `#152238` | 15.9:1 on white |
| Accent | `#FFD43B` | 11.2:1 on navy · 1.4:1 on white |
| Shirt | `#E53935` | 4.2:1 with white on top |
| Secondary | `#2563EB` | 5.2:1 on white |
| Base | `#FFFFFF` | — |
| Skin (illustration only) | `#F2C6A0` | not a brand colour |

Yellow never sits bare on white: it fails contrast as text and as a graphic.
On white, the spark goes inside the navy tile or carries a navy outline. The
skin tone and the hair brown belong to the character, not to the brand palette.

## Rules

- Clear space: the height of the tile on every side. Nothing enters it.
- Minimum size: symbol 16 px, symbol lockup 200 px wide, primary lockup 480 px
  wide. Below that, drop to the symbol.
- Do not deform, rotate, add shadows, gradients or bevels.
- Do not recolour outside the palette. Monochrome means navy on transparent or
  white on transparent, never grey.
- No text inside the symbol. The wordmark is always set beside it or omitted.
- Do not crop the mascot at eye level and do not use it as a small icon.

## Rebuilding

```sh
python3 assets/brand/tools/build.py           # regenerate SVG and PNG
python3 assets/brand/tools/build.py --check   # verify only, write nothing
```

Requires `fontTools`, `rsvg-convert` and, for PNG optimisation, Pillow. The
build writes the composed SVGs, exports the PNGs and fails on a divergent
spark, an external reference, embedded script or a missing export.

## Verification status

Checked by execution on 2026-10-27:

- `tools/build.py --check` exits 0; the spark path is identical in `symbol.svg`,
  `mascot.svg`, `mascot-full.svg`, `logo.svg`, `logo-dark.svg` and both lockups.
- All 15 SVGs contain no `href`, `xlink`, `script`, `foreignObject`, `<image>`
  or `@import`; the only references are local `url(#…)` fragments.
- All 18 PNGs in `png/` were re-exported from their SVG in this commit and their
  dimensions read back from the IHDR header.
- Renders examined at 16, 32 and 64 px: the spark reads as a diagonal bolt at
  16 px, its three segments resolve from 32 px, and the avatar stays readable at
  64 px. The 16 px silhouette is a shape check, not a detail check.
- PNG output inspected visually for the primary lockup in both backgrounds, the
  symbol lockup, the avatar, the full body and the four monochrome builds.

Not verified: print reproduction, CMYK conversion, and rendering in browsers
other than librsvg (Chromium and Firefox were not exercised).
