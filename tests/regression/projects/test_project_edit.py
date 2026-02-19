"""Regression tests for project editing."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.project_modal import ProjectModal
from pages.project_view_page import ProjectViewPage
from utils.helpers import unique_name


@pytest.mark.regression
class TestProjectEdit:
    """Comprehensive project editing tests."""

    def test_edit_project_name(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
    ) -> None:
        """UI-PROJ-004: Edit project name."""
        authenticated_page.goto(f"{base_url}/dashboard/{test_project['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        project_view = ProjectViewPage(authenticated_page, base_url)
        project_view.edit_project()

        modal = ProjectModal(authenticated_page, base_url)
        modal.wait_for_modal()
        new_name = unique_name("edited")
        modal.fill_name(new_name)
        modal.submit()

        expect(authenticated_page.get_by_text(new_name, exact=False).first).to_be_visible(
            timeout=10000
        )

    def test_edit_project_description(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
    ) -> None:
        """UI-PROJ-005: Edit project description."""
        authenticated_page.goto(f"{base_url}/dashboard/{test_project['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        project_view = ProjectViewPage(authenticated_page, base_url)
        project_view.edit_project()

        modal = ProjectModal(authenticated_page, base_url)
        modal.wait_for_modal()
        modal.fill_description("Updated description from automation test")
        modal.submit()

        authenticated_page.wait_for_timeout(2000)
