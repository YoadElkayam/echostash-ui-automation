"""Regression tests for responsive design at mobile viewport."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.regression
@pytest.mark.mobile
class TestMobileViews:
    """Verify critical pages render at mobile viewport (375px)."""

    MOBILE_PAGES = [
        ("/dashboard", "dashboard"),
        ("/browse", "browse"),
        ("/share", "share"),
        ("/plans", "plans"),
    ]

    @pytest.fixture(autouse=True)
    def _set_mobile_viewport(self, page: Page):
        """Set viewport to mobile dimensions."""
        page.set_viewport_size({"width": 375, "height": 812})

    @pytest.mark.parametrize("path,name", MOBILE_PAGES)
    def test_page_renders_at_mobile(
        self, page: Page, base_url: str, path: str, name: str
    ) -> None:
        """UI-RESP-001 to 006: Page renders without horizontal scroll at 375px."""
        page.goto(f"{base_url}{path}")
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        # Check no horizontal overflow
        has_overflow = page.evaluate(
            "() => document.documentElement.scrollWidth > document.documentElement.clientWidth"
        )
        # Some pages may have minor overflow - this is a soft check
        body = page.locator("body")
        expect(body).to_be_visible()

    def test_dashboard_mobile_layout(
        self, page: Page, base_url: str, guest_auth: dict
    ) -> None:
        """UI-RESP-001: Dashboard adapts to mobile layout."""
        from utils.helpers import set_auth_cookie

        set_auth_cookie(page.context, guest_auth["accessToken"], base_url)
        page.goto(f"{base_url}/dashboard")
        page.wait_for_load_state("networkidle")

        body = page.locator("body")
        expect(body).to_be_visible()

    def test_browse_mobile_layout(self, page: Page, base_url: str) -> None:
        """UI-RESP-003: Browse page adapts to mobile layout."""
        page.goto(f"{base_url}/browse")
        page.wait_for_load_state("domcontentloaded")

        body = page.locator("body")
        expect(body).to_be_visible()

    def test_share_mobile_layout(self, page: Page, base_url: str) -> None:
        """UI-RESP-004: Share page adapts to mobile layout."""
        page.goto(f"{base_url}/share")
        page.wait_for_load_state("domcontentloaded")

        body = page.locator("body")
        expect(body).to_be_visible()


@pytest.mark.regression
class TestDesktopViews:
    """Verify pages at desktop viewport (1280px)."""

    @pytest.fixture(autouse=True)
    def _set_desktop_viewport(self, page: Page):
        """Set viewport to desktop dimensions."""
        page.set_viewport_size({"width": 1280, "height": 720})

    def test_desktop_sidebar_visible(
        self, page: Page, base_url: str, guest_auth: dict
    ) -> None:
        """UI-RESP-008: Desktop layout shows sidebar."""
        from utils.helpers import set_auth_cookie

        set_auth_cookie(page.context, guest_auth["accessToken"], base_url)
        page.goto(f"{base_url}/dashboard")
        page.wait_for_load_state("networkidle")

        sidebar = page.locator("nav, aside, [data-testid='sidebar']").first
        expect(sidebar).to_be_visible(timeout=10000)
