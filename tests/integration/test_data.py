from pathlib import Path

import pandas as pd
import pytest

from src.preprocessing import (
    load_data,
    validate_data,
)


ROOT_DIR = (
    Path(__file__)
    .resolve()
    .parents[2]
)

DATA_PATH = (
    ROOT_DIR
    / "data"
    / "ehr_sample.csv"
)


def test_deployed_data_file_exists():

    assert DATA_PATH.exists(), (
        f"Dataset not found: "
        f"{DATA_PATH}"
    )


def test_data_loads_and_has_expected_shape():

    df = load_data(
        DATA_PATH
    )

    assert len(df) == 24

    assert (
        df["patient_id"]
        .is_unique
    )


def test_expected_missing_values_are_present():

    df = load_data(
        DATA_PATH
    )

    assert (
        df["systolic_bp"]
        .isna()
        .sum()
        == 1
    )

    assert (
        df["spo2"]
        .isna()
        .sum()
        == 1
    )


def test_invalid_spo2_is_rejected():

    df = pd.read_csv(
        DATA_PATH
    )

    df.loc[
        0,
        "spo2",
    ] = 120

    with pytest.raises(
        ValueError,
        match="spo2",
    ):

        validate_data(df)