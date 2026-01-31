#!/usr/bin/env python3
"""
ATLAS — Textual Evidence Verifier
"""

import json
from pathlib import Path
import sys
import blake3

ATLAS_ROOT = Path(__file__).resolve().parents[1]
INDEX = ATLAS_ROOT / "evidence-map" / "index.json"

def main():
    index = json.loads(INDEX.read_text())

    for entry in index["entries"]:
        record = json.loads(Path(entry["evidence_file"]).read_text())
        src = Path(record["source_path"])

        if not src.exists():
            sys.exit(f"❌ Fonte ausente: {src}")

        text = src.read_text(encoding="utf-8").strip() + "\n"
        digest = blake3.blake3(text.encode()).hexdigest()

        if digest != record["hash"]:
            sys.exit(
                f"\n❌ VIOLAÇÃO DETECTADA\n"
                f"Repo: {record['repo']}\n"
                f"Esperado: {record['hash']}\n"
                f"Atual:    {digest}\n"
            )

        print(f"✅ OK: {record['repo']}")

    print("\n🔒 Evidência textual íntegra.")

if __name__ == "__main__":
    main()
