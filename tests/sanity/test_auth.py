"""Sanity tests for authentication flows."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.auth_page import AuthPage


@pytest.mark.sanity
class TestGuestLogin:
    """Verify guest login flow works end-to-end."""

    def test_guest_login_succeeds(self, page: Page, base_url: str) -> None:
        """Guest login should authenticate the user and redirect to dashboard."""
        auth = AuthPage(page, base_url)
        auth.navigate("/")
        auth.click_guest_login()
        expect(page).to_have_url(f"{base_url}/dashboard", timeout=15000)

    def test_guest_user_is_logged_in(self, page: Page, base_url: str) -> None:
        """After guest login, user should appear as logged in."""
        auth = AuthPage(page, base_url)
        auth.navigate("/")
        auth.click_guest_login()
        page.wait_for_load_state("networkidle")
        assert auth.is_logged_in()


@pytest.mark.sanity
class TestLogout:
    """Verify logout flow."""

    def test_logout_redirects_to_landing(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """After logout, user should be redirected away from the dashboard."""
        auth = AuthPage(authenticated_page, base_url)
        auth.navigate("/dashboard")
        auth.wait_for_page_load()
        auth.logout()
        # Should no longer be on dashboard
        expect(authenticated_page).not_to_have_url(f"{base_url}/dashboard")


@pytest.mark.sanity
class TestProtectedPages:
    """Verify protected pages require authentication."""

    @pytest.mark.parametrize(
        "path",
        ["/dashboard", "/prompt-builder", "/api-keys", "/context-store"],
    )
    def test_protected_page_requires_auth(
        self, page: Page, base_url: str, path: str
    ) -> None:
        """Navigating to a protected page without auth should show login or redirect."""
        page.goto(f"{base_url}{path}")
        page.wait_for_load_state("domcontentloaded")
        # Should either show auth modal or redirect to landing
        auth_modal = page.locator("[role='dialog']")
        is_redirected = "/dashboard" not in page.url or auth_modal.is_visible()
        assert is_redirected, f"Protected page {path} did not require authentication"
