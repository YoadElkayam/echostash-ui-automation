"""Sanity tests for the landing page and basic navigation."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.auth_page import AuthPage
from pages.dashboard_page import DashboardPage


@pytest.mark.sanity
class TestLandingPage:
    """Verify the landing page loads and basic navigation works."""

    def test_landing_page_loads(self, app_page: Page, base_url: str) -> None:
        """Landing page should load successfully with a non-empty title."""
        expect(app_page).not_to_have_url("about:blank")
        assert app_page.title() != ""

    def test_landing_page_has_content(self, app_page: Page) -> None:
        """Landing page should display visible content."""
        body = app_page.locator("body")
        expect(body).to_be_visible()
        assert app_page.locator("body").inner_text().strip() != ""

    def test_guest_login_navigates_to_dashboard(
        self, page: Page, base_url: str
    ) -> None:
        """After guest login, user should be redirected to the dashboard."""
        auth = AuthPage(page, base_url)
        auth.navigate("/")
        auth.click_guest_login()
        # After login, URL should contain /dashboard
        expect(page).to_have_url(f"{base_url}/dashboard", timeout=15000)

    def test_navigation_to_browse(self, app_page: Page, base_url: str) -> None:
        """User should be able to navigate to the browse page."""
        app_page.goto(f"{base_url}/browse")
        app_page.wait_for_load_state("domcontentloaded")
        expect(app_page).to_have_url(f"{base_url}/browse")

    def test_navigation_to_plans(self, app_page: Page, base_url: str) -> None:
        """User should be able to navigate to the plans page."""
        app_page.goto(f"{base_url}/plans")
        app_page.wait_for_load_state("domcontentloaded")
        expect(app_page).to_have_url(f"{base_url}/plans")
