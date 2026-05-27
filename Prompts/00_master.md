# 00 — PROMPT MESTRE: Apresentação HTML do Projeto A3

> **Como usar este conjunto de prompts:** este arquivo é o ponto de entrada. Você (agente de IA) deve ler **os quatro** arquivos `.md` desta pasta `Prompts/` antes de começar a gerar código. Cada um cobre uma responsabilidade diferente; o entregável final é **um único arquivo HTML**.

---

## 1. Identidade do entregável

- **O quê:** apresentação web estilo "PowerPoint" em **um único arquivo HTML autocontido**.
- **Saída obrigatória:** `projeto_a3/reports/apresentacao_a3.html`
- **Como será usado:** apresentação **ao vivo em projetor / notebook**, navegada por teclado (setas) e botões na tela.
- **Idioma:** **Português do Brasil**. Não traduza para inglês ou espanhol em hipótese alguma — mesmo quando citar termos técnicos do notebook original (que está em espanhol), traduza para PT-BR.
- **Audiência:** professor e banca acadêmica da disciplina de Inteligência Artificial (Universidade São Judas Tadeu).

## 1.1. Acesso ao filesystem (importante)

Você está executando com acesso de leitura/escrita à pasta-raiz do projeto:

```
C:\Users\PICHAU\Desktop\Faculdade_Eng_Software\AI\
```

Este é o seu diretório de trabalho. **Tudo o que você precisa está dentro dele** — não tente baixar nada da internet em runtime (exceto os CDNs do Three.js e Google Fonts no carregamento inicial da página final).

Árvore de diretórios relevante (apenas o que importa para esta tarefa):

```
AI/                                          ← raiz do repositório (você está aqui)
├── Prompts/                                 ← você LÊ estes arquivos
│   ├── 00_master.md                         (este arquivo)
│   ├── 01_slides_conteudo.md
│   ├── 02_simulacao_3d.md
│   ├── 03_estilo_visual.md
│   └── KICKOFF.md                           (mensagem que você recebeu — pode ignorar)
│
├── projeto_a3/                              ← código e dados do projeto
│   ├── README.md                            (leitura útil, opcional)
│   ├── main.py                              (orquestrador — opcional)
│   ├── src/                                 (módulos do pipeline — opcional)
│   ├── data/
│   │   └── raw/sbdb_asteroides.csv          (NÃO precisa ler — simulação é sintética)
│   ├── notebooks/
│   │   └── 01_eda.ipynb                     (referência conceitual — NÃO leia inteiro, é pesado)
│   ├── outputs/                             ← você LÊ daqui
│   │   ├── figures/                         (8 PNGs para embedar em base64)
│   │   │   ├── 01_distribuicao_target.png
│   │   │   ├── 02_heatmap_correlacao.png
│   │   │   ├── 03_pca_2d.png
│   │   │   ├── 04_matrizes_confusao.png
│   │   │   ├── 05_comparacao_metricas.png
│   │   │   ├── 06_curvas_roc.png
│   │   │   ├── 07_curvas_precision_recall.png
│   │   │   └── 08_feature_importance.png
│   │   └── metrics/
│   │       └── relatorio_metricas.csv       (números das métricas — já transcritos em 01_slides_conteudo.md)
│   └── reports/                             ← você ESCREVE aqui
│       └── apresentacao_a3.html             (ESTE é o entregável final)
│
└── (outros arquivos na raiz — ignore)
```

**Regras de acesso:**

- **Leitura permitida em toda a pasta `AI/`.** Mas você só precisa abrir os arquivos listados acima como "você LÊ daqui".
- **Escrita permitida apenas em `projeto_a3/reports/apresentacao_a3.html`.** Não crie nem modifique nada fora desse caminho.
- **Não leia `01_eda.ipynb` inteiro** — ele tem ~300KB com imagens em base64 que poluem seu contexto. O conteúdo conceitual relevante já foi destilado em `01_slides_conteudo.md`. Consulte o notebook apenas se algo em `01_slides_conteudo.md` ficar ambíguo e mesmo assim leia só células específicas via `jq` ou similar.
- **Caminhos absolutos vs. relativos:** use caminhos absolutos no Windows (`C:\Users\PICHAU\...`) ou ajuste para o estilo do seu shell. O arquivo HTML final, ao referenciar imagens, deve usar **data URIs base64** e não caminhos de filesystem.

**Sanidade antes de começar:** liste os 8 PNGs em `projeto_a3/outputs/figures/` e confirme que todos existem. Se algum estiver faltando, pare e me avise — não tente regerar nada (`python main.py` está fora do seu escopo).

## 2. Contexto do projeto (resumo executivo)

O Projeto A3 implementa um **comitê de classificadores supervisionados** para prever se um asteroide é **PHA (Potentially Hazardous Asteroid)** — potencialmente perigoso para a Terra — usando o dataset **NASA JPL Small-Body Database**.

Pipeline (já executado, com saídas em `projeto_a3/outputs/`):

1. Carregamento do CSV (`projeto_a3/data/raw/sbdb_asteroides.csv`)
2. Pré-processamento + engenharia de atributos (4 features derivadas com justificativa física)
3. Balanceamento por undersampling 1:3
4. Treino de 6 classificadores individuais (KNN, Naive Bayes, Decision Tree, SVM, MLP, Random Forest)
5. Construção de ensembles (soft voting, hard voting, threshold tuning)
6. Avaliação + validação cruzada
7. Geração de 8 gráficos PNG em `projeto_a3/outputs/figures/`

Os números, métricas e descrições que devem aparecer nos slides estão em `01_slides_conteudo.md`.

## 3. Arquivos desta pasta (leia todos antes de codar)

| Arquivo | Responsabilidade |
|---|---|
| `00_master.md` | (este arquivo) instruções gerais, stack, regras globais |
| `01_slides_conteudo.md` | conteúdo textual exato de cada um dos 12 slides |
| `02_simulacao_3d.md` | especificação técnica da simulação Three.js (slide 11) |
| `03_estilo_visual.md` | CSS, tipografia, fundo estrelado, transições, navegação |

**Regra:** se houver conflito entre arquivos, a prioridade é: `00_master.md` > `01_slides_conteudo.md` > `02_simulacao_3d.md` > `03_estilo_visual.md`.

## 4. Stack técnica permitida

- **HTML5 + CSS3 + JavaScript vanilla (ES6+)**, em um único arquivo.
- **Bibliotecas via CDN** (sem build step, sem npm, sem bundler):
  - **Three.js** (r160+) — obrigatório, usado na simulação 3D. Importar via CDN ES module ou UMD.
  - **OrbitControls** (módulo do Three.js) — obrigatório para a câmera orbital.
  - **Google Fonts** — `Orbitron` (títulos) e `Space Mono` (corpo / números).
- **PROIBIDO:** React, Vue, frameworks de slides prontos (Reveal.js, Impress.js), Tailwind via build, bundlers.
- **PROIBIDO:** chamar APIs externas em runtime (NASA, Sentry, etc.). Tudo deve funcionar offline depois de carregar (a única exceção são os CDNs de Three.js e Google Fonts no carregamento inicial).

## 5. Como incorporar os 8 gráficos PNG

Os 8 PNGs vivem em `projeto_a3/outputs/figures/`:

```
01_distribuicao_target.png
02_heatmap_correlacao.png
03_pca_2d.png
04_matrizes_confusao.png
05_comparacao_metricas.png
06_curvas_roc.png
07_curvas_precision_recall.png
08_feature_importance.png
```

Você **deve embedar cada PNG em base64** dentro do próprio HTML, usando `<img src="data:image/png;base64,...">`. O arquivo final precisa abrir sem dependência de pasta externa.

Para gerar os data URIs, leia cada PNG do filesystem (caminhos absolutos listados na seção 1.1) e converta para base64. Mantenha as tags `<img>` com `alt` descritivo e `loading="eager"`.

## 6. Arquitetura geral do HTML

```
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>Projeto A3 — Comitê de Classificadores para PHA</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>/* tudo inline — ver 03_estilo_visual.md */</style>
  </head>
  <body>
    <canvas id="stars-bg"></canvas>           <!-- fundo estrelado animado -->
    <main id="deck">
      <section class="slide" data-slide="1">...</section>
      <section class="slide" data-slide="2">...</section>
      ...
      <section class="slide" data-slide="12">...</section>
    </main>

    <nav id="controls">
      <button id="prev" aria-label="Slide anterior">◀</button>
      <span id="counter">1 / 12</span>
      <button id="next" aria-label="Próximo slide">▶</button>
    </nav>

    <div id="progress-bar"><div id="progress-fill"></div></div>

    <!-- Modal/overlay da simulação 3D, ocupa tela cheia quando ativo -->
    <div id="simulation-modal" aria-hidden="true">
      <div id="three-canvas-wrapper"></div>
      <div id="sim-controls">...</div>
      <button id="close-sim">✕ Fechar simulação (ESC)</button>
    </div>

    <script type="module">/* tudo inline — Three.js + lógica de slides */</script>
  </body>
</html>
```

## 7. Navegação (regras invariáveis)

- **Setas ←/→ do teclado** trocam slides.
- **Espaço** avança ao próximo slide.
- **Home/End** vão ao primeiro/último slide.
- **F** (ou tecla nativa F11 do browser também serve) alterna fullscreen.
- **ESC** fecha a simulação 3D se aberta (não sai do fullscreen — esse é controle do browser).
- Botões `◀ ▶` na tela fazem o mesmo que ←/→.
- Barra de progresso no rodapé reflete `(slide_atual / total)`.
- Contador `N / 12` visível no canto.
- Os atalhos de teclado devem ser **desativados quando o modal de simulação estiver aberto** (exceto ESC, que fecha).

## 8. Acessibilidade mínima

- `lang="pt-BR"` no `<html>`.
- `alt` real em todos os `<img>` (descreva o gráfico, não apenas "gráfico 1").
- Botões com `aria-label`.
- Contraste ≥ 4.5:1 entre texto e fundo (o tema é escuro — cuide do texto branco/cinza-claro sobre o azul-marinho).
- Slide deve ter um `<h1>` ou `<h2>` semântico, não apenas `<div>`s estilizados.

## 9. Performance

- Lazy-init da simulação Three.js: só carregue/instancie a cena 3D **quando o usuário clicar no botão "Iniciar simulação"** no slide 11. Não inicialize Three.js no carregamento da página.
- Pause o `requestAnimationFrame` da simulação quando o modal estiver fechado.
- O fundo estrelado (`<canvas id="stars-bg">`) deve usar 2D context e ser leve (≤ 200 estrelas, twinkle suave). Pause a animação dele quando a simulação 3D estiver aberta.

## 10. Fallbacks de robustez

- Se o navegador não suportar WebGL: ao clicar em "Iniciar simulação", mostrar mensagem amigável em português ("Seu navegador não suporta WebGL. A simulação 3D não pode ser exibida.") em vez de quebrar a apresentação.
- Se o usuário tiver `prefers-reduced-motion`: desabilitar a animação do fundo estrelado e as transições entre slides (usar apenas troca instantânea).

## 11. Critérios de aceitação (checklist final)

Antes de declarar pronto, valide:

- [ ] Arquivo único `apresentacao_a3.html` salvo em `projeto_a3/reports/`.
- [ ] Abre em Chrome/Edge mais recentes sem erros no console.
- [ ] 12 slides presentes com o conteúdo de `01_slides_conteudo.md`.
- [ ] Os 8 PNGs estão embedados em base64 (verifique tamanho do HTML — vai ficar grande, é esperado, ~3-8 MB).
- [ ] Navegação por teclado funciona (←/→/espaço/Home/End/F).
- [ ] Botão "Iniciar simulação 3D" no slide 11 abre o modal e roda Three.js conforme `02_simulacao_3d.md`.
- [ ] Tema escuro espacial conforme `03_estilo_visual.md`.
- [ ] Sem chamadas de rede em runtime (apenas CDNs no carregamento).
- [ ] HTML é válido (sem tags abertas, sem atributos duplicados).
- [ ] Sem erros de "mixed content" se aberto via `file://`.

## 12. Postura ao implementar

- **Não invente métricas.** Use somente os números fornecidos em `01_slides_conteudo.md` ou extraídos de `projeto_a3/outputs/metrics/relatorio_metricas.csv`.
- **Não simplifique a simulação 3D** abaixo do mínimo descrito em `02_simulacao_3d.md`.
- **Não adicione slides extras** nem remova slides — são exatamente 12.
- **Não troque a stack** — Three.js é obrigatório para a simulação.
- Se algo for ambíguo entre os arquivos, escolha a opção mais simples e funcional e adicione um comentário `<!-- DECISÃO: ... -->` no HTML para revisão posterior.

---

**Pronto para executar.** Leia agora `01_slides_conteudo.md`.
