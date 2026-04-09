"""Feature engineering orientada pelos achados da EDA."""

import logging

import numpy as np
import pandas as pd

from src.config import RARE_COUNTRY_MIN_SUPPORT

logger = logging.getLogger(__name__)


def engineer_features(df):
    """Aplica transformações de features derivadas da etapa de Data Understanding.

    Transformações:
    - capital-gain/loss: flags binárias + log1p das magnitudes
    - native-country: agrupamento de categorias raras em 'Other'
    """
    df = df.copy()

    # Flags binárias e log para capital gains/losses
    df["capital_gain_flag"] = (df["capital-gain"] > 0).astype(int)
    df["capital_loss_flag"] = (df["capital-loss"] > 0).astype(int)
    df["capital_gain_log"] = np.log1p(df["capital-gain"])
    df["capital_loss_log"] = np.log1p(df["capital-loss"])

    # Agrupamento de países raros
    country_counts = df["native-country"].value_counts()
    rare_countries = country_counts[
        country_counts < RARE_COUNTRY_MIN_SUPPORT
    ].index.tolist()
    df["native-country-grouped"] = df["native-country"].where(
        ~df["native-country"].isin(rare_countries), "Other"
    )
    logger.info(
        "Países raros agrupados em 'Other': %d categorias", len(rare_countries)
    )

    return df
