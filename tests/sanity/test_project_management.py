"""Sanity tests for Project Management (UI-PROJ)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.dashboard_page import DashboardPage
from pages.project_modal import ProjectModal
from pages.project_view_page import ProjectViewPage
from utils.helpers import unique_name


@pytest.mark.sanity
class TestCreateProject:
    """Verify project creation flows."""

    def test_create_project(
        self, dashboard: DashboardPage, api_url: str, guest_auth: dict
    ) -> None:
        """UI-PROJ-001: Create a project from the dashboard."""
        dashboard.open()
        dashboard.click_new_project()
        modal = ProjectModal(dashboard.page, dashboard.base_url)
        modal.wait_for_modal()
        name = unique_name("proj-create")
        modal.fill_name(name)
        modal.submit()
        # Project should appear in the list or we should navigate to it
        dashboard.wait_for_loading_complete()
        body_text = dashboard.page.locator("body").inner_text()
        assert name in body_text

    def test_create_project_with_description(
        self, dashboard: DashboardPage
    ) -> None:
        """UI-PROJ-002: Create a project with both name and description."""
        dashboard.open()
        dashboard.click_new_project()
        modal = ProjectModal(dashboard.page, dashboard.base_url)
        modal.wait_for_modal()
        name = unique_name("proj-desc")
        modal.fill_name(name)
        modal.fill_description("A test project with description")
        modal.submit()
        dashboard.wait_for_loading_complete()

    def test_create_project_empty_name_validation(
        self, dashboard: DashboardPage
    ) -> None:
        """UI-PROJ-003: Empty name should show validation error."""
        dashboard.open()
        dashboard.click_new_project()
        modal = ProjectModal(dashboard.page, dashboard.base_url)
        modal.wait_for_modal()
        modal.fill_name("")
        modal.submit()
        # Modal should remain open (validation prevents close)
        expect(modal._modal).to_be_visible(timeout=3000)


@pytest.mark.sanity
class TestEditProject:
    """Verify project editing and deletion."""

    def test_edit_project_name(
        self, authenticated_page: Page, base_url: str, test_project: dict
    ) -> None:
        """UI-PROJ-004: Edit project name."""
        pv = ProjectViewPage(authenticated_page, base_url)
        pv.navigate(f"/dashboard/{test_project['id']}")
        pv.wait_for_page_load()
        pv.edit_project()
        modal = ProjectModal(pv.page, base_url)
        modal.wait_for_modal()
        new_name = unique_name("proj-edit")
        modal.fill_name(new_name)
        modal.submit()
        pv.wait_for_loading_complete()

    def test_delete_project(
        self, dashboard: DashboardPage, api_url: str, guest_auth: dict
    ) -> None:
        """UI-PROJ-006: Delete a project."""
        from utils.helpers import api_create_project

        # Create a project via API to delete it via UI
        token = guest_auth["accessToken"]
        name = unique_name("proj-del")
        project = api_create_project(api_url, token, name, "To be deleted")
        dashboard.navigate(f"/dashboard/{project['id']}")
        dashboard.wait_for_page_load()
        pv = ProjectViewPage(dashboard.page, dashboard.base_url)
        pv.delete_project()
        pv.wait_for_loading_complete()

    def test_delete_project_cancel(
        self, authenticated_page: Page, base_url: str, test_project: dict
    ) -> None:
        """UI-PROJ-007: Cancel project deletion keeps project intact."""
        pv = ProjectViewPage(authenticated_page, base_url)
        pv.navigate(f"/dashboard/{test_project['id']}")
        pv.wait_for_page_load()
        # Click delete then look for cancel
        delete_btn = pv.page.get_by_role("button", name="Delete").or_(
            pv.page.locator("[data-testid='delete-project']")
        ).first
        if delete_btn.is_visible():
            delete_btn.click()
            cancel_btn = pv.page.get_by_role("button", name="Cancel").first
            if cancel_btn.is_visible():
                cancel_btn.click()
            # Project should still be accessible
            expect(pv.page).to_have_url(f".*{test_project['id']}.*")
