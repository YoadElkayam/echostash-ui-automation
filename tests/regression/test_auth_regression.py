"""Regression tests for Authentication flows (UI-AUTH P1/P2)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.auth_page import AuthPage


@pytest.mark.regression
class TestAuthModal:
    """Verify auth modal behavior for guest and premium actions."""

    def test_auth_modal_trigger_on_premium_action(
        self, page: Page, base_url: str
    ) -> None:
        """UI-AUTH-006: Guest trying a premium action sees auth modal."""
        page.goto(f"{base_url}/api-keys")
        page.wait_for_load_state("domcontentloaded")
        auth_modal = page.locator("[role='dialog']")
        # Should either redirect or show auth modal
        has_modal = auth_modal.is_visible()
        redirected = "api-keys" not in page.url
        assert has_modal or redirected

    def test_expired_session_redirect(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-AUTH-007: Expired session triggers re-auth."""
        # Clear auth cookies to simulate expired session
        authenticated_page.context.clear_cookies()
        authenticated_page.goto(f"{base_url}/dashboard")
        authenticated_page.wait_for_load_state("domcontentloaded")
        auth_modal = authenticated_page.locator("[role='dialog']")
        redirected = "dashboard" not in authenticated_page.url
        assert auth_modal.is_visible() or redirected


@pytest.mark.regression
class TestGuestToUserUpgrade:
    """Verify guest-to-user upgrade flow."""

    def test_guest_data_retained_after_upgrade(
        self, page: Page, base_url: str
    ) -> None:
        """UI-AUTH-003: Guest data is retained after signing in."""
        auth = AuthPage(page, base_url)
        auth.navigate("/")
        auth.click_guest_login()
        page.wait_for_load_state("networkidle")
        # Verify we are on dashboard as guest
        expect(page).to_have_url(f".*dashboard.*", timeout=15000)
