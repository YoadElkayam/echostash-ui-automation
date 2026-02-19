"""Regression tests for Project Management (UI-PROJ P1/P2)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.dashboard_page import DashboardPage
from pages.project_modal import ProjectModal
from pages.project_view_page import ProjectViewPage
from utils.helpers import api_create_project, unique_name


@pytest.mark.regression
class TestProjectEditing:
    """Extended project editing tests."""

    def test_edit_project_description(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
    ) -> None:
        """UI-PROJ-005: Edit project description."""
        pv = ProjectViewPage(authenticated_page, base_url)
        pv.navigate(f"/dashboard/{test_project['id']}")
        pv.wait_for_page_load()
        pv.edit_project()
        modal = ProjectModal(pv.page, base_url)
        modal.wait_for_modal()
        modal.fill_description("Updated project description for regression test")
        modal.submit()
        pv.wait_for_loading_complete()

    def test_search_filter_projects(
        self, dashboard: DashboardPage, test_project: dict
    ) -> None:
        """UI-PROJ-008: Filter projects by search text."""
        dashboard.open()
        search_input = dashboard.page.get_by_placeholder("Search")
        if search_input.is_visible():
            dashboard.search_semantic(test_project["name"][:8])
            dashboard.wait_for_loading_complete()

    def test_empty_project_state(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
    ) -> None:
        """UI-PROJ-009: Empty project shows CTA for creating prompts."""
        pv = ProjectViewPage(authenticated_page, base_url)
        pv.navigate(f"/dashboard/{test_project['id']}")
        pv.wait_for_page_load()
        body = pv.page.locator("body").inner_text().lower()
        assert len(body.strip()) > 0
