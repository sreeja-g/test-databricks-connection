from pathlib import Path

from src.preprocessing import (
    build_features,
    load_data,
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


def test_preprocessing_creates_expected_features():

    df = load_data(
        DATA_PATH
    )

    X = build_features(df)

    assert (
        len(X)
        == len(df)
    )

    assert (
        "medication_count"
        in X.columns
    )

    assert (
        "fever_flag"
        in X.columns
    )

    assert (
        "shock_index"
        in X.columns
    )

    assert (
        "patient_id"
        not in X.columns
    )


def test_preprocessing_handles_medications():

    df = load_data(
        DATA_PATH
    )

    X = build_features(df)

    assert (
        X.loc[
            0,
            "medication_count",
        ]
        == 0
    )

    assert (
        X.loc[
            1,
            "medication_count",
        ]
        == 3
    )