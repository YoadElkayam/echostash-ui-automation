"""Sanity tests for project CRUD operations."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.dashboard_page import DashboardPage
from pages.project_modal import ProjectModal
from pages.project_view_page import ProjectViewPage
from utils.helpers import unique_name


@pytest.mark.sanity
class TestProjectCreate:
    """Verify project creation flow."""

    def test_create_project(
        self, authenticated_page: Page, base_url: str, api_url: str, guest_auth: dict
    ) -> None:
        """UI-PROJ-001: Create a project from dashboard."""
        dashboard = DashboardPage(authenticated_page, base_url)
        dashboard.open()
        dashboard.click_new_project()

        modal = ProjectModal(authenticated_page, base_url)
        modal.wait_for_modal()
        name = unique_name("sanity-proj")
        modal.fill_name(name)
        modal.submit()

        # Project should appear in the list
        expect(authenticated_page.get_by_text(name, exact=False).first).to_be_visible(
            timeout=10000
        )

    def test_create_project_empty_name_validation(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-PROJ-003: Creating a project with empty name shows validation error."""
        dashboard = DashboardPage(authenticated_page, base_url)
        dashboard.open()
        dashboard.click_new_project()

        modal = ProjectModal(authenticated_page, base_url)
        modal.wait_for_modal()
        modal.fill_name("")
        modal.submit()

        # Modal should still be visible (not dismissed) or validation error shown
        dialog = authenticated_page.locator("[role='dialog']")
        expect(dialog).to_be_visible(timeout=3000)


@pytest.mark.sanity
class TestProjectEdit:
    """Verify project editing flow."""

    def test_edit_project_name(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
    ) -> None:
        """UI-PROJ-004: Edit project name and verify update."""
        authenticated_page.goto(f"{base_url}/dashboard/{test_project['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        project_view = ProjectViewPage(authenticated_page, base_url)
        project_view.edit_project()

        modal = ProjectModal(authenticated_page, base_url)
        modal.wait_for_modal()
        new_name = unique_name("edited-proj")
        modal.fill_name(new_name)
        modal.submit()

        expect(authenticated_page.get_by_text(new_name, exact=False).first).to_be_visible(
            timeout=10000
        )


@pytest.mark.sanity
class TestProjectDelete:
    """Verify project deletion flow."""

    def test_delete_project(
        self,
        authenticated_page: Page,
        base_url: str,
        api_url: str,
        guest_auth: dict,
    ) -> None:
        """UI-PROJ-006: Delete a project and verify removal."""
        from utils.helpers import api_create_project

        token = guest_auth["accessToken"]
        name = unique_name("del-proj")
        project = api_create_project(api_url, token, name)

        authenticated_page.goto(f"{base_url}/dashboard/{project['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        project_view = ProjectViewPage(authenticated_page, base_url)
        project_view.delete_project()

        # Should navigate back to dashboard
        expect(authenticated_page).to_have_url(f"{base_url}/dashboard", timeout=10000)
