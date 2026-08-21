# Databricks MLOps CI/CD Pipeline

This repository demonstrates a **CI/CD pipeline for machine learning code using GitHub Actions and Databricks Asset Bundles**.

The project contains an EHR-based machine learning example, but the main purpose of the repository is to demonstrate how code can be:

1. Developed in feature branches
2. Tested automatically through Continuous Integration (CI)
3. Promoted through `dev`, `qa`, and `prod`
4. Validated as a Databricks Asset Bundle
5. Automatically deployed to Databricks through Continuous Deployment (CD)

---

## CI/CD Architecture

```text
Developer
    │
    │ Code changes
    ▼
Feature Branch
    │
    │ Pull Request
    ▼
┌─────────────────────────┐
│   GitHub Actions - CI   │
│                         │
│  • Checkout code        │
│  • Set up Python        │
│  • Install dependencies │
│  • Run pytest           │
└────────────┬────────────┘
             │
             │ CI passes
             ▼
        Merge PR
             │
             ▼
      dev / qa / prod
             │
             │ Push created by merge
             ▼
┌─────────────────────────────┐
│    GitHub Actions - CD      │
│                             │
│  • Install Databricks CLI   │
│  • Verify credentials       │
│  • Authenticate             │
│  • Check connection         │
│  • Validate bundle          │
│  • Deploy bundle            │
└──────────────┬──────────────┘
               │
               ▼
          Databricks
```

---

# Branch Strategy

The repository uses three main environment branches:

| Git Branch | Databricks Target | Purpose                           |
| ---------- | ----------------- | --------------------------------- |
| `dev`      | `dev`             | Development and early integration |
| `qa`       | `qa`              | Testing and validation            |
| `prod`     | `prod`            | Production deployment             |

The expected promotion flow is:

```text
Feature Branch
      │
      │ Pull Request
      ▼
     dev
      │
      │ Pull Request
      ▼
      qa
      │
      │ Pull Request
      ▼
     prod
```

Each pull request runs CI before the code is merged.

After a pull request is merged, the resulting push to the destination branch triggers CD.

---

# Example End-to-End Flow

For example, assume a developer creates:

```text
feature/ehr-model-update
```

The developer opens a pull request:

```text
feature/ehr-model-update
          │
          ▼
         dev
```

This triggers:

```text
CI
│
├── Checkout code
├── Install Python
├── Install dependencies
└── Run pytest
```

If the tests pass and the pull request is merged:

```text
feature/ehr-model-update
          │
          ▼
         dev
```

GitHub creates a push to `dev`.

That push automatically triggers:

```text
CD
│
├── Connect to Databricks
├── Validate bundle for dev
└── Deploy bundle to dev
```

Later, code can be promoted:

```text
dev
 │
 │ PR + CI
 ▼
qa
 │
 │ CD deployment
 ▼
Databricks QA target
```

and eventually:

```text
qa
 │
 │ PR + CI
 ▼
prod
 │
 │ CD deployment
 ▼
Databricks PROD target
```

---

# Continuous Integration (CI)

The CI workflow is defined in:

```text
.github/workflows/ci.yml
```

## When CI Runs

CI runs whenever a pull request targets:

```text
dev
qa
prod
```

The workflow trigger is conceptually:

```yaml
on:
  pull_request:
    branches:
      - dev
      - qa
      - prod
```

This means simply committing to a feature branch does not run this particular CI workflow.

Creating or updating a pull request into one of the three environment branches triggers CI.

---

## CI Steps

The CI workflow runs on:

```text
ubuntu-latest
```

and performs the following steps.

### 1. Checkout Repository

```yaml
uses: actions/checkout@v4
```

This downloads the repository into the GitHub Actions runner.

---

### 2. Set Up Python

The pipeline installs:

```text
Python 3.12
```

using:

```yaml
uses: actions/setup-python@v5
```

---

### 3. Install Dependencies

The pipeline first updates `pip`:

```bash
python -m pip install --upgrade pip
```

Then installs the project's test dependencies:

```bash
pip install -r requirements-dev.txt
```

---

### 4. Run Automated Tests

The CI pipeline executes:

```bash
python -m pytest -v
```

If a test fails, the CI job fails.

The pull request therefore shows a failed GitHub Actions check and should not be promoted until the issue is fixed.

If all tests pass:

```text
Code Change
    │
    ▼
pytest
    │
    ├── FAIL → Fix code
    │
    └── PASS
          │
          ▼
     Ready to merge
```

### Note About Test Discovery

The GitHub Actions job is currently called:

```text
Unit Tests
```

However, the command is:

```bash
python -m pytest -v
```

Because a specific directory such as `tests/unit` is not provided, pytest discovers all matching tests available in the repository.

If CI should run **only unit tests**, the command could instead be:

```bash
python -m pytest tests/unit -v
```

Integration tests could then be handled separately.

---

# What CI Means in This Project

**CI = Continuous Integration.**

The "integration" refers to continuously checking whether a developer's new code can be safely **integrated into the shared codebase**.

For this repository:

```text
New Code
   +
Existing Repository
   +
Dependencies
   +
Automated Tests
        │
        ▼
Can these changes safely be merged?
```

CI does **not** mean only "integration tests."

Unit tests can be part of Continuous Integration.

---

# Continuous Deployment (CD)

The CD workflow is defined in:

```text
.github/workflows/cd.yml
```

Its purpose is to take code that has reached an environment branch and deploy the corresponding Databricks Asset Bundle.

---

## When CD Runs

CD runs on a push to:

```text
dev
qa
prod
```

Conceptually:

```yaml
on:
  push:
    branches:
      - dev
      - qa
      - prod
```

Because merging a pull request creates a push to the destination branch, a normal workflow looks like:

```text
PR to dev
   │
   ▼
CI
   │
   ▼
Merge
   │
   ▼
Push to dev
   │
   ▼
CD
```

The CD workflow can also be started manually using:

```text
workflow_dispatch
```

from the GitHub Actions interface.

---

# Automatic Environment Selection

The CD workflow determines the deployment environment from the Git branch:

```yaml
TARGET: ${{ github.ref_name }}
```

For example:

```text
GitHub branch       TARGET

dev             →   dev
qa              →   qa
prod            →   prod
```

The same CD workflow therefore works for all three environments.

There is no need to maintain:

```text
cd-dev.yml
cd-qa.yml
cd-prod.yml
```

Instead, one reusable workflow determines the environment dynamically.

---

# CD Pipeline Steps

The CD job runs on:

```text
ubuntu-latest
```

and performs the following operations.

---

## 1. Checkout Repository

```yaml
uses: actions/checkout@v4
```

The GitHub runner downloads the exact repository version being deployed.

---

## 2. Install Databricks CLI

The workflow installs the Databricks CLI using:

```yaml
uses: databricks/setup-cli@main
```

The Databricks CLI is then used for authentication, bundle validation, and deployment.

---

## 3. Load Databricks Credentials

The workflow reads Databricks credentials from GitHub Secrets:

```yaml
DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
DATABRICKS_AUTH_TYPE: pat
```

The credentials are therefore not stored directly in the source code.

---

## 4. Verify Secrets Exist

Before attempting deployment, the workflow checks whether:

```text
DATABRICKS_HOST
DATABRICKS_TOKEN
```

have values.

If either one is missing, deployment stops immediately.

Conceptually:

```text
Are credentials configured?
        │
        ├── NO → Stop CD
        │
        └── YES
              │
              ▼
       Continue authentication
```

---

## 5. Verify Databricks Authentication

The CD workflow makes a request to the Databricks API using the configured token.

A successful response confirms that GitHub Actions can authenticate against the Databricks workspace.

```text
GitHub Actions
       │
       │ PAT
       ▼
Databricks API
       │
       ├── Authentication fails → Stop
       │
       └── Authentication succeeds
                      │
                      ▼
               Continue CD
```

---

## 6. Check Databricks Connection

The workflow also runs a Databricks CLI identity check using the selected target.

This verifies that the Databricks CLI can communicate with the workspace using the configured authentication.

---

## 7. Validate Databricks Asset Bundle

Before anything is deployed, CD runs:

```bash
databricks bundle validate --target "$TARGET"
```

For the `dev` branch this becomes:

```bash
databricks bundle validate --target dev
```

For `qa`:

```bash
databricks bundle validate --target qa
```

For `prod`:

```bash
databricks bundle validate --target prod
```

Bundle validation checks that the Databricks configuration can be resolved correctly before deployment.

If validation fails:

```text
Bundle
   │
   ▼
Validate
   │
   ├── FAIL → Nothing deployed
   │
   └── PASS
          │
          ▼
       Deploy
```

This is an important safety step because invalid Databricks configuration is stopped before deployment.

---

# Databricks Asset Bundles

The deployment configuration is stored in:

```text
databricks.yml
```

A Databricks Asset Bundle allows Databricks resources and deployment configuration to be stored as code in Git.

Instead of manually creating or updating jobs through the Databricks UI:

```text
Developer manually edits Databricks
```

the project uses:

```text
Git
 │
 ▼
databricks.yml
 │
 ▼
GitHub Actions
 │
 ▼
Databricks CLI
 │
 ▼
Databricks
```

This makes Databricks configuration version-controlled and repeatable.

---

# Bundle Targets

The bundle contains targets for:

```text
dev
qa
prod
```

Each target assigns the corresponding environment value.

Conceptually:

```yaml
targets:

  dev:
    environment: dev

  qa:
    environment: qa

  prod:
    environment: prod
```

GitHub Actions passes the appropriate target during deployment.

---

# Deploy Databricks Bundle

After successful validation, CD runs:

```bash
databricks bundle deploy --target "$TARGET"
```

Therefore:

### Push to `dev`

```bash
databricks bundle deploy --target dev
```

### Push to `qa`

```bash
databricks bundle deploy --target qa
```

### Push to `prod`

```bash
databricks bundle deploy --target prod
```

`deploy` means:

> Make the Databricks resources defined in the bundle available or update the existing deployed resources for that target.

Deployment does **not necessarily mean running the ML job**.

Deployment creates or updates the Databricks resources described by the bundle.

---

# CI vs CD

The two workflows have different responsibilities.

|                        | CI                     | CD                    |
| ---------------------- | ---------------------- | --------------------- |
| Full Name              | Continuous Integration | Continuous Deployment |
| Workflow               | `ci.yml`               | `cd.yml`              |
| Trigger                | Pull Request           | Push / Merge          |
| Main Purpose           | Validate code          | Deploy code/resources |
| Runs pytest            | Yes                    | No                    |
| Connects to Databricks | No                     | Yes                   |
| Validates bundle       | No                     | Yes                   |
| Deploys bundle         | No                     | Yes                   |

In simple terms:

```text
CI = Should this code be merged?

CD = The code was merged. Deploy it.
```

---

# Complete DEV Flow

```text
Developer
    │
    ▼
feature branch
    │
    │ Pull Request to dev
    ▼
CI starts
    │
    ├── Checkout repository
    ├── Python 3.12
    ├── Install dependencies
    └── pytest
    │
    ▼
Tests Pass
    │
    ▼
Merge PR
    │
    ▼
dev branch receives push
    │
    ▼
CD starts
    │
    ├── Checkout repository
    ├── Install Databricks CLI
    ├── Verify secrets
    ├── Authenticate
    ├── Check Databricks connection
    ├── bundle validate --target dev
    └── bundle deploy --target dev
    │
    ▼
DEV resources deployed to Databricks
```

---

# Complete QA Flow

Once development validation is complete:

```text
dev
 │
 │ Pull Request to qa
 ▼
CI
 │
 ├── Install dependencies
 └── pytest
 │
 ▼
Merge
 │
 ▼
qa
 │
 ▼
CD
 │
 ├── Authenticate
 ├── Validate QA bundle
 └── Deploy QA bundle
 │
 ▼
QA resources deployed to Databricks
```

---

# Complete PROD Flow

After QA validation:

```text
qa
 │
 │ Pull Request to prod
 ▼
CI
 │
 └── pytest
 │
 ▼
Merge
 │
 ▼
prod
 │
 ▼
CD
 │
 ├── Authenticate
 ├── Validate PROD bundle
 └── Deploy PROD bundle
 │
 ▼
Production deployment
```

---

# Overall Promotion Pipeline

```text
                  FEATURE
                     │
                     │ PR
                     ▼
              ┌─────────────┐
              │     CI      │
              │   pytest    │
              └──────┬──────┘
                     │
                   merge
                     ▼
                    DEV
                     │
                     ▼
              ┌─────────────┐
              │     CD      │
              │ deploy dev  │
              └──────┬──────┘
                     │
                     │ PR
                     ▼
              ┌─────────────┐
              │     CI      │
              └──────┬──────┘
                     │
                   merge
                     ▼
                     QA
                     │
                     ▼
              ┌─────────────┐
              │     CD      │
              │  deploy qa  │
              └──────┬──────┘
                     │
                     │ PR
                     ▼
              ┌─────────────┐
              │     CI      │
              └──────┬──────┘
                     │
                   merge
                     ▼
                    PROD
                     │
                     ▼
              ┌─────────────┐
              │     CD      │
              │ deploy prod │
              └──────┬──────┘
                     │
                     ▼
                 Databricks
```

---

# GitHub Secrets

The current CD workflow requires:

```text
DATABRICKS_HOST
DATABRICKS_TOKEN
```

Configure these under:

```text
GitHub Repository
      ↓
Settings
      ↓
Secrets and variables
      ↓
Actions
      ↓
Repository secrets
```

## `DATABRICKS_HOST`

The URL of the Databricks workspace.

Example:

```text
https://<workspace>.cloud.databricks.com
```

## `DATABRICKS_TOKEN`

A Databricks Personal Access Token (PAT) used by GitHub Actions to authenticate with Databricks.

Secrets should never be committed to:

```text
ci.yml
cd.yml
databricks.yml
Python files
README.md
```

---

# Environment Configuration

The current workflow uses:

```text
DATABRICKS_HOST
DATABRICKS_TOKEN
```

for deployment and determines the logical environment using the branch name.

Therefore:

```text
Git branch → Bundle target

dev         → dev
qa          → qa
prod        → prod
```

If the same `DATABRICKS_HOST` and `DATABRICKS_TOKEN` are used for all three branches, then `dev`, `qa`, and `prod` are logical deployment environments within the same Databricks workspace.

If separate Databricks workspaces are introduced later, environment-specific secrets can be used.

For example:

```text
DEV_DATABRICKS_HOST
DEV_DATABRICKS_TOKEN

QA_DATABRICKS_HOST
QA_DATABRICKS_TOKEN

PROD_DATABRICKS_HOST
PROD_DATABRICKS_TOKEN
```

---

# Important Files for CI/CD

```text
.github/
└── workflows/
    ├── ci.yml          # Continuous Integration
    └── cd.yml          # Continuous Deployment

databricks.yml          # Databricks Asset Bundle definition

requirements-dev.txt    # Dependencies used by CI

src/                    # Application / ML source code

tests/                  # Automated tests

data/                   # Sample EHR data
```

The CI/CD relationship is:

```text
src/
tests/
data/
   │
   ├───────────────┐
   │               │
   ▼               ▼
ci.yml        databricks.yml
   │               │
   ▼               ▼
pytest           cd.yml
                   │
                   ▼
              Databricks
```

---

# Running CI Tests Locally

Install the development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the same test command used by GitHub Actions:

```bash
python -m pytest -v
```

Running the same command locally helps detect failures before opening a pull request.

---

# Validate a Bundle Locally

After installing and authenticating the Databricks CLI:

### DEV

```bash
databricks bundle validate --target dev
```

### QA

```bash
databricks bundle validate --target qa
```

### PROD

```bash
databricks bundle validate --target prod
```

---

# Deploy Manually

Although GitHub Actions performs deployment automatically, the equivalent local commands are:

### DEV

```bash
databricks bundle deploy --target dev
```

### QA

```bash
databricks bundle deploy --target qa
```

### PROD

```bash
databricks bundle deploy --target prod
```

---

# Current Pipeline Scope

The current CI/CD implementation automates:

* Pull-request testing
* Dependency installation
* pytest execution
* Databricks CLI setup
* Secret validation
* Databricks authentication checks
* Databricks connection checks
* Asset Bundle validation
* Environment-specific bundle deployment
* `dev` → `qa` → `prod` branch promotion

The current `cd.yml` performs **bundle deployment only** after validation.

It does not currently contain a separate step that automatically runs the deployed ML training job after deployment.

This distinction is important:

```text
databricks bundle deploy
```

means:

```text
Create/update Databricks resources
```

while:

```text
databricks bundle run
```

would mean:

```text
Execute a deployed Databricks job
```

---

# Technologies

* Git
* GitHub
* GitHub Actions
* Python 3.12
* pytest
* Databricks
* Databricks CLI
* Databricks Asset Bundles
* EHR machine learning sample application

---

# Summary

This project demonstrates a basic MLOps promotion workflow:

```text
Develop
   ↓
Pull Request
   ↓
CI Tests
   ↓
Merge
   ↓
CD Validation
   ↓
Databricks Bundle Deployment
   ↓
Promote from DEV → QA → PROD
```

**CI protects the code before merge.**

**CD automatically deploys the merged code and Databricks configuration to the environment represented by the Git branch.**

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
