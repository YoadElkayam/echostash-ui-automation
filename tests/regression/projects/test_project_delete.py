"""Regression tests for project deletion."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.components import ConfirmDialog
from pages.project_view_page import ProjectViewPage
from utils.helpers import api_create_project, unique_name


@pytest.mark.regression
class TestProjectDelete:
    """Comprehensive project deletion tests."""

    def test_delete_project_with_confirmation(
        self,
        authenticated_page: Page,
        base_url: str,
        api_url: str,
        guest_auth: dict,
    ) -> None:
        """UI-PROJ-006: Delete project and confirm removal."""
        token = guest_auth["accessToken"]
        name = unique_name("del-proj")
        project = api_create_project(api_url, token, name)

        authenticated_page.goto(f"{base_url}/dashboard/{project['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        project_view = ProjectViewPage(authenticated_page, base_url)
        project_view.delete_project()

        expect(authenticated_page).to_have_url(f"{base_url}/dashboard", timeout=10000)

    def test_delete_project_cancel(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
    ) -> None:
        """UI-PROJ-007: Cancel project deletion keeps project intact."""
        authenticated_page.goto(f"{base_url}/dashboard/{test_project['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        # Click delete button
        delete_btn = authenticated_page.get_by_role("button", name="Delete").or_(
            authenticated_page.locator("[data-testid='delete-project']")
        ).first
        delete_btn.click()

        # Cancel the confirmation
        cancel_btn = authenticated_page.get_by_role("button", name="Cancel").first
        if cancel_btn.is_visible():
            cancel_btn.click()

        # Should still be on the project page
        authenticated_page.wait_for_timeout(1000)
        assert test_project["id"] in authenticated_page.url
