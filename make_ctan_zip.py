#!/usr/bin/env python3
"""Build superemoji.zip for CTAN.

Produces a single archive with a top-level ``superemoji/`` directory, every
text file normalised to LF line endings (CTAN prefers UNIX), ready to upload
at https://ctan.org/upload. Run after rebuilding the .tex/.pdf:

    python make_ctan_zip.py
"""
import os
import zipfile

# Shipped as text (LF-normalised). Order is cosmetic.
TEXT_FILES = [
    "superemoji.sty",
    "emoji-map.tex",
    "emoji-doc-generated.tex",
    "superemoji-doc.tex",
    "emoji-map.json",
    "generate_emoji_map.py",
    "generate_doc_tables.py",
    "make_ctan_zip.py",
    "README.md",
    "LICENSE",
]
# Shipped verbatim (binary).
BINARY_FILES = ["superemoji-doc.pdf"]

OUT = "superemoji.zip"
PKG = "superemoji"  # top-level directory inside the archive (must be the package name)


def to_lf(data: bytes) -> str:
    text = data.decode("utf-8", "replace")
    if text[:1] == "\ufeff":                      # strip a UTF-8 BOM if present
        text = text[1:]
    return text.replace("\r\n", "\n").replace("\r", "\n")


def main():
    missing = [f for f in TEXT_FILES + BINARY_FILES if not os.path.exists(f)]
    if missing:
        raise SystemExit("Missing files: " + ", ".join(missing))

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for f in TEXT_FILES:
            with open(f, "rb") as fh:
                z.writestr(f"{PKG}/{f}", to_lf(fh.read()))
        for f in BINARY_FILES:
            z.write(f, f"{PKG}/{f}")

    print("Wrote %s (%d bytes) with %d files under %s/"
          % (OUT, os.path.getsize(OUT), len(TEXT_FILES) + len(BINARY_FILES), PKG))


if __name__ == "__main__":
    main()
