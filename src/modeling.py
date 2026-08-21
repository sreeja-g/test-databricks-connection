import numpy as np

from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
)

from sklearn.impute import (
    SimpleImputer,
)

from sklearn.pipeline import (
    Pipeline,
)

from src.preprocessing import (
    prepare_xy,
)


CLASSIFICATION_TARGETS = {
    "hospitalized_30d",
    "er_visit_30d",
}


def make_model(
    target: str,
) -> Pipeline:

    if target in CLASSIFICATION_TARGETS:

        estimator = (
            RandomForestClassifier(
                n_estimators=50,
                max_depth=4,
                random_state=42,
            )
        )

    elif target == "length_of_stay_days":

        estimator = (
            RandomForestRegressor(
                n_estimators=50,
                max_depth=4,
                random_state=42,
            )
        )

    else:

        raise ValueError(
            f"Unknown target: {target}"
        )

    return Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                ),
            ),
            (
                "model",
                estimator,
            ),
        ]
    )


def train_model(
    df,
    target: str,
) -> Pipeline:

    X, y = prepare_xy(
        df,
        target,
    )

    model = make_model(
        target
    )

    model.fit(
        X,
        y,
    )

    return model


def predict(
    model: Pipeline,
    X,
    target: str,
) -> np.ndarray:

    predictions = (
        model.predict(X)
    )

    if (
        target
        == "length_of_stay_days"
    ):
        predictions = np.clip(
            predictions,
            0,
            None,
        )

    return predictions