# DESIGN: Baixar NFS-e

> Technical design for implementing Baixar NFS-e

## Metadata

| Attribute | Value |
|---|---|
| **Feature** | BAIXAR_NFSE |
| **Date** | 2026-11-06 |
| **Author** | SDD Design by RDD |
| **BRAINSTORM** | `BRAINSTORM_BAIXAR_NFSE.md` |
| **DEFINE** | `DEFINE_BAIXAR_NFSE.md` |
| **UX REVIEW** | N/A |
| **LLM Prompts** | false |
| **Status** | Ready for Build |

---

## Architecture Overview

Projeto novo: todos os caminhos abaixo são criados pelo Build dentro de `extensao/`, a pasta que o aluno carrega no Chrome. Não há instalação nem etapa de compilação.

```text
 Aluno: CNPJ, pasta, Baixar, Parar, Recomeçar
        |
        v
+---------------------------------------------------------------+
| Página da extensão (painel lateral ou aba)                    |
|                                                               |
|  sidepanel.js --> tela.js --> sincronizar.js                  |
|  (liga o real)    (só tela)   (as lições 1 e 2 moram aqui)    |
|                                  |      |      |      |       |
|                                  v      v      v      v       |
|                               adn.js  documento  arquivos cursor|
+---------------------------------|---------|------|------|------+
                                  |         |      |      |
             HTTPS com certificado|         |      |      |
             escolhido pelo Chrome|         |      |      |
                                  v         |      v      v
                      adn.nfse.gov.br       |   Pasta   chrome.storage.local
                      (único destino)       |   do      (só cursor por CNPJ)
                                            |   aluno
                                gzip + base64 -> XML

 tests/testes.html roda dentro da extensão: usa tudo acima com rede e disco simulados.
 background.js só faz o clique no ícone abrir o painel.
```

---

## Components

| Component | Purpose | Technology / Pattern | Inputs | Outputs | Dependencies |
|---|---|---|---|---|---|
| Manifesto | Declara permissões mínimas e a política de conteúdo | `manifest.json` MV3 | N/A | Regras aplicadas pelo Chrome | N/A |
| Configuração | Reúne esperas, limites e endereço da API | Módulo JS | N/A | Constantes | N/A |
| CNPJ | Normaliza e valida, inclusive o formato alfanumérico | Funções puras | Texto digitado | CNPJ normalizado ou recusa | N/A |
| API do ADN | Busca um lote e traduz a resposta em lote, fim, transitório ou falha | `fetch` injetado | NSU, CNPJ, sinal de parada | Resultado do lote | Configuração |
| Documento | Decodifica, lê os metadados, classifica e monta o caminho | `DecompressionStream`, `DOMParser` | Item do lote, CNPJ | Bytes e caminho | Configuração |
| Arquivos | Grava os bytes e só termina depois de `close()`; recusa substituir arquivo com bytes diferentes | File System Access | Pasta, caminho, bytes | `gravado`, `ja-existia` ou erro | N/A |
| Cursor | Lê e salva o NSU por CNPJ | Armazenamento injetado | CNPJ, NSU | NSU salvo | N/A |
| Sincronizador | Conduz o download, avança o cursor e define o estado final | Orquestração com dependências injetadas | CNPJ e dependências | Estado final e totais | API do ADN, Documento, Arquivos, Cursor |
| Tela | Reage aos cliques e mostra progresso, estado e resumo só como texto | DOM com `textContent` | Marcação e dependências | Tela atualizada | CNPJ, Sincronizador |
| Ligação real | Conecta a Tela ao Chrome: seletor de pasta, armazenamento e aba do certificado | Módulo de entrada | APIs do Chrome | Tela em funcionamento | Tela, Sincronizador, Arquivos, Cursor, API do ADN |
| Segundo plano | Faz o clique no ícone abrir o painel | Service worker mínimo | Instalação | Comportamento do ícone | Manifesto |
| Página de testes | Prova as lições sem instalar nada | HTML/JS com grupos por lição | Módulos e simulados | "N de N aprovados" | Todos os módulos |

---

## Key Decisions

### Decision 1: Módulos JS sem etapa de compilação, com dependências injetadas

| Attribute | Value |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-11-06 |
| **Source** | DEFINE, Constraints |

**Context:** O aluno não usa Node, npm nem bundler, e as lições precisam ser testadas sem rede real nem disco real.

**Choice:** Usar arquivos `.js` com `import` e `export`, carregados diretamente pelo Chrome. O Sincronizador e a API do ADN recebem `fetch`, gravador, cursor e espera como parâmetros. Só `sidepanel.js` conhece as APIs reais do Chrome.

**Rationale:** A mesma lógica roda de verdade no painel e com simulados na página de testes, sem biblioteca de testes.

**Alternatives Rejected:**
1. Scripts globais sem módulos — dependências escondidas e ordem de carregamento frágil.
2. TypeScript com bundler — exigiria instalação, contra a restrição do projeto.

**Consequences:**
- Um pouco mais de parâmetros nas funções principais.
- Abrir os arquivos direto pelo disco (`file://`) não funciona; a página de testes é aberta dentro da extensão.

### Decision 2: Cursor por documento, depois de `close()`

| Attribute | Value |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-11-06 |
| **Source** | DEFINE, AT-101 a AT-107 |

**Context:** É a primeira lição: o cursor adiantado em relação à gravação pula nota para sempre.

**Choice:** Gravar em ordem numérica crescente de NSU, um documento por vez. A sequência é sempre gravar, aguardar `close()` e só então salvar o cursor. O primeiro erro encerra a execução.

**Rationale:** O cursor nunca passa de uma nota não gravada. Como o CNPJ e o NSU estão no nome do arquivo, baixar de novo encontra o mesmo arquivo: bytes iguais seguem adiante, e bytes diferentes param a execução sem tocar no original.

**Alternatives Rejected:**
1. Salvar o cursor ao fim do lote — o Parar perderia o avanço, e o lote seria regravado.
2. Salvar o cursor ao montar a lista — é o defeito que o exemplo combate.

**Consequences:**
- Uma escrita no armazenamento por documento, custo desprezível para este volume.
- Um documento corrompido, ou um arquivo existente diferente, bloqueia os seguintes até alguém resolver.

### Decision 3: Lista fechada de sinais de fim

| Attribute | Value |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-11-06 |
| **Source** | DEFINE, AT-201 a AT-209 |

**Context:** É a segunda lição: um "Em dia" dado por engano esconde notas não baixadas.

**Choice:** Uma função pura, `interpretarResposta`, recebe status e texto e devolve `lote`, `fim`, `transitorio` ou `falha`. Só três sinais viram `fim`: o código `E2220`, o `StatusProcessamento` igual a `NENHUM_DOCUMENTO_LOCALIZADO` e um `LoteDFe` vazio numa resposta sem erro. Todo o resto que não se reconhece vira `falha`.

**Rationale:** Se a API mudar, o aluno vê uma falha com o motivo, nunca um falso sucesso.

**Alternatives Rejected:**
1. Tratar todo 404 como fim — um 404 de outra origem esconderia uma queda; só o código `E2220` encerra.
2. Tratar resposta sem lote como fim — confunde ausência de resposta útil com caixa vazia.

**Consequences:**
- Se o ADN encerrar por um sinal ainda desconhecido, a tela mostra "Falhou" até a lista ser ajustada.
- O estado final vem de um único ponto, então a tela nunca mostra dois estados.

### Decision 4: Política de conteúdo como barreira de privacidade

| Attribute | Value |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-11-06 |
| **Source** | DEFINE, AT-301 a AT-307 |

**Context:** É a terceira lição: a privacidade não deve depender só de ninguém escrever uma chamada indevida.

**Choice:** Declarar no manifesto `connect-src 'self' https://adn.nfse.gov.br` e `default-src 'self'`. Além disso, a página de testes lê o manifesto e o código da extensão para conferir permissões e URLs.

**Rationale:** O próprio Chrome bloqueia qualquer outro destino, inclusive imagem externa, e o teste avisa se alguém afrouxar a regra.

**Alternatives Rejected:**
1. Só `host_permissions` — essa permissão dispensa CORS, mas não impede chamadas a outros domínios.
2. Só revisão de código — depende de atenção humana a cada mudança.

**Consequences:**
- Nada de `<script>` ou `<style>` embutido no HTML: tudo fica em arquivos próprios.
- A extensão não carrega nada de fora, o que combina com a restrição de zero biblioteca.

### Decision 5: Página de testes dentro da extensão

| Attribute | Value |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-11-06 |
| **Source** | DEFINE, Verify Gate |

**Context:** O Verify Gate não pode depender de Node. As provas precisam de `fetch` dos próprios arquivos e de `import`, que não funcionam em `file://`.

**Choice:** `tests/testes.html`, aberta por um link do painel, roda todos os testes e mostra grupos Lição 1, Lição 2, Lição 3 e Geral, cada teste com o seu AT. A rede é simulada. O disco é simulado nos cenários de falha e real nos testes de bytes, usando o sistema de arquivos privado do navegador (`navigator.storage.getDirectory`).

**Rationale:** O aluno vê as lições aprovadas com um clique, e a mesma rotina de gravação é exercitada num disco de verdade, sem nenhuma pasta escolhida.

**Alternatives Rejected:**
1. `node --test` — exige instalar Node.
2. Chrome em modo sem tela por comando — o caminho muda em cada sistema, e o aluno teria de usar o terminal.

**Consequences:**
- A pasta `tests/` vai junto na extensão, que é local e não publicada.
- A lista de arquivos varridos pelo teste de privacidade é mantida à mão; a página reprova se um arquivo da lista sumir.

### Decision 6: Pasta escolhida a cada abertura

| Attribute | Value |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-11-06 |
| **Source** | DEFINE, Clarifications |

**Context:** Guardar a pasta entre sessões exige um banco local e tratar permissão vencida.

**Choice:** Guardar a referência da pasta só na memória da tela. Antes de cada execução, pedir `requestPermission` em modo de leitura e escrita. Se o seletor não abrir no painel, o link "Abrir em uma aba" abre a mesma tela numa aba da extensão.

**Rationale:** Menos código e menos estados para um exemplo didático, e o armazenamento fica só com cursores.

**Alternatives Rejected:**
1. Guardar a referência em IndexedDB — mais código sem resolver o problema central.

**Consequences:**
- Um clique a mais por sessão.
- Escolher outra pasta não reinicia o cursor. Por isso, "Em dia" mostra o último NSU e avisa onde estão os anteriores, e o aluno usa "Recomeçar do início" quando quiser tudo na pasta nova.

### Decision 7: Certificado sempre com o Chrome

| Attribute | Value |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-11-06 |
| **Source** | DEFINE, AT-304 e AT-406 |

**Context:** O Chrome só apresenta o certificado se a chamada permitir credenciais, e nem sempre abre o seletor numa chamada feita pela extensão.

**Choice:** Chamar com `credentials: 'include'`. Na primeira falha sem resposta do servidor na sessão, abrir o endereço numa aba em segundo plano, esperar carregar por até 60 segundos, fechar e tentar de novo. A API `chrome.tabs` usada aqui (`create`, `get`, `remove`) não pede permissão extra.

**Rationale:** A extensão não toca no certificado: quem escolhe é o Chrome e quem aprova é o aluno.

**Alternatives Rejected:**
1. Pedir um arquivo `.pfx` e senha — custódia de certificado.

**Consequences:**
- O aluno pode ver uma aba aparecer e sumir na primeira execução.
- Para trocar de certificado é preciso fechar o Chrome inteiro; a tela orienta isso no `E2245`.

---

## File Manifest

| # | File | Action | Purpose | Agent / Owner | Dependencies |
|---:|---|---|---|---|---|
| 1 | `extensao/manifest.json` | Create | Permissões mínimas, política de conteúdo e painel | (general) | None |
| 2 | `extensao/config.js` | Create | Constantes da seção Configuration | (general) | None |
| 3 | `extensao/cnpj.js` | Create | `normalizarCnpj`, `calcularDigitos`, `cnpjValido` | (general) | None |
| 4 | `extensao/documento.js` | Create | `decodificarXml`, `lerMetadados`, `caminhoDoDocumento`, `nomeDoArquivo`, `nomeSeguro` | (general) | 2 |
| 5 | `extensao/adn.js` | Create | `interpretarResposta` e `buscarLote` | (general) | 2 |
| 6 | `extensao/arquivos.js` | Create | `gravarArquivo` | (general) | None |
| 7 | `extensao/cursor.js` | Create | `criarCursor` | (general) | None |
| 8 | `extensao/sincronizar.js` | Create | `executarDownload` | (general) | 2, 4, 5, 6, 7 |
| 9 | `extensao/background.js` | Create | Clique no ícone abre o painel | (general) | 1 |
| 10 | `extensao/sidepanel.html` | Create | Marcação da tela, sem script nem estilo embutido | (general) | 1 |
| 11 | `extensao/estilo.css` | Create | Aparência da tela e da página de testes | (general) | 10 |
| 12 | `extensao/tela.js` | Create | `montarTela`, sem acesso direto às APIs do Chrome | (general) | 3, 8, 10 |
| 13 | `extensao/sidepanel.js` | Create | Liga a Tela ao seletor de pasta, ao armazenamento e à aba do certificado | (general) | 5, 6, 7, 8, 12 |
| 14 | `extensao/tests/mini-teste.js` | Create | `teste`, `igual`, `executarTudo`, com grupos e resumo | (general) | None |
| 15 | `extensao/tests/notas-ficticias.js` | Create | Gera XML, lotes e CNPJs fictícios na hora | (general) | 3 |
| 16 | `extensao/tests/simulados.js` | Create | API, disco e armazenamento simulados | (general) | 15 |
| 17 | `extensao/tests/testes.html` | Create | Página de testes | (general) | 11 |
| 18 | `extensao/tests/testes.js` | Create | Um teste por AT, em grupos por lição | (general) | 3, 4, 5, 6, 7, 8, 12, 14, 15, 16, 17 |

**Total Files:** 18

### Agent Assignment Rationale

| Agent / Owner | Files Assigned | Why |
|---|---|---|
| (general) | 1 a 18 | Projeto pequeno em uma só stack, sem especialista necessário |

**Agent Discovery:** Not available

---

## Code Patterns

Os trechos definem contratos. O restante é implementado no Build.

### Pattern 1: Manifesto

```json
{
  "manifest_version": 3,
  "name": "Baixar NFS-e (exemplo didático)",
  "version": "1.0.0",
  "minimum_chrome_version": "120",
  "permissions": ["storage", "sidePanel"],
  "host_permissions": ["https://adn.nfse.gov.br/*"],
  "action": {
    "default_title": "Baixar NFS-e"
  },
  "background": {
    "service_worker": "background.js"
  },
  "side_panel": {
    "default_path": "sidepanel.html"
  },
  "content_security_policy": {
    "extension_pages": "default-src 'self'; connect-src 'self' https://adn.nfse.gov.br; object-src 'none'; base-uri 'none'; form-action 'none'"
  }
}
```

### Pattern 2: O laço das lições 1 e 2

Tudo o que a lição 1 ensina está na ordem do segundo `try`: gravar, salvar o cursor e só depois contar.

```javascript
export async function executarDownload(opcoes) {
  const totais = criarTotais();
  let cursor = await opcoes.cursor.ler(opcoes.cnpj);

  while (true) {
    if (opcoes.deveParar()) return estadoFinal("interrompido", totais);

    const resposta = await opcoes.buscarLote(cursor, opcoes.cnpj);
    if (resposta.tipo === "interrompido") return estadoFinal("interrompido", totais);
    if (resposta.tipo === "falha") return estadoFinal("falhou", totais, resposta.motivo);
    if (resposta.tipo === "fim") return estadoFinal("em-dia", totais);

    const documentos = ordenarPorNsu(resposta.documentos);
    if (documentos === null) return estadoFinal("falhou", totais, "A API devolveu um NSU inválido.");

    for (const item of documentos) {
      if (opcoes.deveParar()) return estadoFinal("interrompido", totais);
      if (item.nsu <= cursor) return estadoFinal("falhou", totais, "O NSU não avançou: " + item.nsu);

      let preparado;
      try {
        preparado = await prepararDocumento(item, opcoes.cnpj);
      } catch (erro) {
        return estadoFinal("falhou", totais, "O documento de NSU " + item.nsu + " não decodifica.");
      }

      try {
        const resultado = await opcoes.gravar(preparado.caminho, preparado.bytes);
        await opcoes.cursor.salvar(opcoes.cnpj, item.nsu);
        contar(totais, preparado.grupo, resultado);
      } catch (erro) {
        return estadoFinal("falhou", totais, "Não consegui gravar o NSU " + item.nsu + ": " + erro.message);
      }
      cursor = item.nsu;
      opcoes.aoProgresso(totais);
    }

    await opcoes.esperar(ESPERA_ENTRE_LOTES_MS);
  }
}
```

### Pattern 3: Gravação que só termina depois de confirmar

```javascript
export async function gravarArquivo(raiz, caminho, bytes) {
  let pasta = raiz;
  const opcaoCriar = criarOpcao();
  for (const parte of caminho.pastas) {
    pasta = await pasta.getDirectoryHandle(parte, opcaoCriar);
  }
  const existente = await abrirSeExistir(pasta, caminho.nome);
  if (existente !== null) {
    const atuais = new Uint8Array(await (await existente.getFile()).arrayBuffer());
    if (bytesIguais(atuais, bytes)) return "ja-existia";
    throw new Error("Já existe um arquivo diferente em " + caminho.pastas.join("/") + "/" + caminho.nome);
  }
  const arquivo = await pasta.getFileHandle(caminho.nome, opcaoCriar);
  const escrita = await arquivo.createWritable();
  try {
    await escrita.write(bytes);
    await escrita.close();
  } catch (erro) {
    await escrita.abort().catch(ignorar);
    throw erro;
  }
  return "gravado";
}

async function abrirSeExistir(pasta, nome) {
  try {
    return await pasta.getFileHandle(nome);
  } catch (erro) {
    if (erro.name === "NotFoundError") return null;
    throw erro;
  }
}

function criarOpcao() {
  return Object.fromEntries([["create", true]]);
}

function ignorar() {
  return undefined;
}
```

O arquivo só aparece na pasta depois de `close()`: até lá o Chrome escreve numa cópia temporária. Por isso, uma queda no meio não deixa arquivo parcial que trave a execução seguinte, e o disco simulado dos testes precisa imitar esse comportamento.

### Pattern 4: Decodificação que preserva os bytes

```javascript
export async function decodificarXml(textoBase64) {
  const bytes = Uint8Array.from(atob(textoBase64), (letra) => letra.charCodeAt(0));
  const ehGzip = bytes[0] === 0x1f && bytes[1] === 0x8b;
  if (ehGzip) {
    const fluxo = new Blob([bytes]).stream().pipeThrough(new DecompressionStream("gzip"));
    return new Uint8Array(await new Response(fluxo).arrayBuffer());
  }
  const inicio = new TextDecoder().decode(bytes.slice(0, 200)).replace(/^﻿/, "").trimStart();
  if (!inicio.startsWith("<")) {
    throw new Error("Conteúdo não é gzip nem XML em texto.");
  }
  return bytes;
}
```

A função devolve os bytes como vieram, e é isso que se grava. O texto só é decodificado à parte, para ler os metadados.

### Pattern 5: Chamada à API

```javascript
const url = URL_DFE + "/" + nsu + "?lote=true&cnpjConsulta=" + encodeURIComponent(cnpj);
const opcoesDaChamada = new Map([
  ["credentials", "include"],
  ["cache", "no-store"],
  ["headers", new Headers([["Accept", "application/json"]])],
  ["signal", controlador.signal],
]);
const resposta = await ambiente.fetch(url, Object.fromEntries(opcoesDaChamada));
const texto = await resposta.text();
const resultado = interpretarResposta(resposta.status, texto);
```

### Pattern 6: Resultado de `interpretarResposta`

| Entrada | `tipo` |
|---|---|
| Código `E2220` ou `NENHUM_DOCUMENTO_LOCALIZADO`, em qualquer status | `fim` |
| 200 com `LoteDFe` vazio, sem `Erros` | `fim` |
| 200 com `LoteDFe` com itens | `lote` |
| 429, 502, 503, 504; 200 vazio, HTML ou JSON inválido | `transitorio` |
| `E2245` ou `E2214` | `falha`, com a orientação ao aluno |
| Qualquer outro caso, incluindo 404 sem `E2220` | `falha`, com o que foi recebido |

### Pattern 7: Teste que injeta falha

```javascript
teste("Lição 1", "AT-103", "falha ao gravar mantém o cursor no documento anterior", async () => {
  const cenario = criarCenario(100);
  cenario.disco.falharNoNsu(30);

  const resultado = await cenario.executar();

  igual(resultado.estado, "falhou");
  igual(await cenario.cursor.ler(cenario.cnpj), 29);
  igual(cenario.disco.nsusGravados().includes(31), false);
});
```

---

### Pattern 8: Elementos da tela

`sidepanel.html` traz só a marcação, e `tela.js` a controla por estes `id`. A mesma marcação serve no painel, na aba e na página de testes.

| `id` | Elemento | Texto ou conteúdo |
|---|---|---|
| `campo-cnpj` | Campo de texto | CNPJ |
| `botao-pasta` | Botão | Escolher pasta |
| `nome-pasta` | Texto | Nome da pasta escolhida, e a orientação "Use uma pasta por empresa, fora do repositório" |
| `botao-baixar` | Botão | Baixar |
| `botao-parar` | Botão | Parar |
| `botao-recomecar` | Botão | Recomeçar do início |
| `botao-confirmar`, `botao-cancelar` | Botões, visíveis só depois de Recomeçar | Confirmar, Cancelar |
| `progresso` | Texto | Lote, NSU e nova tentativa |
| `estado` | Texto | Em dia, Interrompido ou Falhou |
| `motivo` | Texto | Motivo, orientação ou aviso de AT-201 |
| `totais` | Lista | Emitidas, Recebidas, Eventos, Outros, Sem-data, Já existiam |
| `link-testes` | Link para `tests/testes.html`, em nova aba | Abrir testes |
| `link-aba` | Link para `sidepanel.html`, em nova aba | Abrir em uma aba |

`montarTela` recebe a raiz da marcação e um objeto com `escolherPasta`, `pedirPermissao`, `executar` e `cursor`. `tests/testes.html` mostra a linha "N de N aprovados" no elemento `resumo-testes`.

---

## Data Flow

```text
1. Clique em Baixar
   Normaliza e valida o CNPJ; sem CNPJ válido, nenhuma chamada.
   Confere a pasta e a permissão; sem elas, nenhuma chamada.
   │
   ▼
2. Lê o cursor do CNPJ (0 se não houver)
   │
   ▼
3. GET https://adn.nfse.gov.br/contribuintes/DFe/<cursor>?lote=true&cnpjConsulta=<cnpj>
   Sem resposta na 1ª vez: aba do certificado e nova tentativa.
   Transitório: espera crescente, até 5 tentativas; depois, Falhou.
   │
   ▼
4. interpretarResposta
   fim -> Em dia | falha -> Falhou | lote -> continua
   │
   ▼
5. Ordena por NSU numérico; NSU inválido -> Falhou
   │
   ▼
6. Para cada documento:
   a. Parar pedido? -> Interrompido
   b. NSU menor ou igual ao cursor? -> Falhou
   c. Decodifica; erro -> Falhou com o NSU
   d. Lê metadados e define o grupo:
      Eventos | Emitidas | Recebidas | Outros | Sem-data
   e. Grava em Ano/Mês/Grupo/<CNPJ>_<NSU>_<chave>.xml e aguarda close()
      Arquivo igual já existe -> não grava | diferente ou erro -> Falhou com o NSU
   f. Salva o cursor; erro -> Falhou
   g. Atualiza totais (grupo, ou Já existiam) e progresso
   │
   ▼
7. Espera 600 ms e volta ao passo 3 com o último NSU gravado, sem somar 1
   │
   ▼
8. Mostra um único estado final, o motivo, se houver, e os totais por grupo
```

Regras do passo 6d:
- O XML é lido com `DOMParser` a partir de uma cópia em texto. Falha de leitura leva a `Sem-data`.
- `TipoDocumento` igual a `EVENTO`: grupo `Eventos`, mês de `dhEvento` ou `dhProc`.
- Nota: mês de `dCompet`. Grupo `Emitidas` se o CNPJ aparece em `emit` ou `prest`; senão `Recebidas` se aparece em `toma` ou `tomador`; senão `Outros`.
- Sem data no formato `AAAA-MM`, com mês de 01 a 12: grupo `Sem-data`, gravado direto em `Sem-data/`.
- A data é lida do texto, sem `new Date`, para o fuso não mudar o mês.
- O nome tem até 80 caracteres e mantém CNPJ e NSU inteiros: só a chave de acesso é cortada para caber. Sem chave, fica `<CNPJ>_<NSU>.xml`.

---

## Integration Points

| External System | Integration Type | Authentication | Direction | Failure / Retry |
|---|---|---|---|---|
| ADN, `https://adn.nfse.gov.br/contribuintes/DFe` | REST, GET JSON | TLS mútuo: certificado escolhido no Chrome | Saída, sem envio de dado além de NSU e CNPJ | Até 5 tentativas nos casos transitórios; `E2245`, `E2214` e desconhecidos sem nova tentativa |
| File System Access | API do navegador | Permissão do aluno na pasta | Saída para o disco local | Erro interrompe a execução, sem avançar o cursor |
| `chrome.storage.local` | API do navegador | N/A | Bidirecional | Erro ao salvar leva a "Falhou"; o documento é regravado na execução seguinte |

---

## Testing Strategy

| Test Type | Scope / Requirement | Files | Tools | Pass Signal |
|---|---|---|---|---|
| Unit | CNPJ, nome seguro, classificação e `interpretarResposta` (AT-002 a AT-014, AT-201, AT-204 a AT-208) | `extensao/tests/testes.js` | `mini-teste.js` no Chrome | Testes do grupo aprovados |
| Integration | `executarDownload` com rede e disco simulados e 100 notas fictícias: normal, Parar, falha de gravação, queda no 2º lote, 503, timeout e `E2245` no 1º lote (AT-101 a AT-108, AT-209) | `extensao/tests/testes.js`, `extensao/tests/simulados.js` | `mini-teste.js` no Chrome | Nenhuma nota faltando depois da execução seguinte |
| Integration | `gravarArquivo` em disco real do navegador: bytes iguais, repetição sem cópia e recusa de bytes diferentes (AT-013, AT-015, AT-106, AT-108) | `extensao/tests/testes.js` | `navigator.storage.getDirectory` | Bytes lidos iguais aos gravados |
| Integration | Tela com a marcação real e dependências simuladas (AT-002, AT-306, AT-401 a AT-404) | `extensao/tests/testes.js` | DOM do navegador | Estado e botões conferidos |
| Unit | Privacidade: manifesto, política de conteúdo e varredura do código (AT-301 a AT-305, AT-307) | `extensao/tests/testes.js` | `fetch` dos próprios arquivos | Grupo Lição 3 aprovado |
| E2E / Verify Gate | Checklist `manual-ux` do DEFINE: três lições na página de testes, download real, repetição e queda de internet | `extensao/tests/testes.html` | Chrome e certificado do aluno | Checklist assinado |

Regras dos dados de teste:
- CNPJ de teste com dígito válido é calculado na hora por `calcularDigitos`, para o alarme de commit não recusar o arquivo. O vetor conhecido é o exemplo oficial alfanumérico, base `12ABC34501DE` com dígitos `35`.
- Nenhum XML real é usado. As notas fictícias são montadas em `notas-ficticias.js` e comprimidas com `CompressionStream`.
- Prova de que o teste testa: inverter as linhas de gravar e salvar o cursor em `sincronizar.js` tem de reprovar a Lição 1.

---

## Error Handling

| Error Type | Detection | Handling Strategy | Retry? | Observability |
|---|---|---|---|---|
| CNPJ inválido | `cnpjValido` falso, inclusive todos os caracteres iguais a zero | "CNPJ inválido", sem chamada | No | Mensagem na tela |
| Pasta ausente ou permissão negada | Sem referência, `AbortError` ou `requestPermission` diferente de `granted` | Pede a pasta, sem chamada | No | Mensagem na tela |
| Sem resposta do servidor | `fetch` rejeitado | Abre a aba do certificado uma vez por sessão; depois, transitório | Yes | Mensagem de nova tentativa |
| Timeout | Limite de 120 s antes da primeira resposta da sessão, 30 s depois | Transitório | Yes | Mensagem de nova tentativa |
| Instabilidade | 429, 502, 503, 504; 200 vazio, HTML ou JSON inválido | Espera crescente; `Retry-After`, se vier | Yes | Mensagem com tentativa N de 5 |
| Tentativas esgotadas | 5 tentativas sem sucesso | "Falhou" com o último motivo; cursor mantido | No | Estado final |
| `E2245` | Código em `Erros` | "Falhou": certificado sem procuração; orienta a fechar o Chrome inteiro para trocar | No | Texto da API mostrado como texto |
| `E2214` | Código em `Erros` | "Falhou": certificado inválido para a transmissão | No | Texto da API mostrado como texto |
| Resposta desconhecida | Nenhuma regra casa | "Falhou" com o status e até 300 caracteres do corpo | No | Estado final |
| NSU inválido ou que não avança | Não numérico, inseguro ou menor ou igual ao cursor | "Falhou"; cursor mantido | No | NSU na mensagem |
| Documento que não decodifica | Base64 inválido, gzip truncado ou texto que não começa com `<` | "Falhou" com o NSU; cursor no anterior | No | NSU na mensagem |
| XML malformado ou sem data | `parsererror` ou data ausente | Grava sem alterar em `Sem-data/` e conta no resumo | No | Total de `Sem-data` |
| Arquivo existente diferente | Bytes lidos diferem dos recebidos | "Falhou" com NSU e caminho; arquivo e cursor mantidos | No | NSU e caminho na mensagem |
| Falha de gravação | Rejeição de `write` ou `close` | `abort`, depois "Falhou" com NSU e motivo | No | NSU na mensagem |
| Falha ao salvar o cursor | Rejeição do armazenamento | "Falhou"; na execução seguinte, o arquivo é encontrado igual e o cursor avança | No | NSU na mensagem |
| Painel fechado no meio | A execução termina com a página | Cursor no último documento gravado; a execução seguinte continua | No | N/A |

---

## Configuration

Valores em `extensao/config.js`, sem arquivo externo.

| Config Key | Type | Source / Default | Sensitive? | Description |
|---|---|---|---|---|
| `URL_DFE` | texto | `https://adn.nfse.gov.br/contribuintes/DFe` | No | Endereço da API |
| `TENTATIVAS` | número | 5 | No | Máximo de tentativas por lote |
| `ESPERA_BASE_MS` | número | 1000 | No | Primeira espera entre tentativas |
| `FATOR_ESPERA` | número | 1.5 | No | Multiplicador a cada nova tentativa |
| `ESPERA_MAXIMA_MS` | número | 5000 | No | Teto da espera calculada |
| `RETRY_AFTER_MAXIMO_MS` | número | 60000 | No | Teto para `Retry-After` |
| `ESPERA_ENTRE_LOTES_MS` | número | 600 | No | Pausa entre lotes |
| `TEMPO_PRIMEIRA_RESPOSTA_MS` | número | 120000 | No | Limite antes da primeira resposta da sessão, para dar tempo de escolher o certificado |
| `TEMPO_RESPOSTA_MS` | número | 30000 | No | Limite das chamadas seguintes |
| `TEMPO_ABA_CERTIFICADO_MS` | número | 60000 | No | Limite de espera da aba do certificado |

Os limites de tempo e de tentativas vêm do comportamento observado na ferramenta analisada. Não há segredo em nenhuma configuração.

---

## Security Considerations

- **Certificado:** a extensão nunca o lê nem o guarda e não oferece campo de senha ou de arquivo. Quem apresenta é o Chrome, e quem escolhe é o aluno.
- **Destinos de rede:** um único domínio em `host_permissions`, reforçado por `connect-src` na política de conteúdo, que também impede carregar imagem externa.
- **Permissões:** só `storage` e `sidePanel`, sem `content_scripts`, `externally_connectable` ou `web_accessible_resources`.
- **Conteúdo externo:** texto da API e do XML vai para a tela só por `textContent`; `innerHTML` é proibido na extensão. A varredura da Lição 3 confere isso.
- **Nomes de arquivo:** o nome contém o CNPJ consultado e o NSU, para o mesmo NSU de outra empresa não usar o mesmo arquivo. `nomeSeguro` retira `\ / : * ? " < > |` e caracteres de controle, limita a 80 caracteres, retira ponto ou espaço no fim e evita nomes reservados do Windows. As pastas vêm só de números validados e de nomes fixos.
- **Dado fiscal local:** o armazenamento tem só CNPJ e NSU. Os XML ficam na pasta do aluno, e a tela orienta a escolher uma pasta fora do repositório, para nenhuma nota real ir para o git.
- **Registros:** `console` só com status e NSU, nunca conteúdo de nota.
- **Código dinâmico:** sem `eval`, `new Function`, `importScripts`, `sendBeacon` ou `WebSocket`, conferido pela varredura.

---

## Observability

| Aspect | Implementation | Signal / Why |
|---|---|---|
| Logging | Linha de progresso na tela e `console.info` com status e NSU, sem conteúdo de nota | Mostra em que lote parou e por quê |
| Metrics | Totais por `Emitidas`, `Recebidas`, `Eventos`, `Outros`, `Sem-data` e `Já existiam`, e cursor atual | Permite comparar o resumo com a pasta, como pede o Verify Gate |
| Tracing | N/A: tudo roda numa única página | N/A |

---

## Requirements Traceability

| Requirement / AT | Design Element | Test / Gate |
|---|---|---|
| AT-001, AT-004, AT-005, AT-006 | `adn.js`, `cursor.js`, `sincronizar.js`, Pattern 5 | Grupo Geral e Verify Gate |
| AT-002, AT-003 | `cnpj.js`, `tela.js` | Grupo Geral |
| AT-007 a AT-015 | `documento.js`, `arquivos.js`, Pattern 4 | Grupo Geral |
| AT-101 a AT-108 (MUST Lição 1) | `sincronizar.js`, `arquivos.js`, Decision 2, Patterns 2 e 3 | Grupo Lição 1 |
| AT-201 a AT-209 (MUST Lição 2) | `adn.js`, `sincronizar.js`, Decision 3, Pattern 6 | Grupo Lição 2 |
| AT-301 a AT-307 (MUST Lição 3) | `manifest.json`, Decision 4, Decision 7, `tela.js` | Grupo Lição 3 |
| AT-401 a AT-404 (SHOULD Recomeçar e progresso) | `tela.js`, `cursor.js`, Decision 6 | Grupo Geral |
| AT-405, AT-406 | `sidepanel.js`, Decision 7 | Verify Gate, download real |
| MUST Página de testes | `tests/`, Decision 5 | Verify Gate |

---

## Risks and Mitigations

| Risk | Impact | Mitigation | Residual Risk |
|---|---|---|---|
| A resposta real do ADN difere do que foi lido em código (A-001 a A-004) | Falha no primeiro download real | Lista fechada de sinais: a diferença aparece como "Falhou" com o que foi recebido | Ajuste do módulo `adn.js` depois do teste real |
| O seletor de pasta não abre no painel (A-005) | Sem pasta, sem download | Link "Abrir em uma aba" para a mesma tela | Um clique a mais |
| O certificado não é pedido (A-007) | Falha de rede na primeira chamada | Aba em segundo plano e orientação na tela | O aluno pode ter de reiniciar o Chrome |
| ADN recusa CNPJ alfanumérico (A-006) | Empresas novas não baixam | A recusa aparece como "Falhou" com o motivo | Ajuste quando o comportamento for conhecido |
| Certificado A3 com SafeSign falha no TLS | Aluno com esse token não usa a extensão | Limitação registrada; a orientação não inclui rebaixar TLS | Limitação da v1 |
| Aluno escolhe a pasta dentro do repositório | Nota real pode ir para o git | Orientação na tela e alarme de commit da `sdd-higiene-dado` | O alarme não lê todo conteúdo de XML |
| Notas de duas empresas na mesma pasta | Organização confusa, sem perda, porque o nome tem o CNPJ | Orientação na tela | Recusa automática adiada na revisão de governança |
| Download longo com o painel fechado | Execução para no meio | O cursor preserva o avanço; a execução seguinte continua | Nenhum |

---

## Advisor Ledger

None — no formal external design review.

---

## Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-11-06 | SDD Design by RDD | Initial version |

---

## Next Step

Execute o **SDD Build by RDD**.
