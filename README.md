# Projeto A3 - Inteligência Artificial

## Comitê de Classificadores para Asteroides Potencialmente Perigosos

Este repositório apresenta o projeto A3 de Inteligência Artificial, desenvolvido para classificar asteroides potencialmente perigosos para a Terra, conhecidos como **PHA** (*Potentially Hazardous Asteroids*).

O projeto utiliza aprendizado de máquina supervisionado sobre dados do **NASA JPL Small-Body Database**, aplicando pré-processamento, balanceamento de classes, treinamento de múltiplos classificadores e estratégias de ensemble.

## Objetivo

Construir um sistema capaz de prever se um asteroide deve ser classificado como potencialmente perigoso a partir de características orbitais e físicas.

O problema foi formulado como uma **classificação supervisionada binária**:

- `1`: asteroide potencialmente perigoso (PHA)
- `0`: asteroide não perigoso

Como a base possui muito mais asteroides não perigosos do que perigosos, o projeto prioriza métricas como **recall**, reduzindo o risco de falsos negativos.

## Tecnologias utilizadas

- Python
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- HTML, CSS e JavaScript
- Three.js para simulacao 3D

## Modelos implementados

Foram treinados seis modelos supervisionados:

- K-Nearest Neighbors (KNN)
- Gaussian Naive Bayes
- Decision Tree
- Support Vector Machine (SVM)
- Multi-Layer Perceptron (MLP)
- Random Forest

Além dos modelos individuais, foram implementadas estratégias de comitê:

- Soft Voting
- Hard Voting
- Soft Voting com ajuste de threshold

## Pipeline do projeto

1. Carregamento do dataset `sbdb_asteroides.csv`
2. Análise exploratória dos dados
3. Pré-processamento e tratamento de valores ausentes
4. Engenharia de features orbitais
5. Balanceamento por undersampling
6. Separação treino/teste e padronização com `StandardScaler`
7. Treinamento dos classificadores
8. Construção dos ensembles
9. Avaliação por métricas e gráficos
10. Geração da apresentação final em HTML

## Resultados principais

| Modelo | Accuracy | Precision | Recall | F1-Score |
|---|---:|---:|---:|---:|
| KNN | 0.9893 | 0.9589 | 1.0000 | 0.9790 |
| Naive Bayes | 0.9687 | 0.8986 | 0.9863 | 0.9404 |
| Decision Tree | 0.9949 | 0.9847 | 0.9949 | 0.9898 |
| SVM | 0.9914 | 0.9669 | 1.0000 | 0.9832 |
| MLP | 0.9949 | 0.9799 | 1.0000 | 0.9898 |
| Random Forest | 0.9957 | 0.9832 | 1.0000 | 0.9915 |
| Comite Soft Voting | 0.9944 | 0.9782 | 1.0000 | 0.9890 |
| Comite Hard Voting | 0.9949 | 0.9799 | 1.0000 | 0.9898 |
| Comite Soft + Threshold | 0.9919 | 0.9685 | 1.0000 | 0.9840 |

O principal destaque foi o **recall igual a 1.0** nos modelos com voting, indicando que nenhum PHA do conjunto de teste passou despercebido.

## Visualizações geradas

Alguns dos gráficos produzidos pelo pipeline:

- Distribuição da variável alvo
- Heatmap de correlação
- PCA 2D
- Matrizes de confusão
- Comparação de métricas
- Curvas ROC
- Curvas Precision-Recall
- Importância de features

Os arquivos estão em:

```text
projeto_a3/outputs/figures/
```

### Galeria dos gráficos

| Distribuição da variável alvo | Heatmap de correlação |
|---|---|
| ![Distribuição da variável alvo](projeto_a3/outputs/figures/01_distribuicao_target.png) | ![Heatmap de correlação](projeto_a3/outputs/figures/02_heatmap_correlacao.png) |

| PCA 2D | Matrizes de confusão |
|---|---|
| ![PCA 2D](projeto_a3/outputs/figures/03_pca_2d.png) | ![Matrizes de confusão](projeto_a3/outputs/figures/04_matrizes_confusao.png) |

| Comparação de métricas | Curvas ROC |
|---|---|
| ![Comparação de métricas](projeto_a3/outputs/figures/05_comparacao_metricas.png) | ![Curvas ROC](projeto_a3/outputs/figures/06_curvas_roc.png) |

| Curvas Precision-Recall | Importância de features |
|---|---|
| ![Curvas Precision-Recall](projeto_a3/outputs/figures/07_curvas_precision_recall.png) | ![Importância de features](projeto_a3/outputs/figures/08_feature_importance.png) |

## Apresentação final

O entregável final inclui uma apresentação web autocontida, em estilo PowerPoint, com simulação 3D interativa:

```text
projeto_a3/reports/apresentacao_a3.html
```

A apresentação contém:

- 13 slides
- Gráficos embutidos
- Tema visual espacial
- Simulação 3D com Three.js
- Navegação por teclado
- Controles interativos da simulação

## Como executar o projeto

A partir da raiz do repositório:

```bash
cd projeto_a3
pip install -r requirements.txt
python main.py
```

Ao final da execução, o pipeline gera:

```text
outputs/figures/
outputs/metrics/relatorio_metricas.csv
```

## Estrutura principal

```text
projeto_a3/
├── main.py
├── requirements.txt
├── src/
│   ├── carregamento.py
│   ├── preprocessamento.py
│   ├── balanceamento.py
│   ├── modelos.py
│   ├── ensemble.py
│   ├── avaliacao.py
│   └── visualizacoes.py
├── data/
│   └── raw/
├── outputs/
│   ├── figures/
│   └── metrics/
└── reports/
    ├── apresentacao_a3.html
    ├── Relatorio_A3.pdf
    └── Documentacao_Projeto_A3.pdf
```

## Integrantes

| Nome | RA |
|---|---:|
| Matheus Santos Morais Arruda | 825218417 |
| Lucca Campello Rodrigues dos Santos | 82525684 |
| Jorge Antonio de Paula Tosi | 825220685 |
| Guilherme Caposse Tabler | 825126059 |
| Matheus Miano | 82425432 |

## Conclusão

O projeto mostra que modelos clássicos de Machine Learning, quando combinados com pré-processamento adequado, balanceamento e engenharia de features, podem apresentar alto desempenho na classificação de asteroides potencialmente perigosos.

O uso de comitês de classificadores permitiu aumentar a confiabilidade da predição, especialmente no recall, métrica mais importante para reduzir o risco de deixar um asteroide perigoso sem identificação.
