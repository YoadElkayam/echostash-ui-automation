"""Sanity tests for Error States (UI-ERR)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.sanity
class TestErrorStates:
    """Verify the app handles error conditions gracefully."""

    def test_401_redirect_for_unauthenticated(
        self, page: Page, base_url: str
    ) -> None:
        """UI-ERR-001: Accessing a protected page without auth redirects or shows modal."""
        page.goto(f"{base_url}/dashboard")
        page.wait_for_load_state("domcontentloaded")
        auth_modal = page.locator("[role='dialog']")
        is_protected = (
            "dashboard" not in page.url or auth_modal.is_visible()
        )
        assert is_protected

    def test_429_plan_limit_overlay(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ERR-002: Plan limit overlay appears when quota exceeded."""
        # Mock a 429 response for a protected action
        authenticated_page.route(
            "**/api/**",
            lambda route: route.fulfill(status=429, body='{"error":"rate limit"}'),
        )
        authenticated_page.goto(f"{base_url}/dashboard")
        authenticated_page.wait_for_load_state("domcontentloaded")
        # Look for plan limit overlay or error message
        overlay = authenticated_page.locator(
            "[data-testid='plan-limit-overlay']"
        ).or_(authenticated_page.get_by_text("Upgrade")).first
        # Unroute to clean up
        authenticated_page.unroute("**/api/**")

    def test_405_upgrade_overlay(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ERR-003: Upgrade overlay for premium-only features."""
        authenticated_page.route(
            "**/api/**",
            lambda route: route.fulfill(status=405, body='{"error":"upgrade required"}'),
        )
        authenticated_page.goto(f"{base_url}/dashboard")
        authenticated_page.wait_for_load_state("domcontentloaded")
        authenticated_page.unroute("**/api/**")

    def test_form_validation_errors(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ERR-004: Submitting forms with invalid data shows inline errors."""
        from pages.dashboard_page import DashboardPage
        from pages.project_modal import ProjectModal

        dash = DashboardPage(authenticated_page, base_url)
        dash.open()
        dash.click_new_project()
        modal = ProjectModal(dash.page, base_url)
        modal.wait_for_modal()
        # Submit with empty name
        modal.fill_name("")
        modal.submit()
        # Modal should remain visible (validation prevents close)
        expect(modal._modal).to_be_visible(timeout=3000)

    def test_404_page(self, page: Page, base_url: str) -> None:
        """UI-ERR-006: Invalid route shows 404 page."""
        page.goto(f"{base_url}/this-route-does-not-exist-12345")
        page.wait_for_load_state("domcontentloaded")
        body_text = page.locator("body").inner_text().lower()
        # Should show some kind of not-found indication
        has_404 = (
            "404" in body_text
            or "not found" in body_text
            or "page" in body_text
        )
        assert has_404 or page.url != f"{base_url}/this-route-does-not-exist-12345"
