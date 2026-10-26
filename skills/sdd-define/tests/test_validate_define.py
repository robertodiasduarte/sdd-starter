#!/usr/bin/env python3
"""validate_define.py — eval needs a numeric threshold; manual-ux needs cmd N/A and a checklist.

Each case builds a minimal DEFINE in a temp dir and runs the validator as a subprocess (`python3 -I`),
asserting exit code and the reason it prints. Cases that must FAIL against the previous validator do so
by assertion (never by import error), so the gate can tell "has teeth" from "crashed".

Run: python3 -I -B -m unittest discover -s skills/sdd-define/tests -p 'test_*.py'
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL / "scripts" / "validate_define.py"
EXEMPLO = SKILL / "assets" / "DEFINE_EXEMPLO.md"

GATE = """```yaml
verify_gate:
  kind: %(kind)s
  cmd: %(cmd)s
  pass_when: "exit 0"
  threshold: %(threshold)s
  manual_fallback: %(fallback)s
```
"""

BASE = """# DEFINE: Teste

> DEFINE mínimo para o validador

## Metadata

| Attribute | Value |
|---|---|
| **Feature** | TESTE |
| **Clarity Score** | 13/15 |

## Problem Statement

Problema.

## Target Users

| User | Role | Pain Point |
|---|---|---|
| Aluno | Dev | Dor |

## Goals

| Priority | Goal |
|---|---|
| **MUST** | Objetivo |

## Success Criteria

- [ ] Critério

## Acceptance Tests

| ID | Pattern | Criterion (EARS) | Gate (`kind`) |
|---|---|---|---|
| AT-001 | Event-driven | **When** algo acontece, o sistema **shall** responder | test |

## Clarifications

None — Brainstorm supplied sufficient validated detail.

## Verify Gate

%(gate)s
## Out of Scope

- Nada

## Constraints

| Type | Constraint | Impact |
|---|---|---|
| Technical | N/A | — |

## Technical Context

| Aspect | Value | Notes |
|---|---|---|
| **LLM Prompts** | false | sem IA |

## Assumptions

| ID | Assumption | If Wrong, Impact | Validated? |
|---|---|---|---|
| A-001 | None | — | yes |

## Clarity Score Breakdown

| Element | Score (0-3) | Notes |
|---|---:|---|
| **Total** | **13/15** | |

## Open Questions

None - ready for Design.

## Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-10-26 | teste | Initial version |

## Next Step

Execute o **SDD Design by RDD**.
"""

CHECKLIST = '"Eu abri a tela de cadastro e vi o campo CPF."'


def gate(kind="test", cmd='"pytest -q"', threshold='"—"', fallback='"—"'):
    return GATE % dict(kind=kind, cmd=cmd, threshold=threshold, fallback=fallback)


def define(gate_block):
    return BASE % dict(gate=gate_block)


def roda(path):
    return subprocess.run([sys.executable, "-I", str(VALIDATOR), str(path)], capture_output=True, text=True)


def valida(texto):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "DEFINE_TESTE.md"
        p.write_text(texto, encoding="utf-8")
        return roda(p)


class TestEval(unittest.TestCase):
    def test_threshold_sem_numero_reprova(self):
        for t in ('"—"', "—", '""', '"alto"'):
            with self.subTest(threshold=t):
                r = valida(define(gate(kind="eval", threshold=t)))
                self.assertEqual(r.returncode, 2, r.stdout)
                self.assertIn("numeric threshold", r.stdout)

    def test_threshold_numerico_passa(self):
        for t in ('"0.90"', '">= 90%"', "0.9"):
            with self.subTest(threshold=t):
                r = valida(define(gate(kind="eval", threshold=t)))
                self.assertEqual(r.returncode, 0, r.stdout)


class TestManualUx(unittest.TestCase):
    def test_cmd_diferente_de_na_reprova(self):
        for c in ('"pytest -q"', '"N/A"', '"—"'):
            with self.subTest(cmd=c):
                r = valida(define(gate(kind="manual-ux", cmd=c, fallback=CHECKLIST)))
                self.assertEqual(r.returncode, 2, r.stdout)
                self.assertIn('needs cmd: "N/A (manual-ux)"', r.stdout)

    def test_checklist_vazio_reprova(self):
        for f in ('"—"', "—", '""', '"-"'):
            with self.subTest(fallback=f):
                r = valida(define(gate(kind="manual-ux", cmd='"N/A (manual-ux)"', fallback=f)))
                self.assertEqual(r.returncode, 2, r.stdout)
                self.assertIn("needs manual_fallback", r.stdout)

    def test_manual_ux_completo_passa(self):
        r = valida(define(gate(kind="manual-ux", cmd='"N/A (manual-ux)"', fallback=CHECKLIST)))
        self.assertEqual(r.returncode, 0, r.stdout)


def bloco(*linhas):
    return "```yaml\nverify_gate:\n" + "".join("  %s\n" % ln for ln in linhas) + "```\n"


class TestLeituraDoBloco(unittest.TestCase):
    def test_campo_vazio_nao_le_a_linha_seguinte(self):
        casos = [
            ("kind: eval", 'cmd: "python3 avalia.py"', 'pass_when: "exit 0"', "threshold:",
             'manual_fallback: "score >= 0.9"'),
            ("kind: manual-ux", 'cmd: "N/A (manual-ux)"', 'pass_when: "checklist signed"', "manual_fallback:",
             'threshold: "0.9"'),
        ]
        for linhas in casos:
            with self.subTest(kind=linhas[0]):
                r = valida(define(bloco(*linhas)))
                self.assertEqual(r.returncode, 2, r.stdout)

    def test_kind_fora_da_lista_reprova(self):
        for k in ("Manual-UX", "eval2", "{test | smoke | eval | typecheck | manual-ux}"):
            with self.subTest(kind=k):
                r = valida(define(gate(kind=k)))
                self.assertEqual(r.returncode, 2, r.stdout)
                self.assertIn("invalid verify_gate kind", r.stdout)

    def test_kind_dentro_de_outro_campo_nao_vale(self):
        r = valida(define(bloco('manual_fallback: "kind: test"', "kind: manual-ux", 'cmd: "pytest -q"',
                                'pass_when: "exit 0"', 'threshold: "—"')))
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn('needs cmd: "N/A (manual-ux)"', r.stdout)

    def test_checklist_placeholder_ou_bloco_vazio_reprova(self):
        for linhas in [
            ("manual_fallback: \"{human checklist for manual-ux or —}\"",),
            ('manual_fallback: "N/A"',),
            ('manual_fallback: "tbd"',),
            ("manual_fallback: |", 'threshold: "—"'),
        ]:
            with self.subTest(fallback=linhas[0]):
                r = valida(define(bloco("kind: manual-ux", 'cmd: "N/A (manual-ux)"',
                                        'pass_when: "checklist signed"', 'threshold: "—"', *linhas)))
                self.assertEqual(r.returncode, 2, r.stdout)
                self.assertIn("needs manual_fallback", r.stdout)

    def test_checklist_em_bloco_multilinha_passa(self):
        r = valida(define(bloco("kind: manual-ux", 'cmd: "N/A (manual-ux)"', 'pass_when: "checklist signed"',
                                'threshold: "—"', "manual_fallback: |",
                                "  Eu abri a tela de cadastro e vi o campo CPF.")))
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_checklist_em_lista_passa(self):
        r = valida(define(bloco("kind: manual-ux", 'cmd: "N/A (manual-ux)"', 'pass_when: "checklist signed"',
                                'threshold: "—"', "manual_fallback:",
                                '  - "Eu abri a tela de cadastro e vi o campo CPF."')))
        self.assertEqual(r.returncode, 0, r.stdout)


    def test_lista_no_mesmo_recuo_da_chave_passa(self):
        r = valida(define(bloco("kind: manual-ux", 'cmd: "N/A (manual-ux)"', 'pass_when: "checklist signed"',
                                'threshold: "—"', "manual_fallback:",
                                '- "Eu abri a tela de cadastro e vi o campo CPF."')))
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_threshold_com_maior_que_sem_aspas_passa(self):
        for t in (">= 0.90", "> 90%"):
            with self.subTest(threshold=t):
                r = valida(define(gate(kind="eval", threshold=t)))
                self.assertEqual(r.returncode, 0, r.stdout)


class TestSemRegressao(unittest.TestCase):
    def test_bloco_canonico_test_passa(self):
        r = valida(define(gate()))
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_exemplo_passa(self):
        r = roda(EXEMPLO)
        self.assertEqual(r.returncode, 0, r.stdout)


if __name__ == "__main__":
    unittest.main()
