# Aplica técnicas de balanceamento de classes (ex.: SMOTE, undersampling) para lidar com o forte desbalanceamento entre asteroides perigosos e não perigosos.
"""
balanceamento.py
----------------
Responsável pelo balanceamento das classes via undersampling.

Justificativa:
  A classe positiva (PHA=Y) representa ~0.18% do dataset original.
  Treinar sem balanceamento leva qualquer modelo a "chutar tudo N"
  e ainda assim obter ~99.8% de acurácia — métrica inútil nesse contexto.

Estratégia adotada: undersampling da classe majoritária.
  - Mantém TODOS os positivos (asteroides perigosos)
  - Amostra aleatória de (ratio × n_positivos) negativos
  - Proporção final: 1:3 (perigoso : não perigoso)

Por que não SMOTE?
  SMOTE gera amostras sintéticas interpolando positivos existentes.
  Para dados orbitais físicos, interpolar parâmetros como excentricidade
  e inclinação pode gerar asteroides "fisicamente impossíveis".
  Undersampling é mais conservador e defensável academicamente.
"""

import pandas as pd
from src.config import RANDOM_STATE, UNDERSAMPLE_RATIO


def undersample(
    X: pd.DataFrame,
    y: pd.Series,
    ratio: int = UNDERSAMPLE_RATIO
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Balanceia as classes mantendo todos os positivos e
    amostrando (ratio × n_positivos) negativos aleatoriamente.

    Parâmetros
    ----------
    X : pd.DataFrame
        Features processadas (saída de preprocessamento.processar()).
    y : pd.Series
        Target codificado (1 = perigoso, 0 = não perigoso).
    ratio : int
        Quantos negativos por positivo (padrão: 3 → proporção 1:3).

    Retorna
    -------
    X_bal : pd.DataFrame
        Features balanceadas com índice resetado.
    y_bal : pd.Series
        Target balanceado com índice resetado.
    """
    print("\n" + "=" * 60)
    print("3) BALANCEAMENTO (undersampling)")
    print("=" * 60)

    pos_idx = y[y == 1].index
    neg_idx = y[y == 0].index

    n_pos = len(pos_idx)
    n_neg_amostrar = n_pos * ratio

    # Valida se há negativos suficientes
    if n_neg_amostrar > len(neg_idx):
        n_neg_amostrar = len(neg_idx)
        print(f"⚠️  Negativos disponíveis ({len(neg_idx)}) < ratio solicitado.")
        print(f"   Usando todos os negativos disponíveis.")

    neg_sample = y[y == 0].sample(n=n_neg_amostrar, random_state=RANDOM_STATE).index
    keep_idx   = pos_idx.union(neg_sample)

    X_bal = X.loc[keep_idx].reset_index(drop=True)
    y_bal = y.loc[keep_idx].reset_index(drop=True)

    print(f"Positivos mantidos   : {n_pos}")
    print(f"Negativos amostrados : {n_neg_amostrar}  (ratio 1:{ratio})")
    print(f"Total após balance   : {len(X_bal)}")
    print(f"\nDistribuição final:")
    print(f"  Perigoso     (1) → {int(y_bal.sum())}")
    print(f"  Não-Perigoso (0) → {int((y_bal == 0).sum())}")

    return X_bal, y_bal