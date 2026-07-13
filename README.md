# superemoji-latex

Semantic emoji macros for LaTeX. Use stable keys like `\emoji{status-ok1}` or `\emoji{gis-select1}` instead of raw Unicode emoji in your `.tex` files. The package contains **2403 emoji definitions** organized into semantic categories.

## Requirements

- **LuaLaTeX** (required for color emoji rendering)
- **Twemoji Mozilla** font installed (COLR/CPAL vector format—works reliably with LuaLaTeX)

### Installing Twemoji Mozilla

The canonical build is `mozilla/twemoji-colr v0.7.0`, packaged on CTAN as **`twemoji-colr`**.

**Recommended (all platforms) — install into your TeX tree** so LuaLaTeX finds it with no system-font install:
```bash
tlmgr install twemoji-colr      # TeX Live
mpm --install=twemoji-colr      # MiKTeX
```

**Windows (system font):**  
Download `twemoji-colr.zip` from [CTAN](https://mirrors.ctan.org/fonts/twemoji-colr.zip), extract it, and install `TwemojiMozilla.ttf`.

**Linux (Debian/Ubuntu):**
```bash
sudo apt install fonts-twemoji-svginot
```

**Linux (Fedora):**
```bash
sudo dnf install twitter-twemoji-fonts
```

**macOS:**
```bash
brew install --cask font-twemoji
```

> **Note:** The Linux/macOS distro packages above are *different builds* of Twemoji (often a newer, SVG-in-OpenType repertoire) than the canonical `mozilla/twemoji-colr v0.7.0` this package targets. Glyph coverage can differ. For guaranteed consistency, prefer the CTAN `twemoji-colr` package.

### Alternative: Noto Color Emoji

If you prefer Noto Color Emoji, install it and adjust the font name in your document:

```latex
\renewfontfamily\EmojiFont{Noto Color Emoji}[Renderer=HarfBuzz]
```

## Files

| File | Description |
|------|-------------|
| `superemoji.sty` | LaTeX package providing the `\emoji{...}` macro |
| `emoji-map.tex` | Generated `\emojiDefine{key}{emoji}` definitions (2403 emojis) |
| `superemoji-doc.pdf` | Complete reference with all 2403 emojis |
| `README.md` | Installation and usage guide |

## Installation

### From CTAN (TeX Live / MiKTeX)

The package will be available through your TeX distribution's package manager once published to CTAN.

### Manual Installation

Place the files somewhere TeX can find them (or next to your document).

```bash
git clone https://github.com/Nyphur84/superemoji-latex.git
```

## Usage

Minimal example (**compile with LuaLaTeX**):

```latex
\documentclass{article}
\usepackage{fontspec}
\usepackage{etoolbox}
\usepackage{superemoji}

\newfontfamily\EmojiFont{Twemoji Mozilla}[Renderer=HarfBuzz]
\renewcommand{\emoji}[1]{%
  \ifcsdef{emoji@#1}{{\EmojiFont\csname emoji@#1\endcsname}}{?}%
}

\begin{document}

Status OK: \emoji{status-ok1}

Debug: \emoji{log-debug1}

GIS Select: \emoji{gis-select1}

Happy: \emoji{emo-joy1}

Flag DE: \emoji{flag-de}

\end{document}
```

Compile with:
```bash
lualatex yourdocument.tex
```

## Categories

The mapping covers:

- **Status & Logs:** `status-ok1`, `status-error1`, `log-debug1`, `log-critical1`
- **GIS & Mapping:** `gis-select1`, `gis-buffer1`, `gis-clip1`, `map-pin1`
- **Development:** `code-laptop1`, `tools-gear1`, `data-folder1`
- **Data Quality:** `dq-valid1`, `dq-invalid1`, `dq-duplicate1`
- **I/O Operations:** `io-read1`, `io-write1`, `io-export1`
- **Time & Performance:** `time-alarm1`, `perf-fast1`, `perf-slow1`
- **Emotions:** `emo-joy1`, `emo-sad1`, `emo-thinking1`, `emo-party1`
- **Flags:** `flag-de`, `flag-eu`, `flag-us`, etc.
- **UI Controls:** `ui-play1`, `ui-pause1`, `ui-settings1`
- **And more:** Chat, math, media, accessibility, business/money

See `superemoji-doc.pdf` for the complete reference.

## Troubleshooting

**Emoji appear as boxes or question marks?**
- Ensure Twemoji Mozilla (or another color emoji font) is installed
- Verify with: `luaotfload-tool --find="Twemoji Mozilla"`
- Make sure you're compiling with **LuaLaTeX**, not pdfLaTeX or XeLaTeX
- Check that `[Renderer=HarfBuzz]` is set in the font definition

**A few specific emoji show as boxes even when everything is set up correctly?**
Twemoji Mozilla v0.7.0 predates Unicode 15/16, so ~57 newer glyphs have no drawing in this font (e.g. the `*-facing-right` direction variants, shaking-head faces, and some newer symbols/flags). Those entries are tagged `norender-twemoji07` in `emoji-map.json`. They're kept for forward-compatibility — switch to a newer color-emoji font if you need them.

**Unknown key returns `?`**
- Check that the key exists in `superemoji-doc.pdf`
- Keys are case-sensitive

**Compilation errors?**
- Ensure you have the latest version of the package
- Check that all required files are present
- Verify your TeX distribution is up to date

## Contributing

For contributors and maintainers, the source repository includes additional tools for generating and updating emoji definitions. Visit the [GitHub repository](https://github.com/Nyphur84/superemoji-latex) for development documentation.

## Changelog

- **v1.1** (2026-07-11) — 2403 keys: +366 semantic aliases (infra, doc, ci, react, sec, pm, and 19 more families); country flags renamed to `flag-<iso2>`; self-generating 67-page reference doc; generator hardened (UTF-8, `#`-escaping).
- **v1.0** (2026-01-18) — Initial release (2037 keys).

## License

MIT License
