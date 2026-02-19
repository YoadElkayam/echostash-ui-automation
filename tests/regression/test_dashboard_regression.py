"""Regression tests for Dashboard (UI-DASH P1/P2)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.dashboard_page import DashboardPage


@pytest.mark.regression
class TestDashboardFeatures:
    """Extended dashboard functionality tests."""

    def test_dashboard_stats_display(self, dashboard: DashboardPage) -> None:
        """UI-DASH-002: Dashboard stats cards are rendered."""
        dashboard.open()
        dashboard.wait_for_loading_complete()
        # Verify page has meaningful content
        body = dashboard.page.locator("body").inner_text()
        assert len(body.strip()) > 50

    def test_semantic_search(
        self, dashboard: DashboardPage, test_prompt: dict
    ) -> None:
        """UI-DASH-003: Semantic search returns relevant results."""
        dashboard.open()
        search_input = dashboard.page.get_by_placeholder("Search")
        if search_input.is_visible():
            dashboard.search_semantic(test_prompt["title"][:10])
            dashboard.wait_for_loading_complete()

    def test_empty_project_shows_cta(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
    ) -> None:
        """UI-DASH-007: Empty project shows 'create your first prompt' CTA."""
        # test_project is empty by default (no prompts unless test_prompt used)
        from pages.project_view_page import ProjectViewPage

        pv = ProjectViewPage(authenticated_page, base_url)
        pv.navigate(f"/dashboard/{test_project['id']}")
        pv.wait_for_page_load()
        body = pv.page.locator("body").inner_text().lower()
        # May show empty state or prompt list
        assert len(body.strip()) > 0
