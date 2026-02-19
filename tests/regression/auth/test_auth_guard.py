"""Regression tests for authentication guards on protected pages."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.regression
class TestAuthGuard:
    """Verify protected pages redirect unauthenticated users."""

    PROTECTED_PAGES = [
        "/dashboard",
        "/prompt-builder",
        "/api-keys",
        "/context-store",
        "/analytics",
        "/usage",
        "/evals",
    ]

    @pytest.mark.parametrize("path", PROTECTED_PAGES)
    def test_protected_page_redirects(
        self, page: Page, base_url: str, path: str
    ) -> None:
        """UI-AUTH-007: Protected pages redirect or show auth modal."""
        page.goto(f"{base_url}{path}")
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        auth_modal = page.locator("[role='dialog']")
        is_protected = path not in page.url or auth_modal.is_visible()
        assert is_protected, f"Page {path} should be protected"

    def test_auth_modal_has_login_options(self, page: Page, base_url: str) -> None:
        """UI-AUTH-006: Auth modal shows login options when triggered."""
        page.goto(f"{base_url}/dashboard")
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        auth_modal = page.locator("[role='dialog']")
        if auth_modal.is_visible():
            # Should have at least a Guest or Google login option
            guest_btn = auth_modal.get_by_role("button", name="Guest")
            google_btn = auth_modal.get_by_role("button", name="Google")
            has_option = guest_btn.is_visible() or google_btn.is_visible()
            assert has_option, "Auth modal should have login options"
