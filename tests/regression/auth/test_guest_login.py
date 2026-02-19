"""Regression tests for the full guest login flow."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.auth_page import AuthPage
from pages.dashboard_page import DashboardPage


@pytest.mark.regression
class TestGuestLoginFlow:
    """Full guest login flow tests."""

    def test_guest_login_auto_on_first_visit(self, page: Page, base_url: str) -> None:
        """UI-AUTH-001: Guest login happens when user clicks guest button."""
        auth = AuthPage(page, base_url)
        auth.navigate("/")
        auth.click_guest_login()
        expect(page).to_have_url(f"{base_url}/dashboard", timeout=15000)

    def test_guest_user_sees_dashboard(self, page: Page, base_url: str) -> None:
        """After guest login, dashboard is accessible."""
        auth = AuthPage(page, base_url)
        auth.navigate("/")
        auth.click_guest_login()
        page.wait_for_load_state("networkidle")
        dashboard = DashboardPage(page, base_url)
        # Dashboard should have loaded
        expect(page).to_have_url(f"{base_url}/dashboard", timeout=15000)

    def test_guest_user_header_indicator(self, page: Page, base_url: str) -> None:
        """Guest user should see a guest indicator in the header."""
        auth = AuthPage(page, base_url)
        auth.navigate("/")
        auth.click_guest_login()
        page.wait_for_load_state("networkidle")
        # Check for guest-related text
        guest_indicator = page.get_by_text("Guest", exact=False).first
        expect(guest_indicator).to_be_visible(timeout=10000)

    def test_guest_can_create_project(
        self, page: Page, base_url: str
    ) -> None:
        """Guests should be able to create a project."""
        from pages.project_modal import ProjectModal
        from utils.helpers import unique_name

        auth = AuthPage(page, base_url)
        auth.navigate("/")
        auth.click_guest_login()
        page.wait_for_load_state("networkidle")

        dashboard = DashboardPage(page, base_url)
        dashboard.click_new_project()

        modal = ProjectModal(page, base_url)
        modal.wait_for_modal()
        name = unique_name("guest-proj")
        modal.fill_name(name)
        modal.submit()

        expect(page.get_by_text(name, exact=False).first).to_be_visible(timeout=10000)
