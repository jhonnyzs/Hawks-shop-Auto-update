#!/usr/bin/env python3
"""Bump version.json and push it. Usage:

    python release.py 1.1.0 "Fixed X" "Added Y"

Optionally point it at the built exe to fill in size + sha256:

    python release.py 1.1.0 --exe "..\\PC app\\src\\dist\\HawksShop.exe" "note"

Then create the matching GitHub Release (tag vX.Y.Z) with HawksShop.exe attached.
"""
import hashlib
import json
import os
import subprocess
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "version.json")


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    version = argv[0]
    exe = ""
    notes = []
    i = 1
    while i < len(argv):
        if argv[i] == "--exe":
            exe = argv[i + 1]
            i += 2
        else:
            notes.append(argv[i])
            i += 1

    with open(MANIFEST, encoding="utf-8") as f:
        man = json.load(f)
    man["version"] = version
    man["latestVersion"] = version
    man["releaseDate"] = date.today().isoformat()
    if notes:
        man["changelog"] = notes
    if exe and os.path.exists(exe):
        man["fileSizeBytes"] = os.path.getsize(exe)
        h = hashlib.sha256()
        with open(exe, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        man["sha256"] = h.hexdigest()
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(man, f, indent=2)
        f.write("\n")
    print(f"version.json -> {version}")

    subprocess.run(["git", "-C", HERE, "add", "version.json"], check=True)
    subprocess.run(["git", "-C", HERE, "commit", "-m", f"Release {version}"], check=True)
    subprocess.run(["git", "-C", HERE, "push"], check=True)
    print("Pushed. Now create the GitHub Release (tag v%s) with HawksShop.exe attached." % version)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
