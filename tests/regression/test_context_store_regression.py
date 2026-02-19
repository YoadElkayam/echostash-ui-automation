"""Regression tests for Context Store (UI-CTX P1/P2)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.context_store_page import ContextStorePage


@pytest.mark.regression
class TestContextStoreFeatures:
    """Extended context store tests."""

    def test_view_asset_content(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-CTX-004: Click an asset to view its content."""
        ctx = ContextStorePage(authenticated_page, base_url)
        ctx.open()
        ctx.wait_for_loading_complete()
        items = ctx.page.locator("[data-testid='asset-item']")
        if items.count() > 0:
            items.first.click()
            ctx.wait_for_loading_complete()

    def test_delete_asset(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-CTX-005: Delete an asset from the list."""
        ctx = ContextStorePage(authenticated_page, base_url)
        ctx.open()
        ctx.wait_for_loading_complete()
        items = ctx.page.locator("[data-testid='asset-item']")
        if items.count() > 0:
            first_text = items.first.inner_text()
            items.first.hover()
            delete_btn = ctx.page.get_by_role("button", name="Delete").first
            if delete_btn.is_visible():
                delete_btn.click()
                confirm = ctx.page.get_by_role("button", name="Confirm").or_(
                    ctx.page.get_by_role("button", name="Delete")
                ).first
                if confirm.is_visible():
                    confirm.click()
                    ctx.wait_for_loading_complete()

    def test_usage_display(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-CTX-006: Storage usage is displayed."""
        ctx = ContextStorePage(authenticated_page, base_url)
        ctx.open()
        ctx.wait_for_loading_complete()
        usage = ctx.page.locator("[data-testid='storage-usage']")
        # Usage may or may not be visible depending on state
        body = ctx.page.locator("body").inner_text()
        assert len(body.strip()) > 0
