# Limpeza e preparação dos dados: tratamento de valores ausentes, codificação binária do target (Y=1, N=0), separação X/y, split treino/teste e normalização/escalonamento das features.
"""
preprocessamento.py
-------------------
Responsável por:
  - Limpeza e encoding do target
  - Imputação de valores ausentes
  - Feature engineering com justificativa física
  - Split treino/teste e padronização com StandardScaler
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

from src.config import (
    FEATURE_COLS, TARGET_COL, TARGET_ENCODED,
    TEST_SIZE, RANDOM_STATE
)


# ── Features derivadas (engenharia de atributos) ───────────────────────────
# Cada feature tem justificativa física real no domínio orbital.
# Isso fortalece a seção de análise crítica no relatório.
def _engenharia_de_features(X: pd.DataFrame) -> pd.DataFrame:
    """
    Cria features derivadas com base em propriedades orbitais físicas.

    Features criadas
    ----------------
    q_earth_diff   : |q - 1.0|  → proximidade do periélio à órbita terrestre.
                     Quanto menor, maior o risco de cruzamento orbital.

    orbital_energy : e / a       → proxy de energia orbital.
                     Órbitas excêntricas com semi-eixo curto têm mais energia
                     cinética na aproximação.

    orbital_range  : ad - q      → amplitude da órbita (afélio - periélio).
                     Asteroides com grande variação radial têm mais chance
                     de cruzar órbitas planetárias.

    orbital_risk   : e * i       → combinação de excentricidade e inclinação.
                     Feature composta que captura órbitas "desviantes"
                     em relação ao plano eclíptico.

    Parâmetros
    ----------
    X : pd.DataFrame
        DataFrame com as features originais já imputadas.

    Retorna
    -------
    pd.DataFrame
        DataFrame com as features derivadas adicionadas.
    """
    X = X.copy()

    X["q_earth_diff"]  = abs(X["q"] - 1.0)
    X["orbital_energy"] = X["e"] / X["a"].replace(0, np.nan)
    X["orbital_range"]  = X["ad"] - X["q"]
    X["orbital_risk"]   = X["e"] * X["i"]

    return X


def processar(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """
    Aplica limpeza, encoding do target, imputação e feature engineering.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame bruto retornado por carregamento.carregar().

    Retorna
    -------
    X : pd.DataFrame
        Features prontas para modelagem (originais + derivadas).
    y : pd.Series
        Target codificado (1 = perigoso, 0 = não perigoso).
    """
    print("\n" + "=" * 60)
    print("2) PRÉ-PROCESSAMENTO")
    print("=" * 60)

    # 1. Remove linhas sem target
    df = df.dropna(subset=[TARGET_COL]).reset_index(drop=True).copy()
    print(f"Linhas após remover nulos no target : {len(df)}")

    # 2. Codifica target  Y → 1  |  N → 0
    df[TARGET_ENCODED] = (df[TARGET_COL] == "Y").astype(int)

    # 3. Seleciona features originais
    cols_presentes = [c for c in FEATURE_COLS if c in df.columns]
    X = df[cols_presentes].copy()
    y = df[TARGET_ENCODED].copy()

    # 4. Imputação pela mediana (robusta a outliers astronômicos)
    imputer = SimpleImputer(strategy="median")
    X = pd.DataFrame(imputer.fit_transform(X), columns=cols_presentes)

    # 5. Feature engineering
    X = _engenharia_de_features(X)

    print(f"Features originais   : {cols_presentes}")
    print(f"Features derivadas   : ['q_earth_diff', 'orbital_energy', 'orbital_range', 'orbital_risk']")
    print(f"Total de features    : {X.shape[1]}")
    print(f"X.shape = {X.shape} | y.shape = {y.shape}")
    print(f"Positivos (PHA=Y)    : {int(y.sum())}")
    print(f"Negativos (PHA=N)    : {int((y == 0).sum())}")

    return X, y


def split_e_escalar(
    X: pd.DataFrame,
    y: pd.Series
) -> tuple[np.ndarray, np.ndarray, pd.Series, pd.Series, StandardScaler]:
    """
    Divide em treino/teste estratificado e aplica StandardScaler.

    KNN, SVM e MLP exigem features na mesma escala.
    Decision Tree e Naive Bayes não precisam, mas usar scaler
    em todos simplifica o pipeline sem prejudicar resultados.

    Parâmetros
    ----------
    X : pd.DataFrame
        Features processadas (saída de processar()).
    y : pd.Series
        Target codificado.

    Retorna
    -------
    X_train_s : np.ndarray   Features de treino escalonadas
    X_test_s  : np.ndarray   Features de teste escalonadas
    y_train   : pd.Series    Target de treino
    y_test    : pd.Series    Target de teste
    scaler    : StandardScaler  Scaler ajustado (usar em inferência)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        stratify=y,
        random_state=RANDOM_STATE
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)

    print(f"\nTreino : {X_train_s.shape} | Teste : {X_test_s.shape}")

    return X_train_s, X_test_s, y_train, y_test, scaler