#!/usr/bin/env python3
"""Vergleicht die installierbaren DE/EN-Dateien ohne externe Abhängigkeiten."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
IGNORE = {".DS_Store", "__pycache__"}
errors = []

def files(lang):
    base = ROOT / lang
    if not base.is_dir():
        errors.append(f"{lang}/ fehlt")
        return {}
    return {p.relative_to(base).as_posix(): p for p in base.rglob("*")
            if p.is_file() and not any(part in IGNORE for part in p.parts)}

de, en = files("DE"), files("EN")
for name in sorted(de.keys() ^ en.keys()):
    errors.append(f"{name}: fehlt in {'EN' if name in de else 'DE'}")

def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    return parts[1]

def fields(header):
    if header is None:
        return set()
    return set(re.findall(r"^([\w-]+):", header, re.M))

for name in sorted(de.keys() & en.keys()):
    a, b = de[name].read_bytes(), en[name].read_bytes()
    if name.endswith(".json"):
        try:
            left, right = json.loads(a), json.loads(b)
            if left != right:
                errors.append(f"{name}: JSON-Konfiguration unterscheidet sich")
        except (ValueError, UnicodeError) as exc:
            errors.append(f"{name}: ungültiges JSON: {exc}")
    elif name.endswith(".md"):
        left, right = a.decode("utf-8"), b.decode("utf-8")
        fa, fb = frontmatter(left), frontmatter(right)
        if (fa is None) != (fb is None):
            errors.append(f"{name}: YAML-Frontmatter fehlt auf einer Seite")
        elif fa is not None and fields(fa) != fields(fb):
            errors.append(f"{name}: Frontmatter-Schlüssel unterscheiden sich")
    elif a != b:
        errors.append(f"{name}: nicht übersetzbare Datei unterscheidet sich")

if errors:
    print("Atlas-Sprachprüfung fehlgeschlagen:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)
print(f"Atlas-Sprachprüfung erfolgreich: {len(de)} DE- und {len(en)} EN-Dateien.")
print("Hinweis: Inhaltliche Gleichwertigkeit von Markdown-Texten erfordert ein separates Review.")
