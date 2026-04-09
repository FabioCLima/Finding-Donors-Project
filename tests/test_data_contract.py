import pandas as pd

from finding_donors.core.config import DataConfig
from finding_donors.data.contracts import build_dataset_contract, validate_dataframe_contract


def test_validate_dataframe_contract_passes_for_valid_input() -> None:
    data = {
        "age": [39, 50],
        "workclass": ["State-gov", "Self-emp-not-inc"],
        "education_level": ["Bachelors", "Bachelors"],
        "education-num": [13, 13],
        "marital-status": ["Never-married", "Married-civ-spouse"],
        "occupation": ["Adm-clerical", "Exec-managerial"],
        "relationship": ["Not-in-family", "Husband"],
        "race": ["White", "White"],
        "sex": ["Male", "Male"],
        "capital-gain": [2174.0, 0.0],
        "capital-loss": [0.0, 0.0],
        "hours-per-week": [40.0, 13.0],
        "native-country": ["United-States", "United-States"],
        "income": ["<=50K", ">50K"],
    }
    df = pd.DataFrame(data)
    contract = build_dataset_contract(DataConfig())
    validate_dataframe_contract(df, contract)

