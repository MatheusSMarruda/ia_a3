"""
============================================================
 Projeto A3 - Inteligencia Artificial - Universidade Sao Judas Tadeu
 Comite de Classificadores aplicado ao dataset NASA JPL SBDB
============================================================

Base de dados : sbdb_asteroides.csv (NASA JPL Small-Body Database)
Variavel alvo : pha  (Potentially Hazardous Asteroid)  Y/N
Objetivo      : prever se um asteroide e potencialmente perigoso para a Terra

Atende ao enunciado A3:
  3.3 Pre-processamento  3.4 >=3 classificadores individuais
  3.5 Comite (ensemble)  3.6 Avaliacao com accuracy/precision/recall/F1/CM

Execucao: python projeto_a3_comite_classificadores.py
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, ConfusionMatrixDisplay,
)

RANDOM_STATE = 42
DATA_PATH = "projeto_a3/data/raw/sbdb_asteroides.csv"

# ============================================================
# 1) CARREGAMENTO + EDA basico
# ============================================================
print("=" * 60)
print("1) CARREGAMENTO DA BASE")
print("=" * 60)
df = pd.read_csv(DATA_PATH, low_memory=False)
print(f"Shape original: {df.shape}")
print("\nDistribuicao do target 'pha' (antes do pre-processamento):")
print(df["pha"].value_counts(dropna=False))

# ============================================================
# 2) PRE-PROCESSAMENTO
# ============================================================
print("\n" + "=" * 60)
print("2) PRE-PROCESSAMENTO")
print("=" * 60)

# 2.1 Remove linhas sem rotulo (target nao pode ser NaN) e reseta indice
df = df.dropna(subset=["pha"]).reset_index(drop=True).copy()

# 2.2 Codifica target: Y -> 1 (perigoso), N -> 0 (nao perigoso)
df["target"] = (df["pha"] == "Y").astype(int)

# 2.3 Selecao de features.
# Usamos parametros orbitais + magnitude absoluta (proxy de tamanho).
# IMPORTANTE: NAO usamos 'moid' nem 'neo' como features porque a definicao
# oficial de PHA depende deles - seria vazamento de dados (data leakage).
feature_cols = ["q", "ad", "H", "ma", "per", "e", "a", "i"]
X = df[feature_cols].copy()
y = df["target"].copy()

# 2.4 Imputacao de valores ausentes pela mediana (robusta a outliers)
imputer = SimpleImputer(strategy="median")
X = pd.DataFrame(imputer.fit_transform(X), columns=feature_cols)

print(f"Features usadas : {feature_cols}")
print(f"X.shape = {X.shape} | y.shape = {y.shape}")
print(f"Positivos (PHA=Y): {int(y.sum())} | Negativos (PHA=N): {int((y==0).sum())}")

# ============================================================
# 3) BALANCEAMENTO (UNDERSAMPLING DA CLASSE MAJORITARIA)
# A classe positiva e ~0.18% do dataset. Treinar direto leva
# qualquer modelo a "chutar tudo N" e ter 99.8% de acuracia inutil.
# Estrategia: manter todos os positivos e amostrar 3x esse numero
# de negativos => proporcao 1:3 (perigoso : nao perigoso).
# ============================================================
print("\n" + "=" * 60)
print("3) BALANCEAMENTO (undersampling 1:3)")
print("=" * 60)
pos_idx = y[y == 1].index
neg_idx = y[y == 0].sample(n=len(pos_idx) * 3, random_state=RANDOM_STATE).index
keep_idx = pos_idx.union(neg_idx)

X_bal = X.loc[keep_idx].reset_index(drop=True)
y_bal = y.loc[keep_idx].reset_index(drop=True)
print(f"Apos balanceamento: {X_bal.shape}")
print(y_bal.value_counts().rename({0: "Nao-Perigoso (0)", 1: "Perigoso (1)"}))

# ============================================================
# 4) TREINO / TESTE + PADRONIZACAO
# KNN, SVM e MLP exigem features na mesma escala. Decision Tree
# e Naive Bayes nao precisam, mas usar scaler para todos nao
# prejudica e simplifica o pipeline.
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
    X_bal, y_bal, test_size=0.25, stratify=y_bal, random_state=RANDOM_STATE
)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)
print(f"\nTreino: {X_train_s.shape} | Teste: {X_test_s.shape}")

# ============================================================
# 5) MODELOS INDIVIDUAIS (>=3 - usamos 5)
# ============================================================
print("\n" + "=" * 60)
print("5) TREINAMENTO DOS CLASSIFICADORES INDIVIDUAIS")
print("=" * 60)

modelos = {
    "KNN":           KNeighborsClassifier(n_neighbors=5),
    "Naive Bayes":   GaussianNB(),
    "Decision Tree": DecisionTreeClassifier(max_depth=8, random_state=RANDOM_STATE),
    "SVM":           SVC(kernel="rbf", probability=True, random_state=RANDOM_STATE),
    "MLP":           MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=400,
                                   random_state=RANDOM_STATE),
}

resultados = {}
for nome, mdl in modelos.items():
    mdl.fit(X_train_s, y_train)
    y_pred = mdl.predict(X_test_s)
    resultados[nome] = {
        "acc":  accuracy_score(y_test, y_pred),
        "prec": precision_score(y_test, y_pred),
        "rec":  recall_score(y_test, y_pred),
        "f1":   f1_score(y_test, y_pred),
        "cm":   confusion_matrix(y_test, y_pred),
    }
    print(f"\n--- {nome} ---")
    print(classification_report(y_test, y_pred,
                                target_names=["Nao-Perigoso", "Perigoso"]))

# ============================================================
# 6) COMITE DE CLASSIFICADORES (ENSEMBLE)
# Estrategia escolhida: SOFT VOTING (votacao ponderada pelas
# probabilidades preditas). Justificativa:
#   - Soft voting aproveita a CONFIANCA de cada modelo, nao
#     so o rotulo final. Se um classificador esta inseguro
#     (prob ~0.51), ele "pesa" menos no resultado final.
#   - Gera resultados mais estaveis que hard voting quando os
#     modelos tem performance heterogenea, o que e exatamente
#     o caso aqui (ex: NB vs MLP).
# Tambem treinamos HARD VOTING para fins comparativos.
# ============================================================
print("\n" + "=" * 60)
print("6) CONSTRUCAO DO COMITE (VOTING CLASSIFIER)")
print("=" * 60)

estimators = list(modelos.items())

ensemble_soft = VotingClassifier(estimators=estimators, voting="soft")
ensemble_soft.fit(X_train_s, y_train)
y_pred_soft = ensemble_soft.predict(X_test_s)

ensemble_hard = VotingClassifier(estimators=estimators, voting="hard")
ensemble_hard.fit(X_train_s, y_train)
y_pred_hard = ensemble_hard.predict(X_test_s)

for nome, y_pred in [("Comite (Soft Voting)", y_pred_soft),
                     ("Comite (Hard Voting)", y_pred_hard)]:
    resultados[nome] = {
        "acc":  accuracy_score(y_test, y_pred),
        "prec": precision_score(y_test, y_pred),
        "rec":  recall_score(y_test, y_pred),
        "f1":   f1_score(y_test, y_pred),
        "cm":   confusion_matrix(y_test, y_pred),
    }
    print(f"\n--- {nome} ---")
    print(classification_report(y_test, y_pred,
                                target_names=["Nao-Perigoso", "Perigoso"]))

# ============================================================
# 7) COMPARACAO FINAL + VISUALIZACOES
# ============================================================
print("\n" + "=" * 60)
print("7) RESUMO COMPARATIVO")
print("=" * 60)

df_metricas = pd.DataFrame(
    {n: {k: v for k, v in r.items() if k != "cm"} for n, r in resultados.items()}
).T.rename(columns={"acc": "Accuracy", "prec": "Precision",
                    "rec": "Recall", "f1": "F1-Score"})
print(df_metricas.round(4).to_string())

# 7.1 Grafico de barras das metricas
ax = df_metricas.plot(kind="bar", figsize=(12, 6),
                     colormap="viridis", edgecolor="black")
ax.set_title("Comparacao de Metricas - Modelos Individuais x Comite")
ax.set_ylabel("Score")
ax.set_ylim(0, 1.05)
plt.xticks(rotation=20, ha="right")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("comparacao_metricas.png", dpi=120)
plt.close()

# 7.2 Matrizes de confusao
n = len(resultados)
cols = 4
rows = int(np.ceil(n / cols))
fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4.5 * rows))
for ax, (nome, r) in zip(axes.flat, resultados.items()):
    ConfusionMatrixDisplay(r["cm"], display_labels=["Nao", "Sim"]).plot(
        ax=ax, cmap="Blues", colorbar=False)
    ax.set_title(nome)
for ax in axes.flat[n:]:
    ax.axis("off")
plt.tight_layout()
plt.savefig("matrizes_confusao.png", dpi=120)
plt.close()

# 7.3 Validacao cruzada (5 folds estratificados) do melhor modelo
print("\n" + "=" * 60)
print("8) VALIDACAO CRUZADA (5-fold) DO COMITE SOFT")
print("=" * 60)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
scores = cross_val_score(ensemble_soft,
                         StandardScaler().fit_transform(X_bal),
                         y_bal, cv=cv, scoring="f1")
print(f"F1 por fold : {np.round(scores, 4)}")
print(f"F1 medio    : {scores.mean():.4f}  (+/- {scores.std():.4f})")

print("\n" + "=" * 60)
print("9) TOP 5 ASTEROIDES COM MAIOR RISCO DE COLISAO")
print("=" * 60)
# Ranking geometrico: dentre os PHAs (pha == 'Y'), os 5 com menor MOID
# (Minimum Orbit Intersection Distance). Mesma metodologia documentada
# na secao 5 do relatorio (projeto_a3/reports/Documentacao_Projeto_A3.pdf).
# Nao usa o modelo - usa a base bruta - apenas para reportar quais
# asteroides reais merecem maior atencao.
AU_KM = 149_597_870.7  # 1 unidade astronomica em km

top5 = (
    df[df["pha"] == "Y"]
    .dropna(subset=["moid"])
    .nsmallest(5, "moid")
    .loc[:, ["full_name", "H", "moid", "per", "e", "a", "i", "class"]]
    .copy()
)
top5["moid_km"]  = (top5["moid"] * AU_KM).round(0)
top5["per_anos"] = (top5["per"] / 365.25).round(2)
top5["full_name"] = top5["full_name"].str.strip()

print(top5[["full_name", "H", "moid", "moid_km",
            "per_anos", "e", "a", "i", "class"]]
      .to_string(index=False))

print("\nArquivos gerados:")
print("  - comparacao_metricas.png")
print("  - matrizes_confusao.png")
print("\nFim.")
