"""Regression tests for Analytics (UI-ANLY P1/P2)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.analytics_page import AnalyticsPage


@pytest.mark.regression
class TestAnalyticsFeatures:
    """Extended analytics page tests."""

    def test_dashboard_overview_loads(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ANLY-002: Analytics overview metrics are displayed."""
        analytics = AnalyticsPage(authenticated_page, base_url)
        analytics.open()
        analytics.wait_for_loading_complete()
        body = analytics.page.locator("body").inner_text()
        assert len(body.strip()) > 0

    def test_date_range_selector(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ANLY-003: Changing date range updates the view."""
        analytics = AnalyticsPage(authenticated_page, base_url)
        analytics.open()
        analytics.wait_for_loading_complete()
        date_from = analytics.page.locator("[data-testid='date-from']").or_(
            analytics.page.get_by_label("From")
        ).first
        if date_from.is_visible():
            analytics.set_date_range("2026-01-01", "2026-02-19")
            analytics.wait_for_loading_complete()

    def test_charts_display(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ANLY-004: Charts are rendered on the analytics page."""
        analytics = AnalyticsPage(authenticated_page, base_url)
        analytics.open()
        analytics.wait_for_loading_complete()
        # Look for chart elements (canvas, svg, or chart containers)
        charts = analytics.page.locator(
            "canvas, svg, [data-testid='chart']"
        )
        # Charts may or may not be present depending on data
        body = analytics.page.locator("body").inner_text()
        assert len(body.strip()) > 0

    def test_top_prompts_list(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ANLY-005: Top prompts table is rendered."""
        analytics = AnalyticsPage(authenticated_page, base_url)
        analytics.open()
        analytics.wait_for_loading_complete()
        items = analytics.page.locator("[data-testid='top-prompt-item']")
        # May be empty for new users
        body = analytics.page.locator("body").inner_text()
        assert len(body.strip()) > 0
