#!/usr/bin/env python3
"""validate_build_report.py — a migration listed in Files Changed must be proven applied.

Each case builds a minimal COMPLETE report in a temp dir and runs the validator as a subprocess
(`python3 -I`), asserting exit code and the reason it prints. Cases that must FAIL against the previous
validator do so by assertion (never by import error), so the gate can tell "has teeth" from "crashed".

Run: python3 -I -B -m unittest discover -s skills/sdd-build/tests -p 'test_*.py'
"""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL / "scripts" / "validate_build_report.py"
TEMPLATE = SKILL / "assets" / "BUILD_REPORT_TEMPLATE.md"
SECAO = "## Migrations aplicadas"

FILES_CHANGED = "| `skills/x/handler.py` | Modify | 1 | Yes | — |\n"

BASE = """# BUILD REPORT: Teste

> Relatório mínimo para o validador

## Metadata

| Attribute | Value |
|---|---|
| **Feature** | TESTE |
| **Date** | 2026-10-25 |
| **Author** | SDD Build by RDD |
| **Status** | Complete |

---

## Mode Selection

| Signal | Observation |
|---|---|
| Manifest files | 2 |

**Recommendation:** default

**User decision:** default

**Pre-build review:** No — ajuste pequeno

---

## Summary

| Metric | Value |
|---|---|
| **Tasks Completed** | 2/2 |

---

## Task Execution

| # | Manifest ID | Task | Executor | Status | Verification | Evidence |
|---:|---:|---|---|---|---|---|
| 1 | 1 | Modify handler | direct | Complete | `python -m py_compile` | exit 0 |

---

## Files Changed

| File | Action | Manifest ID | Verified | Notes |
|---|---|---:|---|---|
%(files)s
---

%(migracoes)s## Drift Detected

No drift detected.

---

## Verification Results

### Incremental Verification

| Task | Command / Method | Result | Evidence |
|---|---|---|---|
| handler | `python -m py_compile` | Pass | exit 0 |

### Verify Gate

| Attribute | Value |
|---|---|
| **Kind** | test |
| **Command / Method** | `pytest -q` |
| **Exit / Result** | 0 |
| **Status** | Green |
| **Evidence** | 3 passed |

### Manual UX Receipt

N/A

### Complementary Checks

| Check | Command / Method | Status | Evidence |
|---|---|---|---|
| Lint | N/A | N/A | — |

---

## Acceptance Test Verification

| ID | Scenario | Status | Evidence |
|---|---|---|---|
| AT-001 | handler responde | Pass | pytest |

---

## Advisor Ledger

None — no formal external review was executed.

---

## Issues Encountered

None.

---

## Deviations from Design

None.

---

## Blockers

None.

---

## Final Status

### Overall: COMPLETE

- [x] All File Manifest tasks completed

---

## Next Step

Execute o **SDD Handoff by RDD**."""

LINHA_OK = "| `supabase/migrations/20261025_cliente.sql` | Curso · `abcdefghijklmnopqrst` | 2026-10-25 14:32 (cli) | migration list: Remote ✓ · columns: cnpj ✓ |"
LINHA_JA = "| `supabase/migrations/20261025_cliente.sql` | Curso · `abcdefghijklmnopqrst` | já aplicada em 2026-10-20 | migration list: Remote ✓ |"


def secao_migracoes(*linhas):
    cabecalho = "| Arquivo | Projeto (nome · ref) | Aplicada em | Prova por leitura |\n|---|---|---|---|\n"
    return SECAO + "\n\n" + cabecalho + "".join(l + "\n" for l in linhas) + "\n---\n\n"


def relatorio(arquivos=FILES_CHANGED, migracoes=""):
    return BASE % {"files": arquivos, "migracoes": migracoes}


def valida(texto):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "BUILD_REPORT_TESTE.md"
        p.write_text(texto, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(VALIDATOR), str(p)], capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr


class TestSemMigration(unittest.TestCase):
    def test_relatorio_sem_sql_passa(self):
        rc, out = valida(relatorio())
        self.assertEqual(rc, 0, out)


class TestComMigration(unittest.TestCase):
    SQL = FILES_CHANGED + "| `supabase/migrations/20261025_cliente.sql` | Create | 2 | Yes | — |\n"

    def test_sql_sem_secao_reprova(self):
        rc, out = valida(relatorio(self.SQL))
        self.assertEqual(rc, 2, out)
        self.assertIn(SECAO, out)

    def test_secao_vazia_ou_placeholder_reprova(self):
        rc, out = valida(relatorio(self.SQL, secao_migracoes()))
        self.assertEqual(rc, 2, out)
        self.assertIn("no filled row", out)
        rc, out = valida(relatorio(self.SQL, secao_migracoes("| `{path}` | {nome} | {quando} | {prova} |")))
        self.assertEqual(rc, 2, out)

    def test_secao_preenchida_passa(self):
        rc, out = valida(relatorio(self.SQL, secao_migracoes(LINHA_OK)))
        self.assertEqual(rc, 0, out)

    def test_ja_aplicada_passa(self):
        rc, out = valida(relatorio(self.SQL, secao_migracoes(LINHA_JA)))
        self.assertEqual(rc, 0, out)

    def test_caminho_migrations_sem_sql_tambem_exige(self):
        sem_sql = FILES_CHANGED + "| `db/migrations/0007_cliente` | Create | 2 | Yes | — |\n"
        rc, out = valida(relatorio(sem_sql))
        self.assertEqual(rc, 2, out)
        self.assertIn(SECAO, out)

    def test_path_sem_crase_tambem_exige(self):
        sem_crase = FILES_CHANGED + "| supabase/migrations/20261025_cliente.sql | Create | 2 | Yes | — |\n"
        rc, out = valida(relatorio(sem_crase))
        self.assertEqual(rc, 2, out)
        self.assertIn(SECAO, out)


class TestTemplate(unittest.TestCase):
    def test_template_tem_a_secao(self):
        spec = importlib.util.spec_from_file_location("validate_build_report", VALIDATOR)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        constante = getattr(mod, "SECAO_MIGRACOES", None)
        self.assertEqual(constante, SECAO, "o validador precisa exportar SECAO_MIGRACOES com o nome da seção")
        self.assertIn(SECAO, TEMPLATE.read_text(encoding="utf-8"), "o template precisa trazer a seção condicional")


if __name__ == "__main__":
    unittest.main()
