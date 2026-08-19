# test-databricks-connection

Databricks Connection Testing

## Project Structure

```
ml-databricks/
│
├── databricks.yml
│
├── projects/
│   ├── project_1/
│   │   ├── README.md
│   │   ├── notebooks/
│   │   ├── src/
│   │   ├── tests/
│   │   └── resources/
│   │
│   ├── project_2/
│   │   ├── README.md
│   │   ├── notebooks/
│   │   ├── src/
│   │   ├── tests/
│   │   └── resources/
│   │
│   └── project_3/
│       ├── README.md
│       ├── notebooks/
│       ├── src/
│       ├── tests/
│       └── resources/
│
├── shared/
│   ├── preprocessing/
│   ├── utils/
│   ├── features/
│   └── validations/
│
├── tests/
│
└── .github/
    └── workflows/
        ├── ci.yml
        ├── deploy-dev.yml
        └── deploy-prod.yml
```

## Sample Project 

```
projects/
└── project_1/
    │
    ├── notebooks/
    │   ├── 01_preprocessing.ipynb
    │   ├── 02_exploration.ipynb
    │   ├── 03_training.ipynb
    │   └── 04_evaluation.ipynb
    │
    ├── src/
    │   ├── data.py
    │   ├── features.py
    │   ├── train.py
    │   ├── evaluate.py
    │   └── predict.py
    │
    ├── tests/
    │   ├── test_data.py
    │   └── test_features.py
    │
    └── resources/
        └── jobs.yml
```
