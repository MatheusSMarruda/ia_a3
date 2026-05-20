"""
main.py
-------
Orquestrador principal do projeto A3.
Executa o pipeline completo na ordem correta,
delegando cada responsabilidade ao módulo correspondente.

Execução:
  python main.py            (a partir de projeto_a3/)

Saídas geradas:
  outputs/figures/                  → gráficos PNG
  outputs/metrics/relatorio_metricas.csv  → tabela comparativa
"""

from src import (
    carregamento,
    preprocessamento,
    balanceamento,
    modelos,
    ensemble,
    avaliacao,
    visualizacoes,
)
from src.config import DATA_PATH


def main():
    print("\n" + "=" * 60)
    print("  PROJETO A3 — COMITÊ DE CLASSIFICADORES")
    print("  Asteroides Potencialmente Perigosos (PHA)")
    print("  NASA JPL Small-Body Database")
    print("=" * 60)

    # ── 1. Carregamento ───────────────────────────────────────
    df = carregamento.carregar(DATA_PATH)
    carregamento.eda_basico(df)

    # ── 2. Pré-processamento ──────────────────────────────────
    X, y = preprocessamento.processar(df)

    # ── 3. Balanceamento ──────────────────────────────────────
    X_bal, y_bal = balanceamento.undersample(X, y)

    # ── 4. Split + Escalonamento ──────────────────────────────
    X_train_s, X_test_s, y_train, y_test, scaler = \
        preprocessamento.split_e_escalar(X_bal, y_bal)

    # ── 5. Modelos individuais ────────────────────────────────
    mdls = modelos.definir_modelos()
    mdls = modelos.treinar_todos(mdls, X_train_s, y_train)

    # ── 6. Avaliação individual ───────────────────────────────
    resultados = avaliacao.avaliar_todos(mdls, X_test_s, y_test)

    # ── 7. Ensemble ───────────────────────────────────────────
    ensemble_soft, ensemble_hard = ensemble.treinar_ensembles(
        mdls, X_train_s, y_train
    )

    y_pred_soft      = ensemble_soft.predict(X_test_s)
    y_pred_hard      = ensemble_hard.predict(X_test_s)
    y_pred_threshold = ensemble.threshold_tuning(ensemble_soft, X_test_s)

    # ── 8. Avaliação do ensemble ──────────────────────────────
    resultados = avaliacao.avaliar_ensemble(
        resultados, y_test,
        y_pred_soft, y_pred_hard, y_pred_threshold
    )

    # ── 9. Curvas ROC + Precision-Recall ──────────────────────
    curvas = avaliacao.calcular_curvas(mdls, ensemble_soft, X_test_s, y_test)

    # ── 10. Validação cruzada ─────────────────────────────────
    avaliacao.validacao_cruzada(ensemble_soft, X_bal, y_bal)

    # ── 11. Exportar métricas ─────────────────────────────────
    avaliacao.exportar_metricas(resultados)

    # ── 12. Visualizações ─────────────────────────────────────
    visualizacoes.gerar_todos(
        y_original=y,
        y_balanceado=y_bal,
        X_bal=X_bal,
        y_bal=y_bal,
        resultados=resultados,
        curvas=curvas,
        modelos_treinados=mdls,
        feature_names=list(X_bal.columns)
    )

    print("\n" + "=" * 60)
    print("  PIPELINE CONCLUÍDO")
    print("=" * 60)
    print("  outputs/figures/                       → gráficos")
    print("  outputs/metrics/relatorio_metricas.csv → métricas")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
