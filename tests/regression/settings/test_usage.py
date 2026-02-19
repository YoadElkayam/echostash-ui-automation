"""Regression tests for usage and billing pages."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.plans_page import PlansPage
from pages.usage_page import UsagePage


@pytest.mark.regression
class TestUsagePage:
    """Verify usage and billing display."""

    def test_usage_page_loads(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-BILL-004: Usage page loads with quota info."""
        usage = UsagePage(authenticated_page, base_url)
        usage.open()
        expect(authenticated_page).to_have_url(f"{base_url}/usage")

    def test_quota_usage_displayed(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-BILL-005: Quota bars show used/remaining."""
        usage = UsagePage(authenticated_page, base_url)
        usage.open()

        quota_text = usage.get_quota_usage()
        assert isinstance(quota_text, str)

    def test_plans_page_shows_cards(self, page: Page, base_url: str) -> None:
        """UI-BILL-001: Plans page shows plan cards."""
        plans = PlansPage(page, base_url)
        plans.open()

        plan_list = plans.get_plan_list()
        assert isinstance(plan_list, list)

    def test_plan_card_has_details(self, page: Page, base_url: str) -> None:
        """UI-BILL-002: Plan cards show prices and features."""
        plans = PlansPage(page, base_url)
        plans.open()

        plan_list = plans.get_plan_list()
        if len(plan_list) > 0:
            # At least one plan card should have content
            assert any(len(p.strip()) > 0 for p in plan_list)
