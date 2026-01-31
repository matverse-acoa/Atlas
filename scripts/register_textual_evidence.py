#!/usr/bin/env python3
"""
ATLAS — Textual Evidence Registrar
"""

import json
import hashlib
from pathlib import Path
import datetime
import sys

ATLAS_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ATLAS_ROOT / "evidence-map" / "textual"
INDEX_FILE = ATLAS_ROOT / "evidence-map" / "index.json"

EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

REPOS = {
    "core": {"path": "../core/README.md", "regime": "LAW"},
    "cassandra-wrapped-core": {"path": "../cassandra-wrapped-core/README.md", "regime": "KERNEL"},
    "cassandra-run": {"path": "../Cassandra-run/README.md", "regime": "RUNTIME"},
    "papers": {"path": "../papers/README.md", "regime": "SCIENCE"},
    "organismo": {"path": "../organismo/README.md", "regime": "ONTOLOGY"},
    "foundation": {"path": "../foundation/README.md", "regime": "PUBLIC-VERIFY"},
    "qex": {"path": "../QEX/README.md", "regime": "EXPERIMENTAL"},
}

def canonicalize(text: str) -> str:
    lines = [l.rstrip() for l in text.strip().splitlines()]
    return "\n".join(lines) + "\n"

def blake3_hash(data: str) -> str:
    import blake3
    return blake3.blake3(data.encode()).hexdigest()

def main():
    index = {
        "type": "ATLAS_TEXTUAL_EVIDENCE_INDEX",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "entries": []
    }

    for repo, cfg in REPOS.items():
        src = (ATLAS_ROOT / cfg["path"]).resolve()
        if not src.exists():
            sys.exit(f"❌ README não encontrado: {src}")

        raw = src.read_text(encoding="utf-8")
        canonical = canonicalize(raw)
        digest = blake3_hash(canonical)

        record = {
            "repo": repo,
            "regime": cfg["regime"],
            "source_path": str(src),
            "hash": digest,
            "hash_alg": "BLAKE3",
            "bytes": len(canonical.encode()),
            "registered_at": datetime.datetime.utcnow().isoformat() + "Z",
            "type": "TEXTUAL_EVIDENCE",
            "semantics": "README_DECLARATION"
        }

        out = EVIDENCE_DIR / f"{repo}.json"
        out.write_text(json.dumps(record, indent=2), encoding="utf-8")

        index["entries"].append({
            "repo": repo,
            "evidence_file": str(out),
            "hash": digest
        })

        print(f"✅ Evidência registrada: {repo}")

    INDEX_FILE.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print("\n📜 ATLAS atualizado com evidência textual.")

if __name__ == "__main__":
    main()
