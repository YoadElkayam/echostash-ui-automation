# Echostash UI Automation

End-to-end UI tests for the Echostash platform using **Playwright** and **pytest**.

## Project Structure

```
├── .github/workflows/   # CI/CD pipelines (sanity + regression)
├── config/              # Environment config files
├── pages/               # Page Object Model classes
├── tests/
│   ├── sanity/          # Quick smoke/sanity tests
│   └── regression/      # Full regression suite
├── utils/               # Shared helpers and utilities
├── requirements.txt     # Python dependencies
└── pyproject.toml       # Project metadata
```

## Prerequisites

- Python 3.11+
- pip

## Local Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install --with-deps chromium
```

## Running Tests

### Run sanity tests (local environment)

```bash
pytest tests/sanity/ -m sanity --env local -v
```

### Run full regression (stage environment)

```bash
pytest tests/ --env stage -v
```

### Run with HTML report

```bash
pytest tests/sanity/ -m sanity --env local --html=report.html --self-contained-html
```

### Run with Allure reporting

```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

### Run in parallel

```bash
pytest tests/ -n auto -v
```

## CI/CD

### Sanity Pipeline
- **Triggers:** Manual dispatch, pull requests to `main`
- **Scope:** `tests/sanity/` with `-m sanity` marker
- **Artifacts:** HTML report, Allure results

### Regression Pipeline
- **Triggers:** Manual dispatch, nightly schedule (2:00 AM UTC)
- **Scope:** All tests in `tests/`
- **Artifacts:** HTML report, Allure results, videos, screenshots

## Test Markers

| Marker       | Description              |
|-------------|--------------------------|
| `@pytest.mark.sanity`     | Quick sanity checks      |
| `@pytest.mark.regression` | Full regression tests    |

## Environment Configuration

Environment files are in `config/`:

| File        | Target                    |
|-------------|---------------------------|
| `local.env` | http://localhost:3000     |
| `stage.env` | https://stage.echostash.com |
| `prod.env`  | https://app.echostash.com |
