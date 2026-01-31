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
    print("🔒 Selando Atlas — Regime Científico MatVerse")

    # 1. Coleta determinística
    targets = ["REGIME.md", "topology", "laws", "evidence-map", "invariants"]
    files = []
    for t in targets:
        p = ROOT / t
        if p.exists():
            files.append(str(p))

    if not files:
        print("❌ Nada para selar.")
        sys.exit(1)

    # 2. Hash canônico
    hash_cmd = f"cat $(find {' '.join(files)} -type f | sort) | blake3"
    atlas_hash = run(hash_cmd)
    HASH_FILE.write_text(atlas_hash + "\n")

    print("✅ atlas_root.hash gerado")

    # 3. Assinatura (AGE)
    key = run("echo $ATLAS_SIGNING_KEY")
    if not key:
        print("❌ Variável ATLAS_SIGNING_KEY não definida")
        sys.exit(1)

    sig_cmd = f"age -s -i $ATLAS_SIGNING_KEY {HASH_FILE} > {SIG_FILE}"
    run(sig_cmd)

    print("✅ atlas_root.sig gerado")
    print("🔐 REGIME SELADO")
    print("HASH:", atlas_hash)

if __name__ == "__main__":
    main()
