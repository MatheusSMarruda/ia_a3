# 01 — CONTEÚDO DOS SLIDES

> Este arquivo define **exatamente** o que cada slide deve mostrar. Você pode formatar/diagramar livremente respeitando o estilo de `03_estilo_visual.md`, mas **o texto, números e ordem dos elementos são fixos**. Não acrescente nem omita slides.

São **12 slides**. Cada seção abaixo descreve um slide com: `título`, `subtítulo` (opcional), `corpo` (bullets, frases ou imagens) e `notas de implementação`.

---

## SLIDE 1 — Capa

**Título principal (h1, fonte Orbitron, grande):**
> Comitê de Classificadores para Asteroides Potencialmente Perigosos

**Subtítulo:**
> Predição de PHA com base no NASA JPL Small-Body Database

**Rodapé do slide (3 linhas, fonte Space Mono):**
- Projeto A3 — Inteligência Artificial
- Universidade São Judas Tadeu — 2026/1
- Autor: Matheus Arruda

**Notas de implementação:**
- Slide com layout centralizado vertical e horizontalmente.
- Adicione um pequeno "badge" animado no topo com o texto `▸ PRESSIONE → PARA COMEÇAR` que pulsa suavemente.
- Pode incluir um ícone/SVG estilizado de asteroide ou órbita ao lado do título (vetorial, não imagem rasterizada).

---

## SLIDE 2 — O problema e a motivação

**Título:** O Problema

**Pergunta-chave (destaque grande, centro do slide):**
> Dado um asteroide qualquer do catálogo da NASA, **conseguimos prever se ele é potencialmente perigoso para a Terra?**

**Bullets (lado direito ou abaixo da pergunta):**
- **PHA** = *Potentially Hazardous Asteroid* — asteroide cuja órbita aproxima-se da Terra a menos de **0,05 UA** (~7,5 milhões de km) e que tem diâmetro estimado ≥ 140 m.
- A NASA mantém o sistema **Sentry**, que vigia colisões potenciais nos próximos 100 anos.
- O custo de uma identificação errada é assimétrico: **falso negativo** (perigoso classificado como inofensivo) é muito pior que falso positivo.
- Por isso priorizamos **recall** sobre precisão no ajuste final.

**Notas:** use ícone/emoji-livre estilizado de alerta (⚠) com cor de destaque (âmbar/vermelho) ao lado do termo "falso negativo".

---

## SLIDE 3 — Dataset

**Título:** Dataset — NASA JPL Small-Body Database

**Coluna esquerda — Origem:**
- **Fonte oficial:** `https://ssd.jpl.nasa.gov/sbdb_query.cgi`
- **Arquivo local:** `projeto_a3/data/raw/sbdb_asteroides.csv`
- **Tipo:** observações catalográficas de pequenos corpos do sistema solar.

**Coluna direita — Variável alvo:**
- **PHA** (binária):
  - `Y` → potencialmente perigoso → codificado como **1**
  - `N` → não perigoso → codificado como **0**
- **Problema:** classificação **supervisionada binária**.
- **Desbalanceamento severo** na base bruta — tratado na etapa de balanceamento.

**Rodapé técnico (faixa inferior, fonte mono, cinza):**
- Features brutas usadas: `q, ad, H, ma, per, e, a, i` (8 colunas orbitais e físicas)
- Features derivadas: `q_earth_diff, orbital_energy, orbital_range, orbital_risk` (4 colunas — slide 6)

---

## SLIDE 4 — Glossário rápido

**Título:** Glossário Astronômico Essencial

**Tabela de 2 colunas (termo | definição curta):**

| Termo | Significado |
|---|---|
| **UA** | Unidade Astronômica = distância Terra-Sol ≈ 149,6 milhões de km |
| **q** | Periélio — distância mínima do asteroide ao Sol (UA) |
| **ad** | Afélio — distância máxima do asteroide ao Sol (UA) |
| **a** | Semi-eixo maior da órbita (UA) |
| **e** | Excentricidade — quanto a órbita "estica" (0 = circular, 1 = parabólica) |
| **i** | Inclinação orbital em relação ao plano da Terra (graus) |
| **H** | Magnitude absoluta — proxy do tamanho do asteroide |
| **MOID** | *Minimum Orbit Intersection Distance* — distância mínima entre as órbitas do asteroide e da Terra. Se < 0,05 UA → critério PHA |
| **NEO** | *Near-Earth Object* — asteroide com órbita próxima à da Terra |
| **PHA** | NEO grande o suficiente e perto o suficiente para ser monitorado como ameaça |

**Notas:** este slide existe para a banca não perder o fio durante a apresentação. Fonte do termo em **Orbitron negrito** (cor accent), definição em Space Mono normal.

---

## SLIDE 5 — Pipeline geral

**Título:** Pipeline do Projeto

**Diagrama horizontal de 7 etapas conectadas por setas →** (renderize em HTML/CSS puro, sem imagem):

1. **Carregamento** — `sbdb_asteroides.csv`
2. **EDA** — distribuição, correlações, PCA
3. **Pré-processamento** — imputação (mediana) + 4 features derivadas
4. **Balanceamento** — undersampling 1:3 da classe majoritária
5. **Split + Padronização** — 80/20 estratificado + `StandardScaler`
6. **6 Classificadores** — KNN, Naive Bayes, Decision Tree, SVM, MLP, Random Forest
7. **Ensemble + Avaliação** — soft voting, hard voting, threshold tuning, k-fold

**Legenda abaixo:**
> Cada caixa do diagrama corresponde a um módulo em `projeto_a3/src/` (`carregamento.py`, `preprocessamento.py`, `balanceamento.py`, `modelos.py`, `ensemble.py`, `avaliacao.py`).

**Notas:** caixas com borda neon (accent color), setas animadas com `keyframes` (fluxo da esquerda para a direita). Em telas estreitas, quebrar em duas linhas de etapas.

---

## SLIDE 6 — EDA + Engenharia de Atributos

**Título:** Análise Exploratória e Features Derivadas

**Layout em duas colunas:**

### Coluna esquerda — Imagens (embedadas)
1. `01_distribuicao_target.png` — caption: *"Distribuição original do alvo PHA — fortemente desbalanceado."*
2. `02_heatmap_correlacao.png` — caption: *"Correlação entre features físicas e orbitais."*

### Coluna direita — Features derivadas com justificativa física
- **`q_earth_diff = |q − 1.0|`** — proximidade do periélio à órbita terrestre. Quanto menor, maior o risco de cruzamento.
- **`orbital_energy = e / a`** — proxy de energia orbital. Órbitas excêntricas com semi-eixo curto têm mais energia cinética na aproximação.
- **`orbital_range = ad − q`** — amplitude radial da órbita. Asteroides com grande variação radial cruzam mais órbitas planetárias.
- **`orbital_risk = e · i`** — combina excentricidade e inclinação. Captura órbitas "desviantes" em relação ao plano eclíptico.

**Notas:** o ponto-chave para a banca é que as features derivadas **têm fundamento físico**, não foram criadas de forma cega. Destaque essa frase em negrito no slide.

---

## SLIDE 7 — Balanceamento + PCA

**Título:** Tratando o Desbalanceamento

**Bloco 1 — Estratégia:**
- Técnica: **undersampling** da classe majoritária (não-PHA), na razão **1:3** em favor dos PHAs.
- Justificativa: SMOTE/oversampling em dados astronômicos pode criar amostras fisicamente inválidas (combinações de `e`, `i`, `a` impossíveis). Undersampling preserva a fidelidade física.
- Critério inspirado na literatura: asteroides com MOID < 0,05 UA são PHA; usamos como filtro auxiliar.

**Bloco 2 — Visualização (imagem embedada):**
- `03_pca_2d.png` — caption: *"Projeção PCA 2D após balanceamento — a separação entre PHA e não-PHA é visível mesmo em 2 componentes."*

**Notas:** este slide responde à crítica clássica da banca ("você tratou o desbalanceamento?"). Deixe a resposta evidente.

---

## SLIDE 8 — Os 6 Classificadores

**Título:** Comitê de 6 Classificadores Individuais

**Tabela (4 colunas, 6 linhas):**

| Modelo | Tipo | Por que está no comitê | Hiperparâmetros-chave |
|---|---|---|---|
| **KNN** | Distância | Baseline geométrico — sensível a escala | `n_neighbors=5` |
| **Naive Bayes** | Probabilístico | Rápido, assume independência | (Gaussiano padrão) |
| **Decision Tree** | Regras | Interpretável, alta variância | `max_depth=8` |
| **SVM** | Margem máxima | Forte em alta dimensão | `kernel='rbf'`, `probability=True` |
| **MLP** | Rede neural | Captura não-linearidades | `hidden_layer_sizes=(64,32)`, `max_iter=400` |
| **Random Forest** | Ensemble de árvores | Reduz variância do DT | `n_estimators=100`, `max_depth=10` |

**Caixa lateral / nota inferior:**
> Diversidade é proposital: três famílias diferentes (distância, probabilística, baseada em árvore) + SVM e MLP. Comitês ganham quando os erros dos membros são **independentes**.

---

## SLIDE 9 — Comitê (Ensemble)

**Título:** Construção do Comitê

**Três cards lado a lado:**

### Card 1 — Soft Voting
- Combina **probabilidades** preditas dos 6 modelos.
- Pondera quem está "muito certo" mais que quem está "no chute".
- Implementado via `VotingClassifier(voting='soft')`.

### Card 2 — Hard Voting
- Combina **decisões finais** (classe predita) por maioria simples.
- Mais robusto a modelos com calibração ruim.

### Card 3 — Soft + Threshold Tuning
- Mesma probabilidade do Soft, mas o **limiar de decisão** é ajustado abaixo de 0,5 para **maximizar recall**.
- Motivação: na detecção de PHA, falso negativo (perder um asteroide perigoso) custa mais que falso positivo.

**Rodapé:**
- Validação: **k-fold estratificado** sobre o conjunto balanceado.

---

## SLIDE 10 — Resultados

**Título:** Resultados — Métricas Comparativas

**Layout em duas linhas:**

### Linha superior — Tabela de métricas (valores reais do `relatorio_metricas.csv`):

| Modelo | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| KNN | 0,9893 | 0,9589 | 1,0000 | 0,9790 |
| Naive Bayes | 0,9687 | 0,8986 | 0,9863 | 0,9404 |
| Decision Tree | 0,9949 | 0,9847 | 0,9949 | 0,9898 |
| SVM | 0,9914 | 0,9669 | 1,0000 | 0,9832 |
| MLP | 0,9949 | 0,9799 | 1,0000 | 0,9898 |
| **Random Forest** | **0,9957** | **0,9832** | **1,0000** | **0,9915** |
| Comitê Soft Voting | 0,9944 | 0,9782 | 1,0000 | 0,9890 |
| Comitê Hard Voting | 0,9949 | 0,9799 | 1,0000 | 0,9898 |
| Comitê Soft + Threshold | 0,9919 | 0,9685 | 1,0000 | 0,9840 |

→ Destaque visual (linha em accent color) na **Random Forest** e nos três **Comitês**.

### Linha inferior — Galeria de imagens embedadas (lado a lado, miniaturas clicáveis que abrem em lightbox):
- `04_matrizes_confusao.png` — *"Matrizes de confusão dos 6 classificadores + comitês."*
- `05_comparacao_metricas.png` — *"Comparação visual das métricas por modelo."*
- `06_curvas_roc.png` — *"Curvas ROC — AUC próxima de 1 em todos os modelos."*
- `07_curvas_precision_recall.png` — *"Curvas Precision-Recall — confirma robustez sob desbalanceamento."*
- `08_feature_importance.png` — *"Importância de features (Random Forest) — confirma o peso das variáveis derivadas."*

**Conclusão em uma linha (rodapé, negrito):**
> Recall = 1,0 em todos os modelos com voting → **nenhum PHA escapou do classificador no conjunto de teste**.

**Notas de implementação do lightbox:** clique na miniatura → overlay escuro com a imagem grande no centro; ESC ou clique fora fecha. Não interfere com a navegação de slides.

---

## SLIDE 11 — Simulação 3D Interativa

**Título:** Visualização — Asteroides em Órbita

**Texto introdutório (acima do botão):**
> Para tornar o problema tangível, construímos uma simulação 3D do sistema solar interior com asteroides sintéticos. Asteroides **PHA aparecem em vermelho** e suas órbitas cruzam a faixa de risco da Terra (MOID < 0,05 UA). Use o mouse para rotacionar a câmera e os controles para pausar/acelerar o tempo.

**Botão central, grande, com ícone de "play" e efeito glow:**
> `▶ INICIAR SIMULAÇÃO 3D`

**Bullets pequenos abaixo do botão (legenda da simulação):**
- 🟢 Verde: planetas internos (Mercúrio, Vênus, Terra, Marte)
- 🟠 Laranja: Júpiter (referência espacial — não aparece em escala real)
- ⚪ Branco/cinza: asteroides do Cinturão Principal (entre Marte e Júpiter)
- 🔴 Vermelho pulsante: asteroides PHA (cruzam a vizinhança da Terra)

**Notas técnicas:** este botão **não inicializa Three.js** até ser clicado. Comportamento e parâmetros da simulação estão em `02_simulacao_3d.md`.

---

## SLIDE 12 — Conclusões e Insights

**Título:** Conclusões

**3 cards numerados:**

### 1. O problema é tratável com ML clássico
- 6 classificadores e 3 estratégias de ensemble convergiram para **F1 ≥ 0,98** após balanceamento e engenharia de features fisicamente fundamentada.

### 2. Recall máximo é alcançável sem destruir a precisão
- Soft Voting e Hard Voting atingiram **recall = 1,0** mantendo **precisão > 0,97**.
- O *threshold tuning* não foi necessário para esta base — mas fica como mecanismo de segurança caso novos dados degradem o recall.

### 3. As features derivadas importaram
- `q_earth_diff` e `orbital_risk` (criadas a partir de princípios físicos, não estatísticos) aparecem entre as mais importantes na Random Forest (gráfico 08).
- Conclusão didática: **domínio de aplicação ainda derrota força bruta numérica** na engenharia de atributos.

**Card final, destacado, cor de accent:**
> **Limitações & próximos passos:** integrar a API Sentry da NASA em tempo real, expandir a base com observações pós-2024 e experimentar redes neurais profundas (LSTM) sobre séries temporais de observações sucessivas do mesmo asteroide.

**Rodapé final, centralizado:**
> Obrigado. — Matheus Arruda, A3 IA, USJT 2026/1
