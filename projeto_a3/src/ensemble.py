# Implementa o comitê de classificadores (Voting/Stacking), combinando os modelos base definidos em modelos.py para gerar a predição final.
"""
ensemble.py
-----------
Responsável por:
  - Construir o comitê de classificadores (VotingClassifier)
  - Estratégias: soft voting e hard voting
  - Threshold tuning para priorizar recall (minimizar falsos negativos)

Por que Soft Voting?
  Soft voting usa a CONFIANÇA de cada modelo (probabilidade predita),
  não apenas o rótulo final. Se um classificador está inseguro (prob ~0.51),
  ele "pesa" menos no resultado coletivo.
  Isso é especialmente útil quando os modelos têm performance heterogênea
  (ex: Naive Bayes vs MLP), o que é exatamente o caso aqui.

Por que Threshold Tuning?
  O corte padrão de 0.5 otimiza acurácia geral.
  Nesse domínio, falso negativo = asteroide perigoso não detectado.
  Reduzir o threshold para 0.35 aumenta o recall ao custo de mais
  falsos positivos — trade-off aceitável em sistemas de alerta de risco.
"""

import numpy as np
from sklearn.ensemble import VotingClassifier
from src.config import RANDOM_STATE, ENSEMBLE_THRESHOLD


def construir_soft(modelos_treinados: dict) -> VotingClassifier:
    """
    Constrói e treina o VotingClassifier com soft voting.

    Soft voting combina as probabilidades preditas de cada modelo.
    Requer que todos os estimadores suportem predict_proba
    (garantido pelo probability=True no SVC em modelos.py).

    Parâmetros
    ----------
    modelos_treinados : dict
        Dicionário de modelos já treinados (saída de modelos.treinar_todos()).

    Retorna
    -------
    VotingClassifier
        Ensemble soft já ajustado (os estimadores internos já estão treinados,
        mas o VotingClassifier precisa de fit próprio para registrar classes).
    """
    estimators = list(modelos_treinados.items())
    ensemble = VotingClassifier(estimators=estimators, voting="soft")
    return ensemble


def construir_hard(modelos_treinados: dict) -> VotingClassifier:
    """
    Constrói o VotingClassifier com hard voting (votação majoritária).

    Hard voting usa apenas o rótulo final de cada modelo.
    Incluído para comparação direta com soft voting.

    Parâmetros
    ----------
    modelos_treinados : dict
        Dicionário de modelos já treinados.

    Retorna
    -------
    VotingClassifier
        Ensemble hard pronto para fit.
    """
    estimators = list(modelos_treinados.items())
    ensemble = VotingClassifier(estimators=estimators, voting="hard")
    return ensemble


def treinar_ensembles(
    modelos_treinados: dict,
    X_train: np.ndarray,
    y_train
) -> tuple[VotingClassifier, VotingClassifier]:
    """
    Instancia e treina os dois ensembles (soft e hard).

    Parâmetros
    ----------
    modelos_treinados : dict
        Modelos já treinados individualmente.
    X_train : np.ndarray
        Features de treino escalonadas.
    y_train : array-like
        Target de treino.

    Retorna
    -------
    ensemble_soft : VotingClassifier treinado (soft voting)
    ensemble_hard : VotingClassifier treinado (hard voting)
    """
    print("\n" + "=" * 60)
    print("6) CONSTRUÇÃO DO COMITÊ (VOTING CLASSIFIER)")
    print("=" * 60)

    ensemble_soft = construir_soft(modelos_treinados)
    ensemble_soft.fit(X_train, y_train)
    print("  ✔  Soft Voting treinado")

    ensemble_hard = construir_hard(modelos_treinados)
    ensemble_hard.fit(X_train, y_train)
    print("  ✔  Hard Voting treinado")

    return ensemble_soft, ensemble_hard


def threshold_tuning(
    ensemble: VotingClassifier,
    X_test: np.ndarray,
    threshold: float = ENSEMBLE_THRESHOLD
) -> np.ndarray:
    """
    Aplica threshold customizado nas probabilidades do ensemble soft.

    Em vez do corte padrão de 0.5, usa um threshold menor para
    priorizar recall — minimizando falsos negativos (asteroides
    perigosos classificados como seguros).

    Parâmetros
    ----------
    ensemble : VotingClassifier
        Ensemble soft já treinado.
    X_test : np.ndarray
        Features de teste escalonadas.
    threshold : float
        Corte de probabilidade (padrão: 0.35 do config).

    Retorna
    -------
    np.ndarray
        Predições binárias com threshold ajustado.
    """
    y_prob = ensemble.predict_proba(X_test)[:, 1]
    y_pred_ajustado = (y_prob >= threshold).astype(int)

    print(f"\n  Threshold ajustado : {threshold}")
    print(f"  Predições positivas (threshold={threshold}) : {y_pred_ajustado.sum()}")
    print(f"  Predições positivas (threshold=0.50)        : "
          f"{(ensemble.predict_proba(X_test)[:, 1] >= 0.50).sum()}")

    return y_pred_ajustado


def obter_probabilidades(
    ensemble: VotingClassifier,
    X_test: np.ndarray
) -> np.ndarray:
    """
    Retorna as probabilidades brutas da classe positiva.
    Usado para gerar curvas ROC e Precision-Recall em avaliacao.py.

    Parâmetros
    ----------
    ensemble : VotingClassifier
        Ensemble soft treinado.
    X_test : np.ndarray
        Features de teste escalonadas.

    Retorna
    -------
    np.ndarray
        Array de probabilidades para classe 1 (perigoso).
    """
    return ensemble.predict_proba(X_test)[:, 1]