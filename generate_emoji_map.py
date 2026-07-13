#!/usr/bin/env python3
"""Generate emoji-map.tex from emoji-map.json.

Never edit emoji-map.tex by hand: edit emoji-map.json and rerun this script.
"""
import json
from pathlib import Path

JSON_PATH = Path("emoji-map.json")
TEX_PATH = Path("emoji-map.tex")

HEADER = (
    "% emoji-map.tex\n"
    "% AUTO-GENERATED FILE  DO NOT EDIT BY HAND\n"
    "% Generated from emoji-map.json\n\n"
)


def tex_escape(emoji: str) -> str:
    """Escape LaTeX-special ASCII inside an emoji string.

    The only such char that ever appears in an emoji is '#' (keycap
    sequences like '#\ufe0f\u20e3'). A bare '#' is a LaTeX parameter
    character and breaks compilation, so it must be written as '\\#'.
    """
    return emoji.replace("#", r"\#")


def main():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    lines = [HEADER]
    for entry in sorted(data, key=lambda e: e["key"]):
        key = entry["key"]
        emoji = tex_escape(entry["emoji"])
        lines.append(f"\\emojiDefine{{{key}}}{{{emoji}}}\n")

    TEX_PATH.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {TEX_PATH} from {JSON_PATH} ({len(data)} entries).")


if __name__ == "__main__":
    main()
