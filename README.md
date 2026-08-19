# Color_Splash 🎨
![CI](https://github.com/realMNohgee/Color_Splash/actions/workflows/ci.yml/badge.svg) ![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

**Terminal color explorer. Preview ANSI/hex/rgb, generate palettes, check contrast ratios. Zero deps.**

> Part of the **Hermtica Tool Suite** — free, zero-dependency CLI tools for developers and agent builders.

## Why it exists

Working with colors on the command line shouldn't require opening a browser or a GUI app. Color_Splash puts ANSI true-color swatches, WCAG contrast checks, palette generation, and CSS color naming right in your terminal — using only Python's standard library.

## One tool, many domains

| Domain | What Color_Splash does |
|---|---|
| **DevOps** | Verify terminal color rendering, embed color swatches in CI logs |
| **Security** | Check WCAG color contrast ratios for accessibility compliance |
| **Agentic AI** | Let AI agents preview and validate color choices programmatically via `--format json` |
| **Design** | Generate complementary/triadic/analogous palettes, find closest named CSS colors |

## Install

```bash
git clone git@github.com:realMNohgee/Color_Splash.git
cd Color_Splash
python3 color_splash.py --help
```

## Quick start

```bash
# Preview a color
python3 color_splash.py preview "#ff6600"
python3 color_splash.py preview "255 102 0"
python3 color_splash.py preview orange

# Generate a triadic palette from blue
python3 color_splash.py palette --type triadic --base "#3366ff" --count 5

# Find the closest named CSS color
python3 color_splash.py name "#fa8072"

# Check WCAG contrast ratio
python3 color_splash.py contrast "#ffffff" "#1a1a2e"

# Render a gradient bar
python3 color_splash.py gradient "#ff0000" "#0000ff" --steps 40

# Machine-readable JSON output
python3 color_splash.py preview "#ff6600" --format json
python3 color_splash.py contrast "#fff" "#333" --format json
```

## Subcommands

| Command | Description |
|---|---|
| `preview <color>` | Show a color swatch in terminal using ANSI true-color blocks |
| `palette` | Generate color palettes (complementary, triadic, analogous, monochromatic) |
| `name <color>` | Find the closest W3C named CSS color (~150 names, Euclidean distance) |
| `contrast <fg> <bg>` | WCAG 2.1 contrast ratio with AA/AAA pass/fail for normal and large text |
| `gradient <from> <to>` | Render a horizontal gradient bar with configurable step count |

## Color formats accepted

- Hex: `#ff6600`, `#f60`, `ff6600`
- RGB triple: `255 102 0` or `255,102,0`
- ANSI 256-color index: `208`
- W3C named colors: `orange`, `cyan`, `rebeccapurple`

## License

MIT — see [LICENSE](LICENSE).

---
🧰 **[Tool on Hermtica Marketplace](https://hermtica.com/marketplace)**
