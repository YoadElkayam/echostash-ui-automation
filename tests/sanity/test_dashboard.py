"""Sanity tests for dashboard functionality."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.dashboard_page import DashboardPage
from pages.project_modal import ProjectModal


@pytest.mark.sanity
class TestDashboardLoads:
    """Verify the dashboard loads and displays core elements."""

    def test_dashboard_loads_with_projects(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-DASH-001: Dashboard loads and shows project list area."""
        dashboard = DashboardPage(authenticated_page, base_url)
        dashboard.open()
        expect(authenticated_page).to_have_url(f"{base_url}/dashboard")

    def test_dashboard_empty_state(self, page: Page, base_url: str, api_url: str) -> None:
        """UI-DASH-004: New user sees empty state with create CTA."""
        from utils.helpers import api_login_guest, set_auth_cookie

        auth = api_login_guest(api_url)
        set_auth_cookie(page.context, auth["accessToken"], base_url)
        page.goto(f"{base_url}/dashboard")
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_load_state("networkidle")
        # Should see either a CTA button or empty state message
        cta = page.get_by_role("button", name="New Project").or_(
            page.get_by_role("button", name="Create Project")
        ).or_(
            page.get_by_text("Create your first project")
        ).first
        expect(cta).to_be_visible(timeout=10000)

    def test_click_project_navigates(
        self, authenticated_page: Page, base_url: str, test_project: dict
    ) -> None:
        """UI-DASH-005: Clicking a project card navigates to project view."""
        dashboard = DashboardPage(authenticated_page, base_url)
        dashboard.open()
        dashboard.click_project(test_project["name"])
        expect(authenticated_page).to_have_url(
            f"{base_url}/dashboard/{test_project['id']}", timeout=10000
        )

    def test_project_detail_shows_prompts(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-DASH-006: Project detail page lists prompts."""
        authenticated_page.goto(f"{base_url}/dashboard/{test_project['id']}")
        authenticated_page.wait_for_load_state("networkidle")
        prompt_text = authenticated_page.get_by_text(test_prompt["title"], exact=False).first
        expect(prompt_text).to_be_visible(timeout=10000)
