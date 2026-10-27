#!/usr/bin/env python3
"""Build the DrCooper brand assets from a single source.

Sources:
  src/mascot-bust.svg   illustration, bust, transparent
  src/mascot-full.svg   illustration, full body, transparent
  fonts/                Space Grotesk 2.000 (SIL OFL 1.1) for the wordmark

Generated (do not edit by hand):
  symbol.svg, symbol-mono.svg, symbol-mono-inverse.svg
  mascot.svg, mascot-transparent.svg, mascot-mono.svg, mascot-mono-inverse.svg
  mascot-full.svg, mascot-full-mono.svg
  logo.svg, logo-dark.svg, logo-mono.svg, logo-mono-inverse.svg
  lockup-symbol.svg, lockup-symbol-dark.svg
  png/*.png

The spark geometry lives in SPARK and nowhere else: it is injected into the
symbol, both lockups and the chest of both illustrations.

Usage:
  python3 assets/brand/tools/build.py           # rebuild everything
  python3 assets/brand/tools/build.py --check   # verify only, write nothing

Requires fontTools and rsvg-convert.
"""

from __future__ import annotations

import argparse
import math
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

BRAND = Path(__file__).resolve().parent.parent
SRC = BRAND / "src"
PNG = BRAND / "png"
FONT = BRAND / "fonts" / "SpaceGrotesk[wght].ttf"

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

# The spark: three straight segments between two terminals, drawn as one
# rounded stroke in a 128-unit box. Same `d` everywhere it appears.
SPARK_D = "M 34 24 L 80 56 L 56 68 L 94 104"
SPARK_W = 15
SPARK_BOX = 128

INK = "#152238"
YELLOW = "#FFD43B"
RED = "#E53935"
BLUE = "#2563EB"
WHITE = "#FFFFFF"

WORDMARK = "DrCooper"
WORDMARK_WEIGHT = 500
CAP_RATIO = 0.700  # Space Grotesk cap height / em


def fnum(value: float) -> str:
    text = f"{value:.2f}".rstrip("0").rstrip(".")
    return text if text not in ("", "-0") else "0"


def fscale(value: float) -> str:
    """Transform scales need more precision than glyph coordinates: the mono
    build must overlay the colour build exactly."""
    return f"{value:.4f}".rstrip("0").rstrip(".")


def spark_path(stroke: str = YELLOW, width: float = SPARK_W, fill: str = "none") -> str:
    return (
        f'<path d="{SPARK_D}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{fnum(width)}" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def spark_chest(scale: float, halo: float = 9.0) -> str:
    """Chest emblem: the same path and stroke as the symbol, plus the
    illustration's outline so it survives on the red shirt."""
    halo_width = SPARK_W + 2 * halo / scale
    return spark_path(INK, halo_width) + spark_path(YELLOW, SPARK_W)


# --------------------------------------------------------------------------
# Wordmark
# --------------------------------------------------------------------------

_font = None


def font():
    global _font
    if _font is None:
        from fontTools.ttLib import TTFont
        from fontTools.varLib.instancer import instantiateVariableFont

        _font = instantiateVariableFont(TTFont(FONT), {"wght": WORDMARK_WEIGHT}, inplace=True)
    return _font


def wordmark(fill: str, size: float, baseline: float, x: float) -> tuple[str, float]:
    """Outline the wordmark from the vendored font.

    Returns (svg fragment, advance width in user units).
    """
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen

    face = font()
    glyphs = face.getGlyphSet()
    cmap = face.getBestCmap()
    advances = face["hmtx"]

    scale = size / face["head"].unitsPerEm
    cursor = x
    paths = []
    for char in WORDMARK:
        name = cmap[ord(char)]
        pen = SVGPathPen(glyphs, ntos=fnum)
        glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, cursor, baseline)))
        paths.append(pen.getCommands())
        cursor += advances[name][0] * scale

    d = " ".join(paths)
    return f'<g id="wordmark" fill="{fill}"><path d="{d}"/></g>', cursor - x


# --------------------------------------------------------------------------
# Illustration composition
# --------------------------------------------------------------------------

def _inject_spark(root, mono: str | None) -> None:
    for index, group in enumerate(list(root)):
        if group.get("data-spark") != "chest":
            continue
        transform = group.get("transform")
        scale = float(re.search(r"scale\(([\d.]+)\)", transform).group(1))
        markup = spark_path(mono, SPARK_W) if mono else spark_chest(scale)
        wrapper = ET.fromstring(f'<g xmlns="{SVG_NS}" id="spark">{markup}</g>')
        wrapper.set("transform", transform)
        root.remove(group)
        root.insert(index, wrapper)


def _mono_geometry(group) -> list:
    """White paints ink, black cuts a hole. Strokes only: the mono build is
    line art, never a filled silhouette."""
    copy = ET.fromstring(ET.tostring(group))
    gid = copy.get("id", "")
    if gid.startswith("glint"):
        for shape in copy.iter():
            if shape is not copy:
                shape.set("fill", "#000000")
                shape.set("stroke", "none")
    elif gid.startswith("pupil"):
        for shape in copy.iter():
            if shape is not copy:
                shape.set("fill", "#FFFFFF")
                shape.set("stroke", "none")
    elif gid.endswith("-skin") or gid.endswith("-red"):
        # Inner stroke of a capsule pair: cut it out so the limb reads as an
        # outlined shape, not a solid bar.
        copy.set("fill", "none")
        copy.set("stroke", "#000000")
    else:
        copy.set("fill", "none")
        copy.set("stroke", "#FFFFFF")

    nodes = [copy]
    if gid in ("head", "shirt"):
        # Knock out whatever sits behind this shape so the line art does not
        # show the edges of hidden parts through it (neck inside the shirt,
        # neck inside the head).
        knockout = ET.fromstring(ET.tostring(group))
        knockout.set("fill", "#000000")
        knockout.set("stroke", "none")
        nodes.insert(0, knockout)
    return nodes


def art_markup(name: str, mono: str | None = None, indent: str = "  ") -> str:
    """Return the illustration as indented SVG markup, spark injected."""
    root = ET.parse(SRC / name).getroot()
    _inject_spark(root, mono)

    nodes = list(root)
    if mono:
        nodes = [shape for node in root for shape in _mono_geometry(node)]
    wrapper = ET.Element("g")
    wrapper.extend(nodes)
    ET.indent(wrapper, "  ")

    text = ET.tostring(wrapper, encoding="unicode")
    text = text.replace(f' xmlns="{SVG_NS}"', "")
    lines = text.splitlines()
    body = lines[1:-1]  # drop the synthetic <g> wrapper
    return "\n".join(indent + line for line in body)


def svg_document(viewbox: str, body: str, title: str, width: str | None = None,
                 height: str | None = None) -> str:
    size = ""
    if width:
        size += f' width="{width}"'
    if height:
        size += f' height="{height}"'
    return (
        f'<svg xmlns="{SVG_NS}" viewBox="{viewbox}"{size} role="img" '
        f'aria-labelledby="t">\n'
        f'  <title id="t">{title}</title>\n'
        f"{body}\n"
        f"</svg>\n"
    )


def mono_document(viewbox: str, art: str, title: str, ink: str) -> str:
    _, _, w, h = viewbox.split() if len(viewbox.split()) == 4 else viewbox.split()
    body = (
        f'  <mask id="mono" maskUnits="userSpaceOnUse" x="0" y="0" '
        f'width="{w}" height="{h}">\n'
        f"{art}\n"
        f"  </mask>\n"
        f'  <rect x="0" y="0" width="{w}" height="{h}" fill="{ink}" mask="url(#mono)"/>'
    )
    return svg_document(viewbox, body, title)


GRAPH = """    <g stroke="#2563EB" stroke-width="3" opacity="0.30" fill="none">
      <path d="M 44 98 L 96 66 L 142 102"/>
      <path d="M 370 72 L 424 104 L 470 70"/>
      <path d="M 28 252 L 64 234"/>
    </g>
    <g fill="#2563EB" opacity="0.30">
      <circle cx="44" cy="98" r="6"/><circle cx="96" cy="66" r="7"/><circle cx="142" cy="102" r="5"/>
      <circle cx="370" cy="72" r="5"/><circle cx="424" cy="104" r="7"/><circle cx="470" cy="70" r="5"/>
      <circle cx="28" cy="252" r="5"/><circle cx="64" cy="234" r="5"/>
    </g>"""


# --------------------------------------------------------------------------
# Assets
# --------------------------------------------------------------------------

def build_symbols() -> dict[str, str]:
    return {
        "symbol.svg": svg_document(
            "0 0 128 128",
            f'  <rect width="128" height="128" rx="30" fill="{INK}"/>\n  {spark_path()}',
            "DrCooper symbol",
            width="128",
            height="128",
        ),
        "symbol-mono.svg": svg_document(
            "0 0 128 128", f"  {spark_path(INK)}", "DrCooper symbol, monochrome",
            width="128", height="128",
        ),
        "symbol-mono-inverse.svg": svg_document(
            "0 0 128 128", f"  {spark_path(WHITE)}", "DrCooper symbol, monochrome inverse",
            width="128", height="128",
        ),
    }


def build_mascots() -> dict[str, str]:
    bust = art_markup("mascot-bust.svg")
    full = art_markup("mascot-full.svg")
    return {
        "mascot.svg": svg_document(
            "0 0 512 512",
            '  <defs><clipPath id="disc"><circle cx="256" cy="256" r="256"/></clipPath></defs>\n'
            '  <g clip-path="url(#disc)">\n'
            f'    <rect width="512" height="512" fill="{INK}"/>\n'
            f"{GRAPH}\n"
            f"{bust}\n"
            "  </g>",
            "DrCooper mascot",
            width="512",
            height="512",
        ),
        "mascot-transparent.svg": svg_document(
            "0 0 512 512", bust, "DrCooper mascot, transparent", width="512", height="512"
        ),
        "mascot-mono.svg": mono_document(
            "0 0 512 512", art_markup("mascot-bust.svg", mono=WHITE),
            "DrCooper mascot, monochrome", INK,
        ),
        "mascot-mono-inverse.svg": mono_document(
            "0 0 512 512", art_markup("mascot-bust.svg", mono=WHITE),
            "DrCooper mascot, monochrome inverse", WHITE,
        ),
        "mascot-full.svg": svg_document(
            "0 0 512 780", full, "DrCooper mascot, full body", width="512", height="780"
        ),
        "mascot-full-mono.svg": mono_document(
            "0 0 512 780", art_markup("mascot-full.svg", mono=WHITE),
            "DrCooper mascot, full body, monochrome", INK,
        ),
    }


def build_lockups() -> dict[str, str]:
    """Primary lockup: the mascot first, the wordmark second."""
    height = 320
    art_scale = height / 512
    gap = 56
    cap = 96
    size = cap / CAP_RATIO
    baseline = height / 2 + cap / 2
    x = 8 + height + gap

    mascot = art_markup("mascot-bust.svg", indent="    ")
    mascot_mono = art_markup("mascot-bust.svg", mono=WHITE, indent="    ")

    light_word, width = wordmark(INK, size, baseline, x)
    dark_word, _ = wordmark(WHITE, size, baseline, x)
    mono_word, _ = wordmark(INK, size, baseline, x)
    mono_word_inverse, _ = wordmark(WHITE, size, baseline, x)
    total = int(math.ceil(x + width + 8))
    viewbox = f"0 0 {total} {height}"

    mascot_group = (
        f'  <g transform="translate(8 0) scale({fscale(art_scale)})">\n'
        f"{mascot}\n"
        f"  </g>"
    )

    def primary(word: str, title: str) -> str:
        return svg_document(
            viewbox, f"{mascot_group}\n  {word}", title,
            width=str(total), height=str(height),
        )

    def primary_mono(word: str, ink: str, title: str) -> str:
        body = (
            f'  <mask id="mono" maskUnits="userSpaceOnUse" x="0" y="0" '
            f'width="{total}" height="{height}">\n'
            f'    <g transform="translate(8 0) scale({fscale(art_scale)})">\n'
            f"{mascot_mono}\n"
            f"    </g>\n"
            f"  </mask>\n"
            f'  <rect x="0" y="0" width="{total}" height="{height}" '
            f'fill="{ink}" mask="url(#mono)"/>\n'
            f"  {word}"
        )
        return svg_document(viewbox, body, title, width=str(total), height=str(height))

    # Secondary lockup: symbol + wordmark, for widths where the mascot fails.
    tile_gap = 40
    sym_size = 0.096 * 1000
    sym_baseline = 64 + 0.7 * sym_size / 2
    sym_word, sym_width = wordmark(INK, sym_size, sym_baseline, SPARK_BOX + tile_gap)
    dark_word_sym, _ = wordmark(WHITE, sym_size, sym_baseline, 112)

    sym_width_total = int(math.ceil(SPARK_BOX + tile_gap + sym_width + 8))
    dark_width_total = int(math.ceil(112 + sym_width + 8))

    return {
        "logo.svg": primary(light_word, "DrCooper"),
        "logo-dark.svg": primary(dark_word, "DrCooper"),
        "logo-mono.svg": primary_mono(mono_word, INK, "DrCooper, monochrome"),
        "logo-mono-inverse.svg": primary_mono(
            mono_word_inverse, WHITE, "DrCooper, monochrome inverse"
        ),
        "lockup-symbol.svg": svg_document(
            f"0 0 {sym_width_total} 128",
            f'  <rect width="128" height="128" rx="30" fill="{INK}"/>\n'
            f"  {spark_path()}\n"
            f"  {sym_word}",
            "DrCooper symbol lockup",
            width=str(sym_width_total),
            height="128",
        ),
        "lockup-symbol-dark.svg": svg_document(
            f"0 0 {dark_width_total} 128",
            f'  <g transform="translate(0 6.4) scale(0.9)">{spark_path()}</g>\n'
            f"  {dark_word_sym}",
            "DrCooper symbol lockup for dark backgrounds",
            width=str(dark_width_total),
            height="128",
        ),
    }


EXPORTS = [
    ("logo.svg", "logo-1600.png", {"width": 1600}),
    ("logo-dark.svg", "logo-dark-1600.png", {"width": 1600}),
    ("logo-mono.svg", "logo-mono-1600.png", {"width": 1600}),
    ("logo-mono-inverse.svg", "logo-mono-inverse-1600.png", {"width": 1600}),
    ("lockup-symbol.svg", "lockup-symbol-1200.png", {"width": 1200}),
    ("symbol.svg", "symbol-512.png", {"width": 512}),
    ("symbol.svg", "favicon-32.png", {"width": 32}),
    ("symbol.svg", "favicon-16.png", {"width": 16}),
    ("symbol-mono.svg", "symbol-mono-512.png", {"width": 512}),
    ("symbol-mono-inverse.svg", "symbol-mono-inverse-512.png", {"width": 512}),
    ("mascot.svg", "mascot-512.png", {"width": 512}),
    ("mascot.svg", "avatar-128.png", {"width": 128}),
    ("mascot.svg", "avatar-64.png", {"width": 64}),
    ("mascot-transparent.svg", "mascot-transparent-512.png", {"width": 512}),
    ("mascot-mono.svg", "mascot-mono-512.png", {"width": 512}),
    ("mascot-mono-inverse.svg", "mascot-mono-inverse-512.png", {"width": 512}),
    ("mascot-full.svg", "mascot-full-512.png", {"width": 512}),
    ("mascot-full-mono.svg", "mascot-full-mono-512.png", {"width": 512}),
]


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def check_no_external(name: str, text: str) -> list[str]:
    problems = []
    if re.search(r"<script|onload=|onerror=|<foreignObject", text):
        problems.append(f"{name}: executable content")
    stripped = text.replace(f'xmlns="{SVG_NS}"', "")
    if re.search(r"href=|xlink:|@import|<image|https?://", stripped):
        problems.append(f"{name}: external reference")
    return problems


def check_spark(files: dict[str, str]) -> list[str]:
    problems = []
    for name in ("symbol.svg", "symbol-mono.svg", "mascot.svg", "mascot-full.svg",
                 "logo.svg", "logo-dark.svg", "lockup-symbol.svg"):
        if SPARK_D not in files[name]:
            problems.append(f"{name}: spark geometry missing or divergent")
    for name, text in files.items():
        count = text.count(SPARK_D)
        if count > 2:
            problems.append(f"{name}: spark duplicated {count} times")
    return problems


def check_png() -> list[str]:
    problems = []
    for _, png, _ in EXPORTS:
        path = PNG / png
        if not path.exists():
            problems.append(f"{png}: missing")
            continue
        if path.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            problems.append(f"{png}: not a PNG")
    return problems


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify only, write nothing")
    args = parser.parse_args()

    files: dict[str, str] = {}
    files.update(build_symbols())
    files.update(build_mascots())
    files.update(build_lockups())

    problems = check_spark(files)
    for name, text in files.items():
        problems += check_no_external(name, text)
    for problem in problems:
        print(f"error: {problem}", file=sys.stderr)

    if args.check:
        for name, text in files.items():
            path = BRAND / name
            if not path.exists():
                problems.append(f"{name}: missing on disk")
                print(f"error: {name}: missing on disk", file=sys.stderr)
            elif path.read_text(encoding="utf-8") != text:
                problems.append(f"{name}: stale, run the build")
                print(f"error: {name}: stale, run the build", file=sys.stderr)
        problems += check_png()
        if problems:
            return 1
        print("brand assets: ok")
        return 0

    PNG.mkdir(exist_ok=True)
    for name, text in files.items():
        (BRAND / name).write_text(text, encoding="utf-8")

    if not shutil.which("rsvg-convert"):
        print("error: rsvg-convert not found, PNG exports not updated", file=sys.stderr)
        return 1

    for source, png, size in EXPORTS:
        command = ["rsvg-convert", "-o", str(PNG / png)]
        for key, value in size.items():
            command += [f"--{key}", str(value)]
        subprocess.run(command + [str(BRAND / source)], check=True)
        _optimize_png(PNG / png)

    problems += check_png()
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1
    print(f"brand assets: {len(files)} SVG, {len(EXPORTS)} PNG")
    return 0


def _optimize_png(path: Path) -> None:
    """Flatten to 8-bit RGBA so the exports stay small."""
    try:
        from PIL import Image
    except ImportError:
        return
    with Image.open(path) as image:
        image.convert("RGBA").save(path, optimize=True)


if __name__ == "__main__":
    raise SystemExit(main())
