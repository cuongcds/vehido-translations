#!/usr/bin/env python3
"""Validate arb/app_<locale>.arb files against the English template (arb/app_en.arb).

Usage: python scripts/check_translations.py [locale ...]   (default: all files in arb/)
Exit code is 1 if any error is found. Missing keys are warnings only (they fall back to English).
"""
import json
import re
import sys
from pathlib import Path

ARB_DIR = Path(__file__).resolve().parent.parent / "arb"
PLACEHOLDER = re.compile(r"\{(\w+)\}")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def messages(data):
    return {k: v for k, v in data.items() if not k.startswith("@") and isinstance(v, str)}


def main():
    template = load(ARB_DIR / "app_en.arb")
    base = messages(template)
    wanted = sys.argv[1:]
    files = [ARB_DIR / f"app_{c}.arb" for c in wanted] if wanted else sorted(ARB_DIR.glob("app_*.arb"))
    errors = warnings = 0

    for path in files:
        if path.name == "app_en.arb":
            continue
        if not path.exists():
            print(f"ERROR {path.name}: file not found")
            errors += 1
            continue
        try:
            data = load(path)
        except json.JSONDecodeError as e:
            print(f"ERROR {path.name}: invalid JSON ({e})")
            errors += 1
            continue

        locale = path.stem.removeprefix("app_")
        if data.get("@@locale") != locale:
            print(f"ERROR {path.name}: @@locale must be \"{locale}\"")
            errors += 1

        msgs = messages(data)
        for key in sorted(set(msgs) - set(base)):
            print(f"ERROR {path.name}: unknown key \"{key}\"")
            errors += 1
        for key, text in msgs.items():
            if key in base and set(PLACEHOLDER.findall(text)) != set(PLACEHOLDER.findall(base[key])):
                print(f"ERROR {path.name}: placeholders of \"{key}\" differ from English")
                errors += 1
        missing = sorted(set(base) - set(msgs))
        for key in missing:
            print(f"WARN  {path.name}: missing key \"{key}\"")
        warnings += len(missing)
        print(f"{path.name}: {len(msgs)}/{len(base)} keys translated")

    print(f"\n{errors} error(s), {warnings} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
