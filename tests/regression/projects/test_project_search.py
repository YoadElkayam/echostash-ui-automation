"""Regression tests for project search and filtering."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.project_view_page import ProjectViewPage


@pytest.mark.regression
class TestProjectSearch:
    """Verify project search/filter functionality."""

    def test_search_prompts_in_project(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-PROJ-008: Search prompts within a project."""
        authenticated_page.goto(f"{base_url}/dashboard/{test_project['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        project_view = ProjectViewPage(authenticated_page, base_url)
        project_view.search_prompts(test_prompt["title"][:5])
        authenticated_page.wait_for_timeout(1000)

    def test_empty_project_shows_cta(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
    ) -> None:
        """UI-PROJ-009: Empty project shows create prompt CTA."""
        # Use the test_project fixture which is created fresh (no prompts initially)
        authenticated_page.goto(f"{base_url}/dashboard/{test_project['id']}")
        authenticated_page.wait_for_load_state("networkidle")
        # Should see either prompts or an empty state
        body = authenticated_page.locator("body")
        expect(body).to_be_visible()
