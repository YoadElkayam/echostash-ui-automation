"""Pytest configuration and shared fixtures for Echostash UI tests."""

from __future__ import annotations

import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from pages.auth_page import AuthPage
from pages.browse_page import BrowsePage
from pages.dashboard_page import DashboardPage
from pages.prompt_builder_page import PromptBuilderPage
from pages.share_page import SharePage
from pages.sidebar import Sidebar
from utils.helpers import (
    api_create_project,
    api_create_prompt,
    api_delete_project,
    api_login_guest,
    set_auth_cookie,
    unique_name,
)


# ── CLI Options ──────────────────────────────────────────────────────────


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="local",
        choices=["local", "stage", "prod"],
        help="Target environment: local, stage, or prod",
    )


# ── Environment ──────────────────────────────────────────────────────────


@pytest.fixture(scope="session", autouse=True)
def load_env(request):
    """Load the environment-specific .env file."""
    env = request.config.getoption("--env")
    env_file = os.path.join(os.path.dirname(__file__), "..", "config", f"{env}.env")
    load_dotenv(env_file, override=True)


@pytest.fixture(scope="session")
def base_url() -> str:
    """Application base URL."""
    return os.getenv("BASE_URL", "http://localhost:3000")


@pytest.fixture(scope="session")
def api_url() -> str:
    """Backend API base URL."""
    return os.getenv("API_URL", "http://localhost:8085")


@pytest.fixture(scope="session")
def admin_url() -> str:
    """Admin panel base URL."""
    return os.getenv("ADMIN_URL", "http://localhost:3001")


# ── Auth Fixtures ────────────────────────────────────────────────────────


@pytest.fixture
def guest_auth(api_url: str) -> dict:
    """Login as a guest user via the API and return token data.

    Returns:
        Dict with ``accessToken`` and ``refreshToken``.
    """
    return api_login_guest(api_url)


@pytest.fixture
def authenticated_page(page: Page, base_url: str, guest_auth: dict) -> Page:
    """Return a Playwright Page with the auth cookie pre-set.

    The page navigates to the base URL after setting the cookie so the
    application recognises the authenticated session.
    """
    set_auth_cookie(page.context, guest_auth["accessToken"], base_url)
    page.goto(base_url)
    page.wait_for_load_state("domcontentloaded")
    return page


# ── Page Object Fixtures ─────────────────────────────────────────────────


@pytest.fixture
def auth_page(page: Page, base_url: str) -> AuthPage:
    """AuthPage instance (no pre-authentication)."""
    return AuthPage(page, base_url)


@pytest.fixture
def dashboard(authenticated_page: Page, base_url: str) -> DashboardPage:
    """Authenticated DashboardPage instance."""
    return DashboardPage(authenticated_page, base_url)


@pytest.fixture
def prompt_builder(authenticated_page: Page, base_url: str) -> PromptBuilderPage:
    """Authenticated PromptBuilderPage instance."""
    return PromptBuilderPage(authenticated_page, base_url)


@pytest.fixture
def browse(page: Page, base_url: str) -> BrowsePage:
    """BrowsePage instance (no auth required)."""
    return BrowsePage(page, base_url)


@pytest.fixture
def share(page: Page, base_url: str) -> SharePage:
    """SharePage instance (no auth required)."""
    return SharePage(page, base_url)


@pytest.fixture
def sidebar_nav(authenticated_page: Page, base_url: str) -> Sidebar:
    """Authenticated Sidebar instance."""
    return Sidebar(authenticated_page, base_url)


# ── Test Data Fixtures ───────────────────────────────────────────────────


@pytest.fixture
def test_project(authenticated_page: Page, api_url: str, guest_auth: dict):
    """Create a project via the API, yield it, then clean up.

    Yields:
        Project dict with ``id``, ``name``, etc.
    """
    token = guest_auth["accessToken"]
    name = unique_name("proj")
    project = api_create_project(api_url, token, name, "Test project")
    yield project
    api_delete_project(api_url, token, project["id"])


@pytest.fixture
def test_prompt(test_project: dict, api_url: str, guest_auth: dict):
    """Create a prompt inside the test project via the API.

    Yields:
        Prompt dict with ``id``, ``title``, etc.
    """
    token = guest_auth["accessToken"]
    data = {
        "title": unique_name("prompt"),
        "content": "Test prompt content: {{input}}",
        "description": "Automated test prompt",
    }
    prompt = api_create_prompt(api_url, token, test_project["id"], data)
    yield prompt
    # Prompt is deleted when the parent project is deleted


# ── Unauthenticated page fixture ─────────────────────────────────────────


@pytest.fixture
def app_page(page: Page, base_url: str) -> Page:
    """Navigate to base URL without authentication."""
    page.goto(base_url)
    page.wait_for_load_state("domcontentloaded")
    return page
