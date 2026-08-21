# Databricks CI/CD Test Project

A simple MLOps project that demonstrates how to use **GitHub Actions**, **pytest**, and **Databricks Asset Bundles** to test and deploy Python code to Databricks.

## Project Structure

```text
test-databricks-connection/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── src/
│   ├── __init__.py
│   └── hello.py
├── tests/
│   └── test_hello.py
├── databricks.yml
├── requirements-dev.txt
├── .gitignore
└── README.md
```

## Project Overview

The project contains a simple Python application that is:

1. Tested using `pytest`.
2. Validated using Databricks Asset Bundles.
3. Deployed to Databricks through GitHub Actions.

The sample Python function returns a greeting:

```python
def make_message(name: str) -> str:
    return f"Hello {name}!"
```

When the Databricks job runs, it prints:

```text
Hello Databricks!
```

---

## Branch Strategy

The repository uses three main branches:

| Branch | Databricks Target | Purpose |
|---|---|---|
| `dev` | `dev` | Development |
| `qa` | `qa` | Testing and validation |
| `prod` | `prod` | Production |

The expected promotion flow is:

```text
Feature Branch
      |
      v
     dev
      |
      v
      qa
      |
      v
     prod
```

Code is promoted between environments using pull requests.

---

## Continuous Integration (CI)

The CI workflow is located at:

```text
.github/workflows/ci.yml
```

CI runs when a pull request is created against:

- `dev`
- `qa`
- `prod`

The workflow:

1. Checks out the repository.
2. Sets up Python.
3. Installs development dependencies.
4. Runs the automated tests using pytest.

The test command is:

```bash
python -m pytest -v
```

CI verifies that new code works correctly before it is merged.

---

## Continuous Deployment (CD)

The CD workflow is located at:

```text
.github/workflows/cd.yml
```

CD runs when code is pushed or merged into:

- `dev`
- `qa`
- `prod`

The workflow:

1. Checks out the repository.
2. Installs the Databricks CLI.
3. Authenticates with Databricks.
4. Checks the Databricks connection.
5. Validates the Databricks Asset Bundle.
6. Deploys the bundle.

The deployment target is automatically determined from the Git branch:

```yaml
TARGET: ${{ github.ref_name }}
```

Therefore:

```text
dev branch  -> dev target
qa branch   -> qa target
prod branch -> prod target
```

---

## Databricks Asset Bundle

The Databricks Asset Bundle configuration is defined in:

```text
databricks.yml
```

The bundle defines a Databricks job called:

```text
hello_job
```

The job runs:

```text
./src/hello.py
```

The bundle contains three deployment targets:

```yaml
targets:
  dev:
    variables:
      environment: dev

  qa:
    variables:
      environment: qa

  prod:
    variables:
      environment: prod
```

The deployed Databricks job names are separated by environment:

```text
dev-hello-job
qa-hello-job
prod-hello-job
```

Databricks Asset Bundles allow Databricks resources, source code, and deployment configuration to be managed together as code.

---

## GitHub Secrets

The CD pipeline requires two GitHub repository secrets:

```text
DATABRICKS_HOST
DATABRICKS_TOKEN
```

Add them under:

```text
Repository
→ Settings
→ Secrets and variables
→ Actions
→ Repository secrets
```

### DATABRICKS_HOST

The URL of the Databricks workspace.

Example:

```text
https://<workspace>.cloud.databricks.com
```

### DATABRICKS_TOKEN

A Databricks Personal Access Token used by GitHub Actions to authenticate with Databricks.

The token should never be committed directly to the repository.

> The current pipeline uses the same Databricks credentials for `dev`, `qa`, and `prod`. Therefore, these are logical environments within the same Databricks workspace unless separate workspace credentials are configured later.

---

## Run Tests Locally

Install the development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the tests:

```bash
python -m pytest -v
```

Expected result:

```text
1 passed
```

---

## Validate the Databricks Bundle

Validate the development target:

```bash
databricks bundle validate --target dev
```

Validate QA:

```bash
databricks bundle validate --target qa
```

Validate production:

```bash
databricks bundle validate --target prod
```

---

## Deploy Manually

Deploy to development:

```bash
databricks bundle deploy --target dev
```

Deploy to QA:

```bash
databricks bundle deploy --target qa
```

Deploy to production:

```bash
databricks bundle deploy --target prod
```

---

## Run the Databricks Job

After deploying the bundle, run the development job with:

```bash
databricks bundle run --target dev hello_job
```

For QA:

```bash
databricks bundle run --target qa hello_job
```

For production:

```bash
databricks bundle run --target prod hello_job
```

---

## CI/CD Flow

```text
Developer makes code changes
            |
            v
     Create Pull Request
            |
            v
     GitHub Actions CI
            |
            +---- Run pytest
            |
            v
       Tests Pass
            |
            v
       Merge PR
            |
            v
   dev / qa / prod branch
            |
            v
     GitHub Actions CD
            |
            +---- Authenticate with Databricks
            |
            +---- Validate Bundle
            |
            +---- Deploy Bundle
            |
            v
       Databricks Job
```

---

## Technologies Used

- Python
- pytest
- Git
- GitHub
- GitHub Actions
- Databricks CLI
- Databricks Asset Bundles
- Databricks Jobs

## Repository

https://github.com/sreeja-g/test-databricks-connection


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
