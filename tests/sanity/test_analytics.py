"""Sanity tests for Analytics (UI-ANLY)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.analytics_page import AnalyticsPage


@pytest.mark.sanity
class TestAnalytics:
    """Verify analytics page loads."""

    def test_analytics_page_loads(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ANLY-001: Analytics page loads successfully."""
        analytics = AnalyticsPage(authenticated_page, base_url)
        analytics.open()
        expect(analytics.page).to_have_url(f".*analytics.*", timeout=10000)
        analytics.wait_for_loading_complete()
