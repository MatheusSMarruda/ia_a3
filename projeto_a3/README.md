# Projeto A3 — Comitê de Classificadores para Asteroides Perigosos (PHA)

Sistema de classificação supervisionada que prevê se um asteroide é
potencialmente perigoso para a Terra (PHA — *Potentially Hazardous Asteroid*),
usando um comitê de classificadores treinado sobre o dataset
**NASA JPL Small-Body Database** (Kaggle).

## Estrutura

```
projeto_a3/
├── main.py                # orquestrador do pipeline
├── requirements.txt
├── src/                   # módulos do pipeline (importáveis)
│   ├── config.py          # constantes e paths
│   ├── carregamento.py
│   ├── preprocessamento.py
│   ├── balanceamento.py
│   ├── modelos.py
│   ├── ensemble.py
│   ├── avaliacao.py
│   └── visualizacoes.py
├── data/
│   ├── raw/               # CSV original (imutável)
│   └── processed/         # datasets derivados (futuro)
├── notebooks/             # EDA e experimentos
├── outputs/               # gerado pelo pipeline (gitignored)
│   ├── figures/
│   ├── metrics/
│   ├── models/
│   └── logs/
└── reports/               # entregáveis finais (PDF, slides)
```

## Como executar

```bash
pip install -r requirements.txt
python main.py
```

Saídas:

- `outputs/figures/`            → 8 gráficos PNG
- `outputs/metrics/relatorio_metricas.csv` → tabela comparativa

## Pipeline

1. Carregamento + EDA
2. Pré-processamento (imputação, feature engineering, encoding)
3. Balanceamento (undersampling 1:3)
4. Split treino/teste + padronização
5. Treino de 6 classificadores (KNN, NB, DT, SVM, MLP, RF)
6. Construção de ensembles (soft + hard voting)
7. Threshold tuning (foco em recall)
8. Avaliação + validação cruzada
9. Geração de gráficos
