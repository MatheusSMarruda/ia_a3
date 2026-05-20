"""
config.py
---------
Centraliza todas as constantes e configurações do projeto.
Qualquer alteração de parâmetro deve ser feita APENAS aqui.

Todos os paths são absolutos e derivados de PROJECT_ROOT, garantindo
que o pipeline funcione independentemente do diretório de trabalho.
"""
from pathlib import Path

# ── Raiz do projeto ───────────────────────────────────────
# src/config.py  →  parent = src/  →  parent = projeto_a3/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ── Reprodutibilidade ──────────────────────────────────────
RANDOM_STATE = 42

# ── Dados ─────────────────────────────────────────────────
DATA_DIR  = PROJECT_ROOT / "data"
DATA_PATH = DATA_DIR / "raw" / "sbdb_asteroides.csv"

# Features orbitais usadas no modelo.
# moid e neo foram EXCLUÍDOS — causam data leakage direto no target.
FEATURE_COLS = ["q", "ad", "H", "ma", "per", "e", "a", "i"]

# Target
TARGET_COL     = "pha"      # coluna original no CSV  (Y / N)
TARGET_ENCODED = "target"   # coluna após codificação (1 / 0)

# ── Pré-processamento ──────────────────────────────────────
TEST_SIZE         = 0.25    # 75% treino / 25% teste
UNDERSAMPLE_RATIO = 3       # negativos = 3 × positivos  (proporção 1:3)

# ── Ensemble ──────────────────────────────────────────────
# Threshold abaixo de 0.5 prioriza recall (minimiza falsos negativos).
# Falso negativo aqui = asteroide perigoso não detectado → erro crítico.
ENSEMBLE_THRESHOLD = 0.35

# ── Saídas ────────────────────────────────────────────────
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
METRICS_DIR = OUTPUTS_DIR / "metrics"
MODELS_DIR  = OUTPUTS_DIR / "models"
LOGS_DIR    = OUTPUTS_DIR / "logs"

METRICS_CSV = METRICS_DIR / "relatorio_metricas.csv"

# ── Visualização ──────────────────────────────────────────
SEABORN_STYLE   = "whitegrid"
SEABORN_PALETTE = "viridis"
FIGURE_DPI      = 120
