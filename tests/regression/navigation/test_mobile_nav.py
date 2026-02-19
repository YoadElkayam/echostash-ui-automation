"""Regression tests for mobile viewport navigation."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.mobile_nav import MobileNav


@pytest.mark.regression
@pytest.mark.mobile
class TestMobileNav:
    """Verify mobile navigation at small viewport."""

    def test_hamburger_menu_opens(
        self, page: Page, base_url: str, guest_auth: dict
    ) -> None:
        """UI-NAV-002: Mobile hamburger menu opens."""
        from utils.helpers import set_auth_cookie

        set_auth_cookie(page.context, guest_auth["accessToken"], base_url)
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto(f"{base_url}/dashboard")
        page.wait_for_load_state("networkidle")

        mobile = MobileNav(page, base_url)
        mobile.open_menu()
        expect(mobile._menu_panel).to_be_visible()

    def test_hamburger_menu_closes(
        self, page: Page, base_url: str, guest_auth: dict
    ) -> None:
        """Mobile menu closes after clicking close button."""
        from utils.helpers import set_auth_cookie

        set_auth_cookie(page.context, guest_auth["accessToken"], base_url)
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto(f"{base_url}/dashboard")
        page.wait_for_load_state("networkidle")

        mobile = MobileNav(page, base_url)
        mobile.open_menu()
        mobile.close_menu()

    def test_mobile_nav_to_dashboard(
        self, page: Page, base_url: str, guest_auth: dict
    ) -> None:
        """Navigate to dashboard via mobile menu."""
        from utils.helpers import set_auth_cookie

        set_auth_cookie(page.context, guest_auth["accessToken"], base_url)
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto(f"{base_url}/dashboard")
        page.wait_for_load_state("networkidle")

        mobile = MobileNav(page, base_url)
        mobile.navigate_to("Dashboard")
        assert "/dashboard" in page.url

    def test_mobile_nav_to_browse(
        self, page: Page, base_url: str, guest_auth: dict
    ) -> None:
        """Navigate to browse via mobile menu."""
        from utils.helpers import set_auth_cookie

        set_auth_cookie(page.context, guest_auth["accessToken"], base_url)
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto(f"{base_url}/dashboard")
        page.wait_for_load_state("networkidle")

        mobile = MobileNav(page, base_url)
        mobile.navigate_to("Browse")
        page.wait_for_load_state("domcontentloaded")
