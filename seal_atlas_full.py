#!/usr/bin/env python3
"""
ATLAS — Constitutional Sealing Script
REGIME v1.0

Determinístico. Repetível. Auditável.
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

# -------------------------
# CONFIGURAÇÃO CANÔNICA
# -------------------------

ROOT = Path(__file__).resolve().parent
REQUIRED_PATHS = [
    "REGIME.md",
    "topology",
    "laws",
    "evidence-map",
    "invariants",
]

SIGNATURE_DIR = ROOT / "signatures"
SIGNATURE_DIR.mkdir(exist_ok=True)

HASH_FILE = SIGNATURE_DIR / "atlas_root.hash"
SIG_FILE = SIGNATURE_DIR / "atlas_root.sig"
META_FILE = SIGNATURE_DIR / "atlas_root.meta.json"

REGIME_VERSION = "v1.0"
HASH_ALGO = "blake3"
SIGNATURE_ALGO = "age"

# -------------------------
# UTILITÁRIOS
# -------------------------

def fail(msg: str):
    print(f"❌ FALHA CONSTITUCIONAL: {msg}")
    sys.exit(1)

def run(cmd: str) -> str:
    try:
        return subprocess.check_output(
            cmd, shell=True, stderr=subprocess.STDOUT
        ).decode().strip()
    except subprocess.CalledProcessError as e:
        fail(e.output.decode())

# -------------------------
# ETAPA 1 — VERIFICAÇÃO
# -------------------------

print("🔍 Verificando estrutura constitucional...")

for p in REQUIRED_PATHS:
    if not (ROOT / p).exists():
        fail(f"Elemento obrigatório ausente: {p}")

if not Path("REGIME.md").read_text().strip():
    fail("REGIME.md está vazio")

print("✅ Estrutura mínima válida")

# -------------------------
# ETAPA 2 — COLETA CANÔNICA
# -------------------------

print("📦 Coletando artefatos do regime...")

targets = []
for p in REQUIRED_PATHS:
    path = ROOT / p
    if path.is_file():
        targets.append(str(path))
    else:
        files = run(f"find {path} -type f").splitlines()
        targets.extend(files)

if not targets:
    fail("Nenhum arquivo encontrado para selagem")

targets_sorted = sorted(targets)

# -------------------------
# ETAPA 3 — HASH CANÔNICO
# -------------------------

print("🔐 Calculando hash canônico (BLAKE3)...")

hash_cmd = (
    "cat " + " ".join(targets_sorted) + f" | {HASH_ALGO}"
)

atlas_hash = run(hash_cmd)
HASH_FILE.write_text(atlas_hash + "\n")

print(f"✅ atlas_root.hash gerado: {atlas_hash}")

# -------------------------
# ETAPA 4 — ASSINATURA
# -------------------------

print("✍️ Assinando hash constitucional...")

if not run("which age"):
    fail("AGE não encontrado no sistema")

if not run("echo $ATLAS_SIGNING_KEY"):
    fail("Variável ATLAS_SIGNING_KEY não definida")

sig_cmd = f"{SIGNATURE_ALGO} -s -i $ATLAS_SIGNING_KEY {HASH_FILE} > {SIG_FILE}"
run(sig_cmd)

print("✅ atlas_root.sig gerado")

# -------------------------
# ETAPA 5 — METADADOS
# -------------------------

timestamp = datetime.utcnow().isoformat() + "Z"

meta = {
    "regime": "ATLAS",
    "regime_version": REGIME_VERSION,
    "hash_algorithm": HASH_ALGO,
    "signature_algorithm": SIGNATURE_ALGO,
    "atlas_root_hash": atlas_hash,
    "signed_at_utc": timestamp,
    "sealed_by": "ATLAS-CONSTITUTIONAL-SCRIPT",
    "previous_version": None,
}

META_FILE.write_text(json.dumps(meta, indent=2))

print("📜 Metadados de selagem gravados")

# -------------------------
# FINAL
# -------------------------

print("\n🏛️ REGIME SELADO COM SUCESSO")
print("Versão :", REGIME_VERSION)
print("Hash   :", atlas_hash)
print("Data   :", timestamp)
print("\n⚖️ Qualquer alteração exige nova versão constitucional.")
