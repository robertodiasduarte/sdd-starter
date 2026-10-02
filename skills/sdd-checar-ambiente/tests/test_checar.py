"""Testes das checagens de dado exposto da sdd-checar-ambiente.

Rodar: python3 -B -m unittest discover -s skills/sdd-checar-ambiente/tests -p "test_*.py"

O GitHub é simulado por um servidor HTTP local (SDD_CHECAR_GITHUB_API): os testes não usam a rede.
Requer bash e git; o teste de npm é pulado se o npm não existir.
"""
from __future__ import annotations

import hashlib
import http.server
import os
import shutil
import subprocess
import tempfile
import threading
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "checar.sh"


def chave_privada_falsa() -> str:
    return "-" * 5 + "BEGIN " + "PRIVATE" + " KEY" + "-" * 5 + "\nAAAA\n" + "-" * 5 + "END " + "PRIVATE" + " KEY" + "-" * 5 + "\n"


def certificado_publico_falso() -> str:
    return "-" * 5 + "BEGIN CERTIFICATE" + "-" * 5 + "\nAAAA\n" + "-" * 5 + "END CERTIFICATE" + "-" * 5 + "\n"


class GitHubFalso(http.server.BaseHTTPRequestHandler):
    publicos = {"/repos/escritorio/publico"}

    def do_GET(self):  # noqa: N802
        self.send_response(200 if self.path in self.publicos else 404)
        self.end_headers()
        self.wfile.write(b"{}")

    def log_message(self, *args):
        pass


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = http.server.HTTPServer(("127.0.0.1", 0), GitHubFalso)
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()
        cls.api = f"http://127.0.0.1:{cls.srv.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="checar-"))
        self.raiz = self.tmp / "meu-app"
        self.raiz.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Teste")
        self.git("config", "user.email", "teste@exemplo.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.escreve("README.md", "x\n")
        self.commit("README.md")
        # Sem remoto o relatório já tem um ⚠️; o padrão é um repositório privado (404 no GitHub falso).
        self.git("remote", "add", "origin", "https://github.com/escritorio/privado.git")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def git(self, *args: str) -> str:
        return subprocess.run(["git", *args], cwd=self.raiz, check=True, capture_output=True, text=True).stdout

    def escreve(self, nome: str, conteudo: str | bytes) -> None:
        p = self.raiz / nome
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(conteudo, bytes):
            p.write_bytes(conteudo)
        else:
            p.write_text(conteudo, encoding="utf-8")

    def commit(self, *nomes: str) -> None:
        self.git("add", "-f", "--", *nomes)
        self.git("commit", "-q", "--no-verify", "-m", "t")

    def remoto(self, slug: str) -> None:
        self.git("remote", "set-url", "origin", f"git@github.com:{slug}.git")

    def checar(self, **env: str) -> str:
        e = {**os.environ, "SDD_CHECAR_GITHUB_API": self.api, **env}
        r = subprocess.run(["bash", str(SCRIPT)], cwd=self.raiz, capture_output=True, text=True, env=e)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout


class TestDadoExposto(Base):
    def test_saudavel_e_uma_linha_com_identificacao(self):
        out = self.checar()
        self.assertEqual(len(out.strip().splitlines()), 1, out)
        self.assertTrue(out.startswith("✅ Pronto: repo meu-app"), out)
        self.assertRegex(out, r"· sdd-checar-ambiente v\d+\.\d+\.\d+ · [a-z]{3}/\d{4} · versão atual: https://github\.com/robertodiasduarte/sdd-starter/releases/latest")

    def test_repo_publico_sem_segredo_continua_uma_linha(self):
        self.remoto("escritorio/publico")
        out = self.checar()
        self.assertEqual(len(out.strip().splitlines()), 1, out)
        self.assertIn("repo meu-app (público no GitHub)", out)

    def test_repo_privado_nao_menciona_visibilidade(self):
        self.remoto("escritorio/privado")
        out = self.checar()
        self.assertNotIn("público", out)

    def test_api_fora_do_ar_nao_diz_nada(self):
        self.remoto("escritorio/publico")
        out = self.checar(SDD_CHECAR_GITHUB_API="http://127.0.0.1:9")
        self.assertNotIn("público", out)

    def test_env_rastreado_e_dado_exposto_no_topo(self):
        self.escreve(".env", "SENHA=x\n")
        self.commit(".env")
        out = self.checar()
        self.assertTrue(out.startswith("🔴 Dado exposto"), out)
        self.assertIn('git rm --cached ".env"', out)
        self.assertIn("troque as senhas", out)
        self.assertIn("não apaga do histórico", out)

    def test_pfx_em_repo_publico_diz_que_esta_na_internet(self):
        self.remoto("escritorio/publico")
        self.escreve("certificados/empresa.PFX", b"\x30\x82\x00\x01")
        self.commit("certificados/empresa.PFX")
        out = self.checar()
        self.assertTrue(out.startswith("🔴 Dado exposto"), out)
        self.assertIn("certificados/empresa.PFX", out)
        self.assertIn("já está na internet", out)
        self.assertIn("revogue o certificado", out)

    def test_p12_e_env_variante(self):
        self.escreve("a.p12", b"\x30\x82")
        self.escreve("config/.env.production", "X=1\n")
        self.commit("a.p12", "config/.env.production")
        out = self.checar()
        self.assertIn("a.p12", out)
        self.assertIn("config/.env.production", out)

    def test_env_example_e_sample_nao_alarmam(self):
        self.escreve(".env.example", "SENHA=\n")
        self.escreve(".env.sample", "SENHA=\n")
        self.commit(".env.example", ".env.sample")
        out = self.checar()
        self.assertNotIn("Dado exposto", out)

    def test_pem_publico_nao_alarma_privado_alarma(self):
        self.escreve("ca.pem", certificado_publico_falso())
        self.commit("ca.pem")
        self.assertNotIn("Dado exposto", self.checar())
        self.escreve("chave.pem", chave_privada_falsa())
        self.commit("chave.pem")
        out = self.checar()
        self.assertIn("A chave privada chave.pem", out)
        self.assertNotIn("ca.pem", out)

    def test_env_nao_ignorado_e_aviso(self):
        self.escreve(".env", "X=1\n")
        out = self.checar()
        self.assertIn("⚠️ Vale arrumar", out)
        self.assertIn("não está no .gitignore", out)
        self.assertNotIn("Dado exposto", out)

    def test_env_ignorado_nao_diz_nada(self):
        self.escreve(".gitignore", ".env\n")
        self.commit(".gitignore")
        self.escreve(".env", "X=1\n")
        out = self.checar()
        self.assertEqual(len(out.strip().splitlines()), 1, out)

    def test_sem_env_nao_fala_de_gitignore(self):
        self.assertNotIn(".gitignore", self.checar())

    @unittest.skipUnless(shutil.which("npm"), "npm ausente")
    def test_npm_ignore_scripts(self):
        self.escreve("package.json", "{}\n")
        (self.raiz / "node_modules").mkdir()
        out = self.checar(npm_config_ignore_scripts="false")
        self.assertIn("npm config set ignore-scripts true", out)
        out = self.checar(npm_config_ignore_scripts="true")
        self.assertNotIn("ignore-scripts", out)

    def test_sem_package_json_nao_fala_de_npm(self):
        self.assertNotIn("npm", self.checar(npm_config_ignore_scripts="false"))


class TestSomenteLeitura(Base):
    def foto(self) -> dict[str, tuple[int, int, str]]:
        r = {}
        for p in sorted(self.tmp.rglob("*")):
            if p.is_file():
                st = p.stat()
                r[str(p)] = (st.st_size, st.st_mtime_ns, hashlib.sha256(p.read_bytes()).hexdigest())
            else:
                r[str(p)] = (0, 0, "dir")
        return r

    def test_nao_grava_nada(self):
        # Cenário com todos os achados: dado exposto, .env solto, npm, repo público.
        self.remoto("escritorio/publico")
        self.escreve(".env", "X=1\n")
        self.escreve("a.pfx", b"\x30")
        self.escreve("chave.pem", chave_privada_falsa())
        self.commit("a.pfx", "chave.pem")
        self.escreve("package.json", "{}\n")
        antes = self.foto()
        out = self.checar(npm_config_ignore_scripts="false")
        self.assertIn("Dado exposto", out)
        self.assertEqual(antes, self.foto())


if __name__ == "__main__":
    unittest.main()
