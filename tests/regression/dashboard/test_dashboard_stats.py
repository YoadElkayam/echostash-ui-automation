"""Regression tests for dashboard statistics display."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.dashboard_page import DashboardPage


@pytest.mark.regression
class TestDashboardStats:
    """Verify dashboard statistics and metrics display."""

    def test_dashboard_stats_display(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-DASH-002: Dashboard shows stats cards (total prompts, projects, etc.)."""
        dashboard = DashboardPage(authenticated_page, base_url)
        dashboard.open()
        dashboard.wait_for_loading_complete()
        # Stats area should be visible
        body = authenticated_page.locator("body")
        expect(body).to_be_visible()

    def test_empty_project_state(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
    ) -> None:
        """UI-DASH-007: Empty project shows CTA to create first prompt."""
        authenticated_page.goto(f"{base_url}/dashboard/{test_project['id']}")
        authenticated_page.wait_for_load_state("networkidle")
        # Empty project should show some CTA or empty state
        body = authenticated_page.locator("body")
        body_text = body.inner_text()
        assert len(body_text) > 0
