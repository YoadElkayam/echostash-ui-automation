# Echostash UI Automation

End-to-end UI tests for the Echostash platform using **Playwright** and **pytest**.

## Project Structure

```
├── .github/workflows/   # CI/CD pipelines (sanity + regression)
├── config/              # Environment config files (local, stage, prod)
├── pages/               # Page Object Model classes (22 page objects)
├── tests/
│   ├── conftest.py      # Shared fixtures (auth, page objects, test data)
│   ├── sanity/          # Quick smoke tests (18 files)
│   └── regression/      # Full regression suite (47 files, organized by feature)
├── utils/
│   └── helpers.py       # API helpers, auth, data generators
├── requirements.txt     # Python dependencies
├── pytest.ini           # Pytest markers and options
└── pyproject.toml       # Project metadata
```

## Prerequisites

- Python 3.11+
- pip

## Installation

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install --with-deps chromium
```

## Important: Echostash Must Be Running

The UI tests interact with the Echostash frontend and backend. You need a running instance to test against.

### Option 1: Test against local Echostash

Start the Echostash backend and frontend locally first:

```bash
# Start infrastructure (Postgres + Redis)
cd /path/to/Echostash/gra-echostash-be && docker compose up -d

# Start the backend (port 8085)
cd /path/to/Echostash/gra-echostash-be && ./gradlew bootRun

# Start the frontend (port 3000)
cd /path/to/Echostash/gra-echostash-fe && npm run dev
```

Then run tests with `--env local`:

```bash
pytest tests/sanity/ --env local -v
```

### Option 2: Test against stage/prod

No local setup needed -- tests point at remote URLs:

```bash
pytest tests/sanity/ --env stage -v
pytest tests/sanity/ --env prod -v
```

## How to Run Tests

### Run sanity tests

```bash
pytest tests/sanity/ -m sanity -v
```

### Run full regression suite

```bash
pytest tests/ -v
```

### Run tests by area

```bash
pytest tests/sanity/test_auth.py -v             # Auth flows
pytest tests/sanity/test_dashboard.py -v         # Dashboard
pytest tests/regression/prompts/ -v              # All prompt tests
pytest tests/regression/browse/ -v               # Browse/search tests
pytest tests/regression/evals/ -v                # Eval system tests
pytest tests/regression/projects/ -v             # Project management
pytest tests/regression/share/ -v                # Sharing flow
pytest tests/regression/settings/ -v             # API keys, context store, usage
```

### Run with a specific environment

```bash
pytest tests/ --env local -v     # Against http://localhost:3000
pytest tests/ --env stage -v     # Against https://stage.echostash.com
pytest tests/ --env prod -v      # Against https://app.echostash.com
```

### Run in parallel

```bash
pytest tests/ -n auto -v
```

### Run with HTML report

```bash
pytest tests/ --html=report.html --self-contained-html
# Then open report.html in your browser
```

### Run with Allure reporting

```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

### Run with video and screenshot capture

```bash
pytest tests/ --video=on --screenshot=on
# Artifacts saved to test-results/
```

## Test Markers

| Marker                     | Description                  |
|----------------------------|------------------------------|
| `@pytest.mark.sanity`      | Quick sanity checks          |
| `@pytest.mark.regression`  | Full regression tests        |

## Environment Configuration

Environment files are in `config/`:

| File        | Frontend URL                  | Backend URL                      |
|-------------|-------------------------------|----------------------------------|
| `local.env` | http://localhost:3000         | http://localhost:8085            |
| `stage.env` | https://stage.echostash.com  | https://stage-api.echostash.com |
| `prod.env`  | https://app.echostash.com    | https://api.echostash.com       |

## CI/CD (GitHub Actions)

### Sanity Pipeline (`sanity.yml`)

- **Triggers:** Manual dispatch via `workflow_dispatch`, pull requests to `main`
- **Scope:** `tests/sanity/` with `-m sanity` marker
- **Environment:** Select `local`, `stage`, or `prod` from the dispatch dropdown (defaults to `stage`)
- **Artifacts:** HTML report, Allure results, test screenshots
- **Timeout:** 30 minutes

### Regression Pipeline (`regression.yml`)

- **Triggers:** Manual dispatch via `workflow_dispatch`, nightly schedule at 2:00 AM UTC
- **Scope:** All tests in `tests/`
- **Environment:** Select from dispatch dropdown (defaults to `stage`)
- **Artifacts:** HTML report, Allure results, videos, screenshots
- **Timeout:** 60 minutes

To trigger manually: Go to **Actions** tab > select workflow > **Run workflow** > choose environment.

## Page Objects

All page objects extend `BasePage` which provides common methods for navigation, waiting, interactions, toasts, and assertions.

| Page Object           | Covers                                    |
|-----------------------|-------------------------------------------|
| `AuthPage`            | Guest login, Google login, logout         |
| `DashboardPage`       | Project list, semantic search             |
| `PromptBuilderPage`   | Create/edit prompts, Monaco editor        |
| `ProjectModal`        | Create/edit project dialogs               |
| `ProjectViewPage`     | Project detail with prompt list           |
| `Sidebar`             | Main navigation                           |
| `BrowsePage`          | Public prompt browsing                    |
| `SharePage`           | Prompt sharing flow                       |
| `EvalsPage`           | Eval management                           |
| `MonacoEditor`        | Code editor interactions                  |
| `ApiKeysPage`         | API key management                        |
| `ContextStorePage`    | File upload and asset management          |
| `AnalyticsPage`       | Analytics dashboard                       |
| `PlansPage`           | Pricing plans                             |
| `UsagePage`           | Usage statistics                          |
