# Exemplo: extensão que baixa suas NFS-e

Um exemplo completo do método SDD. Os três primeiros documentos já estão prontos, e você constrói a aplicação com o seu agente de IA, sem programar.

Ao final, você terá uma extensão do Chrome que baixa os XML das NFS-e de uma empresa pelo Ambiente Nacional, usando o certificado digital já instalado no navegador. As notas ficam numa pasta do seu computador, separadas por ano, mês e tipo. Nada passa por servidor de terceiros.

> **Situação deste exemplo:** os testes automáticos da extensão foram ensaiados, mas o download real ainda não foi conferido com um certificado. O formato da resposta da API foi lido de código, não da documentação oficial, que só confirma o método. Se o seu primeiro download mostrar "Falhou", leia o motivo na tela e peça ao seu agente para ajustar `extensao/adn.js`.

## O que o exemplo ensina

| Lição | O que acontece | Por que importa |
|---|---|---|
| **1. O cursor só avança com gravação confirmada** | A extensão só anota "baixei até aqui" depois que o Chrome confirma o arquivo gravado | Se o marcador andar antes da gravação, uma falha pula notas para sempre |
| **2. Falha nunca vira sucesso** | "Em dia" só aparece quando a API diz que acabou | Uma tela verde depois de uma queda esconde notas não baixadas |
| **3. Privacidade por desenho** | O próprio Chrome bloqueia qualquer destino fora de `adn.nfse.gov.br` | Você não precisa confiar em promessa: a regra está no manifesto e é testada |

## O que você precisa

- Chrome versão 120 ou mais nova, fora de janela anônima.
- Um agente de IA com as skills SDD instaladas. Veja o [Quickstart](../../docs/quickstart.pt-BR.md).
- Certificado digital da empresa ou da matriz instalado no Chrome, só para o download real. Certificado A3 com SafeSign pode não funcionar nesta versão.

Você não precisa de Node, npm nem de instalar nenhuma biblioteca.

## Passo a passo

### 1. Crie a pasta do projeto

Crie uma pasta nova, fora de iCloud, OneDrive, Dropbox ou Google Drive, e abra essa pasta no seu agente. Dentro dela, crie uma subpasta chamada `sdd`.

### 2. Coloque os três documentos na pasta `sdd`

Baixe estes arquivos e salve-os em `sdd/`, sem mudar os nomes:

- [BRAINSTORM_BAIXAR_NFSE.md](BRAINSTORM_BAIXAR_NFSE.md): por que construir e o que ficou de fora.
- [DEFINE_BAIXAR_NFSE.md](DEFINE_BAIXAR_NFSE.md): o que precisa funcionar e como provar.
- [DESIGN_BAIXAR_NFSE.md](DESIGN_BAIXAR_NFSE.md): como construir, arquivo por arquivo.

### 3. Inicie a sessão de build

Cole este prompt no seu agente:

```text
Execute o SDD Build by RDD para a feature BAIXAR_NFSE.

Os documentos estão em sdd/: BRAINSTORM_BAIXAR_NFSE.md, DEFINE_BAIXAR_NFSE.md e DESIGN_BAIXAR_NFSE.md. Leia os três antes de começar.

Regras desta construção:
- Crie somente os arquivos do File Manifest, todos dentro de extensao/.
- Não instale Node, npm nem biblioteca nenhuma.
- Nunca usei terminal: quando eu precisar fazer algo no Chrome, me passe um passo por vez e diga o que devo ver na tela.
- No Verify Gate, me mostre o checklist um item por vez, espere a minha confirmação e registre o resultado no BUILD_REPORT.
- Não use nenhum dado real de nota, CNPJ de cliente ou certificado em arquivo do projeto.
```

O agente vai perguntar como prefere executar. Aceite a recomendação dele se estiver em dúvida. Ao final desta etapa, a pasta `extensao/` estará pronta.

### 4. Carregue a extensão no Chrome

1. Digite `chrome://extensions` na barra de endereços.
2. Ligue **Modo do desenvolvedor**, no canto superior direito.
3. Clique em **Carregar sem compactação** e escolha a pasta `extensao`. O cartão "Baixar NFS-e (exemplo didático)" aparece, sem botão vermelho de erros.
4. Clique no ícone de quebra-cabeça da barra do Chrome e depois em **Baixar NFS-e**. O painel lateral abre.

### 5. Rode os testes das lições

No painel, clique em **Abrir testes**. Uma aba mostra os grupos Lição 1, Lição 2, Lição 3 e Geral. O resultado esperado é a linha com todos os testes aprovados, por exemplo "45 de 45 aprovados". O número exato pode variar.

Esses testes não usam internet nem certificado: a rede e as falhas são simuladas, com notas fictícias.

### 6. Prove que os testes testam

Peça ao seu agente:

```text
Em extensao/sincronizar.js, inverta a ordem das linhas que gravam o documento e salvam o cursor. Não mude mais nada.
```

Recarregue a extensão em `chrome://extensions` e abra os testes de novo: a Lição 1 precisa reprovar. É esse o defeito que perde notas. Depois peça ao agente para desfazer a mudança e confira que tudo volta a passar.

### 7. Baixe as notas de verdade

1. No painel, digite o CNPJ da empresa.
2. Clique em **Escolher pasta** e escolha uma pasta **fora do projeto**, para nenhuma nota real ir para o git. Use uma pasta por empresa.
3. Clique em **Baixar**. Na primeira vez, o Chrome pede o certificado, e uma aba pode aparecer e sumir sozinha.
4. Ao final, confira o resumo. As notas ficam em `Ano/Mês/Emitidas`, `Recebidas`, `Eventos` ou `Outros`, e em `Sem-data` quando o XML não traz uma data legível.
5. Clique em **Baixar** de novo. A tela deve mostrar **Em dia**, sem arquivo novo.
6. Desligue a internet e clique em **Baixar**. A tela deve mostrar **Falhou**, nunca "Em dia".

Com isso, você confirma para o agente os itens do Verify Gate, e ele fecha o relatório do build.

## Se algo der errado

| O que apareceu | O que fazer |
|---|---|
| Erro ao carregar a extensão | Confira se escolheu a pasta `extensao`, que contém o `manifest.json` |
| O seletor de pasta não abre no painel | Clique em **Abrir em uma aba** e repita lá |
| "Falhou" com certificado sem procuração | Feche o Chrome inteiro, abra de novo e escolha o certificado certo |
| "Falhou" com instabilidade do servidor | Rode de novo mais tarde. A extensão continua de onde parou |
| "Falhou" com arquivo diferente | A extensão não troca uma nota já guardada. Compare os dois XML antes de decidir, ou baixe em outra pasta |
| Um teste reprovado | Mostre ao seu agente a linha reprovada e peça para corrigir o código, sem mudar o teste |
| Quero baixar tudo de novo em outra pasta | Escolha a pasta e use **Recomeçar do início** |

## O que este exemplo não faz

Atende uma empresa por vez e consulta só por CNPJ. Não gera planilha nem PDF e não é publicado na Chrome Web Store. A lista completa está no [DEFINE](DEFINE_BAIXAR_NFSE.md), em "Out of Scope".

A responsabilidade pelo uso do certificado e pela guarda dos documentos fiscais é sua. Este é um exemplo didático, sem garantia de que substitui a sua rotina de conferência.
