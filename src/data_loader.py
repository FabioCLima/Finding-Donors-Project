"""Leitura e validação estrutural dos dados do Census Income."""

import logging

import pandas as pd

from src.config import DATA_PATH, POSITIVE_LABEL, TARGET_COL

logger = logging.getLogger(__name__)


def load_census(path=DATA_PATH):
    """Carrega o CSV e executa validações básicas de sanidade."""
    df = pd.read_csv(path)
    logger.info("Shape: %s", df.shape)

    missing = df.isna().sum()
    if missing.any():
        logger.warning("Valores faltantes:\n%s", missing[missing > 0])

    n_dup = df.duplicated().sum()
    if n_dup > 0:
        logger.info("Duplicados encontrados: %d", n_dup)

    return df


def create_target(df):
    """Cria a coluna target binária e calcula o baseline."""
    df = df.copy()
    df["target"] = (df[TARGET_COL].str.strip() == POSITIVE_LABEL).astype(int)
    baseline = df["target"].mean()
    logger.info("Baseline (taxa classe positiva): %.2f%%", baseline * 100)
    return df, baseline
