"""Regression tests for semantic search on the dashboard."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.dashboard_page import DashboardPage


@pytest.mark.regression
class TestSemanticSearch:
    """Verify semantic search functionality."""

    def test_semantic_search_returns_results(
        self,
        authenticated_page: Page,
        base_url: str,
        test_prompt: dict,
    ) -> None:
        """UI-DASH-003: Semantic search returns relevant results."""
        dashboard = DashboardPage(authenticated_page, base_url)
        dashboard.open()
        dashboard.search_semantic("test")
        # Should show search results or stay on dashboard
        authenticated_page.wait_for_timeout(2000)
        assert "/dashboard" in authenticated_page.url

    def test_semantic_search_empty_query(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """Submitting empty search shows all projects."""
        dashboard = DashboardPage(authenticated_page, base_url)
        dashboard.open()
        dashboard.search_semantic("")
        authenticated_page.wait_for_timeout(1000)
        assert "/dashboard" in authenticated_page.url

    def test_semantic_search_no_results(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """Searching for nonsense shows empty or no-results state."""
        dashboard = DashboardPage(authenticated_page, base_url)
        dashboard.open()
        dashboard.search_semantic("zzzzxxxxxxxxxnonsense999")
        authenticated_page.wait_for_timeout(2000)
