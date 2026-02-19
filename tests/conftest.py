import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="local",
        choices=["local", "stage", "prod"],
        help="Target environment: local, stage, or prod",
    )


@pytest.fixture(scope="session", autouse=True)
def load_env(request):
    env = request.config.getoption("--env")
    env_file = os.path.join(os.path.dirname(__file__), "..", "config", f"{env}.env")
    load_dotenv(env_file, override=True)


@pytest.fixture
def base_url():
    return os.getenv("BASE_URL", "http://localhost:3000")


@pytest.fixture
def api_url():
    return os.getenv("API_URL", "http://localhost:8085")


@pytest.fixture
def app_page(page: Page, base_url: str) -> Page:
    page.goto(base_url)
    page.wait_for_load_state("networkidle")
    return page
