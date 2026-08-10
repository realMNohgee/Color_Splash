#!/usr/bin/env python3
"""Terminal color explorer. Preview ANSI/hex/rgb, generate palettes, check contrast ratios. Zero deps."""

from __future__ import annotations

import argparse
import colorsys
import json
import math
import sys
from typing import NamedTuple


# ─── W3C named colors (148 entries) ──────────────────────────────────────────
NAMED_COLORS: dict[str, tuple[int, int, int]] = {
    "aliceblue": (240, 248, 255), "antiquewhite": (250, 235, 215),
    "aqua": (0, 255, 255), "aquamarine": (127, 255, 212),
    "azure": (240, 255, 255), "beige": (245, 245, 220),
    "bisque": (255, 228, 196), "black": (0, 0, 0),
    "blanchedalmond": (255, 235, 205), "blue": (0, 0, 255),
    "blueviolet": (138, 43, 226), "brown": (165, 42, 42),
    "burlywood": (222, 184, 135), "cadetblue": (95, 158, 160),
    "chartreuse": (127, 255, 0), "chocolate": (210, 105, 30),
    "coral": (255, 127, 80), "cornflowerblue": (100, 149, 237),
    "cornsilk": (255, 248, 220), "crimson": (220, 20, 60),
    "cyan": (0, 255, 255), "darkblue": (0, 0, 139),
    "darkcyan": (0, 139, 139), "darkgoldenrod": (184, 134, 11),
    "darkgray": (169, 169, 169), "darkgreen": (0, 100, 0),
    "darkgrey": (169, 169, 169), "darkkhaki": (189, 183, 107),
    "darkmagenta": (139, 0, 139), "darkolivegreen": (85, 107, 47),
    "darkorange": (255, 140, 0), "darkorchid": (153, 50, 204),
    "darkred": (139, 0, 0), "darksalmon": (233, 150, 122),
    "darkseagreen": (143, 188, 143), "darkslateblue": (72, 61, 139),
    "darkslategray": (47, 79, 79), "darkslategrey": (47, 79, 79),
    "darkturquoise": (0, 206, 209), "darkviolet": (148, 0, 211),
    "deeppink": (255, 20, 147), "deepskyblue": (0, 191, 255),
    "dimgray": (105, 105, 105), "dimgrey": (105, 105, 105),
    "dodgerblue": (30, 144, 255), "firebrick": (178, 34, 34),
    "floralwhite": (255, 250, 240), "forestgreen": (34, 139, 34),
    "fuchsia": (255, 0, 255), "gainsboro": (220, 220, 220),
    "ghostwhite": (248, 248, 255), "gold": (255, 215, 0),
    "goldenrod": (218, 165, 32), "gray": (128, 128, 128),
    "grey": (128, 128, 128), "green": (0, 128, 0),
    "greenyellow": (173, 255, 47), "honeydew": (240, 255, 240),
    "hotpink": (255, 105, 180), "indianred": (205, 92, 92),
    "indigo": (75, 0, 130), "ivory": (255, 255, 240),
    "khaki": (240, 230, 140), "lavender": (230, 230, 250),
    "lavenderblush": (255, 240, 245), "lawngreen": (124, 252, 0),
    "lemonchiffon": (255, 250, 205), "lightblue": (173, 216, 230),
    "lightcoral": (240, 128, 128), "lightcyan": (224, 255, 255),
    "lightgoldenrodyellow": (250, 250, 210), "lightgray": (211, 211, 211),
    "lightgreen": (144, 238, 144), "lightgrey": (211, 211, 211),
    "lightpink": (255, 182, 193), "lightsalmon": (255, 160, 122),
    "lightseagreen": (32, 178, 170), "lightskyblue": (135, 206, 250),
    "lightslategray": (119, 136, 153), "lightslategrey": (119, 136, 153),
    "lightsteelblue": (176, 196, 222), "lightyellow": (255, 255, 224),
    "lime": (0, 255, 0), "limegreen": (50, 205, 50),
    "linen": (250, 240, 230), "magenta": (255, 0, 255),
    "maroon": (128, 0, 0), "mediumaquamarine": (102, 205, 170),
    "mediumblue": (0, 0, 205), "mediumorchid": (186, 85, 211),
    "mediumpurple": (147, 112, 219), "mediumseagreen": (60, 179, 113),
    "mediumslateblue": (123, 104, 238), "mediumspringgreen": (0, 250, 154),
    "mediumturquoise": (72, 209, 204), "mediumvioletred": (199, 21, 133),
    "midnightblue": (25, 25, 112), "mintcream": (245, 255, 250),
    "mistyrose": (255, 228, 225), "moccasin": (255, 228, 181),
    "navajowhite": (255, 222, 173), "navy": (0, 0, 128),
    "oldlace": (253, 245, 230), "olive": (128, 128, 0),
    "olivedrab": (107, 142, 35), "orange": (255, 165, 0),
    "orangered": (255, 69, 0), "orchid": (218, 112, 214),
    "palegoldenrod": (238, 232, 170), "palegreen": (152, 251, 152),
    "paleturquoise": (175, 238, 238), "palevioletred": (219, 112, 147),
    "papayawhip": (255, 239, 213), "peachpuff": (255, 218, 185),
    "peru": (205, 133, 63), "pink": (255, 192, 203),
    "plum": (221, 160, 221), "powderblue": (176, 224, 230),
    "purple": (128, 0, 128), "rebeccapurple": (102, 51, 153),
    "red": (255, 0, 0), "rosybrown": (188, 143, 143),
    "royalblue": (65, 105, 225), "saddlebrown": (139, 69, 19),
    "salmon": (250, 128, 114), "sandybrown": (244, 164, 96),
    "seagreen": (46, 139, 87), "seashell": (255, 245, 238),
    "sienna": (160, 82, 45), "silver": (192, 192, 192),
    "skyblue": (135, 206, 235), "slateblue": (106, 90, 205),
    "slategray": (112, 128, 144), "slategrey": (112, 128, 144),
    "snow": (255, 250, 250), "springgreen": (0, 255, 127),
    "steelblue": (70, 130, 180), "tan": (210, 180, 140),
    "teal": (0, 128, 128), "thistle": (216, 191, 216),
    "tomato": (255, 99, 71), "turquoise": (64, 224, 208),
    "violet": (238, 130, 238), "wheat": (245, 222, 179),
    "white": (255, 255, 255), "whitesmoke": (245, 245, 245),
    "yellow": (255, 255, 0), "yellowgreen": (154, 205, 50),
}


# ─── ANSI color table (0-255 indexed) ─────────────────────────────────────────
ANSI_TO_RGB: list[tuple[int, int, int]] = [
    (0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0),
    (0, 0, 128), (128, 0, 128), (0, 128, 128), (192, 192, 192),
    (128, 128, 128), (255, 0, 0), (0, 255, 0), (255, 255, 0),
    (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255),
]
# 216-color cube (16-231)
for r in range(6):
    for g in range(6):
        for b in range(6):
            ANSI_TO_RGB.append((r * 51 if r > 0 else 0,
                                g * 51 if g > 0 else 0,
                                b * 51 if b > 0 else 0))
# Grayscale (232-255)
for i in range(24):
    v = i * 10 + 8
    ANSI_TO_RGB.append((v, v, v))


class RGB(NamedTuple):
    r: int
    g: int
    b: int


def _parse_color(raw: str) -> RGB:
    """Parse a color from hex (#ff6600 / #fff), rgb (255 102 0), or ANSI index (208)."""
    s = raw.strip().lower()
    # ANSI color index
    if s.isdigit():
        idx = int(s)
        if 0 <= idx < len(ANSI_TO_RGB):
            return RGB(*ANSI_TO_RGB[idx])
        raise ValueError(f"ANSI color index {idx} out of range (0-{len(ANSI_TO_RGB)-1})")
    # RGB triple: "255 102 0" or "255,102,0"
    parts = s.replace(",", " ").split()
    if len(parts) == 3 and all(p.isdigit() for p in parts):
        r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
        if all(0 <= v <= 255 for v in (r, g, b)):
            return RGB(r, g, b)
        raise ValueError("RGB values must be 0-255")
    # Named color
    if s in NAMED_COLORS:
        return RGB(*NAMED_COLORS[s])
    # Hex
    if s.startswith("#"):
        s = s[1:]
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) == 6:
        try:
            return RGB(int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))
        except ValueError:
            pass
    raise ValueError(f"Cannot parse color: {raw}")


def _render_swatch(r: int, g: int, b: int, width: int = 10) -> str:
    """Return an ANSI true-color block of the given RGB."""
    block = " " * width
    return f"\033[48;2;{r};{g};{b}m{block}\033[0m"


def _relative_luminance(r: int, g: int, b: int) -> float:
    """WCAG 2.1 relative luminance."""
    def _linearize(c: int) -> float:
        s = c / 255.0
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4
    return 0.2126 * _linearize(r) + 0.7152 * _linearize(g) + 0.0722 * _linearize(b)


def _contrast_ratio(l1: float, l2: float) -> float:
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def _rgb_to_hsl(r: int, g: int, b: int) -> tuple[float, float, float]:
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    return h, s, l


def _hsl_to_rgb(h: float, s: float, l_: float) -> tuple[int, int, int]:
    r, g, b = colorsys.hls_to_rgb(h, l_, s)
    return (round(r * 255), round(g * 255), round(b * 255))


def _euclidean(rgb1: RGB, rgb2: RGB) -> float:
    return math.sqrt((rgb1.r - rgb2.r) ** 2 + (rgb1.g - rgb2.g) ** 2 + (rgb1.b - rgb2.b) ** 2)


# ─── Subcommands ──────────────────────────────────────────────────────────────

def _cmd_preview(args: argparse.Namespace) -> int:
    """Preview a color with an ANSI swatch."""
    try:
        rgb = _parse_color(args.color)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps({"color": args.color, "rgb": [rgb.r, rgb.g, rgb.b],
                          "hex": f"#{rgb.r:02x}{rgb.g:02x}{rgb.b:02x}"}))
        return 0

    swatch = _render_swatch(rgb.r, rgb.g, rgb.b, width=20)
    print(f"  {swatch}")
    print(f"  #{rgb.r:02x}{rgb.g:02x}{rgb.b:02x}  rgb({rgb.r}, {rgb.g}, {rgb.b})")
    return 0


def _cmd_palette(args: argparse.Namespace) -> int:
    """Generate a color palette."""
    try:
        base = _parse_color(args.base)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    h, s, l_ = _rgb_to_hsl(base.r, base.g, base.b)
    ptype = args.type  # complementary, triadic, analogous, monochromatic
    count = args.count

    hues: list[float] = []

    if ptype == "complementary":
        hues = [(h + 0.5) % 1.0]
    elif ptype == "triadic":
        hues = [(h + 1/3) % 1.0, (h + 2/3) % 1.0]
    elif ptype == "analogous":
        hues = [(h + 0.05 * i) % 1.0 for i in range(-count // 2, (count + 1) // 2)]
    elif ptype == "monochromatic":
        hues = [h] * count

    palette_rgbs: list[RGB] = [base]
    for hue in hues:
        palette_rgbs.append(RGB(*_hsl_to_rgb(hue, s, l_)))

    if args.format == "json":
        out = [{"hex": f"#{r:02x}{g:02x}{b:02x}", "rgb": [r, g, b]}
               for r, g, b in palette_rgbs]
        print(json.dumps(out, indent=2))
        return 0

    # Text: render swatches side by side
    line = ""
    for rgb in palette_rgbs:
        line += _render_swatch(rgb.r, rgb.g, rgb.b, width=6)
    print(line)
    for i, rgb in enumerate(palette_rgbs):
        marker = "▶" if i == 0 else " "
        print(f"  {marker} #{rgb.r:02x}{rgb.g:02x}{rgb.b:02x}")
    return 0


def _cmd_name(args: argparse.Namespace) -> int:
    """Find the closest named CSS color."""
    try:
        rgb = _parse_color(args.color)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    best_name = ""
    best_dist = float("inf")
    for name, (nr, ng, nb) in NAMED_COLORS.items():
        d = _euclidean(rgb, RGB(nr, ng, nb))
        if d < best_dist:
            best_dist = d
            best_name = name

    named_rgb = NAMED_COLORS[best_name]

    if args.format == "json":
        print(json.dumps({
            "input": f"#{rgb.r:02x}{rgb.g:02x}{rgb.b:02x}",
            "closest_name": best_name,
            "closest_hex": f"#{named_rgb[0]:02x}{named_rgb[1]:02x}{named_rgb[2]:02x}",
            "distance": round(best_dist, 2)
        }))
        return 0

    print(f"  Input: {_render_swatch(rgb.r, rgb.g, rgb.b, width=6)} #{rgb.r:02x}{rgb.g:02x}{rgb.b:02x}")
    print(f"  Closest named: {_render_swatch(*named_rgb, width=6)} {best_name}  #{named_rgb[0]:02x}{named_rgb[1]:02x}{named_rgb[2]:02x}")
    return 0


def _cmd_contrast(args: argparse.Namespace) -> int:
    """Check WCAG contrast ratio between two colors."""
    try:
        fg = _parse_color(args.fg)
        bg = _parse_color(args.bg)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    l_fg = _relative_luminance(fg.r, fg.g, fg.b)
    l_bg = _relative_luminance(bg.r, bg.g, bg.b)
    ratio = _contrast_ratio(l_fg, l_bg)

    aa_normal = ratio >= 4.5
    aaa_normal = ratio >= 7.0
    aa_large = ratio >= 3.0
    aaa_large = ratio >= 4.5

    if args.format == "json":
        print(json.dumps({
            "fg": f"#{fg.r:02x}{fg.g:02x}{fg.b:02x}",
            "bg": f"#{bg.r:02x}{bg.g:02x}{bg.b:02x}",
            "contrast_ratio": round(ratio, 2),
            "wcag_aa_normal": aa_normal,
            "wcag_aaa_normal": aaa_normal,
            "wcag_aa_large": aa_large,
            "wcag_aaa_large": aaa_large,
        }))
        return 0

    def _check(ok: bool) -> str:
        return "✅ PASS" if ok else "❌ FAIL"

    print(f"  FG: {_render_swatch(fg.r, fg.g, fg.b, width=6)} #{fg.r:02x}{fg.g:02x}{fg.b:02x}")
    print(f"  BG: {_render_swatch(bg.r, bg.g, bg.b, width=6)} #{bg.r:02x}{bg.g:02x}{bg.b:02x}")
    print(f"  Contrast ratio: {ratio:.2f}:1")
    print(f"  AA  (normal text): {_check(aa_normal)}")
    print(f"  AAA (normal text): {_check(aaa_normal)}")
    print(f"  AA  (large text):  {_check(aa_large)}")
    print(f"  AAA (large text):  {_check(aaa_large)}")
    return 0


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def _cmd_gradient(args: argparse.Namespace) -> int:
    """Render a horizontal gradient bar."""
    try:
        fr = _parse_color(args.from_)
        to = _parse_color(args.to)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    steps = args.steps

    if args.format == "json":
        grad = []
        for i in range(steps):
            t = i / max(steps - 1, 1)
            r = round(_lerp(fr.r, to.r, t))
            g = round(_lerp(fr.g, to.g, t))
            b = round(_lerp(fr.b, to.b, t))
            grad.append({"hex": f"#{r:02x}{g:02x}{b:02x}", "rgb": [r, g, b]})
        print(json.dumps(grad, indent=2))
        return 0

    # Text: render one block per step
    line = ""
    for i in range(steps):
        t = i / max(steps - 1, 1)
        r = round(_lerp(fr.r, to.r, t))
        g = round(_lerp(fr.g, to.g, t))
        b = round(_lerp(fr.b, to.b, t))
        line += _render_swatch(r, g, b, width=3)
    print(line)
    print(f"  #{fr.r:02x}{fr.g:02x}{fr.b:02x}  ⟶  #{to.r:02x}{to.g:02x}{to.b:02x}")
    return 0


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--format", choices=["text", "json"], default="text",
                        help="Output format (default: text)")

    p = argparse.ArgumentParser(
        prog="color_splash",
        description="Terminal color explorer. Preview, palette, contrast, gradient."
    )
    sub = p.add_subparsers(dest="cmd")
    sub.required = True

    # preview
    sp = sub.add_parser("preview", parents=[common],
                         help="Show a color swatch in terminal")
    sp.add_argument("color", help="Color: hex (#ff6600), rgb (255 102 0), ANSI index (208), or named")
    sp.set_defaults(func=_cmd_preview)

    # palette
    sp = sub.add_parser("palette", parents=[common],
                         help="Generate a color palette")
    sp.add_argument("--type", choices=["complementary", "triadic", "analogous", "monochromatic"],
                    default="complementary", help="Palette type (default: complementary)")
    sp.add_argument("--count", type=int, default=5,
                    help="Number of colors (default: 5)")
    sp.add_argument("--base", default="#ff6600",
                    help="Base color (default: #ff6600)")
    sp.set_defaults(func=_cmd_palette)

    # name
    sp = sub.add_parser("name", parents=[common],
                         help="Find closest named CSS color")
    sp.add_argument("color", help="Color: hex, rgb triple, or ANSI index")
    sp.set_defaults(func=_cmd_name)

    # contrast
    sp = sub.add_parser("contrast", parents=[common],
                         help="WCAG contrast ratio between two colors")
    sp.add_argument("fg", help="Foreground color")
    sp.add_argument("bg", help="Background color")
    sp.set_defaults(func=_cmd_contrast)

    # gradient
    sp = sub.add_parser("gradient", parents=[common],
                         help="Render a horizontal gradient bar")
    sp.add_argument("from_", metavar="from", help="Start color")
    sp.add_argument("to", help="End color")
    sp.add_argument("--steps", type=int, default=20,
                    help="Number of steps (default: 20)")
    sp.set_defaults(func=_cmd_gradient)

    args = p.parse_args()
    if not hasattr(args, "func"):
        p.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
