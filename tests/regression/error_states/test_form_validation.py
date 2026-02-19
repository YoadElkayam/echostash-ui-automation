"""Regression tests for form validation across the app."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.dashboard_page import DashboardPage
from pages.project_modal import ProjectModal
from pages.share_page import SharePage


@pytest.mark.regression
class TestFormValidation:
    """Verify form validation errors are shown correctly."""

    def test_project_empty_name(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ERR-004: Empty project name shows validation error."""
        dashboard = DashboardPage(authenticated_page, base_url)
        dashboard.open()
        dashboard.click_new_project()

        modal = ProjectModal(authenticated_page, base_url)
        modal.wait_for_modal()
        modal.fill_name("")
        modal.submit()

        dialog = authenticated_page.locator("[role='dialog']")
        expect(dialog).to_be_visible(timeout=3000)

    def test_share_empty_name(self, page: Page, base_url: str) -> None:
        """Share form: empty name validation."""
        share = SharePage(page, base_url)
        share.open()

        share.fill_name("")
        share.fill_content("Some content")
        share.click_share()

        page.wait_for_timeout(2000)
        assert not share.is_success_visible()

    def test_share_empty_content(self, page: Page, base_url: str) -> None:
        """Share form: empty content validation."""
        share = SharePage(page, base_url)
        share.open()

        share.fill_name("Valid Name")
        share.fill_content("")
        share.click_share()

        page.wait_for_timeout(2000)
        assert not share.is_success_visible()
