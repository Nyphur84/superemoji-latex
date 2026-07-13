#!/usr/bin/env python3
"""Generate emoji-doc-generated.tex -- the reference-table body for superemoji-doc.tex.

Emits one longtable per family (the key prefix before the first '-'), covering
EVERY key defined in emoji-map.json. Rerun this whenever the JSON changes:

    python generate_doc_tables.py

Then compile superemoji-doc.tex (which \\input's the generated file).
"""
import json
from collections import defaultdict
from pathlib import Path

JSON_PATH = Path("emoji-map.json")
OUT_PATH = Path("emoji-doc-generated.tex")

# Nicer section headings for a few known prefixes; others are just title-cased.
PRETTY = {"gis": "GIS", "ui": "UI", "io": "I/O", "dq": "Data Quality",
          "ci": "CI", "pm": "PM"}


def pretty(prefix):
    return PRETTY.get(prefix, prefix[:1].upper() + prefix[1:])


def esc(s):
    """Escape LaTeX-special characters that can appear in a description."""
    s = s or ""
    for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
                 ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}"),
                 ("$", r"\$")):
        s = s.replace(a, b)
    return s


def keydisp(k):
    """Allow line breaks after each hyphen so long CLDR keys wrap in the column."""
    return k.replace("-", "-\\allowbreak ")


def main():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    groups = defaultdict(list)
    for e in data:
        groups[e["key"].split("-", 1)[0]].append(e)

    out = ["% AUTO-GENERATED reference-table body for superemoji-doc.tex",
           "% Generated from emoji-map.json by generate_doc_tables.py -- do not edit by hand.",
           ""]
    for prefix in sorted(groups):
        ents = sorted(groups[prefix], key=lambda e: e["key"])
        out.append(r"\subsection{%s (%d emojis)}" % (pretty(prefix), len(ents)))
        out.append("")
        out.append(r"\begin{longtable}{>{\raggedright\arraybackslash}p{6.8cm}c>{\raggedright\arraybackslash}p{5.2cm}}")
        out.append(r"\toprule")
        out.append(r"\textbf{Key} & \textbf{Emoji} & \textbf{Description} \\")
        out.append(r"\midrule")
        out.append(r"\endhead")
        for e in ents:
            out.append(r"\texttt{\textcolor{keycolor}{%s}} & \emoji{%s} & %s \\"
                       % (keydisp(e["key"]), e["key"], esc(e.get("comment", ""))))
        out.append(r"\bottomrule")
        out.append(r"\end{longtable}")
        out.append("")

    OUT_PATH.write_text("\n".join(out), encoding="utf-8")
    print("Wrote %s: %d entries in %d families." % (OUT_PATH, len(data), len(groups)))


if __name__ == "__main__":
    main()
