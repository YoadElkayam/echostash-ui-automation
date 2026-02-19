"""Shared helpers for API calls, auth, data generation, and UI utilities."""

from __future__ import annotations

import random
import string
import uuid
from typing import Any, Optional

import requests
from playwright.sync_api import BrowserContext, Page


# ── API Helpers (test data setup/teardown) ───────────────────────────────


def api_login_guest(api_url: str) -> dict:
    """Login as a guest user via the backend API.

    Args:
        api_url: Backend API base URL.

    Returns:
        Dict with ``accessToken`` and ``refreshToken``.
    """
    resp = requests.post(f"{api_url}/auth/guest", timeout=15)
    resp.raise_for_status()
    return resp.json()


def api_create_project(
    api_url: str, token: str, name: str, description: str = ""
) -> dict:
    """Create a project via the backend API.

    Args:
        api_url: Backend API base URL.
        token: Bearer access token.
        name: Project name.
        description: Optional project description.

    Returns:
        Created project payload.
    """
    resp = requests.post(
        f"{api_url}/projects",
        json={"name": name, "description": description},
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def api_create_prompt(
    api_url: str, token: str, project_id: str, data: dict
) -> dict:
    """Create a prompt via the backend API.

    Args:
        api_url: Backend API base URL.
        token: Bearer access token.
        project_id: Owning project ID.
        data: Prompt payload (title, content, etc.).

    Returns:
        Created prompt payload.
    """
    resp = requests.post(
        f"{api_url}/projects/{project_id}/prompts",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def api_delete_project(api_url: str, token: str, project_id: str) -> None:
    """Delete a project via the backend API.

    Args:
        api_url: Backend API base URL.
        token: Bearer access token.
        project_id: ID of the project to delete.
    """
    requests.delete(
        f"{api_url}/projects/{project_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )


# ── Auth Helpers ─────────────────────────────────────────────────────────


def set_auth_cookie(context: BrowserContext, token: str, base_url: str) -> None:
    """Set the echostash_token cookie on the browser context.

    Args:
        context: Playwright browser context.
        token: JWT access token value.
        base_url: Application base URL (used for cookie domain).
    """
    from urllib.parse import urlparse

    parsed = urlparse(base_url)
    domain = parsed.hostname or "localhost"

    context.add_cookies(
        [
            {
                "name": "echostash_token",
                "value": token,
                "domain": domain,
                "path": "/",
                "httpOnly": False,
                "secure": parsed.scheme == "https",
                "sameSite": "Lax",
            }
        ]
    )


# ── UI Helpers ───────────────────────────────────────────────────────────


def wait_for_no_spinners(page: Page, timeout: int = 10000) -> None:
    """Wait until all loading spinners disappear from the page.

    Args:
        page: Playwright page instance.
        timeout: Maximum wait time in milliseconds.
    """
    for selector in [
        "[data-testid='loading']",
        ".animate-spin",
        "[role='progressbar']",
    ]:
        locator = page.locator(selector)
        if locator.count() > 0:
            locator.first.wait_for(state="hidden", timeout=timeout)


def get_monaco_value(page: Page) -> str:
    """Get the current value from a Monaco editor on the page.

    Args:
        page: Playwright page instance.

    Returns:
        Editor content as a string.
    """
    return page.evaluate(
        """() => {
            const editor = window.monaco?.editor?.getEditors()?.[0];
            return editor ? editor.getValue() : '';
        }"""
    )


def set_monaco_value(page: Page, value: str) -> None:
    """Set the value of a Monaco editor on the page.

    Args:
        page: Playwright page instance.
        value: Content to set in the editor.
    """
    page.evaluate(
        """(val) => {
            const editor = window.monaco?.editor?.getEditors()?.[0];
            if (editor) {
                editor.setValue(val);
            }
        }""",
        value,
    )


# ── Data Generators ─────────────────────────────────────────────────────


def unique_name(prefix: str = "test") -> str:
    """Generate a unique name with a prefix and short UUID.

    Args:
        prefix: Prefix for the name.

    Returns:
        A unique string like ``test-a1b2c3d4``.
    """
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def random_string(length: int = 8) -> str:
    """Generate a random alphanumeric string.

    Args:
        length: Desired string length.

    Returns:
        Random string of the given length.
    """
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def random_email() -> str:
    """Generate a random test email address.

    Returns:
        Email like ``test_abc12345@echostash-test.com``.
    """
    return f"test_{random_string()}@echostash-test.com"


def random_prompt_content() -> str:
    """Generate random prompt content for testing.

    Returns:
        A sample prompt string.
    """
    topics = ["AI", "coding", "writing", "data", "design"]
    actions = ["explain", "summarize", "generate", "analyze", "review"]
    topic = random.choice(topics)
    action = random.choice(actions)
    return f"Please {action} the following {topic} content: {{{{input}}}}"
