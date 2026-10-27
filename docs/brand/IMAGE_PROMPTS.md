# Brand prompts — review and corrected version

`brief_identidad.md` is a good brief and weak prompts. The brief describes the
character, the palette and the constraints precisely. The three prompts that
close it make mistakes no model can solve on its own.

This document does not replace the brief: it translates it into instructions a
generator can execute.

## Verdict

The current prompts are good for exploring directions, not for producing the
logo. Three things break them:

1. **They ask for text.** `Include the exact text DrCooper in a modern geometric
   sans-serif wordmark` is the most reliable way to get typographic garbage.
   Image models do not typeset letters: they draw them. Even when they get a
   short word right, the result is not a logotype, it is a drawing of a logotype.
2. **They ask for "a yellow lightning bolt".** A bolt with no defined geometry
   converges on the Flash emblem, which is exactly what section 5 forbids. The
   prohibition does not help: the model has no negative catalogue of brands, it
   has a distribution, and "red shirt + yellow lightning bolt" is saturated with
   that reference.
3. **They describe three different characters.** Half body, bust and
   head-and-shoulders with different framing and detail produce three different
   faces. Without a fixed character sheet the mascot is not a character, it is a
   coincidence.

Two minor problems: naming Sheldon Cooper in the prompt *increases* the
resemblance, because the name is a strong semantic cue; and "glasses mandatory"
is not an instruction, it is an ambiguity the model resolves by adding glasses
and a lab coat.

## The seven fixes

| # | What fails | Fix |
|---|---|---|
| 1 | Text inside the image | Generate without text. The wordmark is composed as vector type |
| 2 | Generic bolt | Define the mark by geometry: three segments, two terminals, rounded stroke |
| 3 | Three different characters | One identical character sheet in both character prompts, and the same seed |
| 4 | Naming what is forbidden | Describe positive traits; keep negatives free of brands and people |
| 5 | Ambiguous accessories | Explicitly deny glasses, lab coat, bow tie and gadgets |
| 6 | No delivery format | Fix aspect ratio, resolution, background and number of variants |
| 7 | Logo and mascot mixed | Separate them: the symbol identifies, the mascot illustrates |

## Character sheet

This block is fixed. It goes literally into both character prompts and does not
change between generations.

> Original character, not based on any existing person or fictional character. Male, late twenties, slim build, oversized cartoon head roughly one third of total height. Short dark brown hair (#3A2A22) with a clean side part on his right and a single small cowlick at the crown. Warm mid-tone skin (#F2C6A0). Large almond eyes with dark navy irises and a single highlight dot, thick straight eyebrows, straight nose, asymmetric closed-mouth half-smile with the left corner slightly higher. Calm, analytical, faintly amused expression. Bright red crew-neck t-shirt (#E53935) with a darker red collar band (#C62828). No glasses, no lab coat, no bow tie, no badge, no lanyard, no text anywhere. Flat vector cartoon, clean 4 px navy outlines (#152238), flat fills, no gradients, no texture, no photorealism.

The spark on his chest, described so the Flash bolt does not come out:

> On the chest, one small emblem: a lightning mark drawn as a single rounded stroke with three straight segments — down-right, a short back-step left, then down-right again — ending in two rounded terminals. It reads as a spark, not as a comic-book bolt silhouette. Solid #FFD43B, no outline, no double stroke.

## Prompt 1 — mascot (half body, no text)

```
[CHARACTER SHEET]

Half-body composition, three-quarter view turned slightly to his left, looking at the viewer.
Centered with generous margin. Flat solid background #152238, no gradient, no vignette.
Behind him, at very low opacity, a sparse knowledge graph: four small #2563EB nodes
joined by thin lines, clearly secondary and never overlapping the face.
Style: modern flat vector cartoon for a developer tool, confident geometric shapes,
restrained shading limited to one soft shadow tone, crisp edges.
Square 1:1 canvas, 2048 px. No text, no letters, no watermark, no frame.
```

## Prompt 2 — GitHub avatar (bust, 1:1)

```
[CHARACTER SHEET]

Bust portrait, head and shoulders, facing the viewer, symmetrical framing,
head occupying 70% of the canvas height, small margin above the hair.
Flat solid #152238 background filling the square. The composition must survive
being cropped to a circle: nothing important outside the central 90%.
High contrast between skin, hair and background. Eyes readable when the image
is scaled down to 64 px.
Square 1:1 canvas, 1024 px. No text, no letters, no border, no badge.
```

## Prompt 3 — symbol (no character)

This prompt deliberately contains no character: it produces the reduction, not
a third portrait. The character sheet does not apply and face consistency is
not checked here.

```
Minimal app icon for a developer intelligence tool. A single lightning mark drawn
as one rounded stroke with three straight segments: long diagonal down-right,
a short horizontal back-step to the left, then a second long diagonal down-right.
Rounded line caps and joins, stroke weight 12% of the icon width.
Solid #FFD43B on a #152238 rounded square, corner radius 23%.
Perfectly centered, generous padding of 22% on each side.
Flat vector, no gradient, no shadow, no outline, no 3D, no text, no letters.
Must remain legible at 16 px: thick stroke, no thin details, no decoration.
Square 1:1 canvas, 1024 px.
```

## Negatives

Passed in the negative field, not inside the positive prompt:

```
text, letters, words, typography, watermark, signature, logo of an existing brand,
comic-book bolt silhouette, superhero insignia, glasses, spectacles, lab coat,
bow tie, pocket protector, graduation cap, stethoscope, clipboard, 3D render,
gradient, glow, neon, drop shadow, photorealism, photograph, anime, chibi,
extra fingers, deformed hands, two heads, asymmetric eyes, cropped head
```

## Parameters

- **Fixed seed** while the character is being tuned; change it only to explore.
- **Image reference** for prompt 2: start from the chosen portrait and ask for
  the new framing. It is the only reliable way to keep the same face.
- **Solid background**, never "transparent". Models fake transparency with a
  checkerboard or a halo, and then it has to be cut out by hand.
- **Four variants per prompt** minimum. The first one is usually the average.
- **Do not ask for the full logo.** Ask for the symbol and the character
  separately; the lockup is composed afterwards as vector.

## Acceptance checklist

- [ ] The face is identical in the two images that contain the character
      (prompts 1 and 2). Prompt 3 has no face and is exempt.
- [ ] The chest emblem in both character images follows the three-segment
      geometry above, not a comic-book bolt silhouette.
- [ ] No text, letters or fragments of letters on any edge.
- [ ] No glasses, no lab coat, no accessories that were not asked for.
- [ ] The avatar still reads at 64 px and is not cut when cropped to a circle.
- [ ] The symbol is distinguishable at 16 px.
- [ ] No element resembles an existing registered mark.

When an image passes the checklist it is vectorised: traced by hand or with a
tracer, then cleaned. A generated PNG is not a brand asset: it does not scale,
it cannot be recoloured and its stroke cannot be adjusted.
