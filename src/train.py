import argparse
import sys

from pathlib import Path


ROOT_DIR = (
    Path(__file__)
    .resolve()
    .parents[1]
)

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT_DIR),
    )


from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
)

from sklearn.model_selection import (
    train_test_split,
)

from src.modeling import (
    CLASSIFICATION_TARGETS,
    make_model,
    predict,
)

from src.preprocessing import (
    load_data,
    prepare_xy,
)


DATA_PATH = (
    ROOT_DIR
    / "data"
    / "ehr_sample.csv"
)


def train_and_evaluate(
    target: str,
) -> None:

    print(
        f"Training model for: {target}"
    )

    df = load_data(
        DATA_PATH
    )

    X, y = prepare_xy(
        df,
        target,
    )

    stratify = (
        y
        if target
        in CLASSIFICATION_TARGETS
        else None
    )

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=stratify,
    )

    model = make_model(
        target
    )

    model.fit(
        X_train,
        y_train,
    )

    predictions = predict(
        model,
        X_test,
        target,
    )

    if (
        target
        in CLASSIFICATION_TARGETS
    ):

        metric = accuracy_score(
            y_test,
            predictions,
        )

        print(
            f"Accuracy: {metric:.3f}"
        )

    else:

        metric = mean_absolute_error(
            y_test,
            predictions,
        )

        print(
            f"MAE: {metric:.3f} days"
        )

    print(
        f"Finished training {target}"
    )


def main() -> None:

    parser = (
        argparse.ArgumentParser()
    )

    parser.add_argument(
        "--target",
        required=True,
        choices=[
            "hospitalized_30d",
            "er_visit_30d",
            "length_of_stay_days",
        ],
    )

    args = parser.parse_args()

    train_and_evaluate(
        args.target
    )


if __name__ == "__main__":
    main()