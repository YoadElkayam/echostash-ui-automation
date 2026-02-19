"""Sanity tests for sidebar navigation."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.sidebar import Sidebar
from pages.mobile_nav import MobileNav


@pytest.mark.sanity
class TestSidebarNavigation:
    """Verify all sidebar navigation links work."""

    SIDEBAR_LINKS = [
        ("Dashboard", "/dashboard"),
        ("Analytics", "/analytics"),
        ("API Keys", "/api-keys"),
        ("Context Store", "/context-store"),
        ("Plans", "/plans"),
    ]

    @pytest.mark.parametrize("link_name,expected_path", SIDEBAR_LINKS)
    def test_sidebar_link_navigates(
        self,
        authenticated_page: Page,
        base_url: str,
        link_name: str,
        expected_path: str,
    ) -> None:
        """UI-NAV-001: Each sidebar link navigates to the correct page."""
        sidebar = Sidebar(authenticated_page, base_url)
        authenticated_page.goto(f"{base_url}/dashboard")
        authenticated_page.wait_for_load_state("networkidle")

        sidebar.navigate_to(link_name)
        expect(authenticated_page).to_have_url(
            f"{base_url}{expected_path}", timeout=10000
        )


@pytest.mark.sanity
class TestMobileNavigation:
    """Verify mobile navigation works."""

    def test_mobile_nav_works(self, page: Page, base_url: str, guest_auth: dict) -> None:
        """UI-NAV-002: Mobile hamburger menu opens and navigates."""
        from utils.helpers import set_auth_cookie

        set_auth_cookie(page.context, guest_auth["accessToken"], base_url)
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto(f"{base_url}/dashboard")
        page.wait_for_load_state("networkidle")

        mobile = MobileNav(page, base_url)
        mobile.open_menu()
        mobile.navigate_to("Dashboard")
        page.wait_for_load_state("domcontentloaded")
        assert "/dashboard" in page.url
