# KICKOFF — Mensagem inicial para o agente executor

> Copie o bloco abaixo e cole como **primeira mensagem** ao novo agente de IA. Ele assume que o agente tem acesso ao repositório `C:\Users\PICHAU\Desktop\Faculdade_Eng_Software\AI\` e pode ler arquivos, listar diretórios e escrever no filesystem.

---

```
Você vai produzir o entregável final do meu Projeto A3 de Inteligência Artificial: uma apresentação web estilo PowerPoint em um único arquivo HTML autocontido.

CONTEXTO

- Repositório: C:\Users\PICHAU\Desktop\Faculdade_Eng_Software\AI\
- Projeto: classificação supervisionada de asteroides potencialmente perigosos (PHA) usando comitê de 6 classificadores + ensembles, dataset NASA JPL Small-Body Database.
- Pipeline já está implementado e executado. As saídas (8 gráficos PNG + métricas CSV) já existem em `projeto_a3/outputs/`.
- Idioma: Português do Brasil. Não traduza para outro idioma.

ACESSO AO FILESYSTEM

Você está executando com acesso de leitura/escrita à pasta-raiz do projeto:

  C:\Users\PICHAU\Desktop\Faculdade_Eng_Software\AI\

Esse é o seu diretório de trabalho. Tudo o que você precisa está dentro dele.

- LEITURA: toda a pasta AI/ está disponível. Os arquivos que você efetivamente precisa abrir são:
  * Os 4 arquivos .md de instrução em AI\Prompts\ (listados abaixo)
  * Os 8 PNGs em AI\projeto_a3\outputs\figures\ (para embedar em base64)
  * Opcionalmente AI\projeto_a3\outputs\metrics\relatorio_metricas.csv para conferir números
- NÃO leia AI\projeto_a3\notebooks\01_eda.ipynb inteiro (~300 KB, polui seu contexto). O conteúdo conceitual relevante já está destilado em 01_slides_conteudo.md.
- ESCRITA: apenas AI\projeto_a3\reports\apresentacao_a3.html. Não crie ou modifique nada fora desse caminho.
- Antes de começar a codar, liste os 8 PNGs em outputs\figures\ e confirme que todos existem. Se algum faltar, pare e me avise.

A seção 1.1 de 00_master.md tem a árvore de diretórios completa que você deve consultar.

SUAS INSTRUÇÕES ESTÃO EM 4 ARQUIVOS .md

Antes de escrever qualquer linha de código, leia, na ordem, os quatro arquivos abaixo. Eles contêm a especificação completa do entregável:

1. C:\Users\PICHAU\Desktop\Faculdade_Eng_Software\AI\Prompts\00_master.md
   — regras globais, stack, arquitetura do HTML, critérios de aceitação.

2. C:\Users\PICHAU\Desktop\Faculdade_Eng_Software\AI\Prompts\01_slides_conteudo.md
   — texto literal de cada um dos 12 slides, com números reais a usar.

3. C:\Users\PICHAU\Desktop\Faculdade_Eng_Software\AI\Prompts\02_simulacao_3d.md
   — especificação técnica da simulação Three.js do slide 11.

4. C:\Users\PICHAU\Desktop\Faculdade_Eng_Software\AI\Prompts\03_estilo_visual.md
   — paleta, tipografia, layout, transições, fundo estrelado.

Se houver conflito entre arquivos, a prioridade é 00 > 01 > 02 > 03.

ENTREGÁVEL

Um único arquivo HTML salvo em:
  C:\Users\PICHAU\Desktop\Faculdade_Eng_Software\AI\projeto_a3\reports\apresentacao_a3.html

Ele precisa:
- Conter exatamente 12 slides com o conteúdo definido em 01_slides_conteudo.md.
- Embedar os 8 PNGs de `projeto_a3/outputs/figures/` em base64 (você lê os arquivos do disco e converte).
- Usar Three.js (via CDN) para a simulação 3D do slide 11, conforme 02_simulacao_3d.md.
- Aplicar o tema visual de 03_estilo_visual.md (tema espacial escuro, Orbitron + Space Mono, fundo estrelado animado).
- Navegação por setas ←/→, espaço, Home/End, F (fullscreen), ESC (fecha simulação).
- Funcionar offline depois de carregar (CDNs apenas no carregamento inicial).

PASSOS QUE EU ESPERO QUE VOCÊ SIGA

1. Ler os 4 arquivos .md desta pasta, na ordem.
2. Listar e verificar a existência dos 8 PNGs em `projeto_a3/outputs/figures/` e do CSV `projeto_a3/outputs/metrics/relatorio_metricas.csv`.
3. Ler os PNGs do disco, converter cada um para data URI base64 (preserve a string completa).
4. Montar o HTML único conforme a arquitetura descrita em 00_master.md seção 6.
5. Validar contra o checklist da seção 11 de 00_master.md antes de declarar pronto.
6. Salvar o arquivo no caminho especificado.
7. Me reportar: tamanho final do HTML, lista do que ficou pronto e qualquer decisão que você tomou para resolver ambiguidade (marque cada decisão como comentário <!-- DECISÃO: ... --> no próprio HTML).

RESTRIÇÕES

- Não invente métricas. Use só os números que estão em 01_slides_conteudo.md ou no CSV de métricas.
- Não adicione, remova ou reordene slides.
- Não troque a stack (Three.js é obrigatório; nada de React/Vue/Reveal.js).
- Não baixe imagens ou texturas externas em runtime — só Three.js e Google Fonts via CDN são aceitáveis no carregamento.
- Não otimize para mobile; o alvo é projetor / notebook.

Pode começar. Quando terminar, me dê o caminho final e um resumo do que foi produzido.
```

---

## Como usar

1. Abra uma sessão nova do seu agente de IA (Claude Code, Cursor, etc.) **no diretório raiz do projeto** (`C:\Users\PICHAU\Desktop\Faculdade_Eng_Software\AI\`).
2. Cole o bloco acima como primeira mensagem.
3. Aprove os tool calls de leitura dos `.md` e dos PNGs, e a escrita do HTML final.
4. Quando terminar, abra `projeto_a3/reports/apresentacao_a3.html` no Chrome/Edge em tela cheia e teste a navegação por teclado + o botão da simulação 3D.

## Notas

- Se o agente reclamar que algum PNG não existe, rode antes `python projeto_a3/main.py` para regenerar a pasta `outputs/`.
- Se quiser apresentar sem internet, abra o HTML uma vez com internet (para o navegador cachear Three.js e Google Fonts) e depois desligue — daí em diante roda offline.
- Para iterar o conteúdo dos slides sem ter que regerar tudo, edite `01_slides_conteudo.md` e peça ao agente: *"Re-leia 01_slides_conteudo.md e regere apenas o HTML — mantendo a estrutura, o CSS e a simulação 3D."*
