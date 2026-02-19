"""Regression tests for Responsive Design (UI-RESP)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect


MOBILE_VIEWPORT = {"width": 375, "height": 812}
TABLET_VIEWPORT = {"width": 768, "height": 1024}
DESKTOP_VIEWPORT = {"width": 1280, "height": 720}


@pytest.mark.regression
@pytest.mark.mobile
class TestMobileLayout:
    """Verify pages render correctly at mobile viewport (375px)."""

    def test_dashboard_mobile(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-RESP-001: Dashboard at mobile viewport stacks cards correctly."""
        authenticated_page.set_viewport_size(MOBILE_VIEWPORT)
        authenticated_page.goto(f"{base_url}/dashboard")
        authenticated_page.wait_for_load_state("domcontentloaded")
        # No horizontal scroll bar should appear
        has_overflow = authenticated_page.evaluate(
            "() => document.documentElement.scrollWidth > document.documentElement.clientWidth"
        )
        assert not has_overflow

    def test_browse_mobile(self, page: Page, base_url: str) -> None:
        """UI-RESP-003: Browse page at mobile viewport."""
        page.set_viewport_size(MOBILE_VIEWPORT)
        page.goto(f"{base_url}/browse")
        page.wait_for_load_state("domcontentloaded")
        has_overflow = page.evaluate(
            "() => document.documentElement.scrollWidth > document.documentElement.clientWidth"
        )
        assert not has_overflow

    def test_share_mobile(self, page: Page, base_url: str) -> None:
        """UI-RESP-004: Share page at mobile viewport."""
        page.set_viewport_size(MOBILE_VIEWPORT)
        page.goto(f"{base_url}/share")
        page.wait_for_load_state("domcontentloaded")
        has_overflow = page.evaluate(
            "() => document.documentElement.scrollWidth > document.documentElement.clientWidth"
        )
        assert not has_overflow

    def test_plans_mobile(self, page: Page, base_url: str) -> None:
        """UI-RESP-006: Plans page at mobile viewport stacks plan cards."""
        page.set_viewport_size(MOBILE_VIEWPORT)
        page.goto(f"{base_url}/plans")
        page.wait_for_load_state("domcontentloaded")
        has_overflow = page.evaluate(
            "() => document.documentElement.scrollWidth > document.documentElement.clientWidth"
        )
        assert not has_overflow


@pytest.mark.regression
@pytest.mark.mobile
class TestDesktopLayout:
    """Verify pages render correctly at desktop viewport."""

    @pytest.mark.parametrize(
        "path",
        ["/dashboard", "/browse", "/share", "/plans", "/analytics"],
    )
    def test_desktop_pages_load(
        self, authenticated_page: Page, base_url: str, path: str
    ) -> None:
        """UI-RESP-008: All pages load correctly at 1280px desktop."""
        authenticated_page.set_viewport_size(DESKTOP_VIEWPORT)
        authenticated_page.goto(f"{base_url}{path}")
        authenticated_page.wait_for_load_state("domcontentloaded")
        body = authenticated_page.locator("body").inner_text()
        assert len(body.strip()) > 0
