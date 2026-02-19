"""Regression tests for logout flow."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.auth_page import AuthPage
from pages.sidebar import Sidebar


@pytest.mark.regression
class TestLogoutFlow:
    """Full logout flow tests."""

    def test_logout_from_dashboard(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-AUTH-004: Logout from dashboard returns to landing/guest state."""
        auth = AuthPage(authenticated_page, base_url)
        auth.navigate("/dashboard")
        auth.wait_for_page_load()
        auth.logout()
        expect(authenticated_page).not_to_have_url(f"{base_url}/dashboard")

    def test_logout_via_sidebar(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """Logout via sidebar user menu."""
        sidebar = Sidebar(authenticated_page, base_url)
        authenticated_page.goto(f"{base_url}/dashboard")
        authenticated_page.wait_for_load_state("networkidle")
        sidebar.click_sign_out()
        expect(authenticated_page).not_to_have_url(f"{base_url}/dashboard")

    def test_logout_clears_session(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """After logout, navigating to protected page should not work."""
        auth = AuthPage(authenticated_page, base_url)
        auth.navigate("/dashboard")
        auth.wait_for_page_load()
        auth.logout()
        authenticated_page.wait_for_timeout(1000)

        # Try accessing dashboard again
        authenticated_page.goto(f"{base_url}/dashboard")
        authenticated_page.wait_for_load_state("domcontentloaded")
        authenticated_page.wait_for_timeout(2000)

        # Should be redirected or shown auth modal
        auth_modal = authenticated_page.locator("[role='dialog']")
        is_protected = "/dashboard" not in authenticated_page.url or auth_modal.is_visible()
        assert is_protected
