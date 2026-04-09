"""Configuração centralizada do projeto Finding Donors."""

from pathlib import Path

# Caminhos
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "census.csv"
MODELS_DIR = PROJECT_ROOT / "models"

# Reprodutibilidade
RANDOM_STATE = 42
TEST_SIZE = 0.20
BETA = 0.5
CV_SPLITS = 5

# Features — trilha de produção
CORE_NUMERIC = [
    "age",
    "hours-per-week",
    "capital_gain_log",
    "capital_loss_log",
    "capital_gain_flag",
    "capital_loss_flag",
]

CORE_CATEGORICAL = [
    "workclass",
    "education_level",
    "marital-status",
    "occupation",
    "relationship",
]

# Features excluídas do modelo de produção
SENSITIVE_COLS = ["sex", "race", "native-country"]
REDUNDANT_COLS = ["education-num"]
NON_PREDICTIVE_COLS = ["fnlwgt"]

# Agrupamento de categorias raras
RARE_COUNTRY_MIN_SUPPORT = 50

# Target
TARGET_COL = "income"
POSITIVE_LABEL = ">50K"
