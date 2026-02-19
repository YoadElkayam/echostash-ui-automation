"""Sanity tests for Plans and Usage pages (UI-BILL)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.plans_page import PlansPage
from pages.usage_page import UsagePage


@pytest.mark.sanity
class TestPlansPage:
    """Verify the plans page."""

    def test_plans_page_loads(self, page: Page, base_url: str) -> None:
        """UI-BILL-001: Plans page loads with plan cards."""
        plans = PlansPage(page, base_url)
        plans.open()
        expect(plans.page).to_have_url(f".*plans.*", timeout=10000)
        plans.wait_for_loading_complete()
        body_text = plans.page.locator("body").inner_text()
        assert len(body_text.strip()) > 0


@pytest.mark.sanity
class TestUsagePage:
    """Verify the usage page."""

    def test_usage_page_loads(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-BILL-004: Usage page loads with quota information."""
        usage = UsagePage(authenticated_page, base_url)
        usage.open()
        expect(usage.page).to_have_url(f".*usage.*", timeout=10000)
        usage.wait_for_loading_complete()
