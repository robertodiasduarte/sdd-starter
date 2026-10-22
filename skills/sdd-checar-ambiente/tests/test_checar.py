"""Testes da sdd-checar-ambiente: dado exposto, alcance do remoto e o pré-voo --frente.

Rodar: python3 -B -m unittest discover -s skills/sdd-checar-ambiente/tests -p "test_*.py"

Os testes não usam a rede: a API do GitHub é um servidor HTTP local (SDD_CHECAR_GITHUB_API), os
endereços github.com são reescritos (url.<local>.insteadOf) para repositórios bare na pasta temporária,
e credencial recusada, rede pendurada e ssh são servidores ou comandos locais. A configuração global do
git de quem roda (credential helper, insteadOf) fica de fora: GIT_CONFIG_GLOBAL vazio.
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
import time
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "checar.sh"
BASH = shutil.which("bash") or "bash"   # caminho absoluto: o teste do git fora do PATH troca o PATH


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


class CredencialRecusada(http.server.BaseHTTPRequestHandler):
    """Repositório que exige login (HTTP 401), como um repo privado do GitHub sem credencial."""

    def do_GET(self):  # noqa: N802
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="repo"')
        self.end_headers()

    def log_message(self, *args):
        pass


class Pendurado(http.server.BaseHTTPRequestHandler):
    """Aceita a conexão e nunca responde, como uma rede que engole os pacotes."""

    def do_GET(self):  # noqa: N802
        time.sleep(60)

    def log_message(self, *args):
        pass


def servidor(handler):
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    srv.daemon_threads = True
    srv.block_on_close = False
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = servidor(GitHubFalso)
        cls.api = f"http://127.0.0.1:{cls.srv.server_address[1]}"
        cls.srv401 = servidor(CredencialRecusada)
        cls.srv_pendurado = servidor(Pendurado)

    @classmethod
    def tearDownClass(cls):
        for s in (cls.srv, cls.srv401, cls.srv_pendurado):
            s.shutdown()

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
        # "github.com" sem rede: cada repo do GitHub falso é um bare local com 1 commit na main.
        self.gh = self.tmp / "gh"
        for slug in ("escritorio/privado", "escritorio/publico"):
            bare = self.gh / f"{slug}.git"
            bare.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True)
            self.git("push", "-q", str(bare), "HEAD:refs/heads/main")
        for prefixo in ("https://github.com/", "git@github.com:"):
            self.git("config", "--add", f"url.file://{self.gh}/.insteadOf", prefixo)
        self.global_vazio = self.tmp / "gitconfig-global"
        self.global_vazio.write_text("", encoding="utf-8")

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

    def origin(self, url: str) -> None:
        self.git("remote", "set-url", "origin", url)

    def roda(self, *args: str, **env: str) -> tuple[int, str, float]:
        # O askpass do terminal de quem roda (VS Code/Cursor) mudaria a classificação e poderia abrir a
        # janela de login de verdade: só entra quando o teste o define.
        herdado = {k: v for k, v in os.environ.items() if k not in ("GIT_ASKPASS", "SSH_ASKPASS")}
        e = {**herdado, "SDD_CHECAR_GITHUB_API": self.api, "GIT_CONFIG_GLOBAL": str(self.global_vazio),
             "GIT_CONFIG_NOSYSTEM": "1", **env}
        for k in [k for k, v in e.items() if v is None]:
            del e[k]
        t0 = time.monotonic()
        r = subprocess.run([BASH, str(SCRIPT), *args], cwd=self.raiz, capture_output=True, text=True,
                           env=e, stdin=subprocess.DEVNULL, timeout=60)
        return r.returncode, r.stdout, time.monotonic() - t0

    def checar(self, **env: str) -> str:
        rc, out, _ = self.roda(**env)
        self.assertEqual(rc, 0, out)
        return out


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


class TestRemoto(Base):
    def test_credencial_recusada_rapida(self):
        self.origin(f"http://127.0.0.1:{self.srv401.server_address[1]}/escritorio/privado.git")
        rc, out, t = self.roda()
        self.assertEqual(rc, 0, out)
        self.assertLess(t, 5, out)
        self.assertTrue(out.startswith("🔴 Impede o trabalho"), out)
        self.assertIn("recusou o acesso", out)
        self.assertIn("gh auth login", out)
        self.assertIn("chave SSH", out)
        self.assertNotIn("Password", out)
        self.assertNotIn("Username", out)

    def test_credencial_github_privado_explica_as_duas_causas(self):
        porta = self.srv401.server_address[1]
        self.git("config", f"url.http://127.0.0.1:{porta}/x.git.insteadOf", "https://github.com/escritorio/privado.git")
        out = self.checar()
        self.assertIn("O GitHub não deixou este computador ler escritorio/privado", out)
        self.assertIn("o repositório é privado e este computador não está logado no GitHub", out)

    def test_rede_pendurada(self):
        self.origin(f"http://127.0.0.1:{self.srv_pendurado.server_address[1]}/x.git")
        rc, out, t = self.roda()
        self.assertEqual(rc, 0, out)
        self.assertLessEqual(t, 12, out)
        self.assertIn("sem internet ou rede bloqueada", out)
        for palavra in ("senha", "login", "credencial"):
            self.assertNotIn(palavra, out.lower())

    def test_ssh_pendurado_vigia(self):
        # Neto que não é `exec` (sh -c com 2 comandos): matar só o filho deixaria o pipe aberto.
        self.origin("ssh://git@exemplo.invalid/x.git")
        rc, out, t = self.roda(GIT_SSH_COMMAND="sh -c 'sleep 60; :'")
        self.assertEqual(rc, 0, out)
        self.assertLessEqual(t, 12, out)
        self.assertIn("sem internet ou rede bloqueada", out)
        self.assertNotIn("✅ Pronto", out)

    def test_host_ssh_desconhecido(self):
        self.origin("ssh://git@exemplo.invalid/x.git")
        out = self.checar(GIT_SSH_COMMAND="sh -c 'echo \"Host key verification failed.\" >&2; exit 255'")
        self.assertIn("ainda não confirmou a identidade de exemplo.invalid", out)
        self.assertIn("ssh -T git@exemplo.invalid", out)
        self.assertNotIn("gh auth login", out)

    def test_login_do_editor_esperando(self):
        self.origin(f"http://127.0.0.1:{self.srv401.server_address[1]}/x.git")
        registro = self.tmp / "askpass.log"
        askpass = self.tmp / "askpass.sh"
        askpass.write_text(f"#!/bin/sh\necho chamado >> '{registro}'\nsleep 60\n", encoding="utf-8")
        askpass.chmod(0o755)
        rc, out, t = self.roda(GIT_ASKPASS=str(askpass))
        self.assertEqual(rc, 0, out)
        self.assertLessEqual(t, 12, out)
        self.assertIn("A janela de login do editor está esperando resposta", out)
        self.assertNotIn("sem internet", out)

    def test_remoto_vazio(self):
        vazio = self.tmp / "vazio.git"
        subprocess.run(["git", "init", "-q", "--bare", str(vazio)], check=True)
        self.origin(str(vazio))
        out = self.checar()
        self.assertIn("⚠️ Vale arrumar", out)
        self.assertIn("ainda não tem nenhum commit", out)
        self.assertIn("GIT_TERMINAL_PROMPT=0 git push -u origin main", out)

    def test_vazio_com_warning(self):
        # O aviso do ssh (stderr, rc 0) não é ref: o remoto continua vazio.
        vazio = self.tmp / "vazio.git"
        subprocess.run(["git", "init", "-q", "--bare", str(vazio)], check=True)
        embrulho = self.tmp / "ssh-com-aviso.sh"
        embrulho.write_text("#!/bin/sh\necho \"Warning: Permanently added 'h' (ED25519) to the list of known hosts.\" >&2\n"
                            f"exec git upload-pack '{vazio}'\n", encoding="utf-8")
        embrulho.chmod(0o755)
        self.origin("ssh://git@exemplo.invalid/x.git")
        out = self.checar(GIT_SSH_COMMAND=str(embrulho))
        self.assertIn("ainda não tem nenhum commit", out)

    def test_sem_remoto_continua_aviso(self):
        self.git("remote", "remove", "origin")
        out = self.checar()
        self.assertIn("⚠️ Vale arrumar", out)
        self.assertIn("git remote add origin <url do repositório>", out)

    def test_git_fora_do_path(self):
        bin_ = self.tmp / "bin-sem-git"
        bin_.mkdir()
        for ferramenta in ("dirname", "grep", "sed", "cut", "tr", "head", "awk", "basename"):
            achou = shutil.which(ferramenta)
            if achou:
                (bin_ / ferramenta).symlink_to(achou)
        rc, out, _ = self.roda(PATH=str(bin_))
        self.assertEqual(rc, 0, out)
        self.assertIn("O git não está instalado", out)
        self.assertIn("https://git-scm.com/downloads", out)

    def test_comandos_impressos_sem_prompt(self):
        vazio = self.tmp / "vazio.git"
        subprocess.run(["git", "init", "-q", "--bare", str(vazio)], check=True)
        self.origin(str(vazio))
        saidas = [self.checar(), self.roda("--frente")[1]]
        vistos = 0
        for out in saidas:
            for linha in out.splitlines():
                if any(f"git {c}" in linha for c in ("push", "fetch", "pull", "ls-remote")):
                    vistos += 1
                    self.assertIn("GIT_TERMINAL_PROMPT=0", linha, out)
        # Sem nenhum comando de rede impresso a regra seria vácua: o remoto vazio tem de ensinar o push.
        self.assertGreaterEqual(vistos, 2, saidas)


class TestFrente(Base):
    NADA = "Nada foi criado. Depois de resolver, peça a frente de novo."

    def bloqueia(self, out: str, rc: int) -> None:
        self.assertEqual(rc, 1, out)
        self.assertTrue(out.startswith("🔴 Impede o trabalho"), out)
        self.assertEqual(out.strip().splitlines()[-1], self.NADA, out)
        self.assertNotIn("✅", out)

    def test_frente_saudavel_uma_linha(self):
        rc, out, _ = self.roda("--frente")
        self.assertEqual(rc, 0, out)
        self.assertEqual(len(out.strip().splitlines()), 1, out)
        self.assertTrue(out.startswith("✅ Pronto para abrir a frente: repo meu-app, principal main"), out)

    def test_frente_bloqueia_sem_remoto(self):
        self.git("remote", "remove", "origin")
        rc, out, _ = self.roda("--frente")
        self.bloqueia(out, rc)
        self.assertIn("git remote add origin", out)

    def test_frente_bloqueia_sem_origin(self):
        # Outro remoto não basta: a frente nasce de origin/<principal>.
        self.git("remote", "rename", "origin", "upstream")
        rc, out, _ = self.roda("--frente")
        self.bloqueia(out, rc)
        self.assertIn("nenhum chamado origin", out)

    def test_frente_bloqueia_vazio(self):
        vazio = self.tmp / "vazio.git"
        subprocess.run(["git", "init", "-q", "--bare", str(vazio)], check=True)
        self.origin(str(vazio))
        rc, out, _ = self.roda("--frente")
        self.bloqueia(out, rc)

    def test_frente_bloqueia_credencial(self):
        self.origin(f"http://127.0.0.1:{self.srv401.server_address[1]}/x.git")
        rc, out, _ = self.roda("--frente")
        self.bloqueia(out, rc)
        self.assertIn("gh auth login", out)

    def test_frente_bloqueia_host_ssh(self):
        self.origin("ssh://git@exemplo.invalid/x.git")
        rc, out, _ = self.roda("--frente", GIT_SSH_COMMAND="sh -c 'echo \"Host key verification failed.\" >&2; exit 255'")
        self.bloqueia(out, rc)
        self.assertIn("ssh -T git@exemplo.invalid", out)
        self.assertNotIn("gh auth login", out)

    def test_frente_bloqueia_rede(self):
        self.origin(f"http://127.0.0.1:{self.srv_pendurado.server_address[1]}/x.git")
        rc, out, _ = self.roda("--frente")
        self.bloqueia(out, rc)
        self.assertIn("sem internet", out)

    def test_frente_nao_olha_dado_exposto(self):
        # O pré-voo só decide se a frente pode nascer; o diagnóstico completo é o modo normal.
        self.escreve(".env", "SENHA=x\n")
        self.commit(".env")
        rc, out, _ = self.roda("--frente")
        self.assertEqual(rc, 0, out)
        self.assertNotIn("Dado exposto", out)


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
