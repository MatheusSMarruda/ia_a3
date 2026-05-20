# Define e treina os classificadores base (ex.: Regressão Logística, KNN, Árvore de Decisão, Random Forest, SVM) usados individualmente e como membros do comitê.
"""
modelos.py
----------
Responsável por:
  - Definir os 6 classificadores individuais
  - Treinar cada um separadamente
  - Retornar modelos prontos para avaliação e ensemble

Classificadores utilizados
--------------------------
  1. KNN           → baseado em distância, sensível à escala (requer StandardScaler)
  2. Naive Bayes   → probabilístico, assume independência entre features
  3. Decision Tree → baseado em regras, interpretável, instável (alta variância)
  4. SVM           → margem máxima, eficaz em espaços de alta dimensão
  5. MLP           → rede neural simples, captura não-linearidades
  6. Random Forest → ensemble de árvores, reduz variância do Decision Tree
                     (incluído para comparação direta com o VotingClassifier)
"""

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier

from src.config import RANDOM_STATE


def definir_modelos() -> dict:
    """
    Instancia e retorna os classificadores com hiperparâmetros definidos.

    Os hiperparâmetros foram escolhidos para equilibrar desempenho e
    tempo de treino dentro do escopo acadêmico. Nenhum GridSearch foi
    aplicado intencionalmente — a comparação entre modelos é o foco,
    não a otimização individual.

    Retorna
    -------
    dict
        Dicionário { nome_modelo : instância_sklearn }
    """
    modelos = {
        "KNN": KNeighborsClassifier(
            n_neighbors=5
        ),
        "Naive Bayes": GaussianNB(),

        "Decision Tree": DecisionTreeClassifier(
            max_depth=8,
            random_state=RANDOM_STATE
        ),
        "SVM": SVC(
            kernel="rbf",
            probability=True,   # necessário para soft voting e predict_proba
            random_state=RANDOM_STATE
        ),
        "MLP": MLPClassifier(
            hidden_layer_sizes=(64, 32),
            max_iter=400,
            random_state=RANDOM_STATE
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=RANDOM_STATE
        ),
    }

    print("\n" + "=" * 60)
    print("5) CLASSIFICADORES INDIVIDUAIS DEFINIDOS")
    print("=" * 60)
    for nome in modelos:
        print(f"  ✔  {nome}")

    return modelos


def treinar_todos(
    modelos: dict,
    X_train: np.ndarray,
    y_train
) -> dict:
    """
    Treina todos os classificadores e retorna os modelos ajustados.

    Parâmetros
    ----------
    modelos : dict
        Dicionário retornado por definir_modelos().
    X_train : np.ndarray
        Features de treino escalonadas.
    y_train : pd.Series | np.ndarray
        Target de treino.

    Retorna
    -------
    dict
        Mesmo dicionário com os modelos já treinados (fit).
    """
    print("\n" + "=" * 60)
    print("TREINAMENTO")
    print("=" * 60)

    for nome, mdl in modelos.items():
        mdl.fit(X_train, y_train)
        print(f"  ✔  {nome} treinado")

    return modelos