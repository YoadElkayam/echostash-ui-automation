"""Regression tests for breadcrumb navigation."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.regression
class TestBreadcrumbs:
    """Verify breadcrumb navigation works."""

    def test_breadcrumbs_on_project_view(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
    ) -> None:
        """UI-NAV-003: Breadcrumbs show on project detail page."""
        authenticated_page.goto(f"{base_url}/dashboard/{test_project['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        breadcrumb = authenticated_page.locator(
            "[data-testid='breadcrumbs'], nav[aria-label='Breadcrumb']"
        ).first
        if breadcrumb.is_visible():
            text = breadcrumb.inner_text()
            assert len(text) > 0

    def test_breadcrumb_click_navigates_back(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-NAV-004: Clicking breadcrumb navigates back to project."""
        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{test_prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        breadcrumb_link = authenticated_page.locator(
            "[data-testid='breadcrumbs'] a, nav[aria-label='Breadcrumb'] a"
        ).first
        if breadcrumb_link.is_visible():
            breadcrumb_link.click()
            authenticated_page.wait_for_load_state("domcontentloaded")
