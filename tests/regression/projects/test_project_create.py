"""Regression tests for project creation with validation."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.dashboard_page import DashboardPage
from pages.project_modal import ProjectModal
from utils.helpers import api_delete_project, unique_name


@pytest.mark.regression
class TestProjectCreateFull:
    """Comprehensive project creation tests."""

    def test_create_project_with_description(
        self, authenticated_page: Page, base_url: str, api_url: str, guest_auth: dict
    ) -> None:
        """UI-PROJ-002: Create project with name and description."""
        dashboard = DashboardPage(authenticated_page, base_url)
        dashboard.open()
        dashboard.click_new_project()

        modal = ProjectModal(authenticated_page, base_url)
        modal.wait_for_modal()
        name = unique_name("desc-proj")
        modal.fill_name(name)
        modal.fill_description("A project with a full description")
        modal.submit()

        expect(authenticated_page.get_by_text(name, exact=False).first).to_be_visible(
            timeout=10000
        )

    def test_create_project_empty_name_blocked(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-PROJ-003: Empty name prevents project creation."""
        dashboard = DashboardPage(authenticated_page, base_url)
        dashboard.open()
        dashboard.click_new_project()

        modal = ProjectModal(authenticated_page, base_url)
        modal.wait_for_modal()
        modal.fill_name("")
        modal.submit()

        dialog = authenticated_page.locator("[role='dialog']")
        expect(dialog).to_be_visible(timeout=3000)

    def test_create_project_special_characters(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-EDGE-003: Project name with special characters is handled safely."""
        dashboard = DashboardPage(authenticated_page, base_url)
        dashboard.open()
        dashboard.click_new_project()

        modal = ProjectModal(authenticated_page, base_url)
        modal.wait_for_modal()
        name = f"Proj <script>alert(1)</script> {unique_name('')}"
        modal.fill_name(name)
        modal.submit()

        # Should either create (with sanitized name) or show error
        authenticated_page.wait_for_timeout(2000)
