#!/usr/bin/env python3

import subprocess
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SIG_DIR = ROOT / "signatures"
SIG_DIR.mkdir(exist_ok=True)

HASH_FILE = SIG_DIR / "atlas_root.hash"
SIG_FILE = SIG_DIR / "atlas_root.sig"

def run(cmd):
    return subprocess.check_output(cmd, shell=True).decode().strip()

def main():
    targets = ["REGIME.md", "topology", "laws", "evidence-map", "invariants"]
    files = []

    for t in targets:
        p = ROOT / t
        if p.exists():
            files.append(str(p))

    if not files:
        sys.exit("❌ Nada para selar.")

    atlas_hash = run(f"cat $(find {' '.join(files)} -type f | sort) | b3sum | cut -d' ' -f1")
    HASH_FILE.write_text(atlas_hash + "\n")

    key = run("echo $ATLAS_SIGNING_KEY")
    if not key:
        sys.exit("❌ ATLAS_SIGNING_KEY não definida")

    run(f"age -s -i $ATLAS_SIGNING_KEY {HASH_FILE} > {SIG_FILE}")

    print("🔐 ATLAS SELADO")
    print("HASH:", atlas_hash)

if __name__ == "__main__":
    main()
