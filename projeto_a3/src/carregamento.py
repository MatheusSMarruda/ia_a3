# Responsável por carregar o dataset sbdb_asteroides.csv, selecionar as colunas relevantes (features + target) e retornar o DataFrame bruto pronto para o pré-processamento.
"""
carregamento.py
---------------
Responsável por carregar o CSV e exibir um EDA básico:
shape, tipos, nulos, distribuição do target e estatísticas descritivas.
"""

import pandas as pd
from src.config import DATA_PATH, TARGET_COL, FEATURE_COLS


def carregar(path: str = DATA_PATH) -> pd.DataFrame:
    """
    Lê o CSV bruto e retorna o DataFrame sem nenhuma modificação.

    Parâmetros
    ----------
    path : str
        Caminho para o arquivo CSV (padrão: DATA_PATH do config).

    Retorna
    -------
    pd.DataFrame
        Dataset bruto conforme lido do disco.
    """
    print("=" * 60)
    print("1) CARREGAMENTO DA BASE")
    print("=" * 60)

    df = pd.read_csv(path, low_memory=False)

    print(f"Shape                : {df.shape}")
    print(f"Colunas              : {list(df.columns)}")
    print(f"\nTipos de dados:\n{df.dtypes}")
    print(f"\nValores nulos por coluna:\n{df.isnull().sum()[df.isnull().sum() > 0]}")

    return df


def eda_basico(df: pd.DataFrame) -> None:
    """
    Exibe análise exploratória básica: distribuição do target,
    estatísticas descritivas das features e alertas de nulos.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame bruto retornado por carregar().
    """
    print("\n" + "=" * 60)
    print("EDA BÁSICO")
    print("=" * 60)

    # Distribuição do target
    print(f"\nDistribuição de '{TARGET_COL}':")
    dist = df[TARGET_COL].value_counts(dropna=False)
    total = len(df)
    for val, cnt in dist.items():
        print(f"  {val:>6}  →  {cnt:>7} linhas  ({cnt/total*100:.2f}%)")

    # Estatísticas descritivas das features disponíveis
    cols_presentes = [c for c in FEATURE_COLS if c in df.columns]
    cols_ausentes  = [c for c in FEATURE_COLS if c not in df.columns]

    print(f"\nEstatísticas descritivas das features:")
    print(df[cols_presentes].describe().round(4).to_string())

    if cols_ausentes:
        print(f"\n⚠️  Features ausentes no CSV: {cols_ausentes}")

    # Percentual de nulos nas features
    nulos = df[cols_presentes].isnull().mean() * 100
    nulos = nulos[nulos > 0].sort_values(ascending=False)
    if not nulos.empty:
        print(f"\nPercentual de nulos nas features:")
        for col, pct in nulos.items():
            print(f"  {col:>6}  →  {pct:.2f}%")
    else:
        print("\nNenhum valor nulo nas features selecionadas.")