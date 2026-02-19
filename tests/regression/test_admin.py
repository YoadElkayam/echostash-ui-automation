"""Regression tests for Admin Panel (UI-ADM)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.admin_utm_page import AdminUtmPage
from utils.helpers import unique_name


@pytest.mark.regression
@pytest.mark.admin
class TestAdminUtmPanel:
    """Verify admin UTM panel functionality."""

    def test_utm_panel_loads(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ADM-003: UTM panel page loads and lists links."""
        utm = AdminUtmPage(authenticated_page, base_url)
        utm.open()
        utm.wait_for_loading_complete()
        body = utm.page.locator("body").inner_text()
        assert len(body.strip()) > 0

    def test_create_utm_link(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ADM-002: Create a UTM short link."""
        utm = AdminUtmPage(authenticated_page, base_url)
        utm.open()
        utm.wait_for_loading_complete()
        slug_input = utm.page.get_by_label("Slug").or_(
            utm.page.get_by_placeholder("Short code")
        ).first
        if slug_input.is_visible():
            utm.fill_utm_form(
                {
                    "Slug": unique_name("utm"),
                    "URL": "https://echostash.com",
                    "Source": "test",
                    "Medium": "automation",
                    "Campaign": "regression",
                }
            )
            utm.submit()

    def test_delete_utm_link(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ADM-004: Delete a UTM link."""
        utm = AdminUtmPage(authenticated_page, base_url)
        utm.open()
        utm.wait_for_loading_complete()
        items = utm.page.locator("[data-testid='utm-link-item']")
        if items.count() > 0:
            first_text = items.first.inner_text()
            items.first.hover()
            delete_btn = utm.page.get_by_role("button", name="Delete").first
            if delete_btn.is_visible():
                delete_btn.click()
                confirm = utm.page.get_by_role(
                    "button", name="Confirm"
                ).or_(utm.page.get_by_role("button", name="Delete")).first
                if confirm.is_visible():
                    confirm.click()
                    utm.wait_for_loading_complete()
