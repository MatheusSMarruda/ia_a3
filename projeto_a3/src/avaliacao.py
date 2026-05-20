# Calcula métricas de avaliação (acurácia, precisão, recall, F1, ROC-AUC, matriz de confusão) para cada modelo individual e para o ensemble.
"""
avaliacao.py
------------
Responsável por:
  - Calcular métricas individuais de cada modelo
  - Gerar classification_report
  - Calcular métricas do ensemble (padrão e com threshold tuning)
  - Curva ROC e Precision-Recall (via probabilidades)
  - Validação cruzada estratificada (StratifiedKFold)
  - Exportar tabela comparativa em CSV

Foco em RECALL como métrica principal.
Justificativa: falso negativo = asteroide perigoso não detectado.
Em sistemas de alerta de risco, errar por excesso (mais alarmes)
é preferível a errar por omissão (deixar passar ameaças).
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix,
    roc_auc_score, roc_curve,
    precision_recall_curve, average_precision_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler

from src.config import RANDOM_STATE, METRICS_CSV, METRICS_DIR


# ── Avaliação individual ───────────────────────────────────────────────────

def avaliar_modelo(
    nome: str,
    y_test,
    y_pred
) -> dict:
    """
    Calcula as métricas de um único modelo.

    Parâmetros
    ----------
    nome   : str        Nome do modelo (para identificação).
    y_test : array-like Target real.
    y_pred : array-like Predições do modelo.

    Retorna
    -------
    dict com acc, prec, rec, f1, cm e nome.
    """
    return {
        "nome": nome,
        "acc":  accuracy_score(y_test, y_pred),
        "prec": precision_score(y_test, y_pred, zero_division=0),
        "rec":  recall_score(y_test, y_pred, zero_division=0),
        "f1":   f1_score(y_test, y_pred, zero_division=0),
        "cm":   confusion_matrix(y_test, y_pred),
    }


def avaliar_todos(
    modelos_treinados: dict,
    X_test: np.ndarray,
    y_test
) -> dict:
    """
    Avalia todos os modelos individuais e imprime classification_report.

    Parâmetros
    ----------
    modelos_treinados : dict
        Modelos treinados (saída de modelos.treinar_todos()).
    X_test : np.ndarray
        Features de teste escalonadas.
    y_test : array-like
        Target real.

    Retorna
    -------
    dict
        { nome_modelo : dict_de_metricas }
    """
    print("\n" + "=" * 60)
    print("AVALIAÇÃO — MODELOS INDIVIDUAIS")
    print("=" * 60)

    resultados = {}
    for nome, mdl in modelos_treinados.items():
        y_pred = mdl.predict(X_test)
        resultados[nome] = avaliar_modelo(nome, y_test, y_pred)

        print(f"\n--- {nome} ---")
        print(classification_report(
            y_test, y_pred,
            target_names=["Não-Perigoso", "Perigoso"],
            zero_division=0
        ))

    return resultados


# ── Avaliação do ensemble ──────────────────────────────────────────────────

def avaliar_ensemble(
    resultados: dict,
    y_test,
    y_pred_soft,
    y_pred_hard,
    y_pred_threshold
) -> dict:
    """
    Adiciona as métricas dos ensembles ao dicionário de resultados.

    Parâmetros
    ----------
    resultados      : dict   Resultado dos modelos individuais.
    y_test          : array-like  Target real.
    y_pred_soft     : array-like  Predições soft voting (threshold=0.5).
    y_pred_hard     : array-like  Predições hard voting.
    y_pred_threshold: array-like  Predições soft com threshold ajustado.

    Retorna
    -------
    dict
        resultados atualizado com os ensembles.
    """
    print("\n" + "=" * 60)
    print("AVALIAÇÃO — ENSEMBLE")
    print("=" * 60)

    pares = [
        ("Comitê Soft Voting",       y_pred_soft),
        ("Comitê Hard Voting",       y_pred_hard),
        ("Comitê Soft + Threshold",  y_pred_threshold),
    ]

    for nome, y_pred in pares:
        resultados[nome] = avaliar_modelo(nome, y_test, y_pred)
        print(f"\n--- {nome} ---")
        print(classification_report(
            y_test, y_pred,
            target_names=["Não-Perigoso", "Perigoso"],
            zero_division=0
        ))

    return resultados


# ── Curvas ROC e Precision-Recall ──────────────────────────────────────────

def calcular_curvas(
    modelos_treinados: dict,
    ensemble_soft,
    X_test: np.ndarray,
    y_test
) -> dict:
    """
    Calcula dados para as curvas ROC e Precision-Recall de cada modelo
    e do ensemble soft.

    Usado por visualizacoes.py para plotar as curvas comparativas.

    Parâmetros
    ----------
    modelos_treinados : dict
        Modelos com predict_proba disponível.
    ensemble_soft     : VotingClassifier
        Ensemble soft treinado.
    X_test : np.ndarray
        Features de teste escalonadas.
    y_test : array-like
        Target real.

    Retorna
    -------
    dict
        { nome : { fpr, tpr, auc, precision, recall, ap } }
    """
    curvas = {}

    todos = {**modelos_treinados, "Comitê Soft Voting": ensemble_soft}

    for nome, mdl in todos.items():
        try:
            y_prob = mdl.predict_proba(X_test)[:, 1]

            fpr, tpr, _ = roc_curve(y_test, y_prob)
            auc          = roc_auc_score(y_test, y_prob)

            prec_curve, rec_curve, _ = precision_recall_curve(y_test, y_prob)
            ap = average_precision_score(y_test, y_prob)

            curvas[nome] = {
                "fpr": fpr, "tpr": tpr, "auc": auc,
                "precision_curve": prec_curve,
                "recall_curve": rec_curve,
                "ap": ap,
            }
        except Exception:
            # Modelos sem predict_proba são ignorados silenciosamente
            pass

    print("\n" + "=" * 60)
    print("ROC-AUC POR MODELO")
    print("=" * 60)
    for nome, dados in curvas.items():
        print(f"  {nome:<30} AUC = {dados['auc']:.4f}  |  AP = {dados['ap']:.4f}")

    return curvas


# ── Validação cruzada ──────────────────────────────────────────────────────

def validacao_cruzada(
    ensemble_soft,
    X_bal: pd.DataFrame,
    y_bal,
    n_splits: int = 5
) -> None:
    """
    Executa validação cruzada estratificada (StratifiedKFold) no ensemble soft.

    Usa F1-score como métrica principal, consistente com o foco em
    minimizar falsos negativos sem ignorar completamente a precisão.

    Parâmetros
    ----------
    ensemble_soft : VotingClassifier
        Ensemble soft (será re-treinado internamente pelo cross_val_score).
    X_bal : pd.DataFrame
        Features balanceadas completas (antes do split treino/teste).
    y_bal : array-like
        Target balanceado completo.
    n_splits : int
        Número de folds (padrão: 5).
    """
    print("\n" + "=" * 60)
    print(f"VALIDAÇÃO CRUZADA ({n_splits}-fold estratificado) — COMITÊ SOFT")
    print("=" * 60)

    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_STATE)

    # Re-escala para o cross_val_score (não usa o scaler do split anterior)
    X_scaled = StandardScaler().fit_transform(X_bal)

    scores = cross_val_score(
        ensemble_soft, X_scaled, y_bal,
        cv=cv, scoring="f1"
    )

    print(f"F1 por fold : {np.round(scores, 4)}")
    print(f"F1 médio    : {scores.mean():.4f}  (±{scores.std():.4f})")


# ── Exportação ────────────────────────────────────────────────────────────

def exportar_metricas(resultados: dict, path=METRICS_CSV) -> None:
    """
    Exporta a tabela comparativa de métricas para CSV.

    Parâmetros
    ----------
    resultados : dict
        Dicionário de resultados (saída de avaliar_todos + avaliar_ensemble).
    path : Path | str
        Caminho de saída (padrão: METRICS_CSV do config).
    """
    df = pd.DataFrame(
        {n: {k: v for k, v in r.items() if k not in ("cm", "nome")}
         for n, r in resultados.items()}
    ).T.rename(columns={
        "acc":  "Accuracy",
        "prec": "Precision",
        "rec":  "Recall",
        "f1":   "F1-Score",
    })

    print("\n" + "=" * 60)
    print("RESUMO COMPARATIVO")
    print("=" * 60)
    print(df.round(4).to_string())

    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    df.round(4).to_csv(path)
    print(f"\n  ✔  Métricas exportadas → {path}")