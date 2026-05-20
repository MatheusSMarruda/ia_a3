# Gera e salva em outputs/figures os gráficos do projeto: matrizes de confusão, comparativos de métricas entre modelos, curvas ROC e análises exploratórias.
"""
visualizacoes.py
----------------
Responsável por gerar e salvar todos os gráficos do projeto.

Gráficos gerados
----------------
  1. Distribuição do target (antes e depois do balanceamento)
  2. Heatmap de correlação das features
  3. Scatter PCA 2D (separabilidade das classes)
  4. Matrizes de confusão (todos os modelos)
  5. Comparação de métricas (barplot)
  6. Curvas ROC comparativas
  7. Curvas Precision-Recall comparativas
  8. Feature importance (Decision Tree e Random Forest)

Todos os arquivos são salvos em outputs/figures/
com nomes descritivos e DPI configurado em config.py.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import ConfusionMatrixDisplay

from src.config import (
    FIGURES_DIR, SEABORN_STYLE, SEABORN_PALETTE, FIGURE_DPI, RANDOM_STATE
)


# ── Setup global ──────────────────────────────────────────────────────────

def _setup():
    """Aplica tema seaborn e cria diretório de saída se não existir."""
    sns.set_theme(style=SEABORN_STYLE, palette=SEABORN_PALETTE)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def _salvar(nome_arquivo: str) -> None:
    """Salva o gráfico atual e fecha a figura."""
    path = FIGURES_DIR / nome_arquivo
    plt.savefig(path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close()
    print(f"  ✔  {path}")


# ── 1. Distribuição do target ─────────────────────────────────────────────

def plot_distribuicao_target(y_original: pd.Series, y_balanceado: pd.Series) -> None:
    """
    Barplot lado a lado: distribuição antes e depois do balanceamento.
    Evidencia o desbalanceamento original e justifica o undersampling.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for ax, y, titulo in zip(
        axes,
        [y_original, y_balanceado],
        ["Distribuição Original", "Após Undersampling (1:3)"]
    ):
        contagem = y.value_counts().rename({0: "Não-Perigoso", 1: "Perigoso"})
        sns.barplot(
            x=contagem.index, y=contagem.values,
            hue=contagem.index, palette="viridis",
            legend=False, ax=ax,
        )
        ax.set_title(titulo, fontsize=13, fontweight="bold")
        ax.set_ylabel("Quantidade")
        ax.set_xlabel("Classe")
        for bar, val in zip(ax.patches, contagem.values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(contagem.values) * 0.01,
                f"{val:,}", ha="center", va="bottom", fontsize=10
            )

    plt.suptitle("Balanceamento de Classes", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    _salvar("01_distribuicao_target.png")


# ── 2. Heatmap de correlação ──────────────────────────────────────────────

def plot_heatmap_correlacao(X: pd.DataFrame) -> None:
    """
    Heatmap de correlação entre todas as features (originais + derivadas).
    Identifica multicolinearidade e features redundantes.
    """
    fig, ax = plt.subplots(figsize=(12, 9))
    corr = X.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))

    sns.heatmap(
        corr, mask=mask, annot=True, fmt=".2f",
        cmap="viridis", linewidths=0.5,
        ax=ax, annot_kws={"size": 8}
    )
    ax.set_title("Heatmap de Correlação — Features", fontsize=13, fontweight="bold")
    plt.tight_layout()
    _salvar("02_heatmap_correlacao.png")


# ── 3. PCA 2D ─────────────────────────────────────────────────────────────

def plot_pca_2d(X: pd.DataFrame, y: pd.Series) -> None:
    """
    Reduz as features para 2 componentes principais e plota
    um scatter colorido por classe.
    Mostra visualmente a separabilidade das classes no espaço reduzido.
    """
    X_scaled = StandardScaler().fit_transform(X)
    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    componentes = pca.fit_transform(X_scaled)

    df_pca = pd.DataFrame(componentes, columns=["PC1", "PC2"])
    df_pca["Classe"] = y.map({0: "Não-Perigoso", 1: "Perigoso"}).values

    fig, ax = plt.subplots(figsize=(10, 7))
    cores = {"Não-Perigoso": "#2d7d9a", "Perigoso": "#e84855"}

    for classe, grupo in df_pca.groupby("Classe"):
        ax.scatter(
            grupo["PC1"], grupo["PC2"],
            label=classe, alpha=0.5, s=15,
            color=cores[classe]
        )

    var_exp = pca.explained_variance_ratio_ * 100
    ax.set_xlabel(f"PC1 ({var_exp[0]:.1f}% variância explicada)")
    ax.set_ylabel(f"PC2 ({var_exp[1]:.1f}% variância explicada)")
    ax.set_title("PCA 2D — Separabilidade das Classes", fontsize=13, fontweight="bold")
    ax.legend()
    plt.tight_layout()
    _salvar("03_pca_2d.png")


# ── 4. Matrizes de confusão ───────────────────────────────────────────────

def plot_matrizes_confusao(resultados: dict) -> None:
    """
    Grade com a matriz de confusão de cada modelo e ensemble.
    """
    n = len(resultados)
    cols = 4
    rows = int(np.ceil(n / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4.5 * rows))

    for ax, (nome, r) in zip(axes.flat, resultados.items()):
        ConfusionMatrixDisplay(
            r["cm"], display_labels=["Não", "Sim"]
        ).plot(ax=ax, cmap="Blues", colorbar=False)
        ax.set_title(nome, fontsize=10, fontweight="bold")

    for ax in axes.flat[n:]:
        ax.axis("off")

    plt.suptitle("Matrizes de Confusão", fontsize=14, fontweight="bold", y=1.01)
    plt.tight_layout()
    _salvar("04_matrizes_confusao.png")


# ── 5. Comparação de métricas ─────────────────────────────────────────────

def plot_comparacao_metricas(resultados: dict) -> None:
    """
    Barplot agrupado comparando Accuracy, Precision, Recall e F1-Score
    de todos os modelos e ensembles.
    Recall destacado como métrica principal.
    """
    df = pd.DataFrame(
        {n: {k: v for k, v in r.items() if k not in ("cm", "nome")}
         for n, r in resultados.items()}
    ).T.rename(columns={
        "acc": "Accuracy", "prec": "Precision",
        "rec": "Recall",   "f1":  "F1-Score"
    })

    fig, ax = plt.subplots(figsize=(14, 6))
    df.plot(kind="bar", ax=ax, colormap="viridis", edgecolor="black", width=0.75)

    ax.set_title(
        "Comparação de Métricas — Modelos Individuais × Comitê",
        fontsize=13, fontweight="bold"
    )
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1.1)
    ax.axhline(y=1.0, color="gray", linestyle="--", linewidth=0.8)
    plt.xticks(rotation=25, ha="right", fontsize=9)
    ax.legend(loc="lower right")

    # Destaca a barra de Recall de cada grupo.
    # Matplotlib desenha os patches AGRUPADOS POR COLUNA (todas Accuracy,
    # depois todas Precision, etc.), então o índice do bloco é i // n_modelos.
    metricas   = list(df.columns)
    idx_recall = metricas.index("Recall")
    n_modelos  = len(df.index)
    for i, patch in enumerate(ax.patches):
        if i // n_modelos == idx_recall:
            patch.set_edgecolor("red")
            patch.set_linewidth(2)

    plt.tight_layout()
    _salvar("05_comparacao_metricas.png")


# ── 6. Curvas ROC ─────────────────────────────────────────────────────────

def plot_curvas_roc(curvas: dict) -> None:
    """
    Curvas ROC de todos os modelos no mesmo gráfico.
    Linha diagonal (random classifier) como baseline.
    """
    fig, ax = plt.subplots(figsize=(10, 7))

    palette = sns.color_palette("viridis", len(curvas))

    for (nome, dados), cor in zip(curvas.items(), palette):
        ax.plot(
            dados["fpr"], dados["tpr"],
            label=f"{nome}  (AUC = {dados['auc']:.3f})",
            color=cor, linewidth=2
        )

    ax.plot([0, 1], [0, 1], "k--", linewidth=1, label="Classificador aleatório")
    ax.set_xlabel("Taxa de Falsos Positivos (FPR)")
    ax.set_ylabel("Taxa de Verdadeiros Positivos (TPR / Recall)")
    ax.set_title("Curvas ROC — Comparativo", fontsize=13, fontweight="bold")
    ax.legend(loc="lower right", fontsize=8)
    plt.tight_layout()
    _salvar("06_curvas_roc.png")


# ── 7. Curvas Precision-Recall ────────────────────────────────────────────

def plot_curvas_precision_recall(curvas: dict) -> None:
    """
    Curvas Precision-Recall de todos os modelos.
    Mais informativa que ROC em datasets desbalanceados.
    """
    fig, ax = plt.subplots(figsize=(10, 7))

    palette = sns.color_palette("viridis", len(curvas))

    for (nome, dados), cor in zip(curvas.items(), palette):
        ax.plot(
            dados["recall_curve"], dados["precision_curve"],
            label=f"{nome}  (AP = {dados['ap']:.3f})",
            color=cor, linewidth=2
        )

    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title(
        "Curvas Precision-Recall — Comparativo\n"
        "(mais informativa que ROC para classes desbalanceadas)",
        fontsize=12, fontweight="bold"
    )
    ax.legend(loc="upper right", fontsize=8)
    plt.tight_layout()
    _salvar("07_curvas_precision_recall.png")


# ── 8. Feature importance ─────────────────────────────────────────────────

def plot_feature_importance(modelos_treinados: dict, feature_names: list) -> None:
    """
    Barplot horizontal da importância de features para
    Decision Tree e Random Forest.
    """
    modelos_arvore = {
        k: v for k, v in modelos_treinados.items()
        if k in ("Decision Tree", "Random Forest")
    }

    if not modelos_arvore:
        return

    fig, axes = plt.subplots(1, len(modelos_arvore), figsize=(7 * len(modelos_arvore), 6))
    if len(modelos_arvore) == 1:
        axes = [axes]

    for ax, (nome, mdl) in zip(axes, modelos_arvore.items()):
        importancias = pd.Series(mdl.feature_importances_, index=feature_names)
        importancias = importancias.sort_values(ascending=True)

        importancias.plot(kind="barh", ax=ax, color=sns.color_palette("viridis", len(importancias)))
        ax.set_title(f"Feature Importance — {nome}", fontsize=12, fontweight="bold")
        ax.set_xlabel("Importância")
        ax.axvline(x=0, color="gray", linewidth=0.8)

    plt.tight_layout()
    _salvar("08_feature_importance.png")


# ── Orquestrador ──────────────────────────────────────────────────────────

def gerar_todos(
    y_original: pd.Series,
    y_balanceado: pd.Series,
    X_bal: pd.DataFrame,
    y_bal: pd.Series,
    resultados: dict,
    curvas: dict,
    modelos_treinados: dict,
    feature_names: list
) -> None:
    """
    Gera e salva todos os gráficos do projeto em sequência.

    Parâmetros
    ----------
    y_original      : Series    Target antes do balanceamento.
    y_balanceado    : Series    Target após undersampling.
    X_bal           : DataFrame Features balanceadas completas.
    y_bal           : Series    Target balanceado completo.
    resultados      : dict      Métricas de todos os modelos e ensembles.
    curvas          : dict      Dados ROC/PR (saída de avaliacao.calcular_curvas).
    modelos_treinados: dict     Modelos treinados individualmente.
    feature_names   : list      Nomes das features (originais + derivadas).
    """
    _setup()

    print("\n" + "=" * 60)
    print("7) GERANDO VISUALIZAÇÕES")
    print("=" * 60)

    plot_distribuicao_target(y_original, y_balanceado)
    plot_heatmap_correlacao(X_bal)
    plot_pca_2d(X_bal, y_bal)
    plot_matrizes_confusao(resultados)
    plot_comparacao_metricas(resultados)
    plot_curvas_roc(curvas)
    plot_curvas_precision_recall(curvas)
    plot_feature_importance(modelos_treinados, feature_names)

    print(f"\n  Todos os gráficos salvos em → {FIGURES_DIR}/")