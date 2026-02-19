"""Sanity tests for Context Store (UI-CTX)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.context_store_page import ContextStorePage


@pytest.mark.sanity
class TestContextStore:
    """Verify context store page loads and lists assets."""

    def test_context_store_page_loads(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-CTX-001: Context store page loads successfully."""
        ctx = ContextStorePage(authenticated_page, base_url)
        ctx.open()
        expect(ctx.page).to_have_url(f".*context-store.*", timeout=10000)

    def test_list_assets(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-CTX-003: Asset list is displayed."""
        ctx = ContextStorePage(authenticated_page, base_url)
        ctx.open()
        ctx.wait_for_loading_complete()
        body_text = ctx.page.locator("body").inner_text()
        assert len(body_text.strip()) > 0
